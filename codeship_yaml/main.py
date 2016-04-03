import os
import sys
import yaml
from warnings import warn


class YamlShellCommandsExecuter(object):
    """
    Read a YAML file with shell commands in its sections, and execute them.
    """

    def __init__(self, yml_file_name, emit_warnings=True):
        """
        Load a YAML file for execution of commands later.
        """
        self.emit_warnings = emit_warnings
        try:
            with open(yml_file_name) as yamlfile:
                self.data = yaml.safe_load(yamlfile)
        except FileNotFoundError:
            fail(message='YAML file not found: %s' % yml_file_name)

    def exec_section(self, section_name):
        """
        Execute all commands sequentially specified in a section.
        If the command fails execution of the script is aborted.
        """
        try:
            commands = self.data[section_name]
        except KeyError:
            if self.emit_warnings:
                warn('Section %s not found.' % section_name)
            return

        if isinstance(commands, str):
            commands = [commands]

        for cmd in commands:
            status = os.system(cmd)
            if status > 0:
                fail(exit_code=status)


def fail(message=None, exit_code=1):
    """
    Safely abort script with an error status and optional message.
    """
    if message:
        print(message)

    # NOTE: for some reason a large code, such as 32512, results in status 0
    sys.exit(exit_code if 1 <= exit_code <= 255 else 1)


def main():
    if len(sys.argv) > 1:
        sections = sys.argv[1:]
        warnings = True
    else:
        sections = [
            'install',
            'before_script',
            'script',
            'after_success',
        ]
        warnings = False

    commands = YamlShellCommandsExecuter('codeship.yml', warnings)

    for section_name in sections:
        commands.exec_section(section_name)
