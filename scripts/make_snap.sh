#!/bin/bash
VERSION=$(grep -oP "(?<!meson_)version:\s*'\K[^']+" meson.build)
snapcraft clean
snapcraft --debug --verbose
sudo snap remove cavasik
sudo snap install --dangerous cavasik_${VERSION}_amd64.snap
sudo systemctl restart snapd
sudo systemctl daemon-reload
sudo snap run cavasik || snap run cavasik