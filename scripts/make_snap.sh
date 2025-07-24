#!/bin/bash
snapcraft clean
snapcraft --debug --verbose
sudo snap remove cavasik
sudo snap install --dangerous cavasik*.snap
sudo systemctl restart snapd
sudo systemctl daemon-reload
sudo snap run cavasik || snap run cavasik