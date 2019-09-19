#! /usr/bin/env python3
from datetime import datetime as dtime
from datetime import timedelta as timed
import datetime
import time
import signal
import sys
import argparse as ap

## Title
title = [
   " ______   _______  _______  _______  _  _______    _______  _        _______  _______  _       ",
   "(  ___ \\ (  ____ \\(  ____ \\(  ____ )( )(  ___  )  (  ____ \\( \\      (  ___  )(  ____ \\| \    /\\",
   "| (__/ / | (__    | (__    | (____)|   | |   | |  | |      | |      | |   | || |      |  (_/ / ",
   "|  __ (  |  __)   |  __)   |     __)   | |   | |  | |      | |      | |   | || |      |   _ (  ",
   "| (  \\ \\ | (      | (      | (\\ (      | |   | |  | |      | |      | |   | || |      |  ( \\ \\ ",
   "| )___) )| (____/\\| (____/\\| ) \\ \\__   | (___) |  | (____/\\| (____/\\| (___) || (____/\\|  /  \\ \\",
   "|/ \\___/ (_______/(_______/|/   \\__/   (_______)  (_______/(_______/(_______)(_______/|_/    \\/"]


## DIGIT ASCII ART LISTS
one = ['   ', "/| ", " | "]
two = ["__ ", " _)", "/__"]
three = ["__", "__)","__)"]
four = ['   ', "|_|", "  |"]
five = [" __", "|_ ", "__)"]
six = [" _ ", "|_ ", "|_)"]
seven = [" __", "  /", " / "]
eight = [" _ ", "(_)", "(_)"]
nine = [" _ ", "(_|", " _|"]
zero = [" _ ", "/_\\", "\\_/"]
delimi = ["   ", " o ", " o "]
digits = [zero, one, two, three, four, five, six, seven, eight, nine]

beertime_fancy = """
888888b.   8888888888 8888888888 8888888b. 88888888888 8888888 888b     d888 8888888888
888  \"88b  888        888        888   Y88b    888       888   8888b   d8888 888
888  .88P  888        888        888    888    888       888   88888b.d88888 888
8888888K.  8888888    8888888    888   d88P    888       888   888Y88888P888 8888888
888  \"Y88b 888        888        8888888P\"     888       888   888 Y888P 888 888
888    888 888        888        888 T88b      888       888   888  Y8P  888 888
888   d88P 888        888        888  T88b     888       888   888   \"   888 888
8888888P\"  8888888888 8888888888 888   T88b    888     8888888 888       888 8888888888"""
beertime_plain = "BEERTIME!"

beerdays = {
    "monday" : 0,
    "tuesday" : 1,
    "wednesday" : 2,
    "thursday" : 3,
    "friday" : 4,
    "saturday" : 5,
    "sunday" : 6
}

## Other global variables
show_beertime = True
cursor_up = "\033[A"
delta_days = 0

################################################################################
## Signal Handler for SIGINT
def sigint_handler(sig, frame):
    ## Restore cursor
    print(cursor_up, end="")
    print("\033[?25h")
    sys.exit(0)

################################################################################
def print_time_fancy(days, hours, mins, secs):

    ## Hours
    hour_b = int(hours/10)
    hour_s = (hours%10)

    ## mins
    mins_b = int(mins/10)
    mins_s = (mins%10)

    ## seconds
    secs_b = int(secs/10)
    secs_s = (secs%10)

    for i in range(3):
        print("{:4}{:4}{:4}{:4}{:4}{:4}{:4}{:4}{:4}{:4}".format(
            digits[days][i], delimi[i],
            digits[hour_b][i], digits[hour_s][i], delimi[i],
            digits[mins_b][i], digits[mins_s][i], delimi[i],
            digits[secs_b][i], digits[secs_s][i]))
    print(cursor_up * 4)

################################################################################
def print_time_plain(days, hours, mins, sec):
    print("{}d:{:02d}H:{:02d}M:{:02d}sec".format(days, hours, mins, sec), end="\r")

################################################################################
def print_beertime_fancy():

    global show_beertime
    print(cursor_up, end="")
    print(""*99, end="")
    if show_beertime == True:
        print(beertime_fancy)
    else:
        for i in range(9):
            print(" " * 87)

    print(cursor_up * 9)
    show_beertime = not show_beertime

################################################################################
def print_beertime_plain():
    global show_beertime
    if show_beertime == True:
        print(beertime_plain, end = '\r')
    else:
        print(" " * 16, end = '\r')
    show_beertime = not show_beertime

################################################################################
def parse_user_beertime(ubeer_time):

    beerhour = ubeer_time[:-3]
    beerminute = ubeer_time[-2:]

    try:
        beertime = datetime.time(int(beerhour), int(beerminute), 0, 0)
        return beertime
    except:
        print("Oops, you must provide the beertime in the \"hh:mm\" format"
                " e.g. 16:00 for four o clock")
        print("\033[?25h")
        sys.exit(0)

################################################################################
def parse_user_beerday(ubeer_day):

    try:
        ubeer_day = ubeer_day.lower();
        return beerdays[ubeer_day]
    except:
        print("Oops, looks like you got your beerday wrong. Did you misspell it?"
                "\nValid options are (case insensitive):\n"
                "monday, tuesday, wednesday, thursday, friday, saturday, sunday")
        print("\033[?25h")
        sys.exit(0)

###############################################################################
if __name__ == "__main__":

    parser = ap.ArgumentParser(description="Print Time till the next BEER EVENT!!")
    parser.add_argument("--fancy", help="Print countdown in fancy ASCII art",
            action="store_true")
    parser.add_argument("beerday", nargs="?", help="Your beerday case-insensitive [default: friday]",
            default="friday")
    parser.add_argument("beertime", nargs="?", help="The start of your beertime in hh:mm [default: 16:00]",
            default="16:00")


    ## Print title
    for i in range(len(title)):
        print(title[i])
    print("\n")

    args = parser.parse_args()

    if args.fancy == True:
        print_time = print_time_fancy
        print_beertime = print_beertime_fancy
    else:
        print_time = print_time_plain
        print_beertime = print_beertime_plain

    beeroclock = parse_user_beertime(args.beertime)
    beerday = parse_user_beerday(args.beerday)

    ## Hide cursor
    print("\033[?25l", end="")
    ## Register signal handler
    signal.signal(signal.SIGINT, sigint_handler)

    ## Main Loop
    while True:

        now = dtime.now()
        now_ts = now.timestamp()
        current_weekday = now.weekday()
        now_t = now.time()

        delta_days = (beerday-current_weekday)%7

        beerdate = now.date() + timed(days=delta_days)
        beerdatetime = dtime.combine(beerdate,
                beeroclock)

        if beerdatetime <= now <= beerdatetime + timed(hours=4):
            print_beertime()
            time.sleep(1)
            continue
        elif now > beerdatetime + timed(hours=4):
            beerdatetime = beerdatetime + timed(days=7)

        diff_dtime = beerdatetime - now
        diffhour = diff_dtime.seconds/3600
        diffminute = (diff_dtime.seconds % 3600)/60
        diffsec = (diff_dtime.seconds % 60)

        print_time(diff_dtime.days, int(diffhour), int(diffminute), diffsec)

        sleep_duration = 0.25 - (dtime.now().timestamp() - now_ts)
        if sleep_duration > 0:
            time.sleep(sleep_duration)

