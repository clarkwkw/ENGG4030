#!/usr/bin/python
from __future__ import print_function
import sys

THRESHOLD = 0.005

def get_line(file):
	for line in file:
		line = line.strip()
		yield line

n_baskets = 0
items = {}
freq_items = []

for line in get_line(sys.stdin):
	n_baskets += 1
	unique_words = {word: True for word in line.split()}
	for word in unique_words:
		items[word] = items.get(word, 0) + 1

for item, count in items.items():
	if 1.0*count/n_baskets >= THRESHOLD:
		freq_items.append(item)

for i in range(len(freq_items)):
	for j in range(i + 1, len(freq_items)):
		item1, item2 = sorted((freq_items[i], freq_items[j]))
		print("%s-%s\t1"%(item1, item2))