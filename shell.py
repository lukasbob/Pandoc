import os
import sys
import subprocess


class Shell:
    """Static class that provides some shortcuts to running shell commands."""

    @staticmethod
    def run(command, working_directory):
        """Runs a shell command in the context of the working dir provided."""

        #Get environment variables
        proc_env = os.environ.copy()

        for k, v in proc_env.iteritems():
            encoding = sys.getfilesystemencoding()
            proc_env[k] = os.path.expandvars(v).encode(encoding)

        p = subprocess.Popen(command, stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE, env=proc_env,
                    shell=True, cwd=working_directory)

        return p.communicate()
