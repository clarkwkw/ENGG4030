import sys
import mnist
import argparse
import mr_utils
import py_utils
import numpy as np
from numpy.linalg import norm

def q1a(kernel, n_iter = 15, train_lbl = None, train_img = None, **kwargs):
	if train_lbl is not None and train_img is not None:
		lbl, img = train_lbl, train_img
	else:
		lbl, img = mnist.read("training")
	
	# Generate initial cluster centroids
	clusters = py_utils.initial_clusters(img, 10)

	with open(mr_utils.CLUSTERS_DIR, "w") as f:
		for i in range(clusters.shape[0]):
			f.write("%d\t%s\t0\n"%(i, clusters[i].tolist()))

	# Convert training images to a text file
	mnist.to_txt((lbl, img), mr_utils.HDKM_TRAINING_DIR)

	for i in range(n_iter):
		print("Running #%d.."%(i+1))
		if kernel == "local":
			py_utils.run_local("kmeans_mapper.py", "kmeans_reducer.py", mr_utils.HDKM_TRAINING_DIR, mr_utils.CLUSTERS_DIR)
		else:
			py_utils.run_mr(
				"kmeans_mapper.py", 
				"kmeans_reducer.py",
				input = mr_utils.HDKM_TRAINING_DIR,
				output = mr_utils.CLUSTERS_DIR,
				extra_files = ["mr_utils.py", mr_utils.CLUSTERS_DIR]
			)

def q1b(vote_proportion, test_lbl = None, test_img = None, **kwargs):
	clusters = np.zeros((10, mr_utils.N_DIMENSION))
	majority = np.zeros(10, dtype = np.int32)
	cluster_members = {i: [] for i in range(10)}
	cluster_members_dist = np.zeros((10, 10), dtype = np.int32)
	cluster_test_dist = np.zeros((10, 10), dtype = np.int32)

	# Load clustering result
	with open(mr_utils.CLUSTERS_DIR, "r") as f:
		for line in mr_utils.get_line(f):
			idx, cluster, _ = line.split("\t")
			idx = int(idx)
			clusters[idx] = np.fromstring(cluster.strip("[]"), sep = ",")
	
	if test_lbl is not None and test_img is not None:
		lbls, imgs = test_lbl, test_img
	else:
		lbls, imgs = mnist.read("testing")
	
	# Calculate distance between each images and each centroid
	# Assign the training image to the nearest centroid
	for i in range(imgs.shape[0]):
		lbl, img = lbls[i], imgs[i]
		
		dists = norm(clusters - img, axis = 1)
		idx = np.argmin(dists)
		cluster_members[idx].append((dists[idx], lbl))
		cluster_test_dist[idx, lbl] += 1

	# Output summary statistics for each cluster
	correct = 0
	for idx in range(10):
		cluster_members[idx] = sorted(cluster_members[idx], key = lambda x: x[0])
		n_points = min(int(len(cluster_members[idx])*vote_proportion) + 1, len(cluster_members[idx]))
		for _, lbl in cluster_members[idx][0:n_points]:
			cluster_members_dist[idx, lbl] += 1
		majority[idx] = np.argmax(cluster_members_dist[idx, :])
		correct += cluster_test_dist[idx, majority[idx]]
		
		print("Cluster %d:"%idx)
		print("\t#imgs in cluster: %d"%(len(cluster_members[idx])))
		print("\t#imgs in consideration: %d"%(n_points))
		print("\tmajority label: %d"%(majority[idx]))
		print("\t#correct images: %d"%cluster_test_dist[idx, majority[idx]])
		print("\taccuracy: %.2f%%"%(100.0*cluster_test_dist[idx, majority[idx]]/cluster_test_dist[idx, :].sum()))

	print("overall: %.2f%%"%(100.0*correct/cluster_test_dist.sum()))

def q1c(kernel, vote_proportion, n_iter, n_fold, **kwargs):
	lbl1, img1 = mnist.read("training")
	lbl2, img2 = mnist.read("testing")
	lbl = np.concatenate((lbl1, lbl2), axis = 0)
	img = np.concatenate((img1, img2), axis = 0)
	splits = list(py_utils.split_list(range(lbl.shape[0]), n_fold))
	
	for i in range(n_fold):
		testing_split = splits[i]
		training_split = []
		for j in range(n_fold):
			if i != j:
				training_split += splits[j]

		training_lbl, training_img = lbl[training_split], img[training_split]
		testing_lbl, testing_img = lbl[testing_split], img[testing_split]
		print("Fold %d:"%(i + 1))
		q1a(kernel, n_iter, training_lbl, training_img)
		q1b(vote_proportion, testing_lbl, testing_img)

CASES = {
	"q1a": q1a,
	"q1b": q1b,
	"q1c": q1c
}

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("case", choices = list(CASES.keys()))
	parser.add_argument("--kernel", default = "mr", choices = ["local", "mr"])
	parser.add_argument("--n_iter", default = 15, type = int)
	parser.add_argument("--vote_proportion", default = 0.05, type = float)
	parser.add_argument("--n_fold", default = 5, type = int)
	

	args = parser.parse_args()
	CASES[args.case](kernel = args.kernel, vote_proportion = args.vote_proportion, n_iter = args.n_iter, n_fold = args.n_fold)