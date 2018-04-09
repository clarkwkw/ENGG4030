import mr_utils
import mnist
import hw3_kmeans
from sklearn.decomposition import PCA

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("case", choices = ["train", "test"])
	parser.add_argument("--kernel", default = "mr", choices = ["local", "mr"])
	parser.add_argument("--n_iter", default = 15, type = int)
	parser.add_argument("--vote_proportion", default = 0.05, type = float)

	if args.case == "train":
		lbls, imgs = mnist.read("training")
		pca = PCA(n_components = mr_utils.PCA_N_COMPONENTS, copy = True)
		img = pca.fit_transform(imgs)
		np.save("pca.npy", pca.components_.T)
		mnist.save_img(pca.components_, "eigendigits.png")
		hw3_kmeans.q1a(args.kernel, n_iter = args.n_iter, train_lbl = lbls, train_img = imgs)
	else:
		lbls, imgs = mnist.read("testing")
		pca_components = np.load("pca.npy")
		imgs = np.matmul(imgs, pca_components)
		hw3_kmeans.q1b(vote_proportion = args.vote_proportion, test_lbl = lbls, test_img = imgs)
