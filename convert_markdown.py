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
		my_list = ["HTML", "PDF"]

		commands = {
			'HTML': 'convert_to_html',
			'PDF': 'convert_to_pdf'
		}

		def on_done(i):
			self.view.run_command(commands[my_list[i]])

		self.view.window().show_quick_panel(my_list, on_done)


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

			template = os.path.abspath('data/latex.tex')

			command = 'markdown2pdf --template "%s" -N --xetex --toc --variable filename=%s -o %s.pdf --listings %s' % (template, file_name, file_name, file_name)

			output, err = run_command(command, folder_name)

			print err


