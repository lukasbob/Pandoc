import sublime, sublime_plugin, os, subprocess, sys

class TidyPandocCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		if self.view.file_name():
			folder_name, file_name = os.path.split(self.view.file_name())

			command = 'pandoc -f markdown -t markdown -p --reference-links --no-wrap ' + file_name

			#Get environment variables
			proc_env = os.environ.copy()

			for k, v in proc_env.iteritems():
				proc_env[k] = os.path.expandvars(v).encode(sys.getfilesystemencoding())

			p = subprocess.Popen(command, stdout=subprocess.PIPE,
						stderr=subprocess.PIPE, env=proc_env, shell=True, cwd=folder_name)

			result, err = p.communicate()

			region = sublime.Region(0, self.view.size())

			self.view.replace(edit, region, '\n' + result)
