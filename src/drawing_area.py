# drawing_area.py
#
# Copyright (c) 2023, TheWisker
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

from gi.repository import Gtk, GObject
from threading import Thread
from cavasik.cava import Cava
from cavasik.draw_functions import wave, levels, particles, spine, bars
from cavasik.settings import CavasikSettings

class CavasikDrawingArea(Gtk.DrawingArea):
    __gtype_name__ = 'CavasikDrawingArea'

    def __init__(self, settings, **kwargs):
        super().__init__(**kwargs)

    def new():
        cda = Gtk.DrawingArea.new()
        cda.__class__ = CavasikDrawingArea
        cda.set_vexpand(True)
        cda.set_hexpand(True)
        cda.set_draw_func(cda.draw_func, None, None)
        cda.cava = None
        cda.spinner = None
        cda.settings = CavasikSettings.new(cda.on_settings_changed)
        cda.connect('unrealize', cda.on_unrealize)
        return cda

    def run(self):
        self.on_settings_changed(None)
        if self.cava == None:
            self.cava = Cava()
        self.cava_thread = Thread(target=self.cava.run)
        self.cava_thread.start()
        if self.spinner != None:
            self.spinner.set_visible(False)
        GObject.timeout_add(1000.0 / 60.0, self.redraw)

    def on_settings_changed(self, key):
        self.draw_mode = self.settings['mode']
        self.set_margin_top(self.settings['margin'])
        self.set_margin_bottom(self.settings['margin'])
        self.set_margin_start(self.settings['margin'])
        self.set_margin_end(self.settings['margin'])
        self.offset = self.settings['items-offset']
        self.roundness = self.settings['items-roundness']
        self.thickness = self.settings['line-thickness']
        self.fill = self.settings['fill']
        self.reverse_order = self.settings['reverse-order']
        self.channels = self.settings['channels']
        try:
            color_profile = self.settings['color-profiles'][ \
                self.settings['active-color-profile']]
            self.colors = color_profile[1]
        except:
            self.colors = []
        if len(self.colors) == 0:
            self.settings['color-profiles'] = [(_('Default'), \
                [(53, 132, 228, 1.0)], [])]
            return

        if key in ('bars', 'autosens', 'sensitivity', 'channels', \
                'smoothing', 'noise-reduction'):
            if not self.cava.restarting:
                self.cava.stop()
                self.cava.restarting = True
                if self.spinner != None:
                    self.spinner.set_visible(True)
                    self.cava.sample = []
                GObject.timeout_add_seconds(3, self.run)

    def draw_func(self, area, cr, width, height, data, n):
        if len(self.cava_sample) > 0:
            if self.draw_mode == 'wave':
                wave(self.cava_sample, cr, width, height, self.colors, \
                    self.fill, self.thickness)
            elif self.draw_mode == 'levels':
                levels(self.cava_sample, cr, width, height, self.colors, \
                    self.offset, self.roundness, self.fill, self.thickness)
            elif self.draw_mode == 'particles':
                particles(self.cava_sample, cr, width, height, self.colors, \
                    self.offset, self.roundness, self.fill, self.thickness)
            elif self.draw_mode == 'spine':
                spine(self.cava_sample, cr, width, height, self.colors, \
                    self.offset, self.roundness, self.fill, self.thickness)
            elif self.draw_mode == 'bars':
                bars(self.cava_sample, cr, width, height, self.colors, \
                    self.offset, self.fill, self.thickness)

    def redraw(self):
        self.queue_draw()
        self.cava_sample = self.cava.sample
        if self.reverse_order:
            if self.channels == 'mono':
                self.cava_sample = self.cava_sample[::-1]
            else:
                self.cava_sample = \
                    self.cava_sample[0:int(len(self.cava_sample)/2):][::-1] + \
                    self.cava_sample[int(len(self.cava_sample)/2)::][::-1]
        return True

    def on_unrealize(self, obj):
        self.cava.stop()
