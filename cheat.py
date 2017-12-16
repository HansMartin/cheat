#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
from gui import GUI


# Default directory for the cheatsheets

## !Set this value to the path with your cheatsheets!
cs_directory = os.path.expanduser("cheatsheets")


if len(sys.argv) == 1 or len(sys.argv) > 2:
    print "Usage: cheat.py <cheatsheet name>\n\nOptions:\n\t-l, --list\tprints available cheatsheets"
    exit(1)

# get sheets
# TODO: order by theme and index the sheets
cs_name = sys.argv[1]
sheets = os.listdir(cs_directory)

# print all them
# TODO: change if too much sheets to print
if cs_name == "--list" or cs_name == "-l":
    for item in sheets:
        print "* " + item
    exit(1)


# Search the cheatsheets
for item in sheets:
    if cs_name in item.lower():
        fname = item
        break
else:
    fname = 0


if not fname:
    print "[-] Cheatsheet not found..."
    exit(1)

os.chdir(cs_directory)

# Gui stuff, found in gui.py
with GUI(fname) as gui:
    gui.genWindows()
    gui.fillContent()
    while 1:
        if gui.handleInput() == -1:
             break
