`pycense` by Charlie Pashayan

This program allows the user to insert license and copyright information into source code.  The user can store various named licenses in a central directory, and a huge variety of (user modifiable) named commenting conventions.  File name suffixes can be associated with a given commenting convention to automate the process of selecting comment styles and parts of commenting conventions can be changed either during one instance of `pycense` or permanently in the configuration of the program.

Commenting Conventions:

Comment boxes consist of 8 parts: top_begin, top_fill, top_end, left_wall, right_wall, bottom_begin, bottom_fill, bottom_end.  On the top and bottom, you are the begin and end portions are guaranteed to be shown and any additional space will be filled in with repetitions of the fill portion.  If the fill portion is not an even multiple of the space to be filled, it will be repeated a sufficient number of times and then either the beginning or the end will be trimmed off according to the relevant left justification variable (top_ljust or bottom_ljust).  The width can also be adjusted, within certain common sense constraints that I'll describe below.

Here's an example comment box along with the variables used to create it:

/*BCABCABC
// text %%
// goes %%
// here %%
ABCABCAB*/

top_begin: "/*"
top_fill: "ABC"
top_end: ""
top_ljust: False
left_wall: "// " (buffer space is part of the wall)
right_wall: " %%"
bottom_begin: ""
bottom_fill: "ABC"
bottom_end: "*/"
bottom_ljust: True
width: 9

On `width`:

Because comment boxes are designed to accomodate text, the text portion of the comment box must be at least one character wide.  Furthermore, the maximum line width must be long enough to include all of the guaranteed printable portions of the comment box (that is: top_begin and top_end, bottom_begin and bottom_end, and left_wall, right_wall and one character of text).  If the width explicitly requested by the user is smaller than the minimum width required by the rest of the settings, the printed width will be automatically reset to the required minimum width.  If any other settings are changed to make the explicitly requested width possible, the actual width will be reset to that value.

If there are any words that can't fit within the width of a line, they will be broken off so that they fill as much space as possible.  No hyphens will be inserted.  So you'd be better off leaving ample space for longer words.