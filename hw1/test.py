from __future__ import print_function
import argparse
import numpy as np

name_to_index = {}
names = []
n_count = 0

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("dataset", type = str, help = "path to the dataset")
	parser.add_argument("n_max", type = int, help = "no. of highest similarity to show")
	args = parser.parse_args()
	return args

def get_index(name):
	global name_to_index, n_count, names
	if name not in name_to_index:	
		name_to_index[name] = n_count
		names.append(name)
		n_count += 1
	return name_to_index[name]

def test(args):
	connection_matrix = []
	with open(args.dataset, "r") as f:
		for line in f.readlines():
			name, neighbors = line.strip().split(":", 1)
			index = get_index(name)

			neighbors = neighbors.split(" ")
			tmp_arr = []
			for neighbor in neighbors:
				index_neighbor = get_index(neighbor)
				tmp_arr.append(index_neighbor)
			connection_matrix.append((index, tmp_arr))

	follow_matrix = np.zeros((n_count, n_count))
	for index, tmp_arr  in connection_matrix:
		for neighbor in tmp_arr:
			follow_matrix[index, neighbor] = 1
	print(follow_matrix)
	similarity_matrix = np.dot(follow_matrix, follow_matrix.T)
	print(similarity_matrix)
	highest_similarity_index = similarity_matrix.argsort(axis = 1)[:, -1:-(args.n_max + 2):-1]
	print(highest_similarity_index)
	for i in range(len(connection_matrix)):
		print(names[i]+":", end = " ")
		printed = 0
		for j in range(args.n_max + 1):
			index = highest_similarity_index[i, j]
			if i != index and printed < args.n_max:
				print(names[index] + "(%d)"%similarity_matrix[i, index], end = " ")
				printed += 1
		print()

if __name__ == "__main__":
	test(parse_args())