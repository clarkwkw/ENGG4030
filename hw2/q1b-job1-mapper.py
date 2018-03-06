#!/usr/bin/python
from __future__ import print_function
import utils

n_baskets = 0
items = {}
freq_items = []

args = utils.parse_args()
THRESHOLD, N_ITEM = args.threshold, args.n_item

for line in utils.get_line():
	n_baskets += 1
	unique_words = {word: True for word in line.split()}
	for word in unique_words:
		items[word] = items.get(word, 0) + 1

for item, count in items.items():
	if 1.0*count/n_baskets >= THRESHOLD:
		freq_items.append(item)

freq_items = sorted(freq_items)
for item_tuple in utils.enumerate_recursive(freq_items, N_ITEM):
	print("%s\t1"%("-".join(item_tuple)))