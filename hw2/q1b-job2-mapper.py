#!/usr/bin/python
from __future__ import print_function
import sys

CANDIDATE_FILE = "candidates.txt"

def get_line(file):
	for line in file:
		line = line.strip()
		yield line

candidate_pairs = {}
n_baskets = 0

with open(CANDIDATE_FILE, "r") as f:
	for line in f:
		candidate_pairs["-".join(line.strip().split("\t"))] = 0

for line in get_line(sys.stdin):
	unique_items = list({word: True for word in line.split()}.keys())
	n_baskets += 1
	for i in range(len(unique_items)):
		for j in range(i + 1, len(unique_items))
			pair = "%s-%s"%sorted((unique_items[i], unique_items[j]))
			if pair in candidate_pairs:
				candidate_pairs[pair] += 1

for pair, count in candidate_pairs.items():
	print("%s\t%d\t%d"%(pair, count, n_baskets))