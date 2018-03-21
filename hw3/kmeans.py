import sys
import mnist
import argparse
import mr_utils
import py_utils

def q1a(kernel, n_iter = 15):
	lbl, img = mnist.read("training")
	clusters = py_utils.initial_clusters(img, 10)

	with open(mr_utils.CLUSTERS_DIR, "w") as f:
		for i in range(clusters.shape[0]):
			f.write("%d\t%s\t0\n"%(i, clusters[i].tolist()))

	mnist.to_txt((lbl, img), mr_utils.HDKM_TRAINING_DIR)

	for i in range(n_iter):
		print("Running #%d.."%i)
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

CASES = {
	"q1a": q1a
}

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("case", choices = list(CASES.keys()))
	parser.add_argument("kernel", choices = ["local", "mr"])
	args = parser.parse_args()
	CASES[args.case](kernel = args.kernel)