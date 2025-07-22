# cava.py
#
# Copyright (c) 2023, TheWisker
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

import os
import subprocess
import struct
from cavasik.settings import CavasikSettings

class Cava:
    def __init__(self):
        self.BYTETYPE = "B"
        self.BYTESIZE = 1
        self.BYTENORM = 255
        self.restarting = False

        self.settings = CavasikSettings.new()
        self.fps = self.settings['fps']

        self.sample = []

        if os.getenv('XDG_CONFIG_HOME'):
            self.config_dir = os.getenv('XDG_CONFIG_HOME') + '/cavasik'
        else:
            self.config_dir = os.getenv('HOME') + '/.config/cavasik'
        if not os.path.isdir(self.config_dir):
            os.makedirs(self.config_dir)
        self.config_file_path = self.config_dir + '/config'

    def run(self):
        self.load_settings()
        self.write_config()
        self.process = subprocess.Popen(["cava", "-p", self.config_file_path], \
            stdout=subprocess.PIPE)
        source = self.process.stdout
        self.restarting = False
        self.chunk = self.BYTESIZE * self.bars
        self.fmt = self.BYTETYPE * self.bars
        while True:
            data = source.read(self.chunk)
            if len(data) < self.chunk or self.restarting:
                break
            self.sample = \
                [i / self.BYTENORM for i in struct.unpack(self.fmt, data)]

    def stop(self):
        if not self.restarting:
            self.process.kill()

    def load_settings(self):
        # Cava config options
        self.bars = self.settings['bars']
        self.autosens = int(self.settings['autosens'])
        self.sensitivity = self.settings['sensitivity']
        self.channels = self.settings['channels']
        self.monstercat = \
            ['off', 'monstercat'].index(self.settings['smoothing'])
        self.noise_reduction = self.settings['noise-reduction']
        print(self.noise_reduction)

    def write_config(self):
        try:
            f = open(self.config_file_path, 'w')
            conf = '\n'.join([
                '[general]',
                f'bars = {self.bars}',
                f'autosens = {self.autosens}',
                f'sensitivity = {self.sensitivity ** 2}',
                f'framerate = {self.fps}',
                '[input]',
                'method = pulse',
                '[output]',
                f'channels = {self.channels}',
                'mono_option = average',
                'method = raw',
                'raw_target = /dev/stdout',
                'bit_format = 8bit',
                '[smoothing]',
                f'monstercat = {self.monstercat}',
                f'noise_reduction = {self.noise_reduction}'
            ])
            print(conf)
            f.write(conf)
            f.close()
        except Exception as e:
            print("Can't write config file for cava...'")
            print(e)

