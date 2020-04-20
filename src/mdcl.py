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


scb = '{'
ecb = '}'
sb = '('
eb = ')'
ssb = '['
esb = ']'
def error(text):
    print(text, end='')
    print('\n', end='')
    print(sys.exit(), end='')

def cbstrip(str):
    if (str [0] == scb) and (str [-1] == ecb):
        str = str [1:-1]
    return str . strip ("\n\t ")

def bstrip(str):
    if (str [0] == sb) and (str [-1] == eb):
        str = str [1:-1]
    return str . strip ("\n\t ")

def sbstrip(str):
    if (str [0] == ssb) and (str [-1] == esb):
        str = str [1:-1]
    return str . strip ("\n\t ")

def compile(text, scope=0, canEcho=True, inline=False):
    compiled = ''
    lines = tokeniseFile(text)
    for i in iterate(lines):
        line = ()
        last = ''
        for __ in iterate(tokenise(i)):
            if (__ . startswith (sb)) and (__ . endswith (eb)):
                if last == ':':
                    line += __ ,
                    last = __
                else:
                    n = sb + (compile(bstrip(__) , 0 , False , False) . strip ("\n ")) + eb
                    line += n ,
                    last = n
            elif (__ . startswith (ssb) and (__ . endswith (esb))):
                if last == ':':
                    line += __ ,
                    last = __
                else:
                    n = __ . replace ('#' , '__')
                    line += n ,
                    last = n
            elif __ == 'true':
                line += 'True' ,
                last = 'True'
            elif __ == 'false':
                line += 'False' ,
                last = 'False'
            elif __ == 'null':
                line += 'None' ,
                last = 'None'
            elif __ == '=':
                line += '==' ,
                last = '=='
            elif __ == '#':
                line += '__' ,
                last = '__'
            elif __ == '!':
                line += 'not' ,
                last = 'not'
            else:
                line += __ ,
                last = __
        if len (line) < 1:
            line += None ,
        if ':' in line:
            compiled += scope * ' '
            if line [0] == 'for':
                compiled += 'for ' + (line [1]) + ' in '
                index = 0
                for __ in iterate(line):
                    if __ == ':':
                        break
                    index += 1
                c = ''
                for __ in iterate(range(index + 1, (len(line) - 1))):
                    c += line [__] + ' '
                c = compile(c , 0 , False , True) . strip ()
                compiled += 'iterate(' + c + "):\n"
                compiled += compile(cbstrip(line [-1]) , scope + 4 , True)
            elif '=>' in line:
                compiled += scope * ' '
                compiled += 'def ' + (line [0]) + '(' + (line [2] . strip ('[]')) + "):\n"
                compiled += compile(cbstrip(line [-1]) , scope + 4 , True) . rstrip () + "\n\n"
            else:
                start = ''
                index = 0
                for __ in iterate(line):
                    if __ == ':':
                        break
                    start += __
                    index += 1
                if not start:
                    start = '_'
                compiled += start + ' = '
                c = ''
                for __ in iterate(range(index + 1, (len(line)))):
                    c += line [__] + ' '
                compiled += compile(c , 0 , False , True) . strip ()
                compiled += '\n'
        elif '+:' in line:
            if (not inline):
                compiled += scope * ' '
            start = ''
            index = 0
            for __ in iterate(line):
                if __ == '+:':
                    break
                start += __
                index += 1
            compiled += start + ' += '
            c = ''
            for __ in iterate(range(index + 1, (len(line)))):
                c += line [__] + ' '
            compiled += compile(c , 0 , False , True) . strip ()
            compiled += '\n'
        elif '-:' in line:
            if (not inline):
                compiled += scope * ' '
            start = ''
            index = 0
            for __ in iterate(line):
                if __ == '-:':
                    break
                start += __
                index += 1
            compiled += start + ' -= '
            c = ''
            for __ in iterate(range(index + 1, (len(line)))):
                c += line [__] + ' '
            compiled += compile(c , 0 , False , True) . strip ()
            compiled += '\n'
        elif '*:' in line:
            if (not inline):
                compiled += scope * ' '
            start = ''
            index = 0
            for __ in iterate(line):
                if __ == '*:':
                    break
                start += __
                index += 1
            compiled += start + ' *= '
            c = ''
            for __ in iterate(range(index + 1, (len(line)))):
                c += line [__] + ' '
            compiled += compile(c , 0 , False , True) . strip ()
            compiled += '\n'
        elif '/:' in line:
            if (not inline):
                compiled += scope * ' '
            start = ''
            index = 0
            for __ in iterate(line):
                if __ == '/:':
                    break
                start += __
                index += 1
            compiled += start + ' /= '
            c = ''
            for __ in iterate(range(index + 1, (len(line)))):
                c += line [__] + ' '
            compiled += compile(c , 0 , False , True) . strip ()
            compiled += '\n'
        elif '?' in line:
            compiled += scope * ' '
            cond = ''
            index = 0
            for __ in iterate(line):
                if __ == '?':
                    break
                cond += __ + ' '
                index += 1
            if '\\' in line:
                first = ''
                bindex = 0
                for __ in iterate(range(index + 1 , len (line))):
                    bindex = __
                    if line [__] == '\\':
                        break
                    first += line [__] + ' '
                second = ''
                for __ in iterate(range(bindex + 1 , len (line))):
                    second += line [__] + ' '
            else:
                first = ''
                bindex = 0
                for __ in iterate(range(index + 1 , len (line))):
                    first += line [__] + ' '
                second = 'None'
            compiled += first . strip () + ' if ' + cond . strip () + ' else ' + second . strip () + '\n'
            done = True
        elif (line [0]) in ('if' , 'elif' , 'while'):
            compiled += scope * ' '
            compiled += line [0] + ' '
            index = 0
            for __ in iterate(line):
                if (__ . startswith (scb)) and (__ . endswith (ecb)):
                    break
                index += 1
            for __ in iterate(range(1, index)):
                compiled += line [__] + ' '
            compiled = compiled . rstrip ()
            compiled += ":\n"
            compiled += compile(cbstrip(line [index]) , scope + 4) . rstrip () + '\n'
        elif line [0] == 'else':
            compiled += scope * ' '
            compiled += "else:\n"
            compiled += compile(cbstrip(line [1]) , scope + 4) . rstrip () + '\n'
        elif line [0] == 'for':
            compiled += scope * ' '
            compiled += 'for __ in '
            c = ''
            for __ in iterate(range(1, (len(line) - 1))):
                c += line [__] + ' '
            c = compile(c , 0 , False , True) . strip ()
            compiled += 'iterate(' + c + "):\n"
            compiled += compile(cbstrip(line [-1]) , scope + 4 , True) . rstrip () + '\n'
        elif 'to' in line:
            compiled += scope * ' '
            index = line . index ('to')
            first = ' ' . join (line [:index])
            second = ' ' . join (line [index + 1:])
            compiled += 'range(' + first + ', ' + second + ')\n'
        elif len (line) > 1:
            compiled += scope * ' '
            if (line [1] . startswith (sb)) and (line [1] . endswith (eb)):
                echoable = True
                first = line [0]
                if first in fKeys:
                    index = 0
                    for __ in iterate(fKeys):
                        if __ == first:
                            break
                        index += 1
                    first = fVals [index]
                if first in ('print' , 'echo'):
                    echoable = False
                c = ''
                for __ in iterate(range(1, (len(line)))):
                    c += line [__] + ' '
                c = first + (compile(c , 0 , False , True))
                compiled += "print(" + c + ", end='')\n" if (canEcho and not (__ in keywords) and echoable) else c
                compiled += '\n'
            elif line [0] == 'ret':
                compiled += 'return '
                for __ in iterate(range(1, (len(line)))):
                    if type (line [__]) . __name__ == 'str':
                        compiled += line [__] + ' '
                compiled = compiled . rstrip ()
            elif inline:
                c = ' ' . join (line)
                compiled += "print(" + c + ", end='')\n" if canEcho and __ not in keywords else c
                compiled = compiled . rstrip ()
            else:
                c = compile(' ' . join (line) , 0 , False , True) . strip ()
                compiled += "print(" + c + ", end='')\n" if canEcho and __ not in keywords else c
        elif len (line) == 1:
            for __ in iterate(line):
                if type (__) . __name__ == 'str':
                    compiled += scope * ' '
                    compiled += "print(" + __ + ", end='')\n" if canEcho and __ not in keywords else __
    return compiled

fKeys = ('write' , 'exit' , 'string')
fVals = ('print' , 'sys.exit' , 'str')
keywords = ('break' , 'ret')
this = argv(1)
if not this:
    print('Input file not given.\n', end='')
    print(sys.exit(), end='')
this = os . path . abspath (this)
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
