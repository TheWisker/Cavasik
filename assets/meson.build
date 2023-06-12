desktop_file = i18n.merge_file(
        input: 'io.github.TheWisker.Cavasik.desktop.in',
       output: 'io.github.TheWisker.Cavasik.desktop',
         type: 'desktop',
       po_dir: '../po',
      install: true,
  install_dir: join_paths(get_option('datadir'), 'applications')
)

desktop_utils = find_program('desktop-file-validate', required: false)
if desktop_utils.found()
 	test('Validate desktop file', desktop_utils, args: [desktop_file])
endif

appstream_file = i18n.merge_file(
        input: 'io.github.TheWisker.Cavasik.metainfo.xml.in',
       output: 'io.github.TheWisker.Cavasik.metainfo.xml',
       po_dir: '../po',
      install: true,
  install_dir: join_paths(get_option('datadir'), 'metainfo')
)

appstream_util = find_program('appstream-util', required: false)
if appstream_util.found()
	test('Validate appstream file', appstream_util, args: ['validate-relax', appstream_file])
endif

install_data('io.github.TheWisker.Cavasik.gschema.xml', install_dir: join_paths(get_option('datadir'), 'glib-2.0/schemas'))

gschema_util = find_program('glib-compile-schemas', required: false)
if gschema_util.found()
 	test('Validate gschema file', gschema_util, args: ['--strict', '--dry-run', meson.current_source_dir()])
endif

subdir('icons')