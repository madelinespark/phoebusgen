import os
import xml.etree.ElementTree as ET
import phoebusgen

def parse(fp):
    correct = phoebusgen.lint.lint(fp)
    if correct:
        tree = ET.parse(fp)
        root = tree.getroot()
        screen = phoebusgen.screen.Screen('', fp)
        screen.root = root
        return screen
