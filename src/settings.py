# settings.py
#
# Copyright (c) 2023, TheWisker
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

from gi.repository import Gio, GLib
from inspect import signature
import os

class CavasikSettings(Gio.Settings):
    __gtype_name__ = 'CavasikSettings'

    def __init__(self):
        super().__init__(self)

    def new(callback_fn=None):
        gsettings = Gio.Settings.new('io.github.TheWisker.Cavasik')
        gsettings.__class__ = CavasikSettings
        if callback_fn:
            gsettings.connect('changed', gsettings.on_settings_changed)
            gsettings.callback_fn = callback_fn
            gsettings.callback_fn_sig_len = len(signature(callback_fn).parameters)
        return gsettings

    def on_settings_changed(self, obj, key):
        if self.callback_fn_sig_len > 0:
            self.callback_fn(key)
        else:
            self.callback_fn()

    def _change_colors(self, path, cid):
        try:
            colors = []
            with open(os.path.expanduser(path), "r") as file:
                for line in file:
                    line = line.strip()  # Remove leading/trailing whitespaces
                    if line:  # Skip empty lines
                        color = [float(c) for c in line.split(",")]
                        color += [self['dbus-opacity']/100] if len(color) < 4 else []
                        colors.append(tuple(color))
            profiles = self['color-profiles']
            profiles[0] = (profiles[0][0], colors if cid else profiles[0][1], profiles[0][2] if cid else colors)
            self['active-color-profile'] = 0
            self['color-profiles'] = profiles
            return True
        except FileNotFoundError:
            print(f"File not found: {path}")
        except IOError as e:
            print(f"An error occurred while reading the file: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        return False