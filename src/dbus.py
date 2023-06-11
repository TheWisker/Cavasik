# dbus.py
#
# Copyright 2022 TheWisker
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE X CONSORTIUM BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# Except as contained in this notice, the name(s) of the above copyright
# holders shall not be used in advertising or otherwise to promote the sale,
# use or other dealings in this Software without prior written
# authorization.
#
# SPDX-License-Identifier: MIT

from pydbus import SessionBus
from gi.repository import Adw
from cavalier.settings import CavalierSettings

class BusInterface(object):
    """
        <node>
          <interface name='io.github.fsobolev.Cavalier'>
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
        self.bus.publish('io.github.fsobolev.Cavalier', self)
        self.settings = CavalierSettings.new(self.on_settings_changed)
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
            return False
        except IOError as e:
            print(f"An error occurred while reading the file: {e}")
            return False
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return False

    def on_settings_changed(self):
        self.active = self.settings['dbus-colors']

