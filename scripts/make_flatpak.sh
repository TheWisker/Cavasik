#!/bin/bash
VERSION=$(grep -oP "(?<!meson_)version:\s*'\K[^']+" meson.build)
flatpak remote-add --user --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
flatpak-builder --user --force-clean --install-deps-from=flathub --repo=repo --install builddir io.github.TheWisker.Cavasik.json
flatpak build-bundle ./repo cavasik_${VERSION}_all.flatpak io.github.TheWisker.Cavasik