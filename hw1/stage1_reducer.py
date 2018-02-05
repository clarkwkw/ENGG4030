#!/usr/bin/python
from __future__ import print_function
import sys

def get_line(file):
	for line in file:
		line = line.strip()
		yield line

def reduce():
	prev_followee = None
	prev_followers = []
	for line in get_line(sys.stdin):
		followee, follower = line.split("\t", 1)
		if followee != prev_followee:
			prev_followee = followee
			prev_followers = []
		
		for prev_follower in prev_followers:
			print("%s\t%s\t%s"%(prev_follower, follower, followee))

		prev_followers.append(follower)

if __name__ == "__main__":
	reduce()