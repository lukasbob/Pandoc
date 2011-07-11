import sublime, sublime_plugin, os, subprocess, sys

def run_command(command, working_dir):
	#Get environment variables
	proc_env = os.environ.copy()

	for k, v in proc_env.iteritems():
		proc_env[k] = os.path.expandvars(v).encode(sys.getfilesystemencoding())

	p = subprocess.Popen(command, stdout=subprocess.PIPE,
				stderr=subprocess.PIPE, env=proc_env, shell=True, cwd=working_dir)

	return p.communicate()


class ConvertMarkdownCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		conversions = ["HTML", "PDF"]

		commands = {
			'HTML': 'convert_to_html',
			'PDF': 'convert_to_pdf'
		}

		def on_done(i):
			self.view.run_command(commands[conversions[i]])

		self.view.window().show_quick_panel(conversions, on_done)


class ConvertToHtmlCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		if self.view.file_name():
			folder_name, file_name = os.path.split(self.view.file_name())

			command = 'pandoc -t html -5 -s ' + file_name

			html, err = run_command(command, folder_name)

			new_view = self.view.window().new_file()
			new_view.insert(edit, 0, html+err)


class ConvertToPdfCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		if self.view.file_name():
			folder_name, file_name = os.path.split(self.view.file_name())

			template = os.path.join(sublime.packages_path(), 'Pandoc/templates/latex.tex')

			#Pass through pandoc first to convert to markdown
			command_1 = 'pandoc {0} -t markdown -o {0}.temp.mdown'.format(file_name)
			command_2 = 'markdown2pdf --template "{1}" -N --xetex --toc -o {0}.pdf --listings {0}.temp.mdown'.format(file_name, template)

			output, err = run_command(command_1, folder_name)

			if err:
				return

			output, err = run_command(command_2, folder_name)

			#Tidy up
			output, err = run_command('rm {0}.temp.mdown'.format(file_name), folder_name)


