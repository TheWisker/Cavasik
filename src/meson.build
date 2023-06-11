pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'cavalier')
gnome = import('gnome')

gnome.compile_resources('cavalier',
  'cavalier.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'cavalier.in',
  output: 'cavalier',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

cavalier_sources = [
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

install_data(cavalier_sources, install_dir: moduledir)

configure_file(
  input: 'translator_credits.py.in',
  output: 'translator_credits.py',
  configuration: conf,
  install: true,
  install_dir: moduledir
)