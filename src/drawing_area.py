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
from cavasik.draw_functions import *
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
        cda.timeout = None
        cda.fps = 60
        return cda

    def run(self):
        self.fps = self.settings['fps']
        self.on_settings_changed(None)
        if self.cava == None:
            self.cava = Cava()
        self.cava_thread = Thread(target=self.cava.run)
        self.cava_thread.start()
        if self.spinner != None:
            self.spinner.set_visible(False)
        if self.timeout:
            GObject.source_remove(self.timeout)
        self.cava_sample = self.cava.sample
        self.timeout = GObject.timeout_add(1000.0 / self.fps, self.redraw)

    def on_settings_changed(self, key):
        self.draw_mode = self.settings['mode']
        self.mirror = self.settings['mirror']
        self.mirror_offset = self.settings['mirror-offset']
        self.mirror_opacity = self.settings['mirror-opacity'] / 100
        self.mirror_clones = self.settings['mirror-clones']
        self.mirror_ratio = self.settings['mirror-ratio']
        self.circle = self.settings['circle']
        self.wave_inner_circle = self.settings['wave-inner-circle']
        self.radius = self.settings['radius']
        self.direction = self.settings['direction']
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
        self.color_animation = self.settings['color-animation']
        self.color_animation_length = self.settings['color-animation-length']
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

        try:
            if self.settings['mirror-sync']:
                self.mirror_colors = self.colors
            else:
                color_profile = self.settings['color-profiles'][ \
                    self.settings['mirror-colors']]
                self.mirror_colors = color_profile[1]
        except:
            self.settings['mirror-colors'] = 0
            return
        try:
            color_profile = self.settings['color-profiles'][ \
                self.settings['color-animation-target']]
            self.color_animation_target = color_profile[1]
        except:
            self.settings['color-animation-target'] = 0
            return
        try:
            color_profile = self.settings['color-profiles'][ \
                self.settings['color-animation-mirror-target']]
            self.color_animation_mirror_target = color_profile[1]
        except:
            self.settings['color-animation-mirror-target'] = 0
            return
        self.animation_count = 0
        self.animation_vector = []
        self.mirror_animation_vector = []
        if self.color_animation:
            self.animation_frames = self.fps * self.color_animation_length
            for c, tc in zip(self.colors, self.color_animation_target):
                self.animation_vector.append(((tc[0] - c[0])/self.animation_frames, (tc[1] - c[1])/self.animation_frames, \
                (tc[2] - c[2])/self.animation_frames, (tc[3] - c[3])/self.animation_frames))
            for c, tc in zip(self.colors, self.color_animation_mirror_target):
                self.mirror_animation_vector.append(((tc[0] - c[0])/self.animation_frames, (tc[1] - c[1])/self.animation_frames, \
                (tc[2] - c[2])/self.animation_frames, (tc[3] - c[3])/self.animation_frames))

        if key in ('bars', 'autosens', 'sensitivity', 'channels', \
                'smoothing', 'noise-reduction'):
            if not self.cava.restarting:
                self.cava.stop()
                self.cava.restarting = True
                if self.spinner != None:
                    self.spinner.set_visible(True)
                    self.cava.sample = []
                GObject.timeout_add_seconds(3, self.run)

    def draw_func(self, area, cr, width, height, _, mirror_call):
        if len(self.cava_sample) > 0:
            if not mirror_call:
                if self.color_animation:
                    self.animation_count += 1
                    for i, (c, vc) in enumerate(zip(self.colors, self.animation_vector)):
                        self.colors = self.colors[:i] + [(c[0] + vc[0], c[1] + vc[1], \
                        c[2] + vc[2], c[3] + vc[3])] + self.colors[i+1:]
                    for i, (c, vc) in enumerate(zip(self.mirror_colors, self.mirror_animation_vector)):
                        self.mirror_colors = self.mirror_colors[:i] + [(c[0] + vc[0], c[1] + vc[1], \
                        c[2] + vc[2], c[3] + vc[3])] + self.mirror_colors[i+1:]
                    if self.animation_count >= self.animation_frames:
                        self.animation_count = 0
                        for i, vc in enumerate(self.animation_vector):
                            self.animation_vector = self.animation_vector[:i] + [(-vc[0], -vc[1], -vc[2], -vc[3])] + self.animation_vector[i+1:]
                        for i, vc in enumerate(self.mirror_animation_vector):
                            self.mirror_animation_vector = self.mirror_animation_vector[:i] + [(-vc[0], -vc[1], -vc[2], -vc[3])] + self.mirror_animation_vector[i+1:]

                if self.direction == 'left-right':
                    cr.rotate(0.5*math.pi)
                    cr.translate(0, -width)
                    width, height = height, width
                elif self.direction == 'top-bottom':
                    cr.rotate(math.pi)
                    cr.translate(-width, -height)
                elif self.direction == 'right-left':
                    cr.rotate(1.5*math.pi)
                    cr.translate(-height, 0)
                    width, height = height, width

                if not self.circle and not self.draw_mode == 'spine':
                    match self.mirror:
                        case 'normal':
                            cr.scale(1, -0.5*(1-self.mirror_offset/2))
                            cr.translate(0, (1/(-0.5*(1-self.mirror_offset/2)))*height+(self.mirror_offset*(1/(-0.5*(1-self.mirror_offset/2)))*height/10))
                            prev_colors = [c for c in self.colors]
                            self.colors = [c for c in self.mirror_colors]
                            if not self.mirror_opacity == 1:
                                for c,color in enumerate(self.colors):
                                    self.colors[c] = (self.colors[c][0], self.colors[c][1], self.colors[c][2], self.mirror_opacity)
                            self.draw_func(area, cr, width, height, _, True)
                            self.colors = prev_colors
                            cr.scale(1, -1)
                            cr.translate(0, (1/(-0.5*(1-self.mirror_offset/2)))*height+(self.mirror_offset*(1/(-0.5*(1-self.mirror_offset/2)))*height/5)+1)
                        case 'inverted':
                            cr.scale(1, -0.5)
                            cr.translate(0, -height)
                            prev_colors = [c for c in self.colors]
                            self.colors = [c for c in self.mirror_colors]
                            self.draw_func(area, cr, width, height, _, True)
                            self.colors = prev_colors
                            cr.scale(1, -1)
                        case 'overlapping':
                            self.draw_func(area, cr, width, height, _, True)
                            for i in range(1, self.mirror_clones+1):
                                cr.scale(1, self.mirror_ratio**i)
                                cr.translate(0, (1 - self.mirror_ratio**i)/(self.mirror_ratio**i) * height)
                                if i % 2 == 1:
                                    prev_colors = [c for c in self.colors]
                                    self.colors = [c for c in self.mirror_colors]
                                self.draw_func(area, cr, width, height, _, True)
                                if i % 2 == 1:
                                    self.colors = prev_colors
                        case 'normal+overlapping':
                            cr.scale(1, -0.5*(1-self.mirror_offset/2))
                            cr.translate(0, (1/(-0.5*(1-self.mirror_offset/2)))*height+(self.mirror_offset*(1/(-0.5*(1-self.mirror_offset/2)))*height/10))
                            n_prev_colors = [c for c in self.colors]
                            m_prev_colors = [c for c in self.mirror_colors]
                            if not self.mirror_opacity == 1:
                                for c,color in enumerate(self.colors):
                                    self.colors[c] = (self.colors[c][0], self.colors[c][1], self.colors[c][2], self.mirror_opacity)
                                for c,color in enumerate(self.mirror_colors):
                                    self.mirror_colors[c] = (self.mirror_colors[c][0], self.mirror_colors[c][1], self.mirror_colors[c][2], self.mirror_opacity)
                            self.draw_func(area, cr, width, height, _, True)
                            for i in range(1, self.mirror_clones+1):
                                cr.scale(1, self.mirror_ratio**i)
                                cr.translate(0, (1 - self.mirror_ratio**i)/(self.mirror_ratio**i) * height)
                                if i % 2 == 1:
                                    prev_colors = [c for c in self.colors]
                                    self.colors = [c for c in self.mirror_colors]
                                self.draw_func(area, cr, width, height, _, True)
                                if i % 2 == 1:
                                    self.colors = prev_colors
                            self.colors = n_prev_colors
                            self.mirror_colors = m_prev_colors
                            cr.scale(1, -1) # Flip
                            # Normalize position
                            for i in range(1, self.mirror_clones+1):
                                cr.translate(0, (1 - self.mirror_ratio**i)/(self.mirror_ratio**i) * height)
                                cr.scale(1, (1/(self.mirror_ratio**i)))
                            cr.translate(0, (1/(-0.5*(1-self.mirror_offset/2)))*height+(self.mirror_offset*(1/(-0.5*(1-self.mirror_offset/2)))*height/5)+1)
                            self.draw_func(area, cr, width, height, _, True)
                            for i in range(1, self.mirror_clones+1):
                                cr.scale(1, self.mirror_ratio**i)
                                cr.translate(0, (1 - self.mirror_ratio**i)/(self.mirror_ratio**i) * height)
                                if i % 2 == 1:
                                    prev_colors = [c for c in self.colors]
                                    self.colors = [c for c in self.mirror_colors]
                                self.draw_func(area, cr, width, height, _, True)
                                if i % 2 == 1:
                                    self.colors = prev_colors
                        case 'inverted+overlapping':
                            cr.scale(1, -0.5)
                            cr.translate(0, -height)
                            self.draw_func(area, cr, width, height, _, True)
                            for i in range(1, self.mirror_clones+1):
                                cr.scale(1, self.mirror_ratio**i)
                                cr.translate(0, (1 - self.mirror_ratio**i)/(self.mirror_ratio**i) * height)
                                if i % 2 == 1:
                                    prev_colors = [c for c in self.colors]
                                    self.colors = [c for c in self.mirror_colors]
                                self.draw_func(area, cr, width, height, _, True)
                                if i % 2 == 1:
                                    self.colors = prev_colors
                            cr.scale(1, -1) # Flip
                            # Normalize position
                            for i in range(1, self.mirror_clones+1):
                                cr.translate(0, (1 - self.mirror_ratio**i)/(self.mirror_ratio**i) * height)
                                cr.scale(1, (1/(self.mirror_ratio**i)))
                            self.draw_func(area, cr, width, height, _, True)
                            for i in range(1, self.mirror_clones+1):
                                cr.scale(1, self.mirror_ratio**i)
                                cr.translate(0, (1 - self.mirror_ratio**i)/(self.mirror_ratio**i) * height)
                                if i % 2 == 1:
                                    prev_colors = [c for c in self.colors]
                                    self.colors = [c for c in self.mirror_colors]
                                self.draw_func(area, cr, width, height, _, True)
                                if i % 2 == 1:
                                    self.colors = prev_colors

            if self.draw_mode == 'wave':
                if self.circle:
                    wave_circle(self.cava_sample, cr, width, height, \
                        self.colors, self.radius, self.fill, self.thickness, \
                        self.wave_inner_circle)
                else:
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
                if self.circle:
                    bars_circle(self.cava_sample, cr, width, height, \
                        self.colors, self.offset, self.fill, \
                        self.thickness, self.radius)
                else:
                    bars(self.cava_sample, cr, width, height, self.colors, \
                        self.offset, self.fill, self.thickness)

    def redraw(self):
        self.cava_sample = self.cava.sample
        if self.reverse_order:
            if self.channels == 'mono':
                self.cava_sample = self.cava_sample[::-1]
            else:
                self.cava_sample = \
                    self.cava_sample[0:int(len(self.cava_sample)/2):][::-1] + \
                    self.cava_sample[int(len(self.cava_sample)/2)::][::-1]
        self.queue_draw()
        return True

    def on_unrealize(self, obj):
        self.cava.stop()