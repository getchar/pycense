#! /usr/bin/python

import sys
import os
from textwrap import wrap
from itertools import izip
import argparse

from pprint import pprint

settings_abbrevs = {"tb": "top_begin", "tf": "top_fill", "te": "top_end",
                    "tl": "top_ljust", "lw": "left_wall", "rw": "right_wall",
                    "bb": "bottom_begin", "bf": "bottom_fill", 
                    "be": "bottom_end", "bl": "bottom_ljust", "w": "width",
                    "t": "tab", "sl": "skip_line", "bs": "buffer_size"}

class Commentator:
    """Class for generating boxed comments according to a specifications 
    string.

    top_begin, top_fill, top_end: describe the top of the boxed section;
      top_fill is repeated as many times as possible to fill the space
      between top_begin and top_end.  
    top_ljust: If the space cannot be filled evenly, by repetitions of 
      top_fill, top_ljust decides whether to cut off the beginning or the 
      end of the string it creates.
    left_wall, right_wall: vertical boundaries around comment region.
    bottom_begin, bottom_fill, bottom_end, bottom_fill: behave like
      their counterparts on top.
    width: the maximum width of a line (may be adjusted to suit other
      variables).
    tab: distance between tab stops.  Shouldn't be needed.
    magic_number: if present, comment must be inserted after this.  If
      absent, comment should be first thing in the file."""

    def __init__(self, settings = {}):
        """Initialize a commentator according to settings string."""
        self.width = 1 # hard lower limit
        self.swap_in(settings)

    def clear_all(self):
        """Clear all the values stored in all the data members.
        only really here for testing."""
        for field in vars(self):
            setattr(self, field, "")
        self.width = 1

    def swap_in(self, settings):
        """Applies settings to existing commentator, expands settings as 
        needed.

        settings: a list of alternating variables and values.  Variables
          are data members of the commentator class.
        delim: character that separates settings from values as well as 
          setting/value pairs in the settings string.  delim must not appear
          in either the name of a setting or the value presented."""
        for name in settings:
            self.set_value(name, settings[name])

    def set_value(self, name, value):
        """Set a single value; easier to read for humans; used for tests."""
        if name in settings_abbrevs:
            name = settings_abbrevs[name]
        if name not in settings_abbrevs.values():
            # might want to complain here
            return
        if name == "width":
            # may need to change width; may need to change back
            self.explicit_width = value
        setattr(self, name, value)
        self.validate()

    def sr(self, name, default = ""):
        """Safe reference; if the commentator contains a member by the
        given name, return the value in that member.  Else, return
        empty string.

        name: names data member being referenced.
        default: value to return if no data member by that name."""
        if hasattr(self, name):
            return getattr(self, name)
        else:
            return default

    def validate(self):
        """Verify that settings are meaningful in their present state.  What
        this comes down to is: can the line width requested by the user
        accomodate the lengths of the other elements?  Because we are liable
        to change the width programmatically and later changes might render
        a previously requested width adequate, check to see if we can revert
        to an earlier, explicitly requested value (explicit_width)."""
        top = len(self.sr("top_begin")) + len(self.sr("top_end"))
        mid = len(self.sr("left_wall")) + 1 + len(self.sr("right_wall"))
        # need at least one char width for text
        low = len(self.sr("bottom_begin")) + len(self.sr("bottom_end"))
        min_width = max(top, mid, low)
        # if current width is inadequate, increase it
        if self.width < min_width:
            self.width = min_width
        # if previously requested width becomes adequate, return to it
        explicit_width = self.sr("explicit_width", 0)
        if explicit_width >= min_width:
            # if width has been
            self.width = explicit_width

    def get_buffer(self):
        """Generate a buffer of blank lines to put before and after the
        comment."""
        if not hasattr(self, "buffer_size") or not self.buffer_size:
            return ""
        return "\n" * self.buffer_size

    def get_horizontal(self, side):
        """Generate a horizontal boundary string according to previously
        recorded settings.  Generates top or bottom depending on 
        the variable side.

        side: must be top or bottom; used to retreive variables"""
        if side not in ["top", "bottom"]:
            # raise error
            pass
        d = {}
        names = ["begin", "fill", "end", "ljust"]
        for name in names:
            d[name] = self.sr(side + "_" + name, "")
        if not d["fill"]:
            if d["end"]:
                # replace fill with space to position end
                d["fill"] = " "
            else:
                # shortcut
                return d["begin"]
        fill_space = self.width - (len(d["begin"]) + len(d["end"]))
        # if filler length not a multiple of fill space, we need overspill
        must_fill = fill_space + (len(d["fill"]) - 1)
        fill_times = must_fill / len(d["fill"])
        filler = d["fill"] * fill_times
        if len(filler) > fill_space:
            diff = len(filler) - fill_space
            if d["ljust"]:
                filler = filler[:len(filler) - diff]
            else:
                filler = filler[diff:]
        return "%s%s%s" % (d["begin"], filler, d["end"])

    def get_boxed(self, text):
        """Enclose text in a comment box according to the settings.

        text: any printable text that does not include tabs and paragraphs
        should be divided by bare newlines."""
        def cond_append(l, s):
            if s:
                l.append(s)
        text = text.rstrip("\n")
        comment_lines = []
        cond_append(comment_lines, self.get_horizontal("top"))
        tabwidth = self.sr("tab", 8)
        walls_width = len(self.sr("left_wall")) + len(self.sr("right_wall"))
        line_width = self.width - walls_width
        # futz with text a bit
        text = text.expandtabs(tabwidth)
        # break into paragraphs, force paragraphs to line_width,
        p_list = [wrap(p, line_width) for p in text.split("\n\n")]
        lines = []
        # blank lines to separate paragraphs; ignore extra blank line
        map(lambda s: lines.extend(s + [""]), p_list)
        for line in lines[:-1]:
            nspaces = self.width - (walls_width + len(line))
            cond_append(comment_lines, ("%s%s%s%s" % (self.sr("left_wall"), 
                                                      line,
                                                      " " * nspaces,
                                                      self.sr("right_wall"))))
        cond_append(comment_lines, self.get_horizontal("bottom"))
        return (self.get_buffer() + 
                "\n".join(comment_lines) + 
                self.get_buffer())

    def get_storage(self):
        """Generate dictionary to store current settings."""
        return vars(self)

class SetAction(argparse.Action):
    """Class to handle applying settings from the command line, simplifying
    the process of retreiving settings that have been explicitly set."""

    def __call__(self, parser, namespace, values, option_string):
        opt = option_string.lstrip("-")
        if opt in settings_abbrevs:
            opt = settings_abbrevs[opt]
        try:
            namespace.settings[opt] = values
        except AttributeError:
            setattr(namespace, "settings", {opt: values})
        setattr(namespace, "settings_loaded", True)

class LicenseTypeAction(argparse.Action):
    """Class of action for recording whether to use a named license or a 
    license drawn from a file identified by full or relative file path."""

    def __call__(self, parser, namespace, values, option_string):
        opt = option_string.lstrip("-")
        if hasattr(namespace, "license_loaded"):
            message = "You cannot load more than one license at a time."
            raise argparse.ArgumentError(None, message)
        else:
            setattr(namespace, "license_loaded", True)
            namespace.license = values

class ValueAdded(argparse.Action):
    """Class of action to add substitution scheme for current license."""

    def __call__(self, parser, namespace, values, option_string):
        if len(values) % 2:
            message = ("You must provide a filepath and a license name "
                       "for each license you wish to import.")
            raise argparse.ArgumentError(None, message)
        namespace.value.extend(zip(values[::2], values[1::2]))

class SeeSomeAction(argparse.Action):
    """Class of action for when see is called, to verify that any further 
    arguments are valid and to accumulate them."""

    def __call__(self, parser, namespace, values, option_string):
        unseeables = ", ".join([s for s in values if s not in parser.seeables])
        if unseeables:
            message = "%s not seeable" % unseeables
            raise argparse.ArgumentError(None, message)
        if "all" in values:
            values = parser.seeables[:]
        try:
            namespace.must_see.extend(values)
        except AttributeError:
            setattr(namespace, "must_see", values[:])
            
            
class ImportAction(argparse.Action):
    """Class of action to accumulate import requests."""

    def __call__(self, parser, namespace, values, option_string):
        if len(values) % 2:
            message = ("You must provide a filepath and a license name "
                       "for each license you wish to import.")
            raise argparse.ArgumentError(None, message)
        if not hasattr(namespace, "imports"):
            setattr(namespace, "imports", [])
        no_are = []
        for path, name in izip(values[::2], values[1::2]):
            if not os.path.exists(path):
                nohay.append(path)
            namespace.imports.append((path, name))
        if no_are:
            no_are = ", ".join(nohay)
            message = "%s not found" % (no_are)
            raise argparse.ArgumentError(None, message)

class DefaultAction(argparse.Action):
    """Class of action for accumulating default change requests."""

    def __call__(self, parser, namespace, values, option_string):
        table = {"l": "license", "c": "company", "o": "owner", "t": "tab",
                 "w": "width", "mn": "magic_number", "e": "editor",
                 "bs": "buffer_size"}
        opt = option_string
        opt = opt.split("--default_")[-1]
        opt = opt.split("-d")[-1]
        if opt in table:
            opt = table[opt]
        namespace.defaults.append((opt, values))

class RenameAction(argparse.Action):
    """Class of action for accumulating name change requests for
    profiles and licenses."""

    def __call__(self, parser, namespace, values, option_string):
        opt = option_string.lstrip("-")
        if opt == "rl":
            opt = "license"
        elif opt == "rp":
            opt = "profile"
        else:
            opt = opt.split("_")[1]
        if len(values) % 2:
            message = ("You must provide an old name and a new name "
                       "for ever %s you want to rename." % (opt))
            raise argparse.ArgumentError(None, message)
        accumulator = "rename_%s" % (opt)
        current = getattr(namespace, accumulator)
        for old, new in izip(values[::2], values[1::2]):
            current.append((old, new))
        setattr(namespace, accumulator, current)

            
