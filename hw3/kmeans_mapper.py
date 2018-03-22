#!/home/ubuntu/miniconda2/bin/python
from __future__ import print_function
import sys
sys.path.append('./')
import mr_utils
import numpy as np
from numpy.linalg import norm

clusters = np.zeros((10, mr_utils.N_DIMENSION))
clusters_count = np.zeros(clusters.shape[0])
new_clusters = np.zeros_like(clusters)

with open(mr_utils.CLUSTERS_DIR, "r") as f:
	for line in mr_utils.get_line(f):
		idx, cluster, _ = line.split("\t")
		idx = int(idx)
		clusters[idx] = np.fromstring(cluster.strip("[]"), sep = ",")

count = 0
for line in mr_utils.get_line():
	count += 1
	point = np.fromstring(line.strip("[]"), sep = ",")
	dists = norm(clusters - point, axis = 1)

	idx = np.argmin(dists)
	new_clusters[idx] = (new_clusters[idx]*clusters_count[idx] + point)/(clusters_count[idx] + 1.0)
	clusters_count[idx] += 1

for i in range(new_clusters.shape[0]):
	print("%d\t%s\t%d"%(i, new_clusters[i].tolist(), clusters_count[i]))