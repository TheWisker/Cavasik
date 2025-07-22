<h1 align="center">Cavasik</h1>
<div align="center">
    <a href="https://github.com/TheWisker/Cavasik">
        <img width="400" src="./assets/icons/io.github.TheWisker.Cavasik.png">
    </a>
</div>
<p align="center">Audio visualizer based on CAVA</p>

<h2 align="center">Changelog</h2>

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.1.0] - 2025-07-22

Minor update for **Cavasik**

### Added
- No additions

### Changed
- Maximum bar count from 100 to 512
- Bits per sample from 16 to 8

### Fixed
- No fixes

## [3.0.0] - 2025-07-22

Major update for **Cavasik**.

### Added
- **Shorcutless mode** related setting. Related [issue](https://github.com/TheWisker/Cavasik/issues/13).
- Ability to **open multiple instances**. As of now they share settings. Related [issue](https://github.com/TheWisker/Cavasik/issues/14).
- **Startup colors** related settings. They allow the colors to be read from a file on startup.
- Simple command line interface that allows to get custom help (not GTK help), version and specify files for setting foreground and/or background colors on start (more scripting).
- Startup colors explanations to README.md.
- DBus Interface explanations to README.md.
- Command line explanations to README.md.

### Changed
- DBus Interface internal workings as to allow the creation of multiple instances.
- Migrated to GNOME runtime 48. Related [issue](https://github.com/TheWisker/Cavasik/issues/10). Related [pull request](https://github.com/TheWisker/Cavasik/pull/12).
- Updated the README.md as to give a brief overview of how settings work. Related [issue](https://github.com/TheWisker/Cavasik/issues/7).
- AUR packages -> Deleted -git version.
- Updated all translations with the new strings.
- Added modifier (usually control) to monokey global shorcuts.
- Made settings conditional to each other, as to only be able to modify one if its taking effect (parent option enabled).

### Fixed
- Little to nothing.

## [2.0.1] - 2023-08-31

Minor update for **Cavasik**.

### Added
- **Mirror Sync** related setting.

### Changed
- No changes

### Fixed
- Some typos

## [2.0.0] - 2023-06-17

**First** official version of **Cavasik**.

### Added

- **Circle** related settings.
- **Circle** version of **Waves** and **Bars**.
- All **mirror modes** and settings.
- All **direction modes** and settings.
- **Color animation** and it's settings.
- **DBus interface** to allow changing colors externally.
- **FPS** configuration option.

### Changed
- Keyboard shortcuts (some removed, some added)

### Fixed
- No fixes

## [1.0.0] - 2023-01-29

Latest release of **Cavalier**.

### Added

- New drawing mode — Particles!
- Color profiles! Create as many as you want and change between them instantly. Unfortunately, this new feature required to change how the - application saves colors, and because of this your previous colors settings will be lost after installing this update.
- Added keyboard shortcuts to change most of the settings on the fly.
- Added option to show/hide window controls.
- Added option to autohide headerbar when the main window is not focused.
- Added option to change roundness of items in "levels" and "particles" modes.
- Added option to reverse the order of bars.
- Import/Export Settings

### Changed
-  No changes

### Fixed
- No fixes

<h2 align="center">Author</h2>
<div align="center">
    <a href="https://github.com/TheWisker">
        <img width="200" height="200" src="./assets/profile.png"></img>
    </a>
</div>
<h4 align="center">TheWisker</h4>
