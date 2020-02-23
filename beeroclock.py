#! /usr/bin/env python3
from datetime import datetime as dtime
from datetime import timedelta as timed
import datetime
import time
import signal
import sys
import tkinter
from PIL import ImageTk, Image
import argparse as ap
from pathlib import Path
import subprocess

pwd = Path().absolute()

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
delta_days = 0

################################################################################
def calc_beertime(beerday, beeroclock):
    now = dtime.now()
    now_ts = now.timestamp()
    current_weekday = now.weekday()
    now_t = now.time()

    delta_days = (beerday-current_weekday)%7

    beerdate = now.date() + timed(days=delta_days)
    beerdatetime = dtime.combine(beerdate,
            beeroclock)

    if beerdatetime <= now <= beerdatetime + timed(hours=4):
        return 0
    elif now > beerdatetime + timed(hours=4):
        beerdatetime = beerdatetime + timed(days=7)
    diff_dtime = beerdatetime - now

    return diff_dtime

################################################################################
renderFontPrompt = ("Hack", 120)
renderFontLabel = ("Hack", 90)
renderFontBeertime = ("Hack", 110)

show_bt = True
play_sound = True
def set_t(beerday, beeroclock):
    global label
    global show_bt
    global beermugLabel
    global play_sound
    dt = calc_beertime(beerday, beeroclock)

    if dt != 0: 
        label.config(fg="black", text=str(dt), font=renderFontLabel)
        label.after(33, set_t, beerday, beeroclock)
        play_sound = True
    else:

        if play_sound == True:
            dixiefile = pwd / "dixie-horn_daniel-simion.wav"
            play_sound = False
            subprocess.Popen(['aplay', str(dixiefile)])
        label.config(fg="yellow", text="BEERTIME", font=renderFontBeertime)
        if show_bt == True:
            label.place(relx=.5, rely=.5, anchor="center")
            beermugLabel.place(relx=0.5, rely=0.75, anchor="center")
        else:
            beermugLabel.place_forget()
            label.place_forget()

        show_bt = not show_bt
        label.after(1000, set_t, beerday, beeroclock)
            
################################################################################
## Top Window
top = tkinter.Tk();
top.config(cursor="none")
top.attributes("-fullscreen", True)

## Beermug Label to be displayed
beermugImage = ImageTk.PhotoImage(Image.open('beermug.png').resize((200,200), Image.ANTIALIAS))
beermugLabel = tkinter.Label(top, image = beermugImage)
beermugLabel.place(relx=0.5, rely=0.75, anchor="center")
beermugLabel.place_forget()

## Beeroclock prompt
prompt = tkinter.Label(top, text="Beeroclock!")
prompt.configure(anchor="center")
prompt.config(font=renderFontPrompt) 
prompt.place(relx=.5, rely=.25, anchor="center")

## Countdown
label = tkinter.Label(top, text="", borderwidth=0)
label.configure(anchor="center")
label.config(font=renderFontLabel)
label.place(relx=.5, rely=.5, anchor="center")

def beertime_tkinter(beerday, beeroclock):
    global top
    global label
    top.mainloop()


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
    parser.add_argument("beerday", nargs="?", help="Your beerday case-insensitive [default: friday]",
            default="friday")
    parser.add_argument("beertime", nargs="?", help="The start of your beertime in hh:mm [default: 16:00]",
            default="16:00")

    args = parser.parse_args()

    beeroclock = parse_user_beertime(args.beertime)
    beerday = parse_user_beerday(args.beerday)
    label.after(33, set_t, beerday, beeroclock)

    beertime_tkinter(beerday, beeroclock)

