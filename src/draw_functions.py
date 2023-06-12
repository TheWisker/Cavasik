# draw_functions.py
#
# Copyright (c) 2023, TheWisker
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

import cairo
import math

def set_source(cr, height, colors, offset=0):
    if len(colors) > 1:
        pat = cairo.LinearGradient(0.0, height * offset, 0.0, \
            height + height * offset)
        for i in range(len(colors)):
            (red, green, blue, alpha) = colors[i]
            pat.add_color_stop_rgba(1 / (len(colors) - 1) * i, \
                red / 255, green / 255, blue / 255, alpha)
        cr.set_source(pat)
    else:
        (red, green, blue, alpha) = colors[0]
        cr.set_source_rgba(red / 255, green / 255, blue / 255, alpha)

def draw_element(cr, x, y, width, height, radius):
    degrees = math.pi / 180.0
    cr.new_sub_path()
    cr.arc(x + width * radius / 100, y + height * radius / 100, \
        radius * min(width, height) / 100, -180 * degrees, -90 * degrees)
    cr.arc(x + width - width * radius / 100, y + height * radius / 100, \
        radius * min(width, height) / 100, -90 * degrees, 0)
    cr.arc(x + width - width * radius / 100, y + height - height * radius / 100, \
        radius * min(width, height) / 100, 0, 90 * degrees)
    cr.arc(x + width * radius / 100, y + height - height * radius / 100, \
        radius * min(width, height) / 100, 90 * degrees, -180 * degrees)
    cr.close_path()

def wave(sample, cr, width, height, colors, fill, thickness):
    set_source(cr, height, colors)
    ls = len(sample)
    cr.move_to(0, (1.0 - sample[0]) * height)
    for i in range(ls - 1):
        height_diff = (sample[i] - sample[i+1])
        cr.rel_curve_to(width / (ls - 1) * 0.5, 0.0, \
           width / (ls - 1) * 0.5, height_diff * height, \
           width / (ls - 1), height_diff * height)
    if fill:
        cr.line_to(width, height)
        cr.line_to(0, height)
        cr.fill()
    else:
        cr.set_line_width(thickness)
        cr.stroke()

def levels(sample, cr, width, height, colors, offset, radius, fill, thickness):
    set_source(cr, height, colors)
    ls = len(sample)
    step = width / ls
    offset_px = step * offset / 100
    if fill:
        thickness = 0
    else:
        thickness = min(thickness, \
            (step - offset_px * 2) / 2,
            (height / 10 - offset_px) / 2)
        cr.set_line_width(thickness)
    for i in range(ls):
        q = int(round(sample[i], 1) * 10)
        for r in range(q):
            draw_element(cr, step * i + offset_px + thickness / 2, \
                height - (height / 10 * (r + 1)) + offset_px / 2 + thickness / 2, \
                max(step - offset_px * 2 - thickness, 1), \
                max(height / 10 - offset_px - thickness, 1), radius)
    cr.fill() if fill else cr.stroke()

def particles(sample, cr, width, height, colors, offset, radius, fill, thickness):
    set_source(cr, height, colors)
    ls = len(sample)
    step = width / ls
    offset_px = step * offset / 100
    if fill:
        thickness = 0
    else:
        thickness = min(thickness, \
            (step - offset_px * 2) / 2,
            (height / 10) / 2)
        cr.set_line_width(thickness)
    for i in range(ls):
        draw_element(cr, step * i + offset_px + thickness / 2, \
            height * 0.9 - height * 0.9 * sample[i] + thickness / 2, \
            max(step - offset_px * 2 - thickness, 1), \
            max(height / 10 - thickness, 1), radius)
    cr.fill() if fill else cr.stroke()

def spine(sample, cr, width, height, colors, offset, radius, fill, thickness):
    ls = len(sample)
    cr.set_line_width(thickness)
    if height > width:
        step = height / ls
        for i in range(ls):
            set_source(cr, height, colors, sample[i] - (0.95 - i / ls))
            offset_px = step * offset / 100 * sample[i]
            if fill:
                thickness = 0
            else:
                thickness = min(thickness, \
                    (step * sample[i] - offset_px * 2) / 2)
                cr.set_line_width(thickness)
            draw_element(cr, width / 2 - sample[i] * step / 2 + offset_px + thickness / 2, \
                step * i + step / 2 - sample[i] * step / 2 + offset_px + thickness / 2, \
                step * sample[i] - offset_px * 2 - thickness, \
                step * sample[i] - offset_px * 2 - thickness, radius)
        cr.fill() if fill else cr.stroke()
    else:
        step = width / ls
        for i in range(ls):
            set_source(cr, height, colors, sample[i] - 0.45)
            offset_px = step * offset / 100 * sample[i]
            if not fill:
                offset_px += thickness / 2
            draw_element(cr, \
                step * i + step / 2 - sample[i] * step / 2 + offset_px, \
                height / 2 - sample[i] * step / 2 + offset_px, \
                step * sample[i] - offset_px * 2, \
                step * sample[i] - offset_px * 2, radius)
        cr.fill() if fill else cr.stroke()

def bars(sample, cr, width, height, colors, offset, fill, thickness):
    set_source(cr, height, colors)
    ls = len(sample)
    step = width / ls
    offset_px = step * offset / 100
    if fill:
        thickness = 0
    else:
        thickness = min(thickness, (step - offset_px * 2) / 2)
        cr.set_line_width(thickness)
    for i in range(ls):
        cr.rectangle(step * i + offset_px + thickness / 2, \
            height - height * sample[i] + thickness / 2, \
            max(step - offset_px * 2 - thickness, 1), height * sample[i] - thickness)
    cr.fill() if fill else cr.stroke()
