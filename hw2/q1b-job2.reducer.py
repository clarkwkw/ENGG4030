#!/usr/bin/python
from __future__ import print_function
import sys

THRESHOLD = 0.005

def get_line(file):
	for line in file:
		line = line.strip()
		yield line

prev_pair = None
occurence = 0
n_baskets = 0
for line in get_line(sys.stdin):
	pair, count, sub_baskets = line.split("\t")
	if pair != prev_pair and prev_pair is not None:
		if 1.0*occurence/n_baskets >= THRESHOLD:
			item1, item2 = prev_pair.split("-")
			print("%s, %s: %d"%(item1, item2, occurence))
		occurence = 0
		n_baskets = 0
		
	prev_pair = pair
	occurence += count
	n_baskets += sub_baskets

if 1.0*occurence/n_baskets >= THRESHOLD:
	item1, item2 = prev_pair.split("-")
	print("%s,%s: %d"%(item1, item2, occurence))