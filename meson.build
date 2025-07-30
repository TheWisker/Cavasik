project('cavasik', version: 'v3.2.0', meson_version: '>= 1.1', default_options: ['warning_level=2', 'werror=false'])

i18n = import('i18n')
gnome = import('gnome')

pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
localedir = join_paths(get_option('prefix'), get_option('localedir'))

subdir('assets')
subdir('src')
subdir('lang')

gnome.post_install(glib_compile_schemas: true, gtk_update_icon_cache: true, update_desktop_database: true)
