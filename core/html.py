GLYPHICONS = {
    '+status': 'fire',      '-status': 'thumbs-down',
    'delete': 'trash',      'modify': 'pencil',
    'passwd': 'sunglasses',
}
SYMBOLS = {
    '+enabled': '&#10003;', '-enabled': '&#10003;',
    'asc': '&#8638;',       'desc': '&#8642;',
}
COLORS = {
    '+status': 'red',       '-status': 'lightgrey',
    '+enabled': 'blue',     '-enabled': 'grey',
    'delete': 'green',      'modify': 'purple',
    'passwd': 'black',
}


def get_tag(tag, value, css_class='', href='', style='', attrs=''):
    css_class = ' class="{}"'.format(css_class) if css_class else ''
    href = ' href="{}"'.format(href) if href else ''
    style = ' style="{}"'.format(style) if style else ''
    attrs = ' {}'.format(attrs) if attrs else ''
    return '<{t}{c}{h}{s}{a}>{v}</{t}>'.format(
        t=tag, c=css_class, h=href, s=style, a=attrs, v=value)

def get_symbol(value, color=None):
    color = COLORS[value] if not color and value in COLORS else color
    color_style = 'color:{}'.format(color) if color else ''
    if value in GLYPHICONS:
        css_class = 'glyphicon glyphicon-{}'.format(GLYPHICONS[value])
        attrs = 'aria-hidden="true"'
        return get_tag('span', '', css_class=css_class, style=color_style, attrs=attrs)
    elif value in SYMBOLS:
        span = get_tag('span', SYMBOLS.get(value), style=color_style)
        return get_tag('b', span)
    else:
        return ''