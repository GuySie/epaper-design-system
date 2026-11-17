"""An input's default, from its page definition: where a layout needs a fallback for a threshold, it takes the page's
own default instead of repeating the number."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / 'lib'))


def default(page, name):
    import pages
    for i in pages.load(page)['inputs']:
        if i['name'] == name:
            return i['default']
    raise KeyError(f'pages/{page}.yaml has no input {name}')
