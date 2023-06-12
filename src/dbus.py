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
        self.bus.publish('io.github.TheWisker.Cavasik', self)
        self.settings = CavasikSettings.new(self.on_settings_changed)
        self.active = self.settings['dbus-colors']

    def set_fg_colors(self, path):
        if self.active:
            return self._change_colors(path, True) # True for foreground colors
        return False

    def set_bg_colors(self, path):
        if self.active:
            return self._change_colors(path, False) # False for background colors
        return False

    def _change_colors(self, path, cid):
        try:
            colors = []
            with open(path, "r") as file:
                for line in file:
                    line = line.strip()  # Remove leading/trailing whitespaces
                    if line:  # Skip empty lines
                        color = [float(c) for c in line.split(",")]
                        color += [self.settings['dbus-opacity']/100] if len(color) < 4 else []
                        colors.append(tuple(color))
            profiles = self.settings['color-profiles']
            profiles[0] = (profiles[0][0], colors if cid else profiles[0][1], profiles[0][2] if cid else colors)
            self.settings['active-color-profile'] = 0
            self.settings['color-profiles'] = profiles
            return True
        except FileNotFoundError:
            print(f"File not found: {path}")
        except IOError as e:
            print(f"An error occurred while reading the file: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        return False

    def on_settings_changed(self):
        self.active = self.settings['dbus-colors']

