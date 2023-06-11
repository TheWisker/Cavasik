# Moved to https://github.com/NickvisionApps/Cavalier

<p><img src="https://github.com/fsobolev/cavalier/raw/master/data/icons/hicolor/scalable/apps/io.github.fsobolev.Cavalier.svg" width=128px align="left"><h1>Cavalier</h1>

Audio visualizer based on CAVA</p>

<br/>

<a href="https://flathub.org/apps/details/io.github.fsobolev.Cavalier"><img src="https://flathub.org/assets/badges/flathub-badge-en.png" height=48px></a>
<a href="https://aur.archlinux.org/packages/cavalier-git"><img src="https://camo.githubusercontent.com/f4b1ed57afad4fc0cc6f7acbfdf76be7bebaa104563e1e756ba7b91095eec461/68747470733a2f2f692e696d6775722e636f6d2f3958416a6330482e706e67" height=48px></a>
<a href="https://matrix.to/#/#sable-burrow:matrix.org"><img src="https://camo.githubusercontent.com/870f80ce7fd32ac263ec68010d5ee1439e66ee11433858601680debf7f916d47/68747470733a2f2f692e696d6775722e636f6d2f6373496f72374f2e706e67" height=48px></a>

**Cavalier** is an audio visualizer based on [CAVA](https://github.com/karlstav/cava) with customizable LibAdwaita interface.
* 4 drawing modes!
* Set single color or up to 10 colors gradient for background and foreground.
* Configure smoothing, noise reduction and a few other CAVA settings.
* Change background and foreground colors through a DBus interface.

![](https://raw.githubusercontent.com/fsobolev/cavalier/master/data/screenshots/main.png)

## DBus Interface

The application publishes the *io.github.fsobolev.Cavalier* DBus interface with the following methods:
- set_fg_colors(path: str) => bool: Sets the foreground colors sourcing them from the specified file
- set_bg_colors(path: str) => bool: Sets the background colors sourcing them from the specified file
Both methods return a booleand indicating the success of the operation.

The files must have the following format:
r,g,b
r,g,b,a 
10,10,10
10,10,10,0.1

This interface provides the ability to change colors dynamically from a bash file:

interface=io.github.fsobolev.Cavalier
object=/io/github/fsobolev/Cavalier
method=set_fg_colors
argument="~/colors-rgb"

dbus-send --session --dest=$interface --type=method_call --print-reply $object $interface.$method string:$argument

Thus, it can be integrated with tools like Pywal letting you change the colors of Cavalier dynamically to match the wallpaper.

## Building

The easiest way to build the development version of Cavalier is by using GNOME Builder as described [here](https://wiki.gnome.org/Newcomers/BuildProject).

## Translations

See [instruction](po/README.md) on how to translate the app to your language.

## Code of Conduct

This project follows the [GNOME Code of Conduct](https://wiki.gnome.org/Foundation/CodeOfConduct).
