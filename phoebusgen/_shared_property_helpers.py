from xml.etree.ElementTree import Element, SubElement
from enum import Enum

class _SharedPropertyFunctions(object):
    def __init__(self, root_element):
        self.root = root_element
        from phoebusgen import colors, _predefined_colors, fonts, _predefined_fonts
        self.predefined_colors = _predefined_colors
        self.predefined_fonts = _predefined_fonts
        self.colors = colors
        self.fonts = fonts
        #self.font_styles = {'regular': 'REGULAR', 'italic': 'ITALIC', 'bold': 'BOLD', 'bold_and_italic': 'BOLD_ITALIC'}
        self.arrow_types = {'None': 0, 'From': 1, 'To': 2, 'Both': 3}
        self.line_styles = {'Solid': 0, 'Dashed': 1, 'Dot': 2, 'Dash-Dot': 3, 'Dash-Dot-Dot': 4}
        self.formats_array = ['default', 'decimal', 'exponential', 'engineering', 'hexadecimal',
                              'compact', 'string',  'sexagesimal hh:mm:ss', 'sexagesimal hms 24h rad',
                              'sexagesimal dms 360deg rad', 'binary']

    def add_macro(self, name, val, root_elem=None):
        if root_elem is None:
            root_elem = self.root
        root_macro = root_elem.find('macros')
        if root_macro is None:
            root_macro = SubElement(root_elem, 'macros')
        macro = SubElement(root_macro, name)
        macro.text = str(val)

    def generic_property(self, root_element, prop_type, val=None):
        root_element.append(self.create_element(root_element, prop_type, val))

    def integer_property(self, root_element, prop_type, val):
        if isinstance(val, int) or isinstance(val, float):
            self.generic_property(root_element, prop_type, int(val))
        else:
            print('Property {} must be an integer! Not: {}'.format(prop_type, val))

    def number_property(self, root_element, prop_type, val):
        if isinstance(val, int) or isinstance(val, float):
            self.generic_property(root_element, prop_type, val)
        else:
            print('Property {} must be a number! Not: {}'.format(prop_type, val))

    def boolean_property(self, root_element, prop_type, val):
        if isinstance(val, bool):
            self.generic_property(root_element, prop_type, str(val).lower())
        elif isinstance(val, int):
            self.generic_property(root_element, prop_type, str(bool(val)).lower())
        elif val.lower() == 'true' or val.lower() == 'false':
            self.generic_property(root_element, prop_type, val.lower())
        else:
            print('Property {} must be a boolean value! Not: {}'.format(prop_type, val))

    def create_element(self, root_element, prop_type, val=None):
        element = root_element.find(prop_type)
        if element is not None:
            root_element.remove(element)
        element = Element(prop_type)
        if val is not None:
            if isinstance(val, bool):
                element.text = str(val).lower()
            else:
                element.text = str(val)
        return element

    def valid_rgb_value(self, val):
        try:
            val = int(val)
        except ValueError:
            print('Color RGB value must be a number! Not: {}'.format(val))
            return False
        if 0 <= val <= 255:
            return True
        else:
            print('Color RGB must be between 0 and 255')
            return False

    def create_color_element(self, root_color_elem, name, red, green, blue, alpha, add_to_root=True):
        sub_e = self.create_element(self.root, 'color')
        if name is None:
            for color in [red, green, blue, alpha]:
                if not self.valid_rgb_value(color):
                    return
            sub_e.attrib = {'red': str(red), 'blue': str(blue), 'green': str(green), 'alpha': str(alpha)}
        else:
            if isinstance(name, Enum):
                sub_e.attrib['name'] = name.name
                sub_e.attrib = name.value
            elif isinstance(name, dict):
                sub_e.attrib = name
            elif isinstance(name, str):
                color_attrib = self.predefined_colors.get(name)
                if color_attrib is None:
                    print('Color name is undefined')
                    return
                sub_e.attrib = color_attrib
                sub_e.attrib['name'] = name
            else:
                print('Predefined color input must be phoebusgen.colors.<named-color>, not: {} of type: {}'.format(name, type(name)))
                return
        root_color_elem.append(sub_e)
        if add_to_root:
            self.root.append(root_color_elem)

    def get_font_element(self, root_elem, font_elem_name):
        font_root_elem = root_elem.find(font_elem_name)
        if font_root_elem is None:
            font_root_elem = self.create_element(root_elem, font_elem_name)
            root_elem.append(font_root_elem)
        child_font_elem = font_root_elem.find('font')
        if child_font_elem is None:
            child_font_elem = Element('font')
            child_font_elem.attrib = {'family': 'Liberation Sans', 'size': '14', 'style': 'REGULAR'}
            font_root_elem.append(child_font_elem)
        return child_font_elem

    def add_font_style(self, root_elem, font_elem_name, val):
        if not isinstance(val, self.FontStyle):
            print('The font style parameter must be of type FontStyle enum! Not: {}'.format(type(val)))
            return
        child_elem = self.get_font_element(root_elem, font_elem_name)
        child_elem.attrib['style'] = val.value

    def create_named_font_element(self, root_elem, font_elem_name, name):
        root_font_elem = self.create_element(root_elem, font_elem_name)
        child_font_elem = self.create_element(root_font_elem, 'font')
        if isinstance(name, Enum):
            font_attrib = name.value
        elif isinstance(name, dict):
            font_attrib = name
        elif isinstance(name, str):
            font_attrib = self.predefined_fonts.get(name)
            if font_attrib is None:
                print('Font name is undefined')
                return
            font_attrib['style'] = font_attrib['style'].upper()
        else:
            print('Predefined font input must be phoebusgen.fonts.<named-color>, not: {} of type: {}'.format(name, type(name)))
            return
        child_font_elem.attrib = font_attrib
        root_font_elem.append(child_font_elem)
        self.root.append(root_font_elem)

    class FontStyle(Enum):
        regular = 'REGULAR'
        italic = 'ITALIC'
        bold = 'BOLD'
        bold_and_italic = 'BOLD_ITALIC'

    class HorizontalAlignment(Enum):
        left = 0
        center = 1
        right = 2

    class VerticalAlignment(Enum):
        top = 0
        middle = 1
        bottom = 2

    class RotationStep(Enum):
        zero = 0
        ninety = 1
        one_hundred_eighty = 2
        negative_ninety = 3

    class Mode(Enum):
        toggle = 0
        push = 1
        push_inverted = 2

    class Interpolation(Enum):
        none = 0
        interpolate = 1
        automatic = 2

    class ColorMode(Enum):
        TYPE_CUSTOM = 0
        TYPE_MONO = 1
        TYPE_BAYER = 2
        TYPE_RGB1 = 3
        TYPE_RGB2 = 4
        TYPE_RGB3 = 5
        TYPE_YUV444 = 6
        TYPE_YUV422 = 7
        TYPE_YUV411 = 8
        TYPE_3BYTE_BGR = 9
        TYPE_4BYTE_ABGR = 10
        TYPE_4BYTE_ABGR_PRE = 11
        TYPE_BYTE_BINARY = 12
        TYPE_BYTE_GRAY = 13
        TYPE_BYTE_INDEXED = 14
        TYPE_INT_ARGB = 15
        TYPE_INT_ARGB_PRE = 16
        TYPE_INT_BGR = 17
        TYPE_INT_RGB = 18
        TYPE_USHORT_555_RGB = 19
        TYPE_USHORT_565_RGB = 20
        TYPE_USHORT_GRAY = 21

    class GroupStyle(Enum):
        group_box = 0
        title_bar = 1
        line = 2
        none = 3

    class Resize(Enum):
        no_resize = 0
        size_content_to_fit_widget = 1
        size_widget_to_match_content = 2
        stretch_content_to_fit_widget = 3
        crop_content = 4

    class FileComponent(Enum):
        full_path = 0
        directory = 1
        name_and_extension = 2
        base_name = 3
