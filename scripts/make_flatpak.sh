#!/bin/bash
VERSION=$(grep -oP "(?<!meson_)version:\s*'\K[^']+" meson.build)
flatpak remote-add --user --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
flatpak-builder --user --force-clean --install-deps-from=flathub --repo=repo --install builddir io.github.TheWisker.Cavasik.json
flatpak build-bundle ./repo cavasik_${VERSION}_amd64.flatpak io.github.TheWisker.Cavasik
flatpak-builder --run builddir io.github.TheWisker.Cavasik.json cavasik