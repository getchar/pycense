#! /usr/bin/python

import os
from objects import commentator
import argparse

parser = argparse.ArgumentParser(description = \
                                     ("A friendly and modifiable program for "
                                      "slipping copyright notices into your "
                                      "source code."))

settings = "tb, '#', tf, '#', lw, '# ', bb, '#', bf, '#', w, 50"
com = commentator(settings, ",")
text = open("mit_license.txt", "r").read()
print com.get_boxed(text)
