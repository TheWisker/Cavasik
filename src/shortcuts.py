# shortcuts.py
#
# Copyright (c) 2023, TheWisker
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gio, Gtk

def add_shortcuts(widget, settings):
    action_map = Gio.SimpleActionGroup.new()
    widget.insert_action_group("cavasik", action_map)
    shortcut_controller = Gtk.ShortcutController.new()
    shortcut_controller.set_scope(Gtk.ShortcutScope.MANAGED)
    widget.add_controller(shortcut_controller)

    act_next_mode = Gio.SimpleAction.new("next-mode", None)
    act_next_mode.connect('activate', change_mode, settings, 1)
    action_map.add_action(act_next_mode)
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("D"), \
        Gtk.NamedAction.new("cavasik.next-mode")))
    act_prev_mode = Gio.SimpleAction.new("prev-mode", None)
    act_prev_mode.connect('activate', change_mode, settings, -1)
    action_map.add_action(act_prev_mode)
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("<Shift>D"), \
        Gtk.NamedAction.new("cavasik.prev-mode")))

    act_inc_margin = Gio.SimpleAction.new("increase-margin", None)
    act_inc_margin.connect('activate', change_setting, settings, 'margin', 1)
    action_map.add_action(act_inc_margin)
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("N"), \
        Gtk.NamedAction.new("cavasik.increase-margin")))
    act_dec_margin = Gio.SimpleAction.new("decrease-margin", None)
    act_dec_margin.connect('activate', change_setting, settings, 'margin', -1)
    action_map.add_action(act_dec_margin)
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("<Shift>N"), \
        Gtk.NamedAction.new("cavasik.decrease-margin")))

    act_inc_offset = Gio.SimpleAction.new("increase-offset", None)
    act_inc_offset.connect('activate', change_setting, settings, \
        'items-offset', 1)
    action_map.add_action(act_inc_offset)
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("O"), \
        Gtk.NamedAction.new("cavasik.increase-offset")))
    act_dec_offset = Gio.SimpleAction.new("decrease-offset", None)
    act_dec_offset.connect('activate', change_setting, settings, \
        'items-offset', -1)
    action_map.add_action(act_dec_offset)
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("<Shift>O"), \
        Gtk.NamedAction.new("cavasik.decrease-offset")))

    act_inc_roundness = Gio.SimpleAction.new("increase-roundness", None)
    act_inc_roundness.connect('activate', change_setting, settings, \
        'items-roundness', 1)
    action_map.add_action(act_inc_roundness)
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("R"), \
        Gtk.NamedAction.new("cavasik.increase-roundness")))
    act_dec_roundness = Gio.SimpleAction.new("decrease-roundness", None)
    act_dec_roundness.connect('activate', change_setting, settings, \
        'items-roundness', -1)
    action_map.add_action(act_dec_roundness)
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("<Shift>R"), \
        Gtk.NamedAction.new("cavasik.decrease-roundness")))

    act_inc_thickness = Gio.SimpleAction.new("increase-thickness", None)
    act_inc_thickness.connect('activate', change_setting, settings, \
        'line-thickness', 1)
    action_map.add_action(act_inc_thickness)
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("T"), \
        Gtk.NamedAction.new("cavasik.increase-thickness")))
    act_dec_thickness = Gio.SimpleAction.new("decrease-thickness", None)
    act_dec_thickness.connect('activate', change_setting, settings, \
        'line-thickness', -1)
    action_map.add_action(act_dec_thickness)
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("<Shift>T"), \
        Gtk.NamedAction.new("cavasik.decrease-thickness")))

    act_toggle_fill = Gio.SimpleAction.new("toggle-fill", None)
    act_toggle_fill.connect('activate', toggle_setting, settings, 'fill')
    action_map.add_action(act_toggle_fill)
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("F"), \
        Gtk.NamedAction.new("cavasik.toggle-fill")))

    act_toggle_corners = Gio.SimpleAction.new("toggle-corners", None)
    act_toggle_corners.connect('activate', toggle_setting, settings, \
        'sharp-corners')
    action_map.add_action(act_toggle_corners)
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("S"), \
        Gtk.NamedAction.new("cavasik.toggle-corners")))

    act_toggle_controls = Gio.SimpleAction.new("toggle-controls", None)
    act_toggle_controls.connect('activate', toggle_setting, settings, \
        'window-controls')
    action_map.add_action(act_toggle_controls)
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("H"), \
        Gtk.NamedAction.new("cavasik.toggle-controls")))

    act_toggle_autohide = Gio.SimpleAction.new("toggle-autohide", None)
    act_toggle_autohide.connect('activate', toggle_setting, settings, \
        'autohide-header')
    action_map.add_action(act_toggle_autohide)
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("A"), \
        Gtk.NamedAction.new("cavasik.toggle-autohide")))

    act_inc_bars = Gio.SimpleAction.new("increase-bars", None)
    act_inc_bars.connect('activate', change_setting, settings, 'bars', 2)
    action_map.add_action(act_inc_bars)
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("B"), \
        Gtk.NamedAction.new("cavasik.increase-bars")))
    act_dec_bars = Gio.SimpleAction.new("decrease-bars", None)
    act_dec_bars.connect('activate', change_setting, settings, 'bars', -2)
    action_map.add_action(act_dec_bars)
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("<Shift>B"), \
        Gtk.NamedAction.new("cavasik.decrease-bars")))

    act_toggle_channels = Gio.SimpleAction.new("toggle-channels", None)
    act_toggle_channels.connect('activate', change_channels, settings)
    action_map.add_action(act_toggle_channels)
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("C"), \
        Gtk.NamedAction.new("cavasik.toggle-channels")))

    act_toggle_reverse = Gio.SimpleAction.new("toggle-reverse", None)
    act_toggle_reverse.connect('activate', toggle_setting, settings, \
        'reverse-order')
    action_map.add_action(act_toggle_reverse)
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("E"), \
        Gtk.NamedAction.new("cavasik.toggle-reverse")))

    act_toggle_style = Gio.SimpleAction.new("toggle-style", None)
    act_toggle_style.connect('activate', change_widgets_style, settings)
    action_map.add_action(act_toggle_style)
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("W"), \
        Gtk.NamedAction.new("cavasik.toggle-style")))

    act_next_profile = Gio.SimpleAction.new("next-profile", None)
    act_next_profile.connect('activate', change_color_profile, settings, 1)
    action_map.add_action(act_next_profile)
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("P"), \
        Gtk.NamedAction.new("cavasik.next-profile")))
    act_prev_profile = Gio.SimpleAction.new("prev-profile", None)
    act_prev_profile.connect('activate', change_color_profile, settings, -1)
    action_map.add_action(act_prev_profile)
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("<Shift>P"), \
        Gtk.NamedAction.new("cavasik.prev-profile")))

def change_mode(action, parameter, settings, diff):
    modes = settings.get_range('mode')[1]
    new_index = modes.index(settings['mode']) + diff
    if new_index > len(modes) - 1:
        new_index = 0
    elif new_index < 0:
        new_index = len(modes) - 1
    settings['mode'] = modes[new_index]

def change_channels(action, parameter, settings):
    if settings['channels'] == 'mono':
        settings['channels'] = 'stereo'
    else:
        settings['channels'] = 'mono'

def change_widgets_style(action, parameter, settings):
    if settings['widgets-style'] == 'light':
        settings['widgets-style'] = 'dark'
    else:
        settings['widgets-style'] = 'light'

def change_color_profile(action, parameter, settings, diff):
    profiles = settings['color-profiles']
    new_index = settings['active-color-profile'] + diff
    if new_index > len(profiles) - 1:
        new_index = 0
    elif new_index < 0:
        new_index = len(profiles) - 1
    settings['active-color-profile'] = new_index

def change_setting(action, parameter, settings, key, diff):
    try:
        settings[key] += diff
    except:
        pass

def toggle_setting(action, parameter, settings, key):
    settings[key] = not settings[key]
