'''

MDCL created by Aiden Blishen Cuneo.
First Commit was at: 1/1/2020.

'''

import re
import sys
import string

alphabet = string.letters if sys.version_info[0] < 3 else string.ascii_letters
digits = string.digits
symbols = string.punctuation
whitespace = string.whitespace


def process(code):
    return tokenise_file(code)#.replace('\n', ''))


def isnum(num):
    return re.match('^(-|\+)*[0-9]+$', num)


def isfloat(num):
    return re.match('^(-|\+)*[0-9]*\.[0-9]+$', num)


def isword(word):
    return all([b in alphabet for b in word])


def tokenise(line):
    sq = False
    dq = False
    bt = False
    bcomment = False
    rb = 0
    sb = 0
    cb = 0
    l = []
    o = ''
    p = ''
    t = ''
    for a in line.strip():
        q = p
        if a in alphabet:
            p = 'A'
        elif a in digits:
            p = 'D'
        elif a in symbols:
            p = 'S'
        elif a in whitespace:
            p = 'W'
        if (q != p and p != 'W' or p == 'S') and not (
            t in ('-', '+') and p == 'D'
        ) and not (
            t == '=' and a == '='
        ) and not (
            t == '=' and a == '>'
        ) and not (
            t == '>' and a == '='
        ) and not (
            t == '<' and a == '='
        ) and not (
            t == '+' and a == ':'
        ) and not (
            t == '-' and a == ':'
        ) and not (
            t == '*' and a == ':'
        ) and not (
            t == '/' and a == ':'
        ) and not (
            t == '_' and p == 'A'
        ) and not (
            q == 'A' and a == '_'
        ) and not (
            t == '_' and a == '_'
        ) and not (
            t == 'x' and (a in '"\'')
        ) and not (
            sq or dq or bt or rb > 0 or sb > 0 or cb > 0 or bcomment
        ):
            l.append(o.strip())
            o = ''
        if a == "'" and not (
            dq or bt or rb > 0 or sb > 0 or cb > 0 or bcomment
        ):
            sq = not sq
        elif a == '"' and not (
            sq or bt or rb > 0 or sb > 0 or cb > 0 or bcomment
        ):
            dq = not dq
        elif a == '`' and not (
            sq or dq or rb > 0 or sb > 0 or cb > 0
        ):
            bt = not bt
        elif a == '(' and not (
            sq or dq or bt or sb > 0 or cb > 0
        ):
            rb += 1
        elif a == ')' and not (
            sq or dq or bt or sb > 0 or cb > 0
        ):
            rb -= 1
        elif a == '[' and not (
            sq or dq or bt or rb > 0 or cb > 0
        ):
            sb += 1
        elif a == ']' and not (
            sq or dq or bt or rb > 0 or cb > 0
        ):
            sb -= 1
        elif a == '{' and not (
            sq or dq or bt or rb > 0 or sb > 0
        ):
            cb += 1
        elif a == '}' and not (
            sq or dq or bt or rb > 0 or sb > 0
        ):
            cb -= 1
        elif t == '/' and a == '*' and not (
            sq or dq or bt or rb > 0 or sb > 0 or cb > 0
        ):
            l = l[:-1]
            bcomment = True
        elif t == '*' and a == '/' and not (
            sq or dq or bt or rb > 0 or sb > 0 or cb > 0
        ):
            a = ''
            bcomment = False
        if not bcomment:
            o += a
        t = a
    out = list(filter(None, l + [o]))
    return post_tokenise(out)


def tokenise_file(code, split_at=';', dofilter=True):
    sq = False
    dq = False
    bt = False
    bcomment = False
    rb = 0
    sb = 0
    cb = 0
    l = []
    o = ''
    p = ''
    t = ''
    for a in code:
        if a == "'" and not (
            dq or bt or rb > 0 or sb > 0 or cb > 0 or bcomment
        ):
            sq = not sq
        elif a == '"' and not (
            sq or bt or rb > 0 or sb > 0 or cb > 0 or bcomment
        ):
            dq = not dq
        elif a == '`' and not (
            sq or dq or rb > 0 or sb > 0 or cb > 0 or bcomment
        ):
            bt = not bt
        elif a == '(' and not (
            sq or dq or bt or sb > 0 or cb > 0 or bcomment
        ):
            rb += 1
        elif a == ')' and not (
            sq or dq or bt or sb > 0 or cb > 0 or bcomment
        ):
            rb -= 1
        elif a == '[' and not (
            sq or dq or bt or rb > 0 or cb > 0 or bcomment
        ):
            sb += 1
        elif a == ']' and not (
            sq or dq or bt or rb > 0 or cb > 0 or bcomment
        ):
            sb -= 1
        elif a == '{' and not (
            sq or dq or bt or rb > 0 or sb > 0 or bcomment
        ):
            cb += 1
        elif a == '}' and not (
            sq or dq or bt or rb > 0 or sb > 0 or bcomment
        ):
            cb -= 1
            o += a
            a = split_at
        elif t == '/' and a == '*' and not (
            sq or dq or bt or rb > 0 or sb > 0 or cb > 0
        ):
            bcomment = True
        elif t == '*' and a == '/' and not (
            sq or dq or bt or rb > 0 or sb > 0 or cb > 0
        ):
            bcomment = False
        if a == split_at and not (
            sq or dq or bt or rb > 0 or sb > 0 or cb > 0 or bcomment
        ):
            l.append(o.strip(' \t\v\f\r'))
            o = ''
        else:
            o += a
        t = a
    out = l + [o.strip(' \t\v\f\r')]
    if dofilter:
        out = list(filter(None, out))
    return out


def post_tokenise(lst):
    if 'do' in lst:
        i = lst.index('do')
        lst[i] = '{' + ' '.join(lst[i + 1:]) + '}'
        del lst[i + 1:]
    return lst


import ast
import datetime
import os
import time
import traceback as tb
import types

from pprint import pformat


get_input = raw_input if sys.version_info[0] < 3 else input


def pretty(value):
    return pformat(value)


def read(prompt=''):
    return get_input(prompt)


def readfile(fname):
    with open(fname, 'rb') as f:
        data = f.read()
    data = data.decode('utf-8').replace('\r\n', '\n')
    return data


def writefile(fname, data):
    with open(fname, 'w') as f:
        f.write(data)
    return len(data)


def wait(amount):
    time.sleep(amount)


def argv(arg=None):
    if isinstance(arg, int):
        if arg < len(sys.argv):
            return sys.argv[arg]
        return
    return sys.argv


def iterate(arg):
    if isinstance(arg, int):
        arg = range(arg)
    return arg


tokeniseFile = tokenise_file
del tokenise_file


for __ in iterate(100):
    print('The number is ', end='')
    print(__)
    print('The number divided by 2 is ', end='')
    print(__ / 2)
