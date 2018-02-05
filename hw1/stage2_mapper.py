#!/usr/bin/env python
from __future__ import print_function
import sys

def get_line(file):
	for line in file:
		line = line.strip()
		yield line

def map():
	for line in get_line(sys.stdin):
		user1, user2, followee = line.split("\t")
		print("%s\t%s\t%s"%(user1, user2, followee))
		print("%s\t%s\t%s"%(user2, user1, followee))

if __name__ == "__main__":
	map()