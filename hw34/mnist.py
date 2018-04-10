import os
import struct
import numpy as np
import math

"""
Adopted from: https://gist.github.com/akesling/5358964 (GPL licensed)
"""

def read(dataset = "training", path = "."):
    """
    Python function for importing the MNIST data set.  It returns an iterator
    of 2-tuples with the first element being the label and the second element
    being a numpy.uint8 2D array of pixel data for the given image.
    """

    if dataset is "training":
        fname_img = os.path.join(path, 'train-images-idx3-ubyte')
        fname_lbl = os.path.join(path, 'train-labels-idx1-ubyte')
    elif dataset is "testing":
        fname_img = os.path.join(path, 't10k-images-idx3-ubyte')
        fname_lbl = os.path.join(path, 't10k-labels-idx1-ubyte')
    else:
        raise ValueError("dataset must be 'testing' or 'training'")

    # Load everything in some numpy arrays
    with open(fname_lbl, 'rb') as flbl:
        magic, num = struct.unpack(">II", flbl.read(8))
        lbl = np.fromfile(flbl, dtype=np.int8)

    with open(fname_img, 'rb') as fimg:
        magic, num, rows, cols = struct.unpack(">IIII", fimg.read(16))
        img = np.fromfile(fimg, dtype=np.uint8).reshape(len(lbl), rows * cols)

    return lbl, img

VALID_FORMATS = ["vect"]
def to_txt(collection, filename, format = "vect"):
    if format not in VALID_FORMATS:
        raise Exception("Invalid format '%s'"%format)
    
    if type(collection) is not list:
        collection = [collection]

    f = open(filename, "w")
    count = 0
    for lbls, imgs in collection:
        for i in range(imgs.shape[0]):
            if count > 0:
                f.write("\n")
            f.write("%s"%(imgs[i].tolist()))
            count += 1
    f.close()

def save_img(images, filename):
    """
    Render a given numpy.uint8 2D array of pixel data.
    """
    from matplotlib import pyplot
    import matplotlib as mpl
    fig = pyplot.figure()
    images = images.reshape((-1, 28, 28))
    n_row, n_col = int(math.sqrt(images.shape[0])), int(math.sqrt(images.shape[0]))
    if images.shape[0] > n_row * n_col:
    	n_row += 1

    for i in range(images.shape[0]):
	    ax = fig.add_subplot(n_row, n_col, i + 1)
	    imgplot = ax.imshow(images[i], cmap=mpl.cm.Greys)
	    ax.set_xticklabels([])
	    ax.set_yticklabels([])
	    #imgplot.set_interpolation('nearest')
	    #ax.xaxis.set_ticks_position('top')
	    #ax.yaxis.set_ticks_position('left')

    fig.savefig(filename)
    pyplot.clf()
    pyplot.close(fig)