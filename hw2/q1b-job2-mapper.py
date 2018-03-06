#!/usr/bin/python
from __future__ import print_function
import utils

CANDIDATE_FILE = "candidates.txt"

candidate_pairs = {}
n_baskets = 0

args = utils.parse_args()
THRESHOLD, N_ITEM = args.threshold, args.n_item

with open(CANDIDATE_FILE, "r") as f:
	for line in f:
		candidate_pairs[line.strip().replace("\t", "-")] = 0

for line in utils.get_line():
	unique_items = sorted(list({word: True for word in line.split()}.keys()))
	n_baskets += 1
	for t in utils.enumerate_recursive(unique_items, N_ITEM):
		t = "-".join(t)
		if t in candidate_pairs:
			candidate_pairs[t] += 1

for pair, count in candidate_pairs.items():
	print("%s\t%d\t%d"%(pair, count, n_baskets))