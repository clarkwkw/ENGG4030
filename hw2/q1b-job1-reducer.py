#!/usr/bin/python
from __future__ import print_function
import utils

args = utils.parse_args()
THRESHOLD, N_ITEM = args.threshold, args.n_item

prev_tuple = None
for line in utils.get_line():
	item_tuple_str, _ = line.split("\t")
	if prev_tuple != item_tuple_str and prev_tuple is not None:
		print("%s"%(prev_tuple.replace("-", "\t")))	
	prev_tuple = item_tuple_str