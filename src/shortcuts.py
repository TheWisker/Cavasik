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
    act_next_mode.connect('activate', change_option, settings, "mode", 1)
    action_map.add_action(act_next_mode)
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("D"), \
        Gtk.NamedAction.new("cavasik.next-mode")))
    act_prev_mode = Gio.SimpleAction.new("prev-mode", None)
    act_prev_mode.connect('activate', change_option, settings, "mode", -1)
    action_map.add_action(act_prev_mode)
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("<Shift>D"), \
        Gtk.NamedAction.new("cavasik.prev-mode")))

    act_cycle_shape = Gio.SimpleAction.new("cycle-shape", None)
    act_cycle_shape.connect('activate', toggle_setting, settings, "circle")
    action_map.add_action(act_cycle_shape)
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("S"), \
        Gtk.NamedAction.new("cavasik.cycle-shape")))

    act_next_mirror = Gio.SimpleAction.new("next-mirror", None)
    act_next_mirror.connect('activate', change_option, settings, "mirror", 1)
    action_map.add_action(act_next_mirror)
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("M"), \
        Gtk.NamedAction.new("cavasik.next-mirror")))
    act_prev_mirror = Gio.SimpleAction.new("prev-mirror", None)
    act_prev_mirror.connect('activate', change_option, settings, "mirror", -1)
    action_map.add_action(act_prev_mirror)
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("<Shift>M"), \
        Gtk.NamedAction.new("cavasik.prev-mirror")))

    act_next_direction = Gio.SimpleAction.new("next-direction", None)
    act_next_direction.connect('activate', change_option, settings, "direction", 1)
    action_map.add_action(act_next_direction)
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("A"), \
        Gtk.NamedAction.new("cavasik.next-direction")))
    act_prev_direction = Gio.SimpleAction.new("prev-direction", None)
    act_prev_direction.connect('activate', change_option, settings, "direction", -1)
    action_map.add_action(act_prev_direction)
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("<Shift>A"), \
        Gtk.NamedAction.new("cavasik.prev-direction")))

    act_toggle_fill = Gio.SimpleAction.new("toggle-fill", None)
    act_toggle_fill.connect('activate', toggle_setting, settings, 'fill')
    action_map.add_action(act_toggle_fill)
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("F"), \
        Gtk.NamedAction.new("cavasik.toggle-fill")))

    act_toggle_dbus_colors = Gio.SimpleAction.new("toggle-dbus-colors", None)
    act_toggle_dbus_colors.connect('activate', toggle_setting, settings, \
        'dbus-colors')
    action_map.add_action(act_toggle_dbus_colors)
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("T"), \
        Gtk.NamedAction.new("cavasik.toggle-dbus-colors")))

    act_toggle_controls = Gio.SimpleAction.new("toggle-controls", None)
    act_toggle_controls.connect('activate', toggle_setting, settings, \
        'window-controls')
    action_map.add_action(act_toggle_controls)
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("O"), \
        Gtk.NamedAction.new("cavasik.toggle-controls")))

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

    act_inc_sensitivity = Gio.SimpleAction.new("increase-sensitivity", None)
    act_inc_sensitivity.connect('activate', change_setting, settings, 'sensitivity', 20)
    action_map.add_action(act_inc_sensitivity)
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("V"), \
        Gtk.NamedAction.new("cavasik.increase-sensitivity")))
    act_dec_sensitivity = Gio.SimpleAction.new("decrease-sensitivity", None)
    act_dec_sensitivity.connect('activate', change_setting, settings, 'sensitivity', -20)
    action_map.add_action(act_dec_sensitivity)
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("<Shift>V"), \
        Gtk.NamedAction.new("cavasik.decrease-sensitivity")))

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
    act_next_profile.connect('activate', change_color_profile, settings, "color-profiles", "active-color-profile", 1)
    action_map.add_action(act_next_profile)
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("C"), \
        Gtk.NamedAction.new("cavasik.next-profile")))
    act_prev_profile = Gio.SimpleAction.new("prev-profile", None)
    act_prev_profile.connect('activate', change_color_profile, settings, "color-profiles", "active-color-profile", -1)
    action_map.add_action(act_prev_profile)
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("<Shift>C"), \
        Gtk.NamedAction.new("cavasik.prev-profile")))

    act_next_mirror_profile = Gio.SimpleAction.new("next-mirror-profile", None)
    act_next_mirror_profile.connect('activate', change_color_profile, settings, "color-profiles", "mirror-colors", 1)
    action_map.add_action(act_next_mirror_profile)
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("N"), \
        Gtk.NamedAction.new("cavasik.next-mirror-profile")))
    act_prev_mirror_profile = Gio.SimpleAction.new("prev-mirror-profile", None)
    act_prev_mirror_profile.connect('activate', change_color_profile, settings, "color-profiles", "mirror-colors", -1)
    action_map.add_action(act_prev_mirror_profile)
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("<Shift>N"), \
        Gtk.NamedAction.new("cavasik.prev-mirror-profile")))

    act_toggle_color_animation = Gio.SimpleAction.new("toggle-color-animation", None)
    act_toggle_color_animation.connect('activate', toggle_setting, settings, \
        'color-animation')
    action_map.add_action(act_toggle_color_animation)
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("G"), \
        Gtk.NamedAction.new("cavasik.toggle-color-animation")))

    act_next_target_profile = Gio.SimpleAction.new("next-target-profile", None)
    act_next_target_profile.connect('activate', change_color_profile, settings, "color-profiles", "color-animation-target", 1)
    action_map.add_action(act_next_target_profile)
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("J"), \
        Gtk.NamedAction.new("cavasik.next-target-profile")))
    act_prev_target_profile = Gio.SimpleAction.new("prev-target-profile", None)
    act_prev_target_profile.connect('activate', change_color_profile, settings, "color-profiles", "color-animation-target", -1)
    action_map.add_action(act_prev_target_profile)
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("<Shift>J"), \
        Gtk.NamedAction.new("cavasik.prev-target-profile")))

    act_next_mirror_target_profile = Gio.SimpleAction.new("next-mirror-target-profile", None)
    act_next_mirror_target_profile.connect('activate', change_color_profile, settings, "color-profiles", "color-animation-mirror-target", 1)
    action_map.add_action(act_next_mirror_target_profile)
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("K"), \
        Gtk.NamedAction.new("cavasik.next-mirror-target-profile")))
    act_prev_mirror_target_profile = Gio.SimpleAction.new("prev-mirror-target-profile", None)
    act_prev_mirror_target_profile.connect('activate', change_color_profile, settings, "color-profiles", "color-animation-mirror-target", -1)
    action_map.add_action(act_prev_mirror_target_profile)
    shortcut_controller.add_shortcut(Gtk.Shortcut.new( \
        Gtk.ShortcutTrigger.parse_string("<Shift>K"), \
        Gtk.NamedAction.new("cavasik.prev-mirror-target-profile")))

def change_option(action, parameter, settings, key, diff):
    modes = settings.get_range(key)[1]
    new_index = modes.index(settings[key]) + diff
    if new_index > len(modes) - 1:
        new_index = 0
    elif new_index < 0:
        new_index = len(modes) - 1
    settings[key] = modes[new_index]

def change_widgets_style(action, parameter, settings):
    if settings['widgets-style'] == 'light':
        settings['widgets-style'] = 'dark'
    else:
        settings['widgets-style'] = 'light'

def change_color_profile(action, parameter, settings, masterkey, key, diff):
    profiles = settings[masterkey]
    new_index = settings[key] + diff
    if new_index > len(profiles) - 1:
        new_index = 0
    elif new_index < 0:
        new_index = len(profiles) - 1
    settings[key] = new_index

def change_setting(action, parameter, settings, key, diff):
    try:
        settings[key] += diff
    except:
        pass

def toggle_setting(action, parameter, settings, key):
    settings[key] = not settings[key]
