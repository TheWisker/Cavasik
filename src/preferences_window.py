# preferences_window.py
#
# Copyright 2022 Fyodor Sobolev
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

import os
from gi.repository import Adw, Gtk, GObject, Gdk, Gio, GLib
from cavalier.settings import CavalierSettings
from cavalier.settings_import_export import import_settings, export_settings


class CavalierPreferencesWindow(Adw.PreferencesWindow):
    __gtype_name__ = 'CavalierPreferencesWindow'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_modal(False)
        self.settings = CavalierSettings.new(self.on_settings_changed)
        self.flatpak = os.path.exists('/.flatpak-info')

        self.set_default_size(572, 518)
        self.create_cavalier_page()
        self.create_cava_page()
        self.create_colors_page()
        self.settings_bind = False
        self.do_not_change_profile = False
        self.load_settings()

    def create_cavalier_page(self):
        self.cavalier_page = Adw.PreferencesPage.new()
        self.cavalier_page.set_title('Cavalier')
        self.cavalier_page.set_icon_name('io.github.fsobolev.Cavalier-symbolic')
        self.add(self.cavalier_page)

        self.cavalier_mode_group = Adw.PreferencesGroup.new()
        self.cavalier_mode_group.set_title(_('Drawing Mode'))
        self.cavalier_page.add(self.cavalier_mode_group)

        self.wave_row = Adw.ActionRow.new()
        self.wave_row.set_title(_('Wave'))
        self.wave_check_btn = Gtk.CheckButton.new()
        self.wave_row.add_prefix(self.wave_check_btn)
        self.wave_row.set_activatable_widget(self.wave_check_btn)
        self.cavalier_mode_group.add(self.wave_row)

        self.levels_row = Adw.ActionRow.new()
        self.levels_row.set_title(_('Levels'))
        self.levels_check_btn = Gtk.CheckButton.new()
        self.levels_check_btn.set_group(self.wave_check_btn)
        self.levels_row.add_prefix(self.levels_check_btn)
        self.levels_row.set_activatable_widget(self.levels_check_btn)
        self.cavalier_mode_group.add(self.levels_row)

        self.particles_row = Adw.ActionRow.new()
        self.particles_row.set_title(_('Particles'))
        self.particles_check_btn = Gtk.CheckButton.new()
        self.particles_check_btn.set_group(self.wave_check_btn)
        self.particles_row.add_prefix(self.particles_check_btn)
        self.particles_row.set_activatable_widget(self.particles_check_btn)
        self.cavalier_mode_group.add(self.particles_row)

        self.spine_row = Adw.ActionRow.new()
        self.spine_row.set_title(_('Spine'))
        self.spine_check_btn = Gtk.CheckButton.new()
        self.spine_check_btn.set_group(self.wave_check_btn)
        self.spine_row.add_prefix(self.spine_check_btn)
        self.spine_row.set_activatable_widget(self.spine_check_btn)
        self.cavalier_mode_group.add(self.spine_row)

        self.bars_row = Adw.ActionRow.new()
        self.bars_row.set_title(_('Bars'))
        self.bars_check_btn = Gtk.CheckButton.new()
        self.bars_check_btn.set_group(self.wave_check_btn)
        self.bars_row.add_prefix(self.bars_check_btn)
        self.bars_row.set_activatable_widget(self.bars_check_btn)
        self.cavalier_mode_group.add(self.bars_row)

        self.cavalier_group = Adw.PreferencesGroup.new()
        self.cavalier_page.add(self.cavalier_group)

        self.pref_margin = Adw.ActionRow.new()
        self.pref_margin.set_title(_('Drawing area margin'))
        self.pref_margin.set_subtitle( \
            _('Size of gaps around drawing area (in pixels).'))
        self.pref_margin_scale = Gtk.Scale.new_with_range( \
            Gtk.Orientation.HORIZONTAL, 0.0, 40.0, 1.0)
        self.pref_margin_scale.set_size_request(180, -1)
        self.pref_margin_scale.set_draw_value(True)
        self.pref_margin_scale.set_value_pos(Gtk.PositionType.LEFT)
        self.pref_margin.add_suffix(self.pref_margin_scale)
        self.cavalier_group.add(self.pref_margin)

        self.pref_offset = Adw.ActionRow.new()
        self.pref_offset.set_title(_('Offset between items'))
        self.pref_offset.set_subtitle( \
            _('The size of spaces between elements in "levels", "particles" and "bars" modes (in percent).'))
        self.pref_offset_scale = Gtk.Scale.new_with_range( \
            Gtk.Orientation.HORIZONTAL, 0.0, 20.0, 1.0)
        self.pref_offset_scale.set_size_request(180, -1)
        self.pref_offset_scale.set_draw_value(True)
        self.pref_offset_scale.set_value_pos(Gtk.PositionType.LEFT)
        self.pref_offset.add_suffix(self.pref_offset_scale)
        self.cavalier_group.add(self.pref_offset)

        self.pref_roundness = Adw.ActionRow.new()
        self.pref_roundness.set_title(_('Roundness of items'))
        self.pref_roundness.set_subtitle( \
            _('This setting affects "levels", "particles" and "spine" modes.\n0 - square, 1 - round'))
        self.pref_roundness_scale = Gtk.Scale.new_with_range( \
            Gtk.Orientation.HORIZONTAL, 0.0, 1.0, 0.02)
        self.pref_roundness_scale.set_size_request(190, -1)
        self.pref_roundness_scale.set_draw_value(True)
        self.pref_roundness_scale.set_value_pos(Gtk.PositionType.LEFT)
        self.pref_roundness.add_suffix(self.pref_roundness_scale)
        self.cavalier_group.add(self.pref_roundness)

        self.pref_fill = Adw.ActionRow.new()
        self.pref_fill.set_title(_('Filling'))
        self.pref_fill.set_subtitle( \
            _('Whether shapes should be filled or outlined.'))
        self.pref_fill_switch = Gtk.Switch.new()
        self.pref_fill_switch.set_valign(Gtk.Align.CENTER)
        self.pref_fill.add_suffix(self.pref_fill_switch)
        self.pref_fill.set_activatable_widget( \
            self.pref_fill_switch)
        self.cavalier_group.add(self.pref_fill)

        self.pref_thickness = Adw.ActionRow.new()
        self.pref_thickness.set_title(_('Thickness of lines'))
        self.pref_thickness.set_subtitle( \
            _('Thickness of lines when filling is off (in pixels).'))
        self.pref_thickness_scale = Gtk.Scale.new_with_range( \
            Gtk.Orientation.HORIZONTAL, 1.0, 40.0, 1.0)
        self.pref_thickness_scale.set_size_request(180, -1)
        self.pref_thickness_scale.set_draw_value(True)
        self.pref_thickness_scale.set_value_pos(Gtk.PositionType.LEFT)
        self.pref_thickness.add_suffix(self.pref_thickness_scale)
        self.cavalier_group.add(self.pref_thickness)

        self.dbus_group = Adw.PreferencesGroup.new()
        self.cavalier_page.add(self.dbus_group)

        self.pref_use_dbus_colors = Adw.ActionRow.new()
        self.pref_use_dbus_colors.set_title(_('DBus colors'))
        self.pref_use_dbus_colors.set_subtitle( \
            _('Whether to use colors received through DBus (overwrites default profile).'))
        self.pref_use_dbus_colors_switch = Gtk.Switch.new()
        self.pref_use_dbus_colors_switch.set_valign(Gtk.Align.CENTER)
        self.pref_use_dbus_colors.add_suffix(self.pref_use_dbus_colors_switch)
        self.pref_use_dbus_colors.set_activatable_widget(self.pref_use_dbus_colors_switch)
        self.dbus_group.add(self.pref_use_dbus_colors)

        self.pref_dbus_opacity = Adw.ActionRow.new()
        self.pref_dbus_opacity.set_title(_('DBus opacity'))
        self.pref_dbus_opacity.set_subtitle( \
            _('Opacity for the colors received through DBus.'))
        self.pref_dbus_opacity_scale = Gtk.Scale.new_with_range( \
            Gtk.Orientation.HORIZONTAL, 0.0, 100.0, 2.0)
        self.pref_dbus_opacity_scale.set_size_request(180, -1)
        self.pref_dbus_opacity_scale.set_draw_value(True)
        self.pref_dbus_opacity_scale.set_value_pos(Gtk.PositionType.LEFT)
        self.pref_dbus_opacity_scale.set_increments(1.0, 1.0)
        self.pref_dbus_opacity.add_suffix(self.pref_dbus_opacity_scale)
        self.dbus_group.add(self.pref_dbus_opacity)

        self.window_group = Adw.PreferencesGroup.new()
        self.cavalier_page.add(self.window_group)

        self.pref_borderless = Adw.ActionRow.new()
        self.pref_borderless.set_title(_('Borderless window'))
        self.pref_borderless.set_subtitle( \
            _('Whether to disable window shadow and borders.'))
        self.pref_borderless_switch = Gtk.Switch.new()
        self.pref_borderless_switch.set_valign(Gtk.Align.CENTER)
        self.pref_borderless.add_suffix(self.pref_borderless_switch)
        self.pref_borderless.set_activatable_widget(self.pref_borderless_switch)
        self.window_group.add(self.pref_borderless)

        self.pref_sharp_corners = Adw.ActionRow.new()
        self.pref_sharp_corners.set_title(_('Sharp corners'))
        self.pref_sharp_corners.set_subtitle( \
            _('Whether the main window corners should be sharp.'))
        self.pref_sharp_corners_switch = Gtk.Switch.new()
        self.pref_sharp_corners_switch.set_valign(Gtk.Align.CENTER)
        self.pref_sharp_corners.add_suffix(self.pref_sharp_corners_switch)
        self.pref_sharp_corners.set_activatable_widget( \
            self.pref_sharp_corners_switch)
        self.window_group.add(self.pref_sharp_corners)

        self.pref_show_controls = Adw.ActionRow.new()
        self.pref_show_controls.set_title(_('Window controls'))
        self.pref_show_controls.set_subtitle( \
            _('Whether to show window control buttons.'))
        self.pref_show_controls_switch = Gtk.Switch.new()
        self.pref_show_controls_switch.set_valign(Gtk.Align.CENTER)
        self.pref_show_controls.add_suffix(self.pref_show_controls_switch)
        self.pref_show_controls.set_activatable_widget( \
            self.pref_show_controls_switch)
        self.window_group.add(self.pref_show_controls)

        self.pref_autohide_header = Adw.ActionRow.new()
        self.pref_autohide_header.set_title(_('Autohide headerbar'))
        self.pref_autohide_header.set_subtitle( \
            _('Whether to hide headerbar when main window is not focused.'))
        self.pref_autohide_header_switch = Gtk.Switch.new()
        self.pref_autohide_header_switch.set_valign(Gtk.Align.CENTER)
        self.pref_autohide_header.add_suffix(self.pref_autohide_header_switch)
        self.pref_autohide_header.set_activatable_widget( \
            self.pref_autohide_header_switch)
        self.window_group.add(self.pref_autohide_header)

        self.box_import_export = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 12)
        self.box_import_export.set_halign(Gtk.Align.CENTER)
        self.box_import_export.set_margin_top(24)
        self.window_group.add(self.box_import_export)

        self.btn_import = Gtk.Button.new_with_label(_('Import'))
        self.btn_import.add_css_class('pill')
        self.btn_import.connect('clicked', self.import_settings_from_file)
        self.box_import_export.append(self.btn_import)

        self.btn_export = Gtk.Button.new_with_label(_('Export'))
        self.btn_export.add_css_class('pill')
        self.btn_export.connect('clicked', self.export_settings_to_file)
        self.box_import_export.append(self.btn_export)

    def create_cava_page(self):
        self.cava_page = Adw.PreferencesPage.new()
        self.cava_page.set_title('CAVA')
        self.cava_page.set_icon_name('utilities-terminal-symbolic')
        self.add(self.cava_page)

        self.cava_group = Adw.PreferencesGroup.new()
        self.cava_page.add(self.cava_group)

        self.cava_bars_row = Adw.ActionRow.new()
        self.cava_bars_row.set_title(_('Bars'))
        self.cava_group.add(self.cava_bars_row)
        self.cava_bars_scale = Gtk.Scale.new_with_range( \
            Gtk.Orientation.HORIZONTAL, 6.0, 50.0, 2.0)
        self.cava_bars_scale.set_size_request(180, -1)
        self.cava_bars_scale.set_draw_value(True)
        self.cava_bars_scale.set_value_pos(Gtk.PositionType.LEFT)
        self.cava_bars_scale.set_increments(2.0, 2.0)
        self.cava_bars_row.add_suffix(self.cava_bars_scale)

        self.autosens_row = Adw.ActionRow.new()
        self.autosens_row.set_title(_('Automatic sensitivity'))
        self.autosens_row.set_subtitle( \
            _('Attempt to decrease sensitivity if the bars peak.'))
        self.autosens_switch = Gtk.Switch.new()
        self.autosens_switch.set_valign(Gtk.Align.CENTER)
        self.autosens_row.add_suffix(self.autosens_switch)
        self.autosens_row.set_activatable_widget(self.autosens_switch)
        self.cava_group.add(self.autosens_row)

        self.sensitivity_row = Adw.ActionRow.new()
        self.sensitivity_row.set_title(_('Sensitivity'))
        self.sensitivity_row.set_subtitle( \
            _('Manual sensitivity. If automatic sensitivity is enabled, this will only be the initial value.'))
        self.cava_group.add(self.sensitivity_row)
        self.sensitivity_scale = Gtk.Scale.new_with_range( \
            Gtk.Orientation.HORIZONTAL, 10.0, 250.0, 10.0)
        self.sensitivity_scale.set_size_request(150, -1)
        self.sensitivity_scale.set_draw_value(False)
        self.sensitivity_row.add_suffix(self.sensitivity_scale)

        self.channels_row = Adw.ActionRow.new()
        self.channels_row.set_title(_('Channels'))
        self.cava_group.add(self.channels_row)
        self.channels_buttons_box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 0)
        self.channels_buttons_box.add_css_class('linked')
        self.channels_buttons_box.set_valign(Gtk.Align.CENTER)
        self.channels_row.add_suffix(self.channels_buttons_box)
        self.btn_mono = Gtk.ToggleButton.new_with_label(_('Mono'))
        self.channels_buttons_box.append(self.btn_mono)
        self.btn_stereo = Gtk.ToggleButton.new_with_label(_('Stereo'))
        self.channels_buttons_box.append(self.btn_stereo)

        self.smoothing_row = Adw.ComboRow.new()
        self.smoothing_row.set_title(_('Smoothing'));
        self.cava_group.add(self.smoothing_row);
        self.smoothing_row.set_model(Gtk.StringList.new([_('Off'), _('Monstercat')]))

        self.nr_row = Adw.ActionRow.new()
        self.nr_row.set_title(_('Noise Reduction'))
        self.nr_row.set_subtitle(_('0 - noisy, 1 - smooth'))
        self.cava_group.add(self.nr_row)
        self.nr_scale = Gtk.Scale.new_with_range( \
            Gtk.Orientation.HORIZONTAL, 0.0, 1.0, 0.01)
        self.nr_scale.add_mark(0.77, Gtk.PositionType.BOTTOM, None)
        self.nr_scale.set_size_request(190, -1)
        self.nr_scale.set_draw_value(True)
        self.nr_scale.set_value_pos(Gtk.PositionType.LEFT)
        self.nr_scale.get_first_child().set_margin_bottom(12)
        self.nr_row.add_suffix(self.nr_scale)

        self.reverse_order_row = Adw.ActionRow.new()
        self.reverse_order_row.set_title(_('Reverse order'))
        self.reverse_order_switch = Gtk.Switch.new()
        self.reverse_order_switch.set_valign(Gtk.Align.CENTER)
        self.reverse_order_row.add_suffix(self.reverse_order_switch)
        self.reverse_order_row.set_activatable_widget(self.reverse_order_switch)
        self.cava_group.add(self.reverse_order_row)

    def create_colors_page(self):
        self.colors_page = Adw.PreferencesPage.new()
        self.colors_page.set_title(_('Colors'))
        self.colors_page.set_icon_name('applications-graphics-symbolic')
        self.add(self.colors_page)

        self.style_group = Adw.PreferencesGroup.new()
        self.colors_page.add(self.style_group)

        self.style_row = Adw.ActionRow.new()
        self.style_row.set_title(_('Widgets style'))
        self.style_row.set_subtitle(_('Style used by Adwaita widgets.'))
        self.style_buttons_box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 0)
        self.style_buttons_box.add_css_class('linked')
        self.style_buttons_box.set_valign(Gtk.Align.CENTER)
        self.style_row.add_suffix(self.style_buttons_box)
        self.btn_light = Gtk.ToggleButton.new_with_label(_('Light'))
        self.style_buttons_box.append(self.btn_light)
        self.btn_dark = Gtk.ToggleButton.new_with_label(_('Dark'))
        self.style_buttons_box.append(self.btn_dark)
        self.style_group.add(self.style_row)

        self.colors_group = Adw.PreferencesGroup.new()
        self.colors_group.set_title(_('Colors'))
        self.colors_page.add(self.colors_group)

        self.color_profiles = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 4)
        self.color_profiles.set_valign(Gtk.Align.CENTER)
        self.colors_group.set_header_suffix(self.color_profiles)
        self.profiles_label = Gtk.Label.new(_('Profile:'))
        self.color_profiles.append(self.profiles_label)
        self.profiles_list = Gtk.StringList.new(None)
        self.profiles_dropdown = Gtk.DropDown.new(self.profiles_list, None)
        self.color_profiles.append(self.profiles_dropdown)
        self.profile_add_button = Gtk.MenuButton.new()
        self.profile_add_button.set_icon_name('list-add-symbolic')
        self.profile_add_button.add_css_class('circular')
        self.profile_add_button.set_tooltip_text(_('Add new profile'))
        self.color_profiles.append(self.profile_add_button)
        self.profile_add_popover = Gtk.Popover.new()
        self.profile_add_button.set_popover(self.profile_add_popover)
        self.profile_add_box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 4)
        self.profile_add_popover.set_child(self.profile_add_box)
        self.profile_new_box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 0)
        self.profile_new_box.add_css_class('linked')
        self.profile_add_box.append(self.profile_new_box)
        self.profile_add_entry = Gtk.Entry.new()
        self.profile_add_entry.set_hexpand(True)
        self.profile_add_entry.set_placeholder_text( \
            _('Type a name for a new profile'))
        self.profile_new_box.append(self.profile_add_entry)
        self.profile_new_button_add = Gtk.Button.new_with_label(_('Add'))
        self.profile_new_button_add.add_css_class('suggested-action')
        self.profile_new_button_add.connect('clicked', \
            self.create_color_profile)
        self.profile_new_box.append(self.profile_new_button_add)
        self.profile_new_label = Gtk.Label.new(_('The new profile will be a copy of the active profile.'))
        self.profile_add_box.append(self.profile_new_label)
        self.profile_remove_button = Gtk.MenuButton.new()
        self.profile_remove_button.set_icon_name('list-remove-symbolic')
        self.profile_remove_button.add_css_class('circular')
        self.profile_remove_button.set_tooltip_text(_('Remove profile'))
        self.color_profiles.append(self.profile_remove_button)
        self.profile_remove_popover = Gtk.Popover.new()
        self.profile_remove_button.set_popover(self.profile_remove_popover)
        self.profile_remove_box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 10)
        self.profile_remove_popover.set_child(self.profile_remove_box)
        self.profile_remove_label = Gtk.Label.new( \
            _('Are you sure you want to remove this profile?'))
        self.profile_remove_box.append(self.profile_remove_label)
        self.profile_remove_buttons_box = Gtk.Box.new( \
            Gtk.Orientation.HORIZONTAL, 6)
        self.profile_remove_buttons_box.set_halign(Gtk.Align.CENTER)
        self.profile_remove_box.append(self.profile_remove_buttons_box)
        self.profile_remove_button_confirm = Gtk.Button.new_with_label( \
            _('Remove'))
        self.profile_remove_button_confirm.add_css_class('destructive-action')
        self.profile_remove_button_confirm.connect('clicked', \
            self.remove_color_profile)
        self.profile_remove_buttons_box.append( \
            self.profile_remove_button_confirm)
        self.profile_remove_button_cancel = Gtk.Button.new_with_label( \
            _('Cancel'))
        self.profile_remove_button_cancel.connect('clicked', \
            lambda *args: self.profile_remove_popover.popdown())
        self.profile_remove_buttons_box.append( \
            self.profile_remove_button_cancel)

        self.colors_grid = Gtk.Grid.new()
        self.colors_grid.add_css_class('card')
        self.colors_grid.set_column_homogeneous(True)
        self.colors_group.add(self.colors_grid)
        self.fg_lbl = Gtk.Label.new(_('<b>Foreground</b>'))
        self.fg_lbl.set_use_markup(True)
        self.fg_lbl.set_margin_top(12)
        self.fg_lbl.set_margin_bottom(12)
        self.colors_grid.attach(self.fg_lbl, 0, 0, 1, 1)
        self.bg_lbl = Gtk.Label.new(_('<b>Background</b>'))
        self.bg_lbl.set_use_markup(True)
        self.bg_lbl.set_margin_top(12)
        self.bg_lbl.set_margin_bottom(12)
        self.colors_grid.attach(self.bg_lbl, 1, 0, 1, 1)
        self.fg_color_btns = []
        self.bg_color_btns = []

    def load_settings(self):
        (self.wave_check_btn, self.levels_check_btn, \
            self.particles_check_btn, self.spine_check_btn, self.bars_check_btn)[ \
            self.settings.get_range('mode')[1].index(self.settings['mode']) \
            ].set_active(True)
        self.pref_margin_scale.set_value(self.settings['margin'])
        self.pref_offset_scale.set_value(self.settings['items-offset'])
        self.pref_roundness_scale.set_value( \
            round(self.settings['items-roundness'] / 50.0, 2))
        self.pref_thickness_scale.set_value(self.settings['line-thickness'])
        self.pref_fill_switch.set_active(self.settings['fill'])

        self.pref_use_dbus_colors_switch.set_active(self.settings['dbus-colors'])
        self.pref_dbus_opacity_scale.set_value(self.settings['dbus-opacity'])

        self.pref_borderless_switch.set_active( \
            self.settings['borderless-window'])
        self.pref_sharp_corners_switch.set_active( \
            self.settings['sharp-corners'])
        self.pref_show_controls_switch.set_active( \
            self.settings['window-controls'])
        self.pref_autohide_header_switch.set_active( \
            self.settings['autohide-header'])

        self.cava_bars_scale.set_value(self.settings['bars'])
        self.autosens_switch.set_active(self.settings['autosens'])
        self.sensitivity_scale.set_value(self.settings['sensitivity'])
        if self.settings['channels'] == 'mono':
            self.btn_mono.set_active(True)
        else:
            self.btn_stereo.set_active(True)
        self.smoothing_row.set_selected( \
            ['off', 'monstercat'].index(self.settings['smoothing']))
        self.nr_scale.set_value(self.settings['noise-reduction'])
        self.reverse_order_switch.set_active(self.settings['reverse-order'])

        if self.settings['widgets-style'] == 'light':
            self.btn_light.set_active(True)
        else:
            self.btn_dark.set_active(True)
        if not self.settings_bind:
            self.bind_settings()
        profiles = self.settings['color-profiles']
        active_profile = self.settings['active-color-profile']
        self.do_not_change_profile = True
        while self.profiles_list.get_n_items() > 0:
            self.profiles_list.remove(0)
        for p in profiles:
            self.profiles_list.append(p[0])
        try:
            self.fg_colors = profiles[active_profile][1]
            self.bg_colors = profiles[active_profile][2]
        except:
            self.settings['active-color-profile'] = 0
            return
        self.do_not_change_profile = False
        self.profiles_dropdown.set_selected(active_profile)
        self.profile_remove_button.set_sensitive(active_profile != 0)
        self.clear_colors_grid()
        self.fill_colors_grid()

    def bind_settings(self):
        self.wave_check_btn.connect('toggled', self.change_mode, 'wave')
        self.levels_check_btn.connect('toggled', self.change_mode, 'levels')
        self.particles_check_btn.connect('toggled', self.change_mode, \
            'particles')
        self.spine_check_btn.connect('toggled', self.change_mode, 'spine')
        self.bars_check_btn.connect('toggled', self.change_mode, 'bars')
        self.pref_margin_scale.connect('value-changed', self.save_setting, \
            'margin', self.pref_margin_scale.get_value)
        self.pref_offset_scale.connect('value-changed', self.save_setting, \
            'items-offset', self.pref_offset_scale.get_value)
        self.pref_roundness_scale.connect('value-changed', self.save_setting, \
            'items-roundness', lambda *args : \
            self.pref_roundness_scale.get_value() * 50.0)
        self.pref_thickness_scale.connect('value-changed', self.save_setting, \
            'line-thickness', self.pref_thickness_scale.get_value)
        # `notify::state` signal returns additional parameter that
        # we don't need, that's why lambda is used.
        self.pref_fill_switch.connect('notify::state', \
            lambda *args : self.save_setting(self.pref_fill_switch, \
                'fill', self.pref_fill_switch.get_state()))
        # `notify::state` signal returns additional parameter that
        # we don't need, that's why lambda is used.
        self.pref_use_dbus_colors_switch.connect('notify::state', \
            lambda *args : self.save_setting(self.pref_use_dbus_colors_switch, \
                'dbus-colors', self.pref_use_dbus_colors_switch.get_state()))
        self.pref_dbus_opacity_scale.connect('value-changed', self.change_dbus_opacity)
        # `notify::state` signal returns additional parameter that
        # we don't need, that's why lambda is used.
        self.pref_borderless_switch.connect('notify::state', \
            lambda *args : self.save_setting(self.pref_borderless_switch, \
                'borderless-window', self.pref_borderless_switch.get_state()))
        self.pref_sharp_corners_switch.connect('notify::state', \
            lambda *args : self.save_setting(self.pref_sharp_corners_switch, \
                'sharp-corners', self.pref_sharp_corners_switch.get_state()))
        self.pref_show_controls_switch.connect('notify::state', \
            lambda *args : self.save_setting(self.pref_show_controls_switch, \
                'window-controls', self.pref_show_controls_switch.get_state()))
        self.pref_autohide_header_switch.connect('notify::state', \
            lambda *args : self.save_setting(self.pref_autohide_header_switch, \
                'autohide-header', self.pref_autohide_header_switch.get_state()))

        self.cava_bars_scale.connect('value-changed', self.change_bars_count)
        # `notify::state` signal returns additional parameter that
        # we don't need, that's why lambda is used.
        self.autosens_switch.connect('notify::state', \
            lambda *args : self.save_setting(self.autosens_switch, \
                'autosens', self.autosens_switch.get_state()))
        self.sensitivity_scale.connect('value-changed', self.save_setting, \
            'sensitivity', self.sensitivity_scale.get_value)
        self.btn_mono.bind_property('active', self.btn_stereo, 'active', \
            (GObject.BindingFlags.BIDIRECTIONAL | \
             GObject.BindingFlags.SYNC_CREATE | \
             GObject.BindingFlags.INVERT_BOOLEAN))
        self.btn_mono.connect('toggled', self.change_channels)
        self.btn_stereo.connect('toggled', self.change_channels)
        self.smoothing_row.connect('notify::selected-item', \
            lambda *args: self.save_setting(self.smoothing_row, 'smoothing', \
                ['off', 'monstercat'][self.smoothing_row.get_selected()]))
        self.nr_scale.connect('value-changed', self.save_setting, \
            'noise-reduction', self.nr_scale.get_value)
        # `notify::state` signal returns additional parameter that
        # we don't need, that's why lambda is used.
        self.reverse_order_switch.connect('notify::state', \
            lambda *args : self.save_setting(self.reverse_order_switch, \
                'reverse-order', self.reverse_order_switch.get_state()))

        self.btn_dark.bind_property('active', self.btn_light, 'active', \
            (GObject.BindingFlags.BIDIRECTIONAL | \
             GObject.BindingFlags.SYNC_CREATE | \
             GObject.BindingFlags.INVERT_BOOLEAN))
        self.btn_light.connect('toggled', self.apply_style)
        self.btn_dark.connect('toggled', self.apply_style)

        self.profiles_dropdown.connect('notify::selected', \
            self.select_color_profile)

        self.settings_bind = True

    def fill_colors_grid(self):
        counter = 0
        for fg_color in self.fg_colors:
            box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 6)
            box.set_halign(Gtk.Align.CENTER)
            box.set_margin_top(6)
            box.set_margin_bottom(6)
            color = Gdk.RGBA()
            Gdk.RGBA.parse(color, 'rgba(%d, %d, %d, %f)' % fg_color)
            color_dialog = Gtk.ColorDialog.new()
            color_btn = Gtk.ColorDialogButton.new()
            color_btn.set_rgba(color)
            color_btn.set_dialog(color_dialog)
            color_btn.set_tooltip_text(_('Select color'))
            color_btn.set_size_request(98, -1)
            color_btn.connect('notify::rgba', self.color_changed, (0, counter))
            box.append(color_btn)
            rm_btn = Gtk.Button.new_from_icon_name('edit-delete-symbolic')
            rm_btn.add_css_class('circular')
            rm_btn.set_tooltip_text(_('Remove color'))
            if counter == 0:
                rm_btn.set_sensitive(False)
            rm_btn.connect('clicked', self.remove_color, 0, counter)
            box.append(rm_btn)
            self.colors_grid.attach(box, 0, counter + 1, 1, 1)
            counter += 1
        if counter < 10:
            self.fg_add_box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 4)
            self.fg_add_box.set_halign(Gtk.Align.CENTER)
            self.fg_add_box.set_valign(Gtk.Align.CENTER)
            self.fg_add_box.set_margin_bottom(6)
            self.fg_add_box.append(Gtk.Label.new(_('Add')))
            color = Gdk.RGBA()
            Gdk.RGBA.parse(color, '#000f')
            self.fg_add_colordialog = Gtk.ColorDialog.new()
            self.fg_add_colorbtn = Gtk.ColorDialogButton.new()
            self.fg_add_colorbtn.set_rgba(color)
            self.fg_add_colorbtn.set_dialog(self.fg_add_colordialog)
            self.fg_add_colorbtn.set_tooltip_text(_('Select color'))
            self.fg_add_box.append(self.fg_add_colorbtn)
            self.fg_add_btn = Gtk.Button.new_from_icon_name('list-add-symbolic')
            self.fg_add_btn.add_css_class('circular')
            self.fg_add_btn.set_tooltip_text(_('Add color'))
            self.fg_add_btn.connect('clicked', self.add_color, 0)
            self.fg_add_box.append(self.fg_add_btn)
            self.colors_grid.attach(self.fg_add_box, 0, counter + 1, 1, 1)
        counter = 0
        for bg_color in self.bg_colors:
            box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 6)
            box.set_halign(Gtk.Align.CENTER)
            box.set_margin_top(6)
            box.set_margin_bottom(6)
            color = Gdk.RGBA()
            Gdk.RGBA.parse(color, 'rgba(%d, %d, %d, %f)' % bg_color)
            color_dialog = Gtk.ColorDialog.new()
            color_btn = Gtk.ColorDialogButton.new()
            color_btn.set_rgba(color)
            color_btn.set_dialog(color_dialog)
            color_btn.set_tooltip_text(_('Select color'))
            color_btn.set_size_request(98, -1)
            color_btn.connect('notify::rgba', self.color_changed, (1, counter))
            box.append(color_btn)
            rm_btn = Gtk.Button.new_from_icon_name('edit-delete-symbolic')
            rm_btn.add_css_class('circular')
            rm_btn.set_tooltip_text(_('Remove color'))
            rm_btn.connect('clicked', self.remove_color, 1, counter)
            box.append(rm_btn)
            self.colors_grid.attach(box, 1, counter + 1, 1, 1)
            counter += 1
        if counter < 10:
            self.bg_add_box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 4)
            self.bg_add_box.set_halign(Gtk.Align.CENTER)
            self.bg_add_box.set_valign(Gtk.Align.CENTER)
            self.bg_add_box.set_margin_bottom(6)
            self.bg_add_box.append(Gtk.Label.new(_('Add')))
            color = Gdk.RGBA()
            Gdk.RGBA.parse(color, '#000f')
            self.bg_add_colordialog = Gtk.ColorDialog.new()
            self.bg_add_colorbtn = Gtk.ColorDialogButton.new()
            self.bg_add_colorbtn.set_rgba(color)
            self.bg_add_colorbtn.set_dialog(self.bg_add_colordialog)
            self.bg_add_colorbtn.set_tooltip_text(_('Select color'))
            self.bg_add_box.append(self.bg_add_colorbtn)
            self.bg_add_btn = Gtk.Button.new_from_icon_name('list-add-symbolic')
            self.bg_add_btn.add_css_class('circular')
            self.bg_add_btn.set_tooltip_text(_('Add color'))
            self.bg_add_btn.connect('clicked', self.add_color, 1)
            self.bg_add_box.append(self.bg_add_btn)
            self.colors_grid.attach(self.bg_add_box, 1, counter + 1, 1, 1)

    def clear_colors_grid(self):
        while True:
            if (self.colors_grid.get_child_at(0, 1) != None) or \
                    (self.colors_grid.get_child_at(1, 1) != None):
                self.colors_grid.remove_row(1)
            else:
                break

    def select_color_profile(self, obj, pos):
        if self.do_not_change_profile:
            return
        if self.profiles_dropdown.get_selected() != \
                self.settings['active-color-profile']:
            self.settings['active-color-profile'] = \
                self.profiles_dropdown.get_selected()

    def create_color_profile(self, obj):
        if self.profile_add_entry.get_text() == '':
            return
        profiles = self.settings['color-profiles']
        for p in profiles:
            if p[0] == self.profile_add_entry.get_text():
                self.profile_new_label.set_text( \
                    _('This name is already in use.'))
                return
        self.profile_add_popover.popdown()
        active_profile = self.settings['active-color-profile']
        profiles.append((self.profile_add_entry.get_text(), \
            profiles[active_profile][1], profiles[active_profile][2]))
        self.profile_add_entry.set_text('')
        self.profile_new_label.set_text(_('The new profile will be a copy of the active profile.'))
        self.settings['color-profiles'] = profiles
        self.settings['active-color-profile'] = len(profiles) - 1

    def remove_color_profile(self, obj):
        active_profile = self.settings['active-color-profile']
        self.settings['active-color-profile'] = 0
        profiles = self.settings['color-profiles']
        profiles.pop(active_profile)
        self.settings['color-profiles'] = profiles

    def save_color_profiles(self, *args):
        profiles = self.settings['color-profiles']
        active_profile = self.settings['active-color-profile']
        profiles[active_profile] = (profiles[active_profile][0], \
            self.fg_colors, self.bg_colors)
        self.settings['color-profiles'] = profiles
        return False

    def add_color(self, obj, color_type): # color_type 0 for fg, 1 for bg
        if color_type == 0:
            color = self.fg_add_colorbtn.get_rgba()
            self.fg_colors.append((round(color.red * 255), \
                round(color.green * 255), round(color.blue * 255), color.alpha))
        else:
            color = self.bg_add_colorbtn.get_rgba()
            self.bg_colors.append((round(color.red * 255), \
                round(color.green * 255), round(color.blue * 255), color.alpha))
        self.save_color_profiles()

    def remove_color(self, obj, color_type, index):
        if color_type == 0:
            self.fg_colors.pop(index)
        else:
            self.bg_colors.pop(index)
        self.save_color_profiles()

    def color_changed(self, obj, pspec, args):
        color_type, index = args
        if pspec.name != 'rgba':
            return
        if color_type == 0:
            self.fg_colors.pop(index)
            color = obj.get_rgba()
            self.fg_colors.insert(index, (round(color.red * 255), \
                round(color.green * 255), round(color.blue * 255), color.alpha))
        else:
            self.bg_colors.pop(index)
            color = obj.get_rgba()
            self.bg_colors.insert(index, (round(color.red * 255), \
                round(color.green * 255), round(color.blue * 255), color.alpha))
        # Add delay to let Gtk.ColorDialog close itself
        # before it will be removed
        GLib.timeout_add(100, self.save_color_profiles, None)

    def apply_style(self, obj):
        if self.btn_light.get_active():
            self.settings['widgets-style'] = 'light'
        else:
            self.settings['widgets-style'] = 'dark'

    def change_mode(self, obj, mode):
        if(obj.get_active()):
            self.save_setting(obj, 'mode', mode)

    def change_dbus_opacity(self, obj):
        self.save_setting(obj, 'dbus-opacity', self.pref_dbus_opacity_scale.get_value())

    def change_bars_count(self, obj):
        value = self.cava_bars_scale.get_value()
        if value % 2 != 0:
            value -= 1
            self.cava_bars_scale.set_value(value)
        self.save_setting(obj, 'bars', value)

    def change_channels(self, obj):
        if self.btn_mono.get_active():
            self.settings['channels'] = 'mono'
        else:
            self.settings['channels'] = 'stereo'

    def save_setting(self, obj, key, value):
        if callable(value):
            value = value()
        if type(value) is float and type(self.settings[key]) is int:
            value = round(value)
        self.settings[key] = value

    def on_settings_changed(self):
        self.load_settings()

    def import_settings_from_file(self, obj):
        def on_open(source, res, data):
            try:
                file = source.open_finish(res)
            except:
                return
            import_settings(self, file.get_path())

        file_dialog = Gtk.FileDialog.new()
        file_dialog.set_modal(True)
        file_dialog.set_title(_('Import Settings'))
        file_dialog.set_initial_folder( \
            Gio.File.new_for_path(os.environ['HOME']))
        file_filter = Gtk.FileFilter.new()
        file_filter.set_name(_('Cavalier Settings File (*.cavalier)'))
        file_filter.add_pattern('*.cavalier')
        file_filter_all = Gtk.FileFilter.new()
        file_filter_all.set_name(_('All Files'))
        file_filter_all.add_pattern('*')
        file_filter_list = Gio.ListStore.new(Gtk.FileFilter);
        file_filter_list.append(file_filter)
        file_filter_list.append(file_filter_all)
        file_dialog.set_filters(file_filter_list)
        file_dialog.open(self, None, on_open, None)

    def export_settings_to_file(self, obj):
        def on_save(source, res, data):
            try:
                file = source.save_finish(res)
            except:
                return
            export_settings(self, file.get_path())

        file_dialog = Gtk.FileDialog.new()
        file_dialog.set_modal(True)
        file_dialog.set_title(_('Export Settings'))
        file_dialog.set_initial_folder( \
            Gio.File.new_for_path(os.environ['HOME']))
        file_filter = Gtk.FileFilter.new()
        file_filter.set_name(_('Cavalier Settings File (*.cavalier)'))
        file_filter.add_pattern('*.cavalier')
        file_filter_list = Gio.ListStore.new(Gtk.FileFilter);
        file_filter_list.append(file_filter)
        file_dialog.set_filters(file_filter_list)
        file_dialog.save(self, None, on_save, None)
