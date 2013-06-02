#! /usr/bin/python

import os
import objects as obj
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
d_settings = {"tab": config.getint("defaults", "tab"),
              "width": config.getint("defaults", "width"),
              "magic_number": config.get("defaults", "magic_number")}

parser = argparse.ArgumentParser(description = \
                                     ("A friendly and modifiable program for "
                                      "slipping copyright notices into your "
                                      "source code."))

setattr(parser, "d_settings", d_settings)
# loading named entities
parser.add_argument("--profile", "-p", type = str,
                    help = "the comment style profile to load")
parser.add_argument("--license", "-l", type = str, action = obj.LicenseTypeAction,
                    default = d_license, 
                    help = ("license to load; default is %s"
                            % d_license))
parser.add_argument("--license_file", "-lf", type = str, 
                    action = obj.LicenseTypeAction,
                    help = ("license to load that hasn't previously been "
                            "imported"))

# settings
parser.add_argument("--tab", "-t", type = int, action = obj.SetAction,
                    default = d_settings["tab"],
                    help = ("tab width of document (there shoulldn't be any "
                            "tabs in your license"))
parser.add_argument("--width", "-w", type = int, action = obj.SetAction,
                    default = d_settings["width"],
                    help = ("maximum line width in source code"))
parser.add_argument("--top_begin", "-tb", type = str, action = obj.SetAction,
                    help = ("start of string marking the uppoer boundary of "
                            "commented license"))
parser.add_argument("--top_fill", "-tf", type = str, action = obj.SetAction,
                    help = ("string to repeat along the upper boundary of "
                            "commented license"))
parser.add_argument("--top_ljust", "-tl", type = str, action = obj.SetAction,
                    help = ("whether to left justify the fill along the "
                            "upper boundary of the commented license; "
                            "use True or False"))
parser.add_argument("--top_end", "-te", type = str, action = obj.SetAction,
                    help = ("end of string marking the uppoer boundary of "
                            "commented license"))
parser.add_argument("--left_wall", "-lw", type = str, action = obj.SetAction,
                    help = ("left wall of commented license; surrounds "
                            "text of licesne; include any spaces desired as "
                            "buffer"))
parser.add_argument("--right_wall", "-rw", type = str, action = obj.SetAction,
                    help = ("right wall of commented license; surrounds "
                            "text of licesne; include any spaces desired as "
                            "buffer"))
parser.add_argument("--bottom_begin", "-bb", type = str, action = obj.SetAction,
                    help = ("start of string marking the lower boundary of "
                            "commented license"))
parser.add_argument("--bottom_fill", "-bf", type = str, action = obj.SetAction,
                    help = ("string to repeat along the lower boundary of "
                            "commented license"))
parser.add_argument("--bottom_ljust", "-bl", type = str, action = obj.SetAction,
                    help = ("whether to left justify the fill along the "
                            "lower boundary of the commented license; "
                            "use True or False"))
parser.add_argument("--bottom_end", "-be", type = str, action = obj.SetAction,
                    help = ("end of string marking the lower boundary of "
                            "commented license"))
parser.add_argument("--magic_number", "-mn", type = str, action = obj.SetAction,
                    nargs = "+",
                    help = ("python ready regular expression (including a list of "
                            "optional flags) describing any text that has to "
                            "be skipped before inserting the commented "
                            "license"))
# storing named entities
parser.add_argument("--store_in_place", "-sip", action = 'store_true', 
                    default = False,
                    help = ("overwrite the named comment profile currently "
                            "loaded with the substitutions currently made"))
parser.add_argument("--store_as", "-sa", type = str, metavar = "NAME",
                    help = ("name to store currently loaded comment "
                            "profile under"))
parser.add_argument("--rename_profile", "-rp", type = str, nargs = 2,
                    metavar = ("OLD", "NEW"),
                    help = ("rename a named profile"))
parser.add_argument("--import", "-i", type = str, nargs = 2,
                    metavar = ("FILE", "LICENSE_NAME"),
                    help = ("import a file into the license library"))
parser.add_argument("--rename_license", "-rl", type = str, nargs = 2,
                    metavar = ("OLD", "NEW"),
                    help = ("rename a named license"))

# setting defaults
parser.add_argument("--default_license", "-dl", type = str, nargs = '?',
                    metavar = "LICENSE",
                    help = ("set previously imported license as default"))
parser.add_argument("--default_company", "-dc", type = str,
                    metavar = "COMPANY",
                    help = ("set default company"))
parser.add_argument("--default_copyright_holders", "-dch", type = str,
                    nargs = "+", metavar = "COPYRIGHT_HOLDER",
                    help = ("set list of default copyright holders"))
parser.add_argument("--default_tab", "-dt", type = int,
                    help = ("default tab width to use in all source code"))
parser.add_argument("--default_width", "-dw", type = int,
                    help = ("default line width to use in all source code"))
parser.add_argument("--default_magic_number", "-dmn", type = str, 
                    nargs = "+",
                    help = ("set default magic number; added for completeness; "
                            "you probably shouldn't use it"))
parser.add_argument("--add_suffix", "-as", type = str, nargs = "+",
                    metavar = "SUFFIX",
                    help = ("add to the list of suffixes that take "
                            "the currently loaded profile by default"))
parser.add_argument("--del_suffix", "-ds", type = str, nargs = "+",
                    metavar = "SUFFIX",
                    help = ("delete items from the list of suffixes that take "
                            "the currently loaded profile by default"))

# set one time substitutions
parser.add_argument("--year", "-y", type = str,
                    help = ("replace <year> with this"))
parser.add_argument("--company", "-c", type = str,
                    help = ("replace <company> with this"))
parser.add_argument("--copyright_holders", "-ch", type = str,
                    help = ("replace <copyright holders> with this"))
parser.add_argument("--value", "-v", type = str, nargs = 2,
                    action = obj.ValueAdded, metavar = ("OLD", "NEW"),
                    help = ("replace <OLD> with NEW"))

# produce commented licenses and either write to file or view
parser.add_argument("--apply_to", "-a", type = str, nargs = "+",
                    metavar = "SOURCE",
                    help = ("a list of source files to apply the current "
                            "settings to"))




args = parser.parse_args()

try:
    settings = str(args.settings)
except AttributeError:
    settings = str(d_settings)
# create Commentator, either from explicit settings or defauls
com = obj.Commentator(settings)
print com.magic_number
pprint(vars(args))
text = open("licenses/mit_license.txt", "r").read()


# conflicts: (license, license_file)! (store_as, store_in_place)?
