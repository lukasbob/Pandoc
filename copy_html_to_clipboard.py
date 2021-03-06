import sublime, sublime_plugin, os, subprocess, sys
import webbrowser

class copyHtmlToClipboardCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		if self.view.file_name():
			folder_name, file_name = os.path.split(self.view.file_name())

			command = 'pandoc -t html -5 -s ' + file_name

			#Get environment variables
			proc_env = os.environ.copy()

			for k, v in proc_env.iteritems():
				proc_env[k] = os.path.expandvars(v).encode(sys.getfilesystemencoding())

			p = subprocess.Popen(command, stdout=subprocess.PIPE,
						stderr=subprocess.PIPE, env=proc_env, shell=True, cwd=folder_name)

			result, err = p.communicate()

			set_clipboard(result)

			self.view.set_status('copyhtmltoclipboard','Copied to clipboard as HTML')
			sublime.set_timeout(self.clear,2000)



	def clear(self):
		self.view.erase_status('copyhtmltoclipboard')
