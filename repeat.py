from __future__ import print_function
import argparse
from os.path import basename
import os
import subprocess
import sys

# Place under hadoop root directory

HD_INPUT_DIR = "/medium_stage_1_output"
HD_OUTPUT_DIR = "/medium_stage_2_output"
LOG_NAME = "trial_%d.txt"
MAPPER_DIR = "/home/clarkwkw/ENGG4030/hw1/stage2_mapper.py"
REDUCER_DIR = "/home/clarkwkw/ENGG4030/hw1/stage2_reducer.py"

def get_job_cmd(nmapper, nreducer):
	cmd = [
		"./bin/hadoop",
		"jar" ,
		"./share/hadoop/tools/lib/hadoop-streaming-2.7.5.jar"
	]

	if nmapper is not None:
		cmd.extend([
			"-D", "mapred.map.tasks=%d"%nmapper
		])

	if nreducer is not None:
		cmd.extend([
			"-D", "mapred.reduce.tasks=%d"%nreducer
		])

	mapper_name = basename(MAPPER_DIR)
	reducer_name = basename(REDUCER_DIR)
	cmd.extend([
		"-file", MAPPER_DIR,
		"-mapper", mapper_name,
		"-file", REDUCER_DIR,
		"-reducer", reducer_name,
		"-input", HD_INPUT_DIR,
		"-output", HD_OUTPUT_DIR
	])
	return cmd

def get_clean_up_cmd():
	return ["./bin/hadoop", "fs", "-rmr", "-skipTrash", HD_OUTPUT_DIR]

parser = argparse.ArgumentParser()
parser.add_argument("niter", type = int)
parser.add_argument("--mapper", type = int, default = None, help = "no. of mappers to invoke")
parser.add_argument("--reducer", type = int, default = None, help = "no. of reducers to invoke")
parser.add_argument("--ignore_err", action = "store_true", help = "if set to True, the job will be triggered for 'niter' times regardless of its exit status")
parser.add_argument("--clean", action = "store_true", help = "if set to True, an additional cleanup command will be triggered before the first iteration")

args = parser.parse_args()

try:
	if args.clean:
		print("extra cleaning..")
		FNULL = open(os.devnull, 'w')
		subprocess.call(get_clean_up_cmd(), stdout = FNULL, stderr = FNULL.fileno())
		FNULL.close()

	for i in range(args.niter):
		print("#%d running..."%(i+1), end = "")
		sys.stdout.flush()
		with open(LOG_NAME%(i+1), "w") as f:
			status = subprocess.call(get_job_cmd(args.mapper, args.reducer), stdout = f, stderr = f.fileno())

			if status != 0:
				print("[ERR(%d)]"%status)
				if not args.ignore_err:
					exit(status)
			else:
				print("[OK]")

			subprocess.call(get_clean_up_cmd(), stdout = f, stderr = f.fileno())
except OSError:
	print("\nCannot locate hadoop executable, please check configuration")