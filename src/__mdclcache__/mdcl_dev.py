'''

MDCL created by Aiden Blishen Cuneo.
First Commit was at: 1/1/2020.

'''

import datetime
import os
import re
import sys
import string
import time
import traceback as tb
import types

from pprint import pformat

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


get_input = raw_input if sys.version_info[0] < 3 else input


def clirun(cmd):
    if isinstance(cmd, (list, tuple)):
        cmd = ' '.join(cmd)
    if isinstance(cmd, str):
        return os.system(cmd)
    return


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


def error(text):
    print('-->', end='')
    print(text, end='')
    print('\n', end='')
    print(sys.exit(), end='')

def tokenise(code):
    sq = False
    dq = False
    bcomment = False
    l = []
    o = ''
    p = ''
    t = ''
    for a in iterate(code . strip ()):
        q = p
        if a in alphabet:
            p = 'A'
        elif a in digits:
            p = 'D'
        elif a in symbols:
            p = 'S'
        elif a in whitespace:
            p = 'W'
        if (not q == p and not p == 'W' or p == 'S') and not (t in ('-' , '+') and p == 'D') and not (t == '=' and a == '=') and not (t == '=' and a == '>') and not (t == '>' and a == '=') and not (t == '<' and a == '=') and not (t == '+' and a == ':') and not (t == '-' and a == ':') and not (t == '*' and a == ':') and not (t == '/' and a == ':') and not (t == '_' and p == 'A') and not (q == 'A' and a == '_') and not (t == '_' and a == '_') and not (sq or dq or bcomment):
            print(l . append (o . strip ()), end='')
            o = ''
        if a == "'" and not (dq or bcomment):
            sq = not sq
        elif a == '"' and not (sq or bcomment):
            dq = not dq
        elif t == '/' and a == '*' and not (sq or dq):
            l = l [:-1]
            bcomment = True
        elif t == '*' and a == '/' and not (sq or dq):
            a = ''
            bcomment = False
        if not bcomment:
            o += a
        t = a
    out = list(filter(None , l + [o]))
    return post_tokenise (out)

def post_tokenise(lst):
    if 'do' in lst:
        i = lst . index ('do')
        lst[i] = '{' + ' ' . join (lsst [i + 1:]) + '};;'
        for __ in iterate(range(i + 1, len (lst))):
            print(lst . pop (__), end='')
    return lst

def compile(text):
    compiled = ''
    lines = tokenise(text)
    return lines

fKeys = 'write' , 'exit' , 'string'
fVals = 'print' , 'sys.exit' , 'str'
keywords = 'break' , 'ret' , 'yield'
this = argv(1)
if not this:
    print('Input file not given.\n', end='')
    print(sys.exit(), end='')
this = os . path . abspath (this)
compiled = compile(readfile(this))
print(compiled)
print(sys.exit(), end='')

cachedir = os . path . abspath ('/' . join (os . path . split (this) [:-1]) + '/__mdclcache__')
cachefile = cachedir + '/' + os . path . splitext (os . path . basename (this)) [0] + '.py'
if not os . path . isdir (cachedir):
    _ = os . mkdir (cachedir)
code = readfile(this)
execScript = os . path . abspath (argv(0))
pcd = '/' . join (os . path . split (execScript) [:-1]) + '/__pcd__.py'
compiled = readfile(pcd) + '\n\n'
compiled += compile(code)
compiled = compiled . strip () + '\n'
_ = writefile(cachefile , compiled)
_ = sys . path . insert (0 , cachedir)
print(os . path . splitext (os . path . basename (cachefile)) [0])
sys.argv = sys . argv [1:]
_ = exec('import ' + os . path . splitext (os . path . basename (cachefile)) [0])
