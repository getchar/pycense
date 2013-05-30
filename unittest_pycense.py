#! /usr/bin/python

import unittest
import pycense

class TestSequenceFunctions(unittest.TestCase):
    
    def setUp(self):
        self.com = pycense.commentator("")

    def test_horizontal_endless(self):
        settings = "tb, '//', tf, '=', te, '', w, 5"
        self.com.swap_in(settings, ",")
        should_top = "//==="
        is_top = self.com.get_horizontal("top")
        self.assertEqual(should_top, is_top)


    def test_horizontal_full_sequence(self):
        settings = "tb, '/*', tf, '=', te, '*/', w, 5"
        self.com.swap_in(settings, ",")
        should_top = "/*=*/"
        is_top = self.com.get_horizontal("top")
        self.assertEqual(should_top, is_top)

    def test_horizontal_no_fill(self):
        settings = "tb, '/*', tf, '', te, '*/', w, 5"
        self.com.swap_in(settings, ",")
        should_top = "/* */"
        is_top = self.com.get_horizontal("top")
        self.assertEqual(should_top, is_top)

    def test_horizontal_endlessly_unfulrilled(self):
        settings = "tb, '/*', tf, '', te, '', w, 5"
        self.com.swap_in(settings, ",")
        should_top = "/*"
        is_top = self.com.get_horizontal("top")
        self.assertEqual(should_top, is_top)

    def test_horizontal_bottom(self):
        settings = "bb, '#', bf, '#', be, '#', w, 5"
        self.com.swap_in(settings, ",")
        should_top = "#####"
        is_top = self.com.get_horizontal("bottom")
        self.assertEqual(should_top, is_top)

    def test_horizontal_ljust_on(self):
        settings = "bb, '//', bf, 'AB', be, '', w, 5, bl, True"
        self.com.swap_in(settings, ",")
        should_top = "//ABA"
        is_top = self.com.get_horizontal("bottom")
        self.assertEqual(should_top, is_top)

    def test_horizontal_ljust_off(self):
        settings = "bb, '//', bf, 'AB', be, '', w, 5, bl, False"
        self.com.swap_in(settings, ",")
        should_top = "//BAB"
        is_top = self.com.get_horizontal("bottom")
        self.assertEqual(should_top, is_top)

    def test_min_width(self):
        settings = ("tb, '/*', tf, '', te, '*/', "
                    "lw, '//', rw, '', "
                    "bb, '/*', bf, '', be, '*/'")
        self.com.swap_in(settings, ",")
        should_width = 4
        self.assertEqual(self.com.width, should_width)

if __name__ == "__main__":
    unittest.main()
