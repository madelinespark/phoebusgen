import os
import xml.etree.ElementTree as ET
import phoebusgen

def _bool_helper(b):
    bool_dict = {
        'true': True,
        'false': False,
        '0': False,
        '1': True
    }
    return bool_dict[b]
properties = {
    'name': lambda obj, n: obj.name(str(n)),
    'x': lambda obj, x: obj.x(int(x)),
    'y': lambda obj, y: obj.y(int(y)),
    'width': lambda obj, w: obj.width(int(w)),
    'height': lambda obj, h: obj.height(int(h)),
    # rule
    'version': [],
    'pv_name': lambda obj, n: obj.pv_name(str(n)),
    # "predefined_font": [],
    # "font_family": [],
    # "font_size": [],
    # "font_style_bold": [],
    # "font_style_italic": [],
    # "font_style_bold_italic": [],
    # "font_style_regular": [],
    ## title fonts
    ## scale fonts
    ## label fonts
    ## foreground color
    ## predef background color
    # "background_color": [],
    'transparent': lambda obj, t: obj.transparent(_bool_helper(t)),
    # "format": [],
    # "precision": [],
    'show_units': lambda obj, u: obj.show_units(_bool_helper(u)),
    # horizontal alignment -> enums
    # vertical alignment -> enums
    'wrap_words': lambda obj, wr: obj.show_units(_bool_helper(wr)),
    'text': lambda obj, t: obj.text(str(t)),
    'auto_size': [],
    # rotation step -> enums
    # border
    'macro': [],    # call multiple times over list??
    'bit': [],
    # off color
    # off
    # off image
    # on color
    # on
    # on image
    # line color
    'line_width': [],
    # corner class
    'corner_width': [],
    'corner_height': [],
    'square': [],
    'labels_from_pv': [],
    'alarm_border': [],
    'enabled': [],
    # confirmation
    'multi_line': [],
    # angle class
    'angle_start': [],
    'angle_size': [],
    'rotation': [],
    'file': [],
    'stretch_to_fit': [],
    # actions
    'label': [],
    'horizontal': [],
    # traces -> generic widgets
    # trace types
    # point type
    'point_size': [],
    # color
    'axis': [], # might be 'axes' in xml
    'x_pv': [],
    'y_pv': [],
    'err_pv': [],
    'width_pv': [],
    'height_pv': [],
    'on_right': [],
    # y axes
    # x axis
    # markers
    'interactive': [],
    'items_from_pv': [],
    'show_value_tip': [],
    'bar_length': [],
    'show_value': [],
    'show_limits': [],
    'limits_from_pv': [],
    'minimum': [],
    'maximum': [],
    # needle color
    # knob color
    # fill color
    # empty color
    'scale_visible': [],
    'show_led': [],
    # mode
    # style
    # resize behavior
    'group_name': [],
    # structure
    'url': [],
    'show_toolbar': [],
    'buttons_on_left': [],
    'increment': [],
    # file component
    'editable': [],
    # selected color
    # deselected color
    'selection_value_pv': [],
    'point': [],
    # arrow
    # line style
    # tabs
    # nav tabs
    'active_tab': [],
    'tab_height': [],
    'tab_width': [],
    'tab_spacing': [],
    # direction
    'num_bits': [],
    'reverse_bits': [],
    # labels
    'array_index': [],
    'symbols': [],
    'initial_index': [],
    'show_index': [],
    'preserve_ratio': [],
    'show_scale': [],
    'show_minor_ticks': [],
    'major_ticks_pixel_dist': [],
    'scale_format': [],
    # levels
    # states
    # fallback
    'select_rows': [],
    'selection_pv': [],
    # column
    'title': [],
    'auto_scale': [],
    'data_height': [],
    'data_width': [],
    'unsigned_data': [],
    'log_scale': [],
    'show_legend': [],
    'show_grid': [],
    'time_range': [],
    # grid color
    # cursor
    # interpolation
    # color mode
    # roi
    'bar_size': [],
    # color bar
    # color map
}

nested_properties = {}

def _generic_init(w_fn):
    w = None
    try:
        w = w_fn('', 0, 0, 0, 0)
        #return w
    except:
        try:
            w = w_fn('', '', 0, 0, 0, 0)
            #return w
        except:
            try:
                w = w_fn('', '', '', 0, 0, 0, 0)
            except:
                print('Invalid widget', w_fn)
    return w

def _lint_widget(w_list, w_xml, w_type):
    valid_widgets = phoebusgen.widget_versions.keys()
    if w_type not in valid_widgets:
        return False

    lower_name = ''.join(w_type.split('_'))
    l_names = [c.__name__.lower() for c in w_list]
    ind = l_names.index(lower_name)
    w = _generic_init(w_list[ind])
    widget_methods_attrs = [m for m in dir(w) if callable(getattr(w, m)) and not m.startswith('__')]
    # print(w_type, widget_methods_attrs)
    if w is not None:
        for child in w_xml:
            if child.tag == 'widget':
                _lint_widget(child, child.attrib['type'])
            else:
                # print(child.tag)
                if child.tag in widget_methods_attrs:
                    try:
                        #w.name(child.text)
                        # n_l = lambda obj, n: obj.name(n)
                        # n_l(w, "test")
                        #print(child.text)
                        properties[child.tag](w, child.text)
                        #print(properties[child.tag])
                        # print(w)
                    except:
                        print(f"Invalid input for {child.tag}")
                        #return False
                else:
                    pass
                    # print(f"Widget attribute or method '{child.tag}' invalid")
                    # return False
        return True

def lint(fp: str) -> bool:
    # check if file exists
    if not os.path.isfile(fp):
        print(f"File {fp} does not exist.")
        return False

    # check file type
    _, extension = os.path.splitext(fp)
    if not extension == '.bob':
        print(f"File is of type {extension}, not .bob.")
        return False

    # lint_screen
    tree = ET.parse(fp)
    root = tree.getroot()
    s = phoebusgen.screen.Screen('', fp)
    s.root = root
    screen_methods_attrs = [m for m in dir(s) if callable(getattr(s, m)) and not m.startswith('__')]
    screen_methods_attrs.extend(['macros', 'name'])
    l = [cls for cls in phoebusgen.widget.widget._Widget.__subclasses__()]
    for child in root:
        if child.tag in screen_methods_attrs:
            pass
        elif child.tag == 'widget' and child.attrib['type']:
            if not _lint_widget(l, child, child.attrib['type']):
                return False

        else:
            print('Not a valid element', child.tag)
            return False

    return True
