#!/usr/bin/python
from __future__ import print_function
import sys
sys.path.append('./')
import utils

prev_pair = None
occurence = 0
n_baskets = 0

args = utils.parse_args()
THRESHOLD, N_ITEM = args.threshold, args.n_item

for line in utils.get_line():
	pair, count, sub_baskets = line.split("\t")
	if pair != prev_pair and prev_pair is not None:
		if 1.0*occurence/n_baskets >= THRESHOLD:
			print("%s\t%d"%(prev_pair.replace("-", ","), occurence))
		occurence = 0
		n_baskets = 0
		
	prev_pair = pair
	occurence += int(count)
	n_baskets += int(sub_baskets)

if 1.0*occurence/n_baskets >= THRESHOLD:
	print("%s\t%d"%(prev_pair.replace("-", ","), occurence))