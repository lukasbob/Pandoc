import os
import sublime
import sublime_plugin
from shell import Shell


class TidyPandocCommand(sublime_plugin.TextCommand):

    opts = [
        'pandoc',
        '-f markdown',          # Format to convert from
        '-t markdown',          # Format to convert to
        '--reference-links',    # Convert links to reference links
    ]

    def run(self, edit):

        if self.view.file_name():
            folder_name, file_name = os.path.split(self.view.file_name())

            cmd = ' '.join(list(self.opts).append(file_name))

            result, err = Shell.run(cmd, folder_name)

            region = sublime.Region(0, self.view.size())
            self.view.replace(edit, region, result)
