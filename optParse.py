#!/usr/bin/env python
# -*- coding: utf-8 -*-

from optparse import OptionParser
parser = OptionParser()

parser.add_option("-o", "--operation", dest="operation", help="Operation")
parser.add_option("-v", "--verbose",   dest="verbose",   help="Verbose Output!", default=False, action="store_true")



(optionen, args) = parser.parse_args()


if len(args) >= 2:
    parser.error("Es wurden zuviele Parameter angegeben!")

def onAdd():
    return "You have call: '-o add'"

def onUpdate():
    return "you called: '-o update"

argument = {
    "add": onAdd(),
    "update": onUpdate(),
    None: onAdd()
}

if optionen.verbose:
    print "Verbose mode is activated!!"

op = optionen.operation
if op in argument:
    print "Ergebnis:" + argument[op]
else:
    parser.error("%s ist keine Operation" % op)
