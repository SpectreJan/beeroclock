#! /bin/env python3
from datetime import datetime as dtime
from datetime import timedelta as timed
import time
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

## Other global variables
show_beertime = True
cursor_up = "\033[A"
beerday = 4
beeroclock = 16
delta_days = 0

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
    if show_beertime == True:
        print(beertime_fancy)
    else:
        for i in range(9):
            print(" " * 87)
        
    print(cursor_up * 10)
    show_beertime = not show_beertime

################################################################################
def print_beertime_plain():
    global show_beertime
    if show_beertime == True:
        print(beertime_plain, end = '\r')
    else:
        print(" " * 16, end = '\r')
    show_beertime = not show_beertime


###############################################################################
if __name__ == "__main__":

    parser = ap.ArgumentParser(description="Print Time till the next BEER EVENT!!")
    parser.add_argument("--fancy", help="Print countdown in fancy ASCII art",
            action="store_true")

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

    ## Main Loop
    while True:
        now = dtime.now()
        now_ts = now.timestamp()
        current_weekday = now.weekday()
        now_t = now.time()
        if((beerday == current_weekday) and (now_t.hour >= beeroclock)):
            if(now_t.hour<(beeroclock+4)):
                print_beertime()
                time.sleep(1)
                continue;
            else:
                delta_days = 7
        else:
            delta_days = (beerday-current_weekday)%7
        
        beerdate = now.date() + timed(days=delta_days)
        beerdatetime = dtime(beerdate.year, beerdate.month, beerdate.day,
                beeroclock, 0,0,0)
        diff_dtime = beerdatetime - now

        diffhour = diff_dtime.seconds/3600
        diffminute = (diff_dtime.seconds % 3600)/60
        diffsec = (diff_dtime.seconds % 60)

        print_time(diff_dtime.days, int(diffhour), int(diffminute), diffsec)
        time.sleep(0.25 - (dtime.now().timestamp() - now_ts))

