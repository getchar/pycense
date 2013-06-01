#! /usr/bin/python

import os
from objects import Commentator, SetAction
import argparse
import ConfigParser

from pprint import pprint

config_file = "config.conf"

cwd = os.path.dirname(os.path.abspath(__file__)) + os.sep

config = ConfigParser.ConfigParser()
config.read(config_file)

d_license = config.get("defaults", "license")
d_company = config.get("defaults", "company")
d_copyright_holders = eval(config.get("defaults", "copyright_holders"))

parser = argparse.ArgumentParser(description = \
                                     ("A friendly and modifiable program for "
                                      "slipping copyright notices into your "
                                      "source code."))

# named entities
parser.add_argument("--profile", "-p", type = str,
                    help = "the comment style profile to load")
parser.add_argument("--license", "-l", type = str,
                    default = d_license, 
                    help = ("license to load; default is %s"
                            % d_license))
parser.add_argument("--license_file", "-lf", type = str,
                    help = ("license to load that hasn't previously been "
                            "imported"))
# settings
parser.add_argument("--tab", "-t", type = int,
                    help = ("tab width of document (there shoulldn't be any "
                            "tabs in your license"))
parser.add_argument("--width", "-w", type = int,
                    help = ("maximum line width in source code"))
parser.add_argument("--top_begin", "-tb", type = str,
                    help = ("start of string marking the uppoer boundary of "
                            "commented license"))
parser.add_argument("--top_fill", "-tf", type = str,
                    help = ("string to repeat along the upper boundary of "
                            "commented license"))
parser.add_argument("--top_ljust", "-tl", type = str,
                    help = ("whether to left justify the fill along the "
                            "upper boundary of the commented license; "
                            "use True or False"))
parser.add_argument("--top_end", "-te", type = str,
                    help = ("end of string marking the uppoer boundary of "
                            "commented license"))
parser.add_argument("--bottom_begin", "-bb", type = str,
                    help = ("start of string marking the lower boundary of "
                            "commented license"))
parser.add_argument("--bottom_fill", "-bf", type = str,
                    help = ("string to repeat along the lower boundary of "
                            "commented license"))
parser.add_argument("--bottom_ljust", "-bl", type = str,
                    help = ("whether to left justify the fill along the "
                            "lower boundary of the commented license; "
                            "use True or False"))
parser.add_argument("--bottom_end", "-be", type = str,
                    help = ("end of string marking the lower boundary of "
                            "commented license"))
# storing named entities
parser.add_argument("--store_in_place", "-sip", action = 'store_true', 
                    default = False,
                    help = ("overwrite the named comment profile currently "
                            "loaded with the substitutions currently made"))
parser.add_argument("--store_as", "-sa", type = str, metavar = "NAME",
                    help = ("name to store currently loaded comment "
                            "profile under"))
parser.add_argument("--rename_profile", "-rp", type = str, nargs = 2,
                    megavar = ("OLD", "NEW"),
                    help = ("rename a named profile"))
parser.add_argument("--import", "-i", type = str, nargs = 2,
                    metavar = ("FILE", "LICENSE_NAME"),
                    help = ("import a file into the license library"))
parser.add_argument("--rename_license", "-rl", type = str, nargs = 2,
                    megavar = ("OLD", "NEW"),
                    help = ("rename a named license"))

args = parser.parse_args()
pprint(vars(args))

# can't store_as and store_in_place ... or can you?
