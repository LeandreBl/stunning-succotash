#!python3
import pandas as pd
import sys
import re
from io import StringIO
import difflib

if len(sys.argv) != 3:
    print(f'USAGE: {sys.argv[0]} <intra_list.csv> <attendance.csv>')
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
    print('login;present')
    for name, status in dic.items():
        print(f'{name};{status}')


def remove_dot_spaces(entry: str):
    return entry.replace(r'.|-', ' ')

def initial_presence_dict(logins: list):
    attendances = {}
    for name in logins:
        attendances[name] = 'absent'
    return attendances

with open(sys.argv[1], 'r', errors='ignore') as intra_csv:
    intra_csv = clean_string(intra_csv.read())
    intra_csv = pd.read_csv(StringIO(intra_csv), sep=';')
    with open(sys.argv[2], 'r', errors='ignore') as attendance_csv:
        string = clean_string(attendance_csv.read())
        attendance_csv = pd.read_csv(StringIO(string), index_col=None, header=0,
                                     skipinitialspace=True, sep='\t')
        attendances = initial_presence_dict(intra_csv['login'])
        for name in attendances.keys():
            epur_name = remove_dot_spaces(name.replace('@epitech.eu', ''))
            names = difflib.get_close_matches(epur_name, attendance_csv['nom complet'])
            if len(names) > 0:
                attendances[name] = 'present'
        print_csv(attendances)
