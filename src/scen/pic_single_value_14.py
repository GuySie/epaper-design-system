# the reference picture of this layout (lib/pictures.py): in English, on a BWRY panel; the page shows one level at a
# time: the severe one, with an icon
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/sv_sev.py').read())
INPUTS.update({'weekday_format': 'en', 'icon': 'mdi:molecule-co2', 'displays': ['dev1']})
MODELS = {'dev1': 'BWRY'}
