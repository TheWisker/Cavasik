gnome = import('gnome')
python = import('python')

moduledir = join_paths(pkgdatadir, 'cavasik')

cavasik_sources = [
  '__init__.py',
  'main.py',
  'window.py',
  'cava.py',
  'drawing_area.py',
  'draw_functions.py',
  'settings.py',
  'settings_import_export.py',
  'preferences_window.py',
  'shortcuts.py',
  'dbus.py'
]

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)

install_data(cavasik_sources, install_dir: moduledir)
gnome.compile_resources('cavasik', 'cavasik.gresource.xml', gresource_bundle: true, install: true, install_dir: pkgdatadir)
configure_file(input: 'cavasik.in', output: 'cavasik', configuration: conf, install: true, install_dir: get_option('bindir'))
configure_file(input: 'translation_credits.py.in', output: 'translation_credits.py', configuration: conf, install: true, install_dir: moduledir)