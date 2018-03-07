#!/usr/bin/python
from __future__ import print_function
import sys
sys.path.append('./')
import utils

CANDIDATE_FILE = "candidates.txt"

candidate_pairs = {}
freq_items = {}
n_baskets = 0

args = utils.parse_args()
THRESHOLD, N_ITEM = args.threshold, args.n_item

with open(CANDIDATE_FILE, "r") as f:
	for line in f:
		for item in line.strip().split("\t"):
			freq_items[item] = True

for line in utils.get_line():
	unique_items = sorted(list({word: True for word in line.split()}.keys()))
	n_baskets += 1
	for t in utils.enumerate_recursive(unique_items, N_ITEM):
		is_freq = True
		for item in t:
			if t not in freq_items:
				is_freq = False
				break
		if is_freq:
			t = "-".join(t)
			candidate_pairs[t] = candidate_pairs.get(t, 0) + 1

for pair, count in candidate_pairs.items():
	print("%s\t%d\t%d"%(pair, count, n_baskets))