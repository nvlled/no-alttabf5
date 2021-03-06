version = "1.0.2"

import time
import re
import argparse
from os import path
from sys import argv, exit
from watchgod import watch
from xdo import Xdo
xdo = Xdo()

progname = path.basename(argv[0])
desc = "{} - Send keypress events when selected files are modified".format(progname)
argparser = argparse.ArgumentParser(description=desc)
argparser.add_argument("filenames",   type=str,   nargs="*", help="filenames to include")
argparser.add_argument("--filenames", type=str,   nargs="+", help="filenames to include")
argparser.add_argument("--filepat",   default="", type=str,  help="filename regex to include")
argparser.add_argument("--xfilepat",  default="", type=str,  help="filename regex to exclude")
argparser.add_argument("--delay",     default=0,  type=float,  help="number of seconds to delay refresh")
argparser.add_argument("--winpat",    default="", type=str,
        help="a window name regex, reload only when selected window has the matching regex")
argparser.add_argument("--version",   action="store_true", help="show version")
args = argparser.parse_args()

filepat   = args.filepat or None
xfilepat  = args.xfilepat or None
winpat    = args.winpat or None
filenames = [path.abspath(f) for f in args.filenames]
key = "F5"

def included(filename):
    if path.abspath(filename) in filenames:
        return True
    if filepat and re.search(filepat, filename):
        return True
    if xfilepat and not re.search(xfilepat, filename):
        return True
    return False

def getWindowName(winId):
    name = xdo.get_window_name(winId)
    if name:
        return name.decode("utf-8")
    return ""

if args.version:
    print("{} v{}".format(progname, version))
    exit()

if not (filenames or filepat or xfilepat):
    argparser.print_help()
    exit()

print("(!) select window to send keypress events ...")
targetWin = xdo.select_window_with_click()
if targetWin:
    winname = getWindowName(targetWin)
    print("selected window: {}".format(winname))

for changes in watch("."):
    winname = getWindowName(targetWin)
    if winpat and not re.match(winpat, winname):
        continue

    reload = any([included(e[1]) for e in changes])
    time.sleep(args.delay)
    if reload:
        curWin = xdo.get_active_window()
        xdo.focus_window(targetWin)
        xdo.send_keysequence_window(targetWin, key.encode("utf-8"))
        xdo.focus_window(curWin)
        print("sending {} to {}".format(key, targetWin))

