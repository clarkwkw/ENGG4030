#!/usr/bin/env python
from __future__ import print_function
import sys

K = 3

def get_line(file):
	for line in file:
		line = line.strip()
		yield line

def output(prev_user, similarities, checksums):
	neighbor_sim = [(n, len(fs)) for n, fs in similarities.items()]
	neighbor_sim = sorted(neighbor_sim, key = lambda t: t[1], reverse = True)
	last_index = min(K, len(neighbor_sim))
	for neighbor, sim in neighbor_sim[0:last_index]:
		print("%s: %s, {%s}, %s"%(prev_user, neighbor, ', '.join(similarities[neighbor]), checksums[neighbor]))


def reduce():
	prev_user = None
	similarities, checksums = {}, {}

	for line in get_line(sys.stdin):
		user, peer, followee = line.split("\t")
		if user != prev_user:
			if prev_user is not None:
				output(prev_user, similarities, checksums)
			prev_user = user
			similarities, checksums = {}, {}

		if peer not in similarities:
			similarities[peer] = []
			checksums[peer] = 0
		
		similarities[peer].append(followee)
		checksums[peer] += int(followee)
		
	output(prev_user, similarities, checksums)

if __name__ == "__main__":
	reduce()