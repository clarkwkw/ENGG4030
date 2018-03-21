#!/usr/bin/python
from __future__ import print_function
import sys
sys.path.append('./')
import mr_utils
import numpy as np
from numpy.linalg import norm

clusters = np.zeros((10, mr_utils.N_DIMENSION))
clusters_count = np.zeros(clusters.shape[0])

for line in mr_utils.get_line():
	idx, cluster, count = line.split("\t")
	idx = int(idx)
	count = int(count)
	cluster = np.fromstring(cluster.strip("[]"), sep = ",")

	prev_count = clusters_count[idx]
	clusters[idx] = (clusters[idx] * prev_count + cluster * count)/(prev_count + count)
	clusters_count[idx] += count

clusters_mat = None
for i in range(clusters.shape[0]):
	if clusters_count[i] > 0:
		print("%d\t%s\t%d"%(i, clusters[i].tolist(), clusters_count[i]))