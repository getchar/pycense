#! /usr/bin/python

import os
import objects as obj
import argparse
import ConfigParser
import os
import shutil
from pprint import pformat

def name_to_path(name):
    """Creates a path to a license out of its name."""
    cwd = os.path.dirname(os.path.abspath(__file__)) + os.sep
    return cwd + "licenses" + os.sep + name + ".txt"

config_file = "config.conf"

config = ConfigParser.ConfigParser()
config.read(config_file)

sample_text = "Software license information goes here."

d_license = config.get("defaults", "license")
d_company = config.get("defaults", "company")
d_copyright_holders = eval(config.get("defaults", "copyright_holders"))
d_settings = {"tab": config.getint("defaults", "tab"),
              "width": config.getint("defaults", "width"),
              "magic_number": config.get("defaults", "magic_number")}
seeables = ["all", "defaults", "profiles", "sample"]

parser = argparse.ArgumentParser(description = \
                                     ("A friendly and modifiable program for "
                                      "slipping copyright notices into your "
                                      "source code."))
setattr(parser, "d_settings", d_settings)
setattr(parser, "seeables", seeables)

# loading named entities
parser.add_argument("--profile", "-p", type = str,
                    help = "the comment style profile to load")
parser.add_argument("--license", "-l", type = str, 
                    action = obj.LicenseTypeAction, dest = "license",
                    help = ("license to load; default is %s"
                            % d_license))

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
parser.add_argument("--bottom_begin", "-bb", type = str, 
                    action = obj.SetAction,
                    help = ("start of string marking the lower boundary of "
                            "commented license"))
parser.add_argument("--bottom_fill", "-bf", type = str, action = obj.SetAction,
                    help = ("string to repeat along the lower boundary of "
                            "commented license"))
parser.add_argument("--bottom_ljust", "-bl", type = str, 
                    action = obj.SetAction,
                    help = ("whether to left justify the fill along the "
                            "lower boundary of the commented license; "
                            "use True or False"))
parser.add_argument("--bottom_end", "-be", type = str, action = obj.SetAction,
                    help = ("end of string marking the lower boundary of "
                            "commented license"))
parser.add_argument("--magic_number", "-mn", type = str, 
                    action = obj.SetAction, nargs = "+",
                    help = ("python ready regular expression (including a "
                            "list of optional flags) describing any text "
                            "that has to be skipped before inserting the "
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
                    metavar = ("OLD", "NEW"),
                    help = ("rename a named profile"))
parser.add_argument("--import_license", "-il", type = str, nargs = "+",
                    action = obj.ImportAction,
                    metavar = ("FILE", "LICENSE_NAME"), 
                    help = ("import a file into the license library"))
parser.add_argument("--rename_license", "-rl", type = str, nargs = 2,
                    metavar = ("OLD", "NEW"),
                    help = ("rename a named license"))
parser.add_argument("--remove_license", "-rml", type = str, nargs = "+",
                    metavar = "LICENSE", default = [],
                    help = "remove these licenses from the library")
parser.add_argument("--remove_profile", "-dp", type = str, nargs = "+",
                    metavar = "PROFILE", default = [],
                    help = "remove these profiles from the library")

# setting defaults
parser.add_argument("--default_license", "-dl", type = str,
                    metavar = "LICENSE", action = obj.DefaultAction,
                    help = ("set a previously imported license as default"))
parser.add_argument("--default_company", "-dc", type = str,
                    metavar = "COMPANY", action = obj.DefaultAction,
                    help = ("set default company"))
parser.add_argument("--default_owner", "-do", type = str,
                    metavar = "OWNER", action = obj.DefaultAction,
                    help = ("set list of default copyright holders"))
parser.add_argument("--default_tab", "-dt", type = int,
                    action = obj.DefaultAction,
                    help = ("default tab width to use in all source code"))
parser.add_argument("--default_width", "-dw", type = int,
                    action = obj.DefaultAction,
                    help = ("default line width to use in all source code"))
parser.add_argument("--default_magic_number", "-dmn", type = str, 
                    action = obj.DefaultAction, nargs = "+",
                    help = ("set default magic number; added for "
                            "completeness; you probably shouldn't use it"))

# set one time substitutions
parser.add_argument("--year", "-y", type = str,
                    help = ("replace <year> with this once"))
parser.add_argument("--company", "-c", type = str,
                    help = ("replace <company> with this once"))
parser.add_argument("--owner", "-o", type = str,
                    help = ("replace <owner> with this once"))
parser.add_argument("--value", "-v", type = str, nargs = 2,
                    action = obj.ValueAdded, metavar = ("OLD", "NEW"),
                    help = ("replace <OLD> with NEW once"))

# produce commented licenses and either write to file or view
parser.add_argument("--apply_to", "-a", type = str, nargs = "+",
                    metavar = "SOURCE",
                    help = ("a list of source files to apply the current "
                            "settings to"))
parser.add_argument("--see", "-s", type = str, action = obj.SeeSomeAction,
                    nargs = "+", metavar = "SEEABLE",
                    help = ("see some information; options include defaults, "
                            "profiles, and sample, which means that the "
                            "currently selected license will be printed to the"
                            "screen using the currently selected comment"
                            "profile"))
args = parser.parse_args()
# remove stuff
for toremove in args.remove_license:
    try:
        os.remove(name_to_path(toremove))
    except OSError as err:
        # fail silently unless --silent, --verbose  support added
        pass
if args.remove_profile:
    for toremove in args.remove_profile:
        try:
            assert config.remove_option("profiles", toremove) == True
        except AssertionError:
            # fail silently unless --silent, --verbose  support added
            pass

# import stuff
if hasattr(args, "imports"):
    for filepath, newname in args.imports:
        shutil.copy(filepath, name_to_path(newname))
        
# adjust defaults
if hasattr(args, "defaults"):
    for default in args.defaults:
        config.set("defaults", default, args.defaults[default])

# load license
if not args.license and (args.apply_to or "sample" in args.must_see): 
    args.license = d_license
if args.license:
    license_file = name_to_path(args.license)
    try:
        license_text = open(license_file, "r").read().rstrip("\n")
    except:
        print "No license named '%s' found" % (args.license)

# create Commentator
try:
    settings = str(args.settings)
except AttributeError:
    settings = str(d_settings)
    if hasattr(args, "settings"):
        for setting in args.settings:
            # insert all the settings from the command line
            settings[setting] = args.settings[settings]
com = obj.Commentator(settings)

# see what must be seen
if "defaults" in args.must_see:
    for var, val in config.items("defaults"):
        print "default %s: %s" % (var, val)
if "profiles" in args.must_see:
    for var, val in config.items("profiles"):
        print "profile %s" % (var)
        # get rid of braces
        dicstr = pformat(eval(val)).replace("{", " ")[:-1]
        for line in dicstr.split("\n"):
            # get rid of single quotes around the data member names
            line = line.replace("'", "")
            line = line.replace("'", "")
            print "\t%s" % (line)
if "sample" in args.must_see:
    print com.get_boxed(license_text)

with open(config_file, "wb") as fp:
    config.write(fp)

