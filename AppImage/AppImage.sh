#!/bin/sh

set -eu

ARCH=$(uname -m)
VERSION=$(pacman -Q cavasik-git | awk '{print $2; exit}') # example command to get version of application here
export ARCH VERSION

SHARUN="https://raw.githubusercontent.com/pkgforge-dev/Anylinux-AppImages/refs/heads/main/useful-tools/quick-sharun.sh"
DEBLOATED_PKGS="https://raw.githubusercontent.com/pkgforge-dev/Anylinux-AppImages/refs/heads/main/useful-tools/get-debloated-pkgs.sh"

export OUTPATH=./dist
export ADD_HOOKS="self-updater.bg.hook"
#export UPINFO="gh-releases-zsync|${GITHUB_REPOSITORY%/*}|${GITHUB_REPOSITORY#*/}|latest|*$ARCH.AppImage.zsync"
export ICON=/usr/share/icons/hicolor/scalable/apps/io.github.TheWisker.Cavasik.svg
export DESKTOP=/usr/share/applications/io.github.TheWisker.Cavasik.desktop
export PATH_MAPPING='/usr/share/cavasik:${SHARUN_DIR}/share/cavasik'
export DEPLOY_PYTHON=1

#Remove leftovers
rm -rf AppDir dist

# ADD LIBRARIES
wget --retry-connrefused --tries=30 "$SHARUN" -O ./quick-sharun
wget --retry-connrefused --tries=30 "$DEBLOATED_PKGS" -O ./get-debloated-pkgs
chmod +x ./quick-sharun ./get-debloated-pkgs

# Debloated pkgs
./get-debloated-pkgs --add-common --prefer-nano

# Deploy dependencies
./quick-sharun \
	/usr/bin/cava \
	/usr/bin/cavasik

# Turn AppDir into AppImage
./quick-sharun --make-appimage
