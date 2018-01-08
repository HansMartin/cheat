#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
from utils.gui import GUI
from utils.cheatsheet import CS




# Default directory for the cheatsheets
cs_directory = os.path.expanduser("~/.cheatsheets")


# user can set custom path in env. variable
if os.getenv("CHEATSHEET_PATH") != None:
    cs_directory = os.path.expanduser(os.getenv("CHEATSHEET_PATH"))


""" Prints the cheat.py usage message """
def usage():
        print "Usage: cheat.py <cheatsheet name>\n\nOptions:\n\t-l, --list\tprints available cheatsheets"

""" Parses the contents of the cheatsheet folder """


def walkFolders(cs_name, out=False):
    global cs_directory
    cheatsheet = None

    # Loop through all files in this directory
    for root, dirs, files in os.walk(cs_directory):
        for fl in files:
            if cs_name and cs_name in fl:
                # first cheatsheet found
                cheatsheet = CS(os.path.join(root, fl), fl, os.path.basename(root))
                break
            if out:
                print "- " + fl

    if cheatsheet:
        return cheatsheet
    return None




if __name__ == "__main__":
    if len(sys.argv) == 1:
        usage()
        exit(0)


    # TODO: order by theme and index the sheets
    cs_name = sys.argv[1]

    # Command line Arguments
    # TODO: change if too much sheets to print
    if cs_name == "--list" or cs_name == "-l":
        walkFolders(None, True)
        exit(0)

    # Try to get the cheatsheet
    cheatsheet = walkFolders(cs_name)

    if not cheatsheet:
        print "[-] Cheatsheet not found..."
        exit(1)


    # Gui stuff, found in gui.py
    with GUI(cheatsheet) as gui:
        gui.genWindows()
        gui.fillContent()
        while 1:
            if gui.handleInput() == -1:
                 break
