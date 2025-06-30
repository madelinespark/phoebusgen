import xml.etree.ElementTree as ET
import phoebusgen
import phoebusgen.screen
import phoebusgen.screen.screen

widget_dict = {
    'arc': {
        'count': 0,
        'var_name': lambda : 'arc' + str(widget_dict['arc']['count']),
        'init': lambda n, x, y, w, h : widget_dict['arc']['var_name']() + f' = phoebusgen.widget.Arc({n}, {x}, {y}, {w}, {h})'
    },
    'ellipse': {},
    'label': {},
    'picture': {},
    'polygon': {},
    'polyline': {},
    'rectangle': {},
    'byte_monitor': {},
    'led': {},
    'multi_state_led': {},
    'meter': {},
    'progressbar': {},
    'symbol': {},
    'table': {},
    'tank': {},
    'text-symbol': {},
    'textupdate': {},
    'thermometer': {},
    'action_button': {},
    'bool_button': {},
    'checkbox': {},
    'choice': {},
    'combo': {},
    'fileselector': {},
    'radio': {},
    'scaledslider': {},
    'scrollbar': {},
    'slide_button': {},
    'spinner': {},
    'textentry': {},
    'databrowser': {},
    'image': {},
    'stripchart': {},
    'xyplot': {},
    'array': {},
    'embedded': {}, #special case?
    'group': {},    #special case
    'navtabs': {},
    'tabs': {},
    '3dviewer': {},
    'webbrowser': {}
}

generic_dict = {
    'trace': {},
    'x_axis': {},
    'y_axis': {},
    'marker': {},
    'roi': {},
    'color_bar': {},
    'section': {}
}

function_dict = {}

def _parse(r):
    if not list(r):
        return {r.tag: r.attrib if len(r.attrib) != 0 else r.text}
    elif r.tag == 'widget': # widgets
        return {'widget' : {r.attrib['type']: list(map(_parse, list(r)))}}
    elif r.tag in ['trace', 'y_axis', 'x_axis', 'marker', 'roi', 'color_bar', 'section']:   # generics
        return {r.tag: list(map(_parse, list(r)))}
    else:   # properties/methods
        return list(map(_parse, list(r)))


def _parse_generic(n: str, g: dict):
    g_type = list(g.keys())[0]
    if g_type in generic_dict:
        pass
    else:
        raise KeyError('Generic widget type does not exist.')

def _parse_function(n: str, f: dict) -> list:
    f_type = list(f.keys())[0]
    if f_type in function_dict:
        pass
    else:
        raise KeyError('Function type does not exist.')

def _parse_widget(w: dict) -> list:
    w_type = list(w.keys())[0]
    if w_type in widget_dict:
        pass
    else:
        raise KeyError('Widget type does not exist.')


def parse_to_python_file(fp, fd=None):
    tree = ET.parse(fp)
    root = tree.getroot()
    nested_dicts = _parse(root)  # pre-parsed into list of dictionaries
    python_strings = ['import phoebusgen', 'widgets = []']
    #print(nested_dicts)

    # using dictionary mapping, map into python code in string form
    for d in nested_dicts:
        if 'widget' in d:
            print(d)
            #python_strings.extend(_parse_widget(d['widget']))
        elif 'name' in d:
            v = d['name']
            python_strings.append(f'my_screen = phoebusgen.screen.Screen("{v}")')
        else:
            print(d)
            k = list(d.keys())[0]   # all dictionaries have one k,v pair
            python_strings.append(f'my_screen.{k}({d[k]})')
    # append to list
    # write list to file
    python_strings.extend(['my_screen.add_widget(widgets)', f'my_screen.write_screen("{fp}_new")']) # can change fp... this is for testing
    print(python_strings)   # also for testing

def parse(fp):
    tree = ET.parse(fp)
    root = tree.getroot()
    screen = phoebusgen.screen.Screen('', '')
    screen.bob_file = fp
    screen.root = root
    return screen
