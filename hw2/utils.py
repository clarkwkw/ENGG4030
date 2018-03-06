import sys
import argparse

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("threshold", type = float)
	parser.add_argument("n_item", type = int)
	return parser.parse_args()

def get_line(file = sys.stdin):
	for line in file:
		line = line.strip()
		yield line

def enumerate_recursive(items, num):
	if num == 0:
		yield []

	elif len(items) == num:
		yield items

	elif len(items) > num:
		for i in range(len(items)):
			for sub_list in enumerate_recursive(items[(i+1): len(items)], num - 1):
				yield [items[i]] + sub_list