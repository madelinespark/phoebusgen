import sys
sys.path.insert(1, '../phoebusgen/')
sys.path.insert(1, './phoebusgen/')

import unittest
import phoebusgen

class TestParse(unittest.TestCase):
    def test_parse_correct(self):
        p = phoebusgen.parse.parse('../examples/testphoebus1.bob')
        self.assertIsNotNone(p)
        self.assertIsNotNone(p.find_widget('macros'))

    def test_wrong_file_type(self):
        #p = parser.parse("./test_screen.py")
        p = phoebusgen.parse.parse('./test_screen.py')
        self.assertIsNone(p)

    def test_not_a_file(self):
        p = phoebusgen.parse.parse('hello')
        self.assertIsNone(p)

    def test_adding_a_widget(self):
        pass

if __name__ == '__main__':
    unittest.main()
