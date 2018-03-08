from __future__ import print_function
import argparse
import utils

THRESHOLD = 0.005
MAX_RESULT = 40

def parse_args():
	parser = argparse.ArgumentParser(description = "Aprior algorithm")
	parser.add_argument("dataset", nargs = "+", help = "Shakespeare data files")

	return parser.parse_args().dataset

def solve(dataset):
	term_count, term_freq, pair_count = {}, {}, {}
	n_baskets = 0
	max_freq = -1

	# Pass 1
	for path in dataset:
		f = open(path, "r")
		for line in f:
			n_baskets += 1
			unique_terms = list({term: True for term in line.strip().split(" ")}.keys())
			for term in unique_terms:
				term_count[term] = term_count.get(term, 0) + 1
		f.close()

	for term, occurence in term_count.items():
		max_freq = max(max_freq, occurence)
		if 1.0*occurence/n_baskets >= THRESHOLD:
			term_freq[term] = 1

	# Pass 2
	for path in dataset:
		f = open(path, "r")
		for line in f:
			unique_terms = sorted(list({term: True for term in line.strip().split(" ")}.keys()))
			for pair in utils.enumerate_recursive(unique_terms, 2):
				is_freq = True
				for item in pair:
					if item not in term_freq:
						is_freq = False
						break
				if is_freq:
					pair_count[tuple(pair)] = pair_count.get(tuple(pair), 0) + 1

		f.close()

	freq_pairs = []
	for pair, occurence in pair_count.items():
		if 1.0*occurence/n_baskets >= THRESHOLD:
			freq_pairs.append((pair, occurence))
	freq_pairs = sorted(freq_pairs, key = lambda p: p[1], reverse = True)

	for i in range(min(len(freq_pairs), MAX_RESULT)):
		pair, occurence = freq_pairs[i]
		print("%s\t%d"%(",".join(pair), occurence))

if __name__ == "__main__":
	solve(parse_args())