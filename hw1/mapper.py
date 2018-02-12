#!/usr/bin/python
from __future__ import print_function
import sys

QUICKMODE = False
SID_SUFFIX = "63461"

def get_line(file):
	for line in file:
		line = line.strip()
		yield line

def map():
	for line in get_line(sys.stdin):
		followee, followers = line.split(":", 1)
		followers = followers.strip().split(" ")
		for i in range(len(followers)):
			for j in range(i + 1, len(followers)):
				if QUICKMODE:
					if followers[i].endswith(SID_SUFFIX):
						print("%s\t%s\t%s"%(followers[i], followers[j], followee))
					if followers[j].endswith(SID_SUFFIX):
						print("%s\t%s\t%s"%(followers[j], followers[i], followee))
				else:
					print("%s\t%s\t%s"%(followers[i], followers[j], followee))
					print("%s\t%s\t%s"%(followers[j], followers[i], followee))
					
if __name__ == "__main__":
	map()