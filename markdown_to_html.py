import sublime, sublime_plugin, os, subprocess, sys
import webbrowser

class MarkdownToHtmlCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		if self.view.file_name():
			folder_name, file_name = os.path.split(self.view.file_name())

			target_file_name = '.'.join(file_name.split('.')[0:-1]) + '.html'

			command = 'pandoc -f markdown -t html -5 -s -o ' + target_file_name + ' ' + file_name

			#Get environment variables
			proc_env = os.environ.copy()

			for k, v in proc_env.iteritems():
				proc_env[k] = os.path.expandvars(v).encode(sys.getfilesystemencoding())

			p = subprocess.Popen(command, stdout=subprocess.PIPE,
						stderr=subprocess.PIPE, env=proc_env, shell=True, cwd=folder_name)

			webbrowser.open(os.path.join(folder_name, target_file_name))

			self.view.set_status('markdowntohtml','Converted to ' + target_file_name)
			sublime.set_timeout(self.clear,2000)



	def clear(self):
		self.view.erase_status('markdowntohtml')
