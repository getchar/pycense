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

"""Creates a copy of the script in ~/.pycense, if desired creates copy of 
wrapper script for pycense.py with name of user's choosing."""

import os
import shutil
import argparse

parser = argparse.ArgumentParser(description = "installer script for pycense")
parser.add_argument("--destination", "-d",
                    help = ("where to put script that calls pycense"))

args = parser.parse_args()
old = "script"
new = os.path.expanduser("~") + os.sep + ".pycense"
#shutil.copytree(old, new)
if args.destination:
    shutil.copy("pycense", args.destination)
