#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

parser = argparse.ArgumentParser(description='Test Stepper Motor!')
parser.add_argument('device', metavar='N', type=str, nargs='+', help='a device name e.g. stepper or lcd')
parser.add_argument('id', metavar='M', type=str, nargs='+', help='id of device')
parser.add_argument('steps', metavar='steps', type=int, nargs='+', help='a device name e.g. stepper or lcd')


args = parser.parse_args()
print args

print args.steps



