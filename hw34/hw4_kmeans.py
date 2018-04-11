import mr_utils, py_utils
import mnist
import hw3_kmeans
import argparse
import numpy as np
from sklearn.decomposition import PCA
import os

def train(args, lbls = None, imgs = None):
	if lbls is None or imgs is None:
		lbls, imgs = mnist.read("training")
	pca = PCA(n_components = mr_utils.PCA_N_COMPONENTS, copy = True)
	imgs = pca.fit_transform(imgs)
	np.save("pca.npy", pca.components_.T)
	try:
		mnist.save_img(pca.components_, "eigendigits.png")
	except:
		print("Cannot export eigen digits image")
	hw3_kmeans.q1a(args.kernel, n_iter = args.n_iter, train_lbl = lbls, train_img = imgs)

def test(args, lbls = None, imgs = None):
	if lbls is None or imgs is None:
		lbls, imgs = mnist.read("testing")
	pca_components = np.load("pca.npy")
	imgs = np.matmul(imgs, pca_components)
	hw3_kmeans.q1b(vote_proportion = args.vote_proportion, test_lbl = lbls, test_img = imgs)

def valid(args):
	FNULL = open(os.devnull, "w")
	py_utils.redirect_HD_output(FNULL, FNULL)
	
	lbl1, img1 = mnist.read("training")
	lbl2, img2 = mnist.read("testing")
	lbl = np.concatenate((lbl1, lbl2), axis = 0)
	img = np.concatenate((img1, img2), axis = 0)
	splits = list(py_utils.split_list(range(lbl.shape[0]), args.n_fold))
	
	for i in range(args.n_fold):
		testing_split = splits[i]
		training_split = []
		for j in range(args.n_fold):
			if i != j:
				training_split += splits[j]

		training_lbl, training_img = lbl[training_split], img[training_split]
		testing_lbl, testing_img = lbl[testing_split], img[testing_split]
		print("Fold %d:"%(i + 1))
		train(args, training_lbl, training_img)
		test(args, testing_lbl, testing_img)

CASES = {
	"train": train,
	"test": test,
	"valid": valid
}
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("case", choices = ["train", "test", "valid"])
	parser.add_argument("--kernel", default = "mr", choices = ["local", "mr"])
	parser.add_argument("--n_iter", default = 15, type = int)
	parser.add_argument("--vote_proportion", default = 0.05, type = float)
	parser.add_argument("--n_fold", default = 5, type = int)

	args = parser.parse_args()
	CASES[args.case](args)