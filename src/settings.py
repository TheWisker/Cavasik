# settings.py
#
# Copyright (c) 2023, TheWisker
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

from gi.repository import Gio, GLib
from inspect import signature

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
    
