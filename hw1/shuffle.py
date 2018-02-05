#!/usr/bin/env python
from __future__ import print_function
import sys

def get_line(file):
	for line in file:
		line = line.strip()
		yield line

def shuffle():
	lines = []
	for line in get_line(sys.stdin):
		lines.append((line.split("\t", 1)[0], line))
	lines = sorted(lines, key = lambda t: t[0])
	for _, line in lines:
		print(line)
		
if __name__ == "__main__":
	shuffle()