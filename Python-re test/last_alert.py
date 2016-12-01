# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys
import re

from datetime import datetime, timedelta

"""
@autor Jose Arcos Aneas
@date 19 Mar 2016


Use:
    chmod +x  last_alert.py
    python last_alert
        (or)
    python last_alert -n (int)


        YYYY MMM DD HH:MM:SS
    '((19|20)\d\d)+\s+(Jan|Feb|Mar|Apr|May|Jun|Jul)+\s+(\d+)\s([0-2][0-9].[0-5][0-9].[0-5][0-9])'

example: 2016 Feb 17 20:14:41

The file to be read is stored in:
alerts.log (o .json)

"""


def main(logs):
    """
    main function.
    If the number of arguments is 1: shows the last timeslap
    If the number of arguments is 3: shows true if there was
    a timeslap in the last n days, where n is the value 3 argument.
    """
    if(len(sys.argv) == 1):
        simpleUse(logs)
    elif(len(sys.argv) == 3):
        extendUse(logs)
    else:
        print "Use: ./last_alert.py  or ./last_alert.py -n intiger"


def simpleUse(text):
    """
        Simple use of the program:
      When the number of arguments is one.
        We write the regular expression and
        look for matches in the text.
        We show the last match.
    """
    # Regular expresion
    fa = '((19|20)\d\d)+\s+(Jan|Feb|Mar|Apr|May|Jun|Jul)+\s+(\d+)\s([0-6][0-9].[0-6][0-9].[0-6][0-9])'
    f = re.findall(fa, text)
#    print type(f) # type list
    last_alert = f[-1]
#    print type(last_alert)    # type tuple
    year = (last_alert[0])
    m = (last_alert[2])
    mes = (strings_to_numbers(m))
    day = int(last_alert[3])
    h = int(last_alert[4][0] + last_alert[4][1])
    m = int(last_alert[4][3] + last_alert[4][4])
    s = int(last_alert[4][6] + last_alert[4][7])
    # Define formato1
    formato1 = "%Y %b %d %H:%M:%S"
    # last_day equal to format1 format
    fecha_last = datetime(int(year), int(
        mes), int(day), int(h), int(m), int(s))
    fecha_last_logs = fecha_last.strftime(formato1)
    print fecha_last_logs


def strings_to_numbers(arg):
    """
        Function that swaps the values of
        dates (strings) by an integer value.
    """
    switcher = {
        "Jan": 1,
        "Feb": 2,
        "Mar": 3,
        "Apr": 4,
        "May": 5,
        "Jun": 6,
        "Jul": 7,
        "Aug": 8,
        "Sep": 9,
        "Oct": 10,
        "Nov": 11,
        "Dec": 12,
    }
    return switcher.get(arg, "nothing")


def extendUse(text):
    """
        Extended use of the program:
        First we store the regular expression and seek their
        matches, we store the last, as in the simple function.
        Then we define a format using DataTime library.
        We transform the last timeslap, we have saved to this format.
        We estimate the current date and check if the last timeslap
        this deadline.
        Show whether it is true or not and the last timeslap.
    """
    fa = '((19|20)\d\d)+\s+(Jan|Feb|Mar|Apr|May|Jun|Jul)+\s+(\d+)\s([0-6][0-9].[0-6][0-9].[0-6][0-9])'
    f = re.findall(fa, text)
#    print type(f) # type list
    last_alert = f[-1]
#    print type(last_alert)    # type tuple
    # Extract the variables hour, minutes, seconds, day,
    # month and year of the last timeslap
    year = (last_alert[0])
    m = (last_alert[2])
    mes = (strings_to_numbers(m))
    day = int(last_alert[3])
    h = int(last_alert[4][0] + last_alert[4][1])
    m = int(last_alert[4][3] + last_alert[4][4])
    s = int(last_alert[4][6] + last_alert[4][7])

    # Define format1
    formato1 = "%Y %b %d %H:%M:%S"
    # keep the number of days in n
    n = sys.argv[2]
    # we subtract the current date n days
    today = datetime.today() - timedelta(days=int(n))  # actual time
    time_aux = today.strftime(formato1)  # time in formato1
    # last_day equal to format1
    fecha_last = datetime(int(year), int(
        mes), int(day), int(h), int(m), int(s))
    fecha_last_logs = fecha_last.strftime(formato1)
#    print fecha_last_logs
    # show the result

    if (time_aux >= fecha_last_logs):
        print "False " + "(" + fecha_last_logs + ")"
    else:
        print "True " + "(" + fecha_last_logs + ")"

# Read and save the file
infile = open("alerts.log", "rb")
logs = infile.read()

if __name__ == "__main__":
    main(logs)
