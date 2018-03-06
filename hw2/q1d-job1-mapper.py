#!/usr/bin/python
from __future__ import print_function
import sys
sys.path.append('./')
import utils

N_BUCKETS = 100000

def pcy_hash(words):
	return hash("".join(words)) % N_BUCKETS

n_baskets = 0
items = {}
freq_items = []
buckets = [0 for _ in range(N_BUCKETS)]
buckets_pairs = [{} for _ in range(N_BUCKETS)]

args = utils.parse_args()
THRESHOLD, N_ITEM = args.threshold, args.n_item

for line in utils.get_line():
	n_baskets += 1
	unique_words = sorted({word: True for word in line.split()}.keys())
	for word in unique_words:
		items[word] = items.get(word, 0) + 1

	for t in utils.enumerate_recursive(unique_words, N_ITEM):
		h_value = pcy_hash(t)
		buckets[h_value] += 1
		if tuple(t) not in buckets_pairs[h_value]:
			buckets_pairs[h_value][tuple(t)] = True

for i in range(N_BUCKETS):
	if 1.0*buckets[i]/n_baskets >= THRESHOLD:
		for t in buckets_pairs[i]:
			is_all_frequent = True
			for item in t:
				if 1.0*items[item]/n_baskets < THRESHOLD:
					is_all_frequent = False
					break
			if is_all_frequent:
				print("%s\t1"%("-".join(t)))