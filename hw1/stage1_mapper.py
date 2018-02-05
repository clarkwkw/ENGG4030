#!/usr/bin/python
from __future__ import print_function
import sys

def get_line(file):
	for line in file:
		line = line.strip()
		yield line

def map():
	for line in get_line(sys.stdin):
		follower, followees = line.split(":", 1)
		followees = followees.split(" ")
		for followee in followees:
			print("%s\t%s"%(followee, follower))

if __name__ == "__main__":
	map()