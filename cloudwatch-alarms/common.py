#!/usr/bin/env python

ok = '\033[94m'
endc = '\033[0m'
fail = '\033[91m'

def info(input):
    print '        ' + ok + input + endc

def error(input):
    print '        ' + fail + input + endc
