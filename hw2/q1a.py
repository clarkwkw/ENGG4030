from __future__ import print_function
import argparse

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

	print("Pass 1...")
	# Pass 1
	for path in dataset:
		f = open(path, "r")
		for line in f:
			n_baskets += 1
			occured = {}
			for term in line.strip().split(" "):
				if term not in occured:
					occured[term] = True
					term_count[term] = term_count.get(term, 0) + 1
		f.close()

	print("# baskets: %d"%n_baskets)
	print("# unique terms: %d"%len(term_count))

	for term, occurence in term_count.items():
		max_freq = max(max_freq, occurence)
		if 1.0*occurence/n_baskets >= THRESHOLD:
			term_freq[term] = 1

	print("max freq: %d"%max_freq)
	print("# frequent terms: %d"%len(term_freq))
	print("Pass 2...")

	# Pass 2
	for path in dataset:
		f = open(path, "r")
		for line in f:
			words = line.strip().split(" ")
			pair_occured = {}
			for i in range(len(words)):
				term1 = words[i]
				if term1 in term_freq:
					for j in range(i + 1, len(words)):
						term2 = words[j]
						if term2 in term_freq:
							pair = tuple(sorted([term1, term2]))
							if pair not in pair_occured:
								pair_occured[pair] = True
								pair_count[pair] = pair_count.get(pair, 0) + 1
		f.close()

	print("Sorting %d unique pairs..."%len(pair_count))
	freq_pairs = []
	for pair, occurence in pair_count.items():
		if 1.0*occurence/n_baskets >= THRESHOLD:
			freq_pairs.append((pair, occurence))
	freq_pairs = sorted(freq_pairs, key = lambda p: p[1], reverse = True)

	print("Frequent pairs:")
	for i in range(min(len(freq_pairs), MAX_RESULT)):
		pair, occurence = freq_pairs[i]
		print("%s\t%d"%(",".join(pair), occurence))

if __name__ == "__main__":
	solve(parse_args())
