#!/usr/bin/python
from __future__ import print_function
import sys
sys.path.append('./')
import utils

CANDIDATE_FILE = "candidates.txt"

candidate_pairs = {}
candidate_items = {}
n_baskets = 0

args = utils.parse_args()
THRESHOLD, N_ITEM = args.threshold, args.n_item

with open(CANDIDATE_FILE, "r") as f:
	for line in f:
		items = line.strip().split("\t")
		for item in items:
			candidate_items[item] = 0
		candidate_pairs["-".join(items)] = 0

for line in utils.get_line():
	unique_items = sorted(list({word: True for word in line.split() if word in candidate_items}.keys()))
	n_baskets += 1
	for t in utils.enumerate_recursive(unique_items, N_ITEM):
		t = "-".join(t)
		if t in candidate_pairs:
			candidate_pairs[t] += 1

for pair, count in candidate_pairs.items():
	print("%s\t%d\t%d"%(pair, count, n_baskets))