#! /usr/bin/python
###############################################################################
# Copyright (c) 2013 Charlie Pashayan                                         #
#                                                                             #
# Permission is hereby granted, free of charge, to any person obtaining a     #
# copy of this software and associated documentation files (the "Software"),  #
# to deal in the Software without restriction, including without limitation   #
# the rights to use, copy, modify, merge, publish, distribute, sublicense,    #
# and/or sell copies of the Software, and to permit persons to whom the       #
# Software is furnished to do so, subject to the following conditions:        #
#                                                                             #
# The above copyright notice and this permission notice shall be included in  #
# all copies or substantial portions of the Software.                         #
#                                                                             #
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR  #
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,    #
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE #
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER      #
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING     #
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER         #
# DEALINGS IN THE SOFTWARE.                                                   #
###############################################################################

import unittest
import objects

class TestSequenceFunctions(unittest.TestCase):
    def setUp(self):
        self.com = objects.Commentator("")

    def test_horizontal_endless(self):
        """Generate horizontal border with no end."""
        settings = eval("[('tb', '//'), ('tf', '='), ('te', ''), ('w', 5)]")
        self.com.swap_in(settings)
        should_top = "//==="
        is_top = self.com.get_horizontal("top")
        self.assertEqual(should_top, is_top)


    def test_horizontal_full_sequence(self):
        """Generate horizontal border with beginning, fill and end."""
        settings = eval("[('tb', '/*'), ('tf', '='), ('te', '*/'), ('w', 5)]")
        self.com.swap_in(settings)
        should_top = "/*=*/"
        is_top = self.com.get_horizontal("top")
        self.assertEqual(should_top, is_top)

    def test_horizontal_no_fill(self):
        """Generate horizontal border with beginning and end but no fill;
        verify that get_horizonal fills in necessary region with spaces."""
        settings = eval("[('tb', '/*'), ('tf', ''), ('te', '*/'), ('w', 5)]")
        self.com.swap_in(settings)
        should_top = "/* */"
        is_top = self.com.get_horizontal("top")
        self.assertEqual(should_top, is_top)

    def test_horizontal_endlessly_unfulfilled(self):
        """Generate horizontal border with only a beginnint."""
        settings = eval("[('tb', '/*'), ('tf', ''), ('te', ''), ('w', 5)]")
        self.com.swap_in(settings)
        should_top = "/*"
        is_top = self.com.get_horizontal("top")
        self.assertEqual(should_top, is_top)

    def test_horizontal_bottom(self):
        """All previous tests were for the top piece.  Make one for the 
        bottom."""
        settings = eval("[('bb', '#'), ('bf', '#'), ('be', '#'), ('w', 5)]")
        self.com.swap_in(settings)
        should_top = "#####"
        is_top = self.com.get_horizontal("bottom")
        self.assertEqual(should_top, is_top)

    def test_horizontal_rjust_on(self):
        """Make a horizontal border where the length of the fill is not an even
        multiple of the space between the end pieces.  Verify that fill is
        justified to the left."""
        settings = eval("[('bb', '//'), ('bf', 'AB'), ('be', ''), ('w', 5), ('br', False)]")
        self.com.swap_in(settings)
        should_top = "//ABA"
        is_top = self.com.get_horizontal("bottom")
        self.assertEqual(should_top, is_top)

    def test_horizontal_rjust_off(self):
        """Make a horizontal border where the length of the fill is not an even
        multiple of the space between the end pieces.  Verify that fill is
        justified to the right."""
        settings = eval("[('bb', '//'), ('bf', 'AB'), ('be', ''), ('w', 5), ('br', True)]")
        self.com.swap_in(settings)
        should_top = "//BAB"
        is_top = self.com.get_horizontal("bottom")
        self.assertEqual(should_top, is_top)

    def test_min_width_by_length(self):
        """Create a Commentator with a width smaller than the lengths of the
        end pieces will allow.  Veryfiy that the validation process replaces
        that bad width with something reasonable."""
        settings = eval(("[('tb', '/*'), ('tf', ''), ('te', '*/'), "
                        "('lw', '//'), ('rw', ''), "
                        "('bb', '/*'), ('bf', ''), ('be', '*/')]"))
        self.com.swap_in(settings)
        should_width = 4
        self.assertEqual(self.com.width, should_width)

    def test_min_width_created_a_priori(self):
        """Verify that when creatd, width contains a minimum reasonable
        value."""
        newcom = objects.Commentator()
        should_width = 1
        self.assertEqual(newcom.width, should_width)
        del newcom

    def test_min_width_cleared_a_priori(self):
        """Verify that when all variables are cleared, width retains a minimum
        reasonable value."""
        self.com.clear_all()
        should_width = 1
        self.assertEqual(self.com.width, should_width)

    def test_min_width_return_to_explicit(self):
        """Verify that once a minimum width has been set, Commentator will 
        return to the last explicitly requested width if further changes make 
        it possible to do so."""
        settings = eval("[('tb', '/*'), ('tf', '='), ('te', '*/'), ('w', 3)]")
        self.com.swap_in(settings)
        self.com.set_value("te", "")
        should_width = 3
        self.assertEqual(self.com.width, should_width)

if __name__ == "__main__":
    unittest.main()
