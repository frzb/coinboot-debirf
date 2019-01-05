#!/usr/bin/python3

# Copyright (C) 2018 Gunter Miegel coinboot.io
#
# This file is part of Coinboot.
#
# Coinboot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Create Coinboot Plugins

Usage:
  create_plugin start
  create_plugin finish <plugin_name>

Options:
  -h --help     Show this screen.

"""

import os
import tarfile
import re
from subprocess import call
from docopt import docopt

DPKG_STATUS = '/var/lib/dpkg/status'
INITIAL_DPKG_STATUS = '/tmp/initial_status'
FINAL_DPKG_STATUS = '/tmp/dpkg_status'
PLUGIN_DIR = '/mnt/plugin/rootfs'

EXCLUDE = ('/dev',
           '/proc',
           '/run',
           '/sys',
           '/tmp',
           '/usr/share/dbus-1/system-services',
           '/vagrant',
           '/var/cache',
           '/var/lib/dpkg/[^info]',
           '/var/log',
           '.*__pycache__.*',
           '.wget-hsts'
           )


def find(path_to_walk):
    """Return results similar to the Unix find command run without options
    i.e. traverse a directory tree and return all the file paths
    """
    return [os.path.join(path, file)
            for (path, dirs, files) in os.walk(path_to_walk)
            for file in files]

def main(arguments):
    print(arguments)
    if arguments['start']:
         call(['cp', '-v', DPKG_STATUS, INITIAL_DPKG_STATUS])
    elif arguments['finish']:
        f = open(FINAL_DPKG_STATUS, 'w')
        call(['dpkg_status.py', '--old', 'INITIAL_DPKG_STATUS', '--new', 'DPKG_STATUS', '--diff'], stdout=f)

        valid_files = []

        for path in  find(PLUGIN_DIR):
            if any(re.findall(pattern, path) for pattern in EXCLUDE):
                print('Ignore:', path)
            else:
                print(' Valid:', path)
                valid_files.append(path)

        valid_files.append(FINAL_DPKG_STATUS)
:w

        files_for_plugin_archive = []

        for path in valid_files:
            cleaned_path = re.sub(PLUGIN_DIR, '/', path)
            print(cleaned_path)
            files_for_plugin_archive.append(cleaned_path)

        tar = tarfile.open(arguments['<plugin_name>'] + ".tar.gz", "w:gz")
        for path in files_for_plugin_archive:
            tar.add(path)
        tar.close()


if __name__ == '__main__':
    arguments = docopt(__doc__, version='Create Coinboot Plugins v0.1')
    main(arguments)
