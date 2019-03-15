"""
Shell execution of YAML configuration commands for Codeship.
"""
from warnings import warn

import os
import sys
import time
import yaml

try:
    # only available in Python 3
    FileNotFoundError
except NameError:
    # Python 2
    FileNotFoundError = IOError  # pylint: disable=redefined-builtin


class YamlShellCommandsExecuter:
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
        elif commands is None:
            commands = []

        for cmd in commands:
            log('========== Running: {}'.format(cmd), color='blue')
            start = time.time()
            status = os.system(cmd)
            duration = round(time.time() - start, 2)

            duration_msg = '{seconds}s: {command}'.format(
                seconds=duration, command=cmd)

            if status > 0:
                fail('========== Errored after {}'.format(duration_msg),
                     exit_code=status)
            else:
                log('========== Finished in {}'.format(duration_msg),
                    color='green')


def log(message, color=None):
    """
    Print a provided string and color it by wrapping it in ANSI color escape
    codes. Valid colors are blue, green and red.
    """
    if color == 'blue':
        color = '\033[94m'
    elif color == 'green':
        color = '\033[92m'
    elif color == 'red':
        color = '\033[91m'
    else:
        color = ''

    print('{color}{message}{stop_colors}'.format(
        message=message,
        color=color,
        stop_colors='\033[0m',
    ))


def fail(message=None, exit_code=1):
    """
    Safely abort script with an error status and optional message.
    """
    if message:
        log(message, color='red')

    # NOTE: for some reason a large code, such as 32512, results in status 0
    sys.exit(exit_code if 1 <= exit_code <= 255 else 1)


def main():
    """
    Entry point for console command ``codeship-yaml``.
    """
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
