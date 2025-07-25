# main.py
#
# Copyright (c) 2023, TheWisker
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Adw
from .window import CavasikWindow
from .preferences_window import CavasikPreferencesWindow
from .translation_credits import get_translation_credits

from .dbus import BusInterface
from .settings import CavasikSettings

class CavasikApplication(Adw.Application):
    """The main application singleton class"""

    def __init__(self, version, args):
        super().__init__(application_id="io.github.TheWisker.Cavasik", flags=Gio.ApplicationFlags.NON_UNIQUE)
        self.version = version
        self.startup_actions = do_args(version, args)
        if not self.startup_actions:
            print('Bad command line input -> Aborting...')
            self.quit()
            return
        if not self.startup_actions[0]:
            self.quit()
            return
        self.startup_actions = self.startup_actions[1]
        self.settings = CavasikSettings.new() # Must be before self.create_action calls
        self.create_action('about', self.on_about_action)
        self.create_action('open-menu', self.on_menu_action, 'F10')
        self.create_action('toggle-fullscreen', self.on_fullscreen_action, 'F11')
        self.create_action('preferences', self.on_preferences_action, '<primary>P')
        self.create_action('shortcuts', self.on_shortcuts_action, '<primary>H')
        self.create_action('close', self.on_close_action, '<primary>w')
        self.create_action('quit', self.on_quit_action, '<primary>q')
        if self.settings['startup-colors']:
            self.settings._change_colors(self.settings['startup-colors-file'], True)
        if 'set-fg' in self.startup_actions:
            self.settings._change_colors(self.startup_actions['set-fg'], True)
        if 'set-bg' in self.startup_actions:
            self.settings._change_colors(self.startup_actions['set-bg'], False)
        self.bus_interface = BusInterface()

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        self.win = self.props.active_window
        if not self.win:
            self.win = CavasikWindow(application=self)
        self.win.present()

    def on_about_action(self, *args):
        """Callback for the app.about action."""
        about = Adw.AboutWindow(transient_for=self.props.active_window,
                                application_name='Cavasik',
                                application_icon='io.github.TheWisker.Cavasik',
                                developer_name=_('TheWisker'),
                                version=self.version,
                                developers=[_('TheWisker')],
                                copyright='© 2023 TheWisker',
                                website='https://github.com/TheWisker/Cavasik',
                                issue_url='https://github.com/TheWisker/Cavasik/issues',
                                license_type=Gtk.License.GPL_3_0,
                                translator_credits=get_translation_credits())
        about.present()

    def on_preferences_action(self, widget, _):
        self.pref_win = None
        for w in self.get_windows():
            if type(w) == CavasikPreferencesWindow:
                self.pref_win = w
                break
        if not self.pref_win:
            self.pref_win = CavasikPreferencesWindow(application=self)
        self.pref_win.present()

    def on_shortcuts_action(self, widget, _):
        self.shortcuts_win = None
        for w in self.get_windows():
            if type(w) == Gtk.ShortcutsWindow:
                self.shortcuts_win = w
                break
        if not self.shortcuts_win:
            builder = Gtk.Builder.new_from_resource( \
                '/io/github/TheWisker/Cavasik/shortcuts_dialog.ui')
            self.shortcuts_win = builder.get_object('dialog')
        self.shortcuts_win.present()

    def on_quit_action(self, widget, _):
        self.win.close()
        self.quit()

    def on_close_action(self, widget, _):
        win = self.props.active_window
        win.close()
        if type(win) == CavasikWindow:
                self.quit()

    def on_menu_action(self, widget, _):
        self.win.menu_button.activate()

    def on_fullscreen_action(self, widget, _):
        self.win.unfullscreen() if self.win.is_fullscreen() else self.win.fullscreen()

    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional accelerator
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)

        if (shortcuts) and not self.settings['shortcutless-app']:
            self.set_accels_for_action(f"app.{name}", [shortcuts])

def do_args(version, args):
    index = 1 # Skip script name
    actions = {}
    while index < len(args):
        match args[index]:
            case '--version':
                print(f'Cavasik version {version}')
                return False, 'version'
            case '--set-fg':
                index += 1 # Skip over to payload
                if index >= len(args) or args[index].startswith('--'):
                    print('--set-fg is missing argument!')
                    return False # Bad formatted
                actions['set-fg'] = args[index]
            case '--set-bg':
                index += 1 # Skip over to payload
                if index >= len(args) or args[index].startswith('--'):
                    print('--set-bg is missing argument!')
                    return False # Bad formatted
                actions['set-bg'] = args[index]
            case '--help':
                print(
                    "Help with Cavasik - Audio visualizer based on CAVA\n"
                    "DISCLAIMER: Cavasik is mostly a GUI application, thus all configuration is done through the GUI.\n"
                    "\n"
                    "Usage: cavasik [OPTIONS]\n"
                    "\n"
                    "Help with OPTIONS:\n"
                    "--version: Prints the current version.\n"
                    "--set-fg [FILE]: Sets the foreground to the colors read from the file. Overwrites default profile. File works like the startup colors file and dbus interface file.\n"
                    "--set-bg [FILE]: Sets the background to the colors read from the file. Overwrites default profile. File works like the startup colors file and dbus interface file.\n"
                    "--help: Prints this help.\n"
                )
                return False, 'help'
            case _:
                print(f'Invalid argument received \'{args[index]}\' -> Ignoring it...')
        index += 1
    return True, actions

def main(version):
    """The application's entry point."""
    app = CavasikApplication(version, sys.argv)
    return app.run([]) # No args for them