import sublime
import sublime_plugin
import os
from shell import Shell


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

            html, err = Shell.run(command, folder_name)

            new_view = self.view.window().new_file()
            new_view.insert(edit, 0, html + err)


class ConvertToPdfCommand(sublime_plugin.TextCommand):
    temp_md = [
        'pandoc',
        '{0}',
        '-t markdown',
        '-o {1}'
    ]
    md2pdf = [
        'markdown2pdf',
        '--template "{0}"',
        '-N',
        '--xetex',
        '--toc',
        '-o {0}.pdf',
        '--listings',
        '{1}'
    ]

    def run(self, edit):
        if not self.view.file_name():
            return

        folder_name, fn = os.path.split(self.view.file_name())

        tpl_path = [sublime.packages_path(), 'Pandoc/templates/latex.tex']
        tpl = os.path.join(tpl_path)

        # Pass through pandoc first to convert to markdown
        temp_fn = fn + '.temp.md'
        blank_to_md = ' '.join(list(self.temp_md)).format(fn, temp_fn)
        output, err = Shell.run(blank_to_md, folder_name)

        if err:
            return

        # Then go from markdown to pdf.
        md_to_pdf = ' '.join(list(self.md2pdf)).format(tpl, temp_fn)
        output, err = Shell.run(md_to_pdf, folder_name)

        # Tidy up
        os.remove('/'.join([folder_name, temp_fn]))
