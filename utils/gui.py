# -*- coding: utf-8 -*-
import curses
import linecache
import re

# for the CS Class
from cheatsheet import CS
from parser import preparser


class GUI:

    status_base = "Cheatsheet %s (%s) line %d (Press q to quit)"

    # Keep track of line/col
    current_line = 1
    current_col = 1

    """ Setup Settings/Variables """
    def __init__(self, cheatsheet):

        # parsing CS()
        self.cs = cheatsheet

        # Use stdscr as global object
        self.stdscr = self.initCurses()

        # Get Console Height and Width
        self.maxy, self.maxx = self.stdscr.getmaxyx()

        self.num_lines = self.getLineNum()
        self.num_cols = self.getColNum()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Revert curse Settings
        curses.nocbreak()
        self.stdscr.keypad(0)
        curses.echo()
        curses.endwin()

    """ Initializes curses with the needed Settings"""
    def initCurses(self):
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(1)
        curses.start_color()
        stdscr.refresh()
        return stdscr

    """ Display Status Line """
    def updateStatus(self):
        if not self.status_win or not self.content_pad:
            raise NameError("Window and/or Pad not initialized")

        status_msg = self.status_base % (self.cs.cs_name, self.cs.topic, self.current_line)
        self.status_win.clear()
        self.status_win.addstr(0, 0, status_msg[:self.maxx-1], curses.color_pair(1))
        self.status_win.refresh()

    def getLineNum(self):
        return sum([1 for line in open(self.cs.full_path)])

    def getColNum(self):
        return max([len(line) for line in open(self.cs.full_path)])

    """ Generate the Status Windows and the Content Pad """
    def genWindows(self):
        # Color for the status windows
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

        status_height = 1
        status_width = self.maxx
        pad_height = self.num_lines
        pad_width = self.num_cols

        self.content_pad = curses.newpad(pad_height+2, max(pad_width, self.maxx))
        self.status_win = curses.newwin(status_height, self.maxx, self.maxy-1, 0)

        self.updateStatus()

    """ Get the content of the Cheatshet and put it in the Pad """
    def fillContent(self):

    	lnCount = 1
        for i in xrange(self.num_lines + 1):
        	pre = preparser()
        	line = pre.parse(linecache.getline(self.cs.full_path, i))
        	if line: 
        		self.parser(self.content_pad, lnCount, line)
        		lnCount += 1

    """ Fucked up color parser, 
        used for curses specific colors
    """
    def parser(self, pad, y, line):


        attr_mapping = {
                "fg":curses.COLOR_WHITE,
                "bg":curses.COLOR_BLACK,
                "at":curses.A_NORMAL
                }


        curses_mappings = {
                "black":curses.COLOR_BLACK,
                "blue":curses.COLOR_BLUE,
                "cyan":curses.COLOR_CYAN,
                "green":curses.COLOR_GREEN,
                "magenta":curses.COLOR_MAGENTA,
                "red":curses.COLOR_RED,
                "white":curses.COLOR_WHITE,
                "yellow":curses.COLOR_YELLOW,
                "normal":curses.A_NORMAL,
                "underline":curses.A_UNDERLINE,
                "bold":curses.A_BOLD
                }


        pat = "{(((?!}).)*)}(((?!{end}).)*){end}"
        attr_pat = "((fg|bg|at)=(red|yellow|cyan|green|white|black|magenta|blue|bold|normal|underline))"

        index = 0   # to keep track of the indizes
        cntReplaced = 0
        formatThere = False
        colCode = 0
        colInit = y + 3

        for i in re.finditer(pat, line):
            formatThere = True

            fmt = i.group(1)
            content = i.group(3)
            between = i.start()-(index+cntReplaced)

            tmp = line.replace(i.group(0), content)
            cntReplaced = len(line) - len(tmp)
            line = tmp

            for inner in re.finditer(attr_pat, fmt, re.I):
                key, value = inner.group(2), inner.group(3).lower()
                attr_mapping[key] = curses_mappings[value]          # Set the colors/attributes

            # 1) Print string until end
            pad.addstr(y, index+1, line[index:index+between+len(content)])

            curses.init_pair(colInit+colCode, attr_mapping["fg"], attr_mapping["bg"])              # add the colorscheme

            # 2) Print formatted string
            pad.addstr(y, index+between+1, content, curses.color_pair(colInit + colCode) | attr_mapping["at"])

            index += len(content) + between

            # Set to default values for next format
            attr_mapping["fg"] = curses.COLOR_WHITE
            attr_mapping["bg"] = curses.COLOR_BLACK
            attr_mapping["at"] = curses.A_NORMAL

            colCode += 1

        # append the last part
        pad.addstr(y, index+1, line[index::])
        pad.move(0, 0)


        # * Changing ---- to a hor. line
        if not formatThere:
            # Changing lines with ----- to a full line
            if sum([1 for x in line if x == "-"]) == len(line)-1 and len(line) > 5:
                pad.hline(y, 1, curses.ACS_HLINE, len(line))

            else:
                pad.addstr(y, 1, line)

        # Replace * and - with a diamond for bullet lists
        if line.startswith("* ") or line.startswith("- "):
                pad.addch(y, 1, curses.ACS_DIAMOND)



    """ Called when the Terminal resizes """
    def resize(self):
        self.maxy, self.maxx = self.stdscr.getmaxyx()
        self.status_win.mvwin(self.maxy - 1, 0)
        self.stdscr.clear()


    """ Gets user input """
    def handleInput(self):

        # update the Windows & Pad
        self.updateStatus()
        self.content_pad.refresh(self.current_line, self.current_col, 1, 1, self.maxy-2, self.maxx-2)


        c = self.stdscr.getch()
        if c == ord('q'):
            return  -1

        elif c == curses.KEY_RESIZE:
            self.resize()

        elif c == curses.KEY_DOWN or c == ord("j"):
            if self.current_line < self.num_lines:
                self.current_line += 1

        elif c == curses.KEY_UP or c == ord("k"):
            if self.current_line > 1: self.current_line -= 1

        elif c == curses.KEY_LEFT or c == ord("h"):
            if self.current_col > 1: self.current_col -= 1

        elif c == curses.KEY_RIGHT or c == ord("l"):
            if self.current_col < self.num_cols - 1:
                    self.current_col += 1

        elif c == ord("g"):
            self.current_line = 1

        elif c == ord("G"):
                self.current_line = self.num_lines - (self.maxy-3)
                if self.current_line <= 0:
                    self.current_line=1
        # Reset to (1/1)
        elif c == ord("0"):
            self.current_line = 1
            self.current_col = 1
