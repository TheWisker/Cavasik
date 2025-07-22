# dbus.py
#
# Copyright (c) 2023, TheWisker
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

from pydbus import SessionBus
from gi.repository import Adw
from cavasik.settings import CavasikSettings

class BusInterface(object):
    """
        <node>
          <interface name='io.github.TheWisker.Cavasik'>
            <method name='set_fg_colors'>
              <arg type='s' name='path' direction='in'/>
              <arg type='b' name='state' direction='out'/>
            </method>
            <method name='set_bg_colors'>
              <arg type='s' name='path' direction='in'/>
              <arg type='b' name='state' direction='out'/>
            </method>
          </interface>
        </node>
    """

    def __init__(self):
        self.window = None
        self.bus = SessionBus()
        try:
            self.bus.publish("io.github.TheWisker.Cavasik", self)
        except Exception as e:
            print("Interface already published, we are not the first to be here...")
            print(e)
            self.proxy = self.bus.get("io.github.TheWisker.Cavasik", "/io/github/TheWisker/Cavasik")
            self.proxy.onset_fg_colors = self.set_fg_colors
            self.proxy.onset_bg_colors = self.set_bg_colors
        self.settings = CavasikSettings.new(self.on_settings_changed)
        self.active = self.settings['dbus-colors']

    def set_fg_colors(self, path):
        if self.active:
            return self.settings._change_colors(path, True) # True for foreground colors
        return False

    def set_bg_colors(self, path):
        if self.active:
            return self.settings._change_colors(path, False) # False for background colors
        return False

    def on_settings_changed(self):
        self.active = self.settings['dbus-colors']
