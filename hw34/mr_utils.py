import sys
import argparse

CLUSTERS_DIR = "clusters.txt"
HDKM_TRAINING_DIR = "hdkm_training.txt"
PCA_N_COMPONENTS = 25
N_DIMENSION = 28*28 if PCA_N_COMPONENTS is None else PCA_N_COMPONENTS

def get_line(file = sys.stdin):
	for line in file:
		line = line.strip()
		yield line