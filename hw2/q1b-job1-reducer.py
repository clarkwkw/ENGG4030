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
		print("%s\t%s"%prev_pair.split("-"))
	prev_pair = pair