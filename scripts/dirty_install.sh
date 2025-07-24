#!/bin/bash

# CLEAN
[[ -d build ]] && rm -fr build

#BUILD
mkdir build
arch-meson . build
meson compile -C build

#INSTALL
sudo meson install -C build
sudo install -Dm644 ./LICENSE -t "/usr/share/licenses/cavasik"