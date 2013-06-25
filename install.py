#! /usr/bin/python

import os
import shutil

old = "script"
new = os.path.expanduser("~") + os.sep + ".pycense"
shutil.copytree(old, new)
