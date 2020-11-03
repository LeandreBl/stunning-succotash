#!/usr/bin/env python3
import pandas as pd
import sys
import re
from io import StringIO
import difflib

if len(sys.argv) != 3:
    print(f"USAGE: {sys.argv[0]} <intra_list.csv> <attendance.csv>")
    exit(1)

REPLACERS = {
    r'é|ë': 'e',
    r';\n': '\n',
    'ï': 'i',
    'à': 'a',
}


def clean_string(string: str):
    for reg, rep in REPLACERS.items():
        string = re.sub(reg, rep, string)
    string = string.lower()
    return re.sub(r'[^a-zA-Z0-9_\n\t -.:/@;]', '', string)


def print_csv(dic: dict):
    print("login;present")
    for name, status in dic.items():
        print(f"{name};{status}")


with open(sys.argv[1], 'r', errors="ignore") as intra_csv:
    intra_csv = clean_string(intra_csv.read())
    intra_csv = pd.read_csv(StringIO(intra_csv), sep=";")
    with open(sys.argv[2], 'r', errors="ignore") as attendance_csv:
        string = clean_string(attendance_csv.read())
        attendance_csv = pd.read_csv(StringIO(string), index_col=None, header=0,
                                     skipinitialspace=True, sep='\t')
        attendance = {}
        for name in intra_csv["login"]:
            attendance[name] = "absent"
        for name in attendance_csv["nom complet"]:
            names = difflib.get_close_matches(name, intra_csv["login"])
            if len(names) == 1:
                attendance[names[0]] = "present"
        print_csv(attendance)
