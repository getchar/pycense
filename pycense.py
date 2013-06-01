#! /usr/bin/python

import os
from objects import commentator
import argparse

cwd = os.path.dirname(os.path.abspath(__file__))
print cwd

parser = argparse.ArgumentParser(description = \
                                     ("A friendly and modifiable program for "
                                      "slipping copyright notices into your "
                                      "source code."))

settings = "{'tb': '#', 'tf': '#', 'lw': '# ', 'bb': '#', 'bf': '#', 'w': 50}"
com = commentator()
com.swap_in(settings)
text = open("licenses/lorem.txt", "r").read()
print com.get_boxed(text)
