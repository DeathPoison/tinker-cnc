#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('foo', default='a')
parser.add_argument('bar', default='b', nargs='?')
parser.add_argument('baz', default='Blubb', nargs='*')
print parser.parse_args()

