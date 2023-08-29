# settings_import_export.py
#
# Copyright (c) 2023, TheWisker
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

import subprocess
from gi.repository import Adw

def import_settings(window, path):
    try:
        with open(path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if line != '\n':
                    subprocess.run(['gsettings', 'set', \
                        'io.github.TheWisker.Cavasik', line.split(' ')[0], \
                        line.replace(line.split(' ')[0], '').strip()])
        toast_msg = _('Settings successfully imported')

    except Exception as e:
        print('Can\'t import settings from file: ' + path)
        print(e)
        toast_msg = _('Failed to import settings')

    window.add_toast(Adw.Toast.new(toast_msg))


def export_settings(window, path):
    gsettings_list = subprocess.run( \
        ['gsettings', 'list-recursively', 'io.github.TheWisker.Cavasik'], \
        stdout=subprocess.PIPE).stdout.decode('utf-8')
    try:
        with open(path, 'w') as file:
            for line in gsettings_list.split('\n'):
                file.write(' '.join(line.split(' ')[1::]) + '\n')
        toast_msg = _('File successfully saved')

    except Exception as e:
        print('Can\'t export settings to file: ' + path)
        print(e)
        toast_msg = _('Failed to save file')

    window.add_toast(Adw.Toast.new(toast_msg))
