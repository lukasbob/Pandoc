import sublime, sublime_plugin

class ConvertFileCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		options = ["PDF", "HTML", "Markdown", "MediaWiki", "Textile"]

		def on_done(i):
			print options[i]

		self.view.window().show_quick_panel(options, on_done)
