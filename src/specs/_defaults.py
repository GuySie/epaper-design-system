"""What a layout takes from elsewhere instead of typing it: an input's default from its page definition (a threshold's
fallback), and how many points a line chart may have on its screen."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / 'lib'))


def default(page, name):
    import pages
    for i in pages.load(page)['inputs']:
        if i['name'] == name:
            return i['default']
    raise KeyError(f'pages/{page}.yaml has no input {name}')


def chart_points(spec, widest):
    """the most points a line chart shows: one per 2 x line.base of plot width (*Chart frame (all charts)*, Density).
    The plot is the canvas between the paddings, less the label margin: the widest value label and space.s"""
    import derive_tokens as dt, doc_values
    from layouts import layouts
    from PIL import ImageFont
    tier = next(l['tier'] for l in layouts() if l['spec'] == spec)
    W = dt.KNOWN[tier][0]
    tk = dt.derive(*dt.KNOWN[tier])[0]
    size = tk['type']['label'][1]
    fonts = pathlib.Path(__file__).resolve().parent.parent / 'fonts'
    label = ImageFont.truetype(str(fonts / dt.font_files()[tk['type']['label'][0]]), size).getlength(str(widest))
    plot = W - 2 * tk['space']['pad'] - int(label) - int(doc_values.value(f's.{size}'))
    return plot // (2 * tk['line']['base'])
