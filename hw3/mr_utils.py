import sys
import argparse

CLUSTERS_DIR = "clusters.txt"
HDKM_TRAINING_DIR = "hdkm_training.txt"
N_DIMENSION = 28*28

def get_line(file = sys.stdin):
	for line in file:
		line = line.strip()
		yield line