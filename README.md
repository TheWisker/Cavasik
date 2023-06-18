<h1 align="center">Cavasik</h1>
<div align="center">
    <img width="400" src="./assets/icons/io.github.TheWisker.Cavasik.png">
</div>
<p align="center">Audio visualizer based on CAVA</p>

<h2 align="center">Description</h2>

<p align="center">This is an audio visualizer based on CAVA with extended capabilities.</p>

<h2 align="center">Details</h2>

The visualizer features:

- Five normal drawing modes!
- Two circle drawing modes!
- Three mirror drawing modes!
- Four drawing directions!
- Customizable LibAdwaita interface!
- Set a single color or up to a 10 color linear gradient for background and foreground!
- Select different foreground colors for the mirrored images in mirror mode!
- Set up a color animation that changes the colors gradually in a loop!
- Configure smoothing, noise reduction and a few other CAVA settings!
- Change background and foreground colors through a DBus interface!

<h2 align="center">Screenshots</h2>

<div align="center">
    <img src="./assets/screenshots/main.png"></img>
</div>

<h3 align="center">Waves mode</h2>

<div align="center">
    <img src="./assets/screenshots/waves.png"></img>
</div>

<h3 align="center">Levels mode</h2>

<div align="center">
    <img src="./assets/screenshots/levels.png"></img>
</div>

<h3 align="center">Particles mode</h2>

<div align="center">
    <img src="./assets/screenshots/particles.png"></img>
</div>

<h3 align="center">Spine mode</h2>

<div align="center">
    <img src="./assets/screenshots/spine.png"></img>
</div>

<h3 align="center">Bars mode</h2>

<div align="center">
    <img src="./assets/screenshots/bars.png"></img>
</div>

<h3 align="center">Normal mirror + Waves mode</h2>

<div align="center">
    <img src="./assets/screenshots/mirror_normal.png"></img>
</div>

<h3 align="center">Inverted mirror + Waves mode</h2>

<div align="center">
    <img src="./assets/screenshots/mirror_inverted.png"></img>
</div>

<h3 align="center">Overlapping mirror + Waves mode</h2>

<div align="center">
    <img src="./assets/screenshots/mirror_overlapping.png"></img>
</div>

<h3 align="center">Direction top-bottom + Waves mode</h2>

<div align="center">
    <img src="./assets/screenshots/direction_top.png"></img>
</div>

<h3 align="center">Normal mirror + Direction left-right + Waves mode</h2>

<div align="center">
    <img src="./assets/screenshots/mirror_column.png"></img>
</div>

<h2 align="center">Installation</h2>

<h3>Flathub</h3>

You can install the **Cavasik** app from [Flathub][flathub] in its [app page][flathub-cavasik].

<h3>Arch Linux</h3>

You can install **Cavasik** from the [AUR][aur] repository:

- Release version:
<a href="https://aur.archlinux.org/packages/cavasik"><img src="https://camo.githubusercontent.com/f4b1ed57afad4fc0cc6f7acbfdf76be7bebaa104563e1e756ba7b91095eec461/68747470733a2f2f692e696d6775722e636f6d2f3958416a6330482e706e67" height=48px></a>

- Development version:
<a href="https://aur.archlinux.org/packages/cavasik-git"><img src="https://camo.githubusercontent.com/f4b1ed57afad4fc0cc6f7acbfdf76be7bebaa104563e1e756ba7b91095eec461/68747470733a2f2f692e696d6775722e636f6d2f3958416a6330482e706e67" height=48px></a>

<h3>Manually</h3>

<h2 align="center">Contributing</h2>

All contributions are welcome!
The steps involved when making a contribution are listed in the [CONTRIBUTING.md][contributing] file.

<h2 align="center">Translations</h2>

All translations are welcome!
The steps involved when making a translation are listed in the [CONTRIBUTING.md][contributing] file.
More specific steps can be found in the [CONTRIBUTING.md][lang-contributing] file in the `/lang` folder.

<h2 align="center">Code of Conduct</h2>

<p align="center">This project follows the Covenant Code of Conduct which can be found [here][coc].</p>

[flathub]: https://flathub.org/
[flathub-cavasik]: x
[aur]: https://aur.archlinux.org/
[contributing]: ./CONTRIBUTING.md
[lang-contributing]: ./lang/CONTRIBUTING.md
[coc]: ./.github/CODE_OF_CONDUCT.md

<h2 align="center">Forked</h2>
<div align="center">
    <img width="200" height="200" src="./assets/fork_profile.png"></img>
</div>
<h4 align="center">Fsobolev</h4>

<h2 align="center">Author</h2>
<div align="center">
    <img width="200" height="200" src="./assets/profile.png"></img>
</div>
<h4 align="center">TheWisker</h4>


<a href="https://flathub.org/apps/details/io.github.TheWisker.Cavasik"><img src="https://flathub.org/assets/badges/flathub-badge-en.png" height=48px></a>

<a href="https://matrix.to/#/#sable-burrow:matrix.org"><img src="https://camo.githubusercontent.com/870f80ce7fd32ac263ec68010d5ee1439e66ee11433858601680debf7f916d47/68747470733a2f2f692e696d6775722e636f6d2f6373496f72374f2e706e67" height=48px></a>

**Cavasik** is an audio visualizer based on [CAVA](https://github.com/karlstav/cava) with customizable LibAdwaita interface.
* 4 drawing modes!
* Set single color or up to 10 colors gradient for background and foreground.
* Configure smoothing, noise reduction and a few other CAVA settings.
* Change background and foreground colors through a DBus interface.

![](https://raw.githubusercontent.com/TheWisker/cavasik/master/data/screenshots/main.png)

## DBus Interface

The application publishes the *io.github.TheWisker.Cavasik* DBus interface with the following methods:
- set_fg_colors(path: str) => bool: Sets the foreground colors sourcing them from the specified file
- set_bg_colors(path: str) => bool: Sets the background colors sourcing them from the specified file
Both methods return a booleand indicating the success of the operation.

The files must have the following format:
r,g,b
r,g,b,a 
10,10,10
10,10,10,0.1

This interface provides the ability to change colors dynamically from a bash file:

interface=io.github.TheWisker.Cavasik
object=/io/github/TheWisker/Cavasik
method=set_fg_colors
argument="~/colors-rgb"

dbus-send --session --dest=$interface --type=method_call --print-reply $object $interface.$method string:$argument

Thus, it can be integrated with tools like Pywal letting you change the colors of Cavasik dynamically to match the wallpaper.

## Building

The easiest way to build the development version of Cavasik is by using GNOME Builder as described [here](https://wiki.gnome.org/Newcomers/BuildProject).

## Translations

See [instruction](po/README.md) on how to translate the app to your language.

## Code of Conduct

This project follows the [GNOME Code of Conduct](https://wiki.gnome.org/Foundation/CodeOfConduct).
