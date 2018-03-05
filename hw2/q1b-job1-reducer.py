#!/usr/bin/python
from __future__ import print_function
import sys
import argparse

def get_line(file):
	for line in file:
		line = line.strip()
		yield line

prev_pair = None
for line in get_line(sys.stdin):
	pair, _ = line.split("\t")
	if prev_pair != pair and prev_pair is not None:
		item1, item2 = prev_pair.split("-")
		print("%s\t%s"%(item1, item2))
	prev_pair = pair