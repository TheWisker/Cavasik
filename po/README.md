## Translating the app

If you want to make a translation, thank you, you're awesome! 😍 Here are some instructions.

Creating a translation starts by adding `<locale_code>.po` file. There is `cavasik.pot` file which is a template you can copy to begin with.<br/>
If you have never worked with `.po` files before, you can find some help in [gettext manual](https://www.gnu.org/software/gettext/manual/html_node/PO-Files.html). You can also use special apps ([GTranslator](https://flathub.org/apps/details/org.gnome.Gtranslator), for example) instead of text editor.

After editing a file with translation, add language code to `LINGUAS` file. Please keep it alphabetically sorted!

Now, it's time for the world to know your name, hero! Edit `CREDITS.json`. Here you need to specify your name, language and, optionally, email or URL. Example:

```
"Jango Fett": {
    "lang": "Mandalorian",
    "email": "jango@galaxyfarfar.away"
}
```

If you made multiple translations, use an array to list all languages:

```
"C-3PO": {
    "lang": ["Ewokese", "Wookieespeak", "Jawaese"],
    "url": "https://free.droids"
}
```

While editing `CREDITS.json`, don't worry about the order, the app will sort it like it needs. But be aware of commas!

After all is done, send PR! I will review it as soon as possible 😊
