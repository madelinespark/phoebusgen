import os
import xml.etree.ElementTree as ET
import phoebusgen.screen

def parse(fp):
    # check if file exists
    if not os.path.isfile(fp):
        print(f"File {fp} does not exist.")
        return False

    # check file type
    _, extension = os.path.splitext(fp)
    if not extension == '.bob':
        print(f"File is of type {extension}, not .bob.")
        return False

    tree = ET.parse(fp)
    root = tree.getroot()
    screen = phoebusgen.screen.Screen('', fp)
    screen.root = root
    return screen
