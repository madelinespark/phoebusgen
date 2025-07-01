import xml.etree.ElementTree as ET
import phoebusgen

def parse(fp):
    try:
        tree = ET.parse(fp)
    except:
        print(f'File "{fp}" does not exist.')
        return
    else:
        root = tree.getroot()
        screen = phoebusgen.screen.Screen('', '')
        screen.bob_file = fp
        screen.root = root
        return screen
