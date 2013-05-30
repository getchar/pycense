#! /usr/bin/python

import sys
from textwrap import wrap
from itertools import izip

from pprint import pprint

settings_abbrevs = {"tb": "top_begin", "tf": "top_fill", "te": "top_end",
                    "tl": "top_ljust", "lw": "left_wall", "rw": "right_wall",
                    "bb": "bottom_begin", "bf": "bottom_fill", 
                    "be": "bottom_end", "bl": "bottom_ljust", "w": "width"}

class commentator:
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
      their counterparts on top."""

    def __init__(self, settings = "", delim = "\n"):
        """Initialize a commentator according to settings string."""
        self.width = 1 # needs to be an int >= 1 no matter what
        self.swap_in(settings, delim)

    def clear_all(self):
        """Clear all the values stored in all the data members.
        only really here for testing."""
        for field in vars(self):
            setattr(self, field, "")
        self.width = 1

    def swap_in(self, settings, delim):
        """Applies settings to existing commentator, expands settings as 
        needed.

        settings: a list of alternating variables and values.  Variables
          are data members of the commentator class.
        delim: character that separates settings from values as well as 
          setting/value pairs in the settings string.  delim must not appear
          in either the name of a setting or the value presented."""
        interleaved = settings.split(delim)
        for name, value in izip(interleaved[::2], interleaved[1::2]):
            name = name.strip(" ")
            self.set_value(name, eval(value))

    def set_value(self, name, value):
        """Set a single value; easier to read for humans; used for tests."""
        if name in settings_abbrevs:
            name = settings_abbrevs[name]
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
            try:
                d[name] = getattr(self, side + "_" + name)
            except:
                d[name] = " "
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
        text = text.rstrip("\n")
        comment_lines = []
        comment_lines.append(self.get_horizontal("top"))
        tabwidth = self.sr("tab", 8)
        walls_width = len(self.sr("left_wall")) + len(self.sr("right_wall"))
        line_width = self.width - walls_width
        text = text.expandtabs(tabwidth)
        paragraphs = text.split("\n\n")
        # generate a list of lists of lines
        p_list = [wrap(p, line_width) for p in paragraphs]
        # put an list containing an empty string after every list of lines
        paragraphs = sum([[pl, [""]] for pl in p_list], [])[:-1]
        # flatten list into a list of strings separated by empty strings
        lines = [line for paragraph in paragraphs for line in paragraph]
        for line in lines:
            nspaces = self.width - (walls_width + len(line))
            comment_lines.append("%s%s%s%s" % (self.sr("left_wall"), 
                                               line,
                                               " " * nspaces,
                                               self.sr("right_wall")))
        comment_lines.append(self.get_horizontal("bottom"))
        return "\n".join(comment_lines)
