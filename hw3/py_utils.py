import numpy as np
import random
import subprocess
import os

stdout_r, stderr_r = None, None
def redirect_HD_output(stdout = None, stderr = None):
	global stdout_r, stderr_r
	stdout_r, stderr_r = stdout, stderr

def initial_clusters(imgs, k = 10):
	clusters = np.zeros((k, imgs.shape[1]))
	chosen_idx = random.sample(range(imgs.shape[0]), k)
	for i in range(k):
		clusters[i, :] = imgs[chosen_idx[i], :]
	return clusters

def split_list(l, n_split):
	random.shuffle(l)
	prev_ptr = 0
	for i in range(n_split):
		n_data = len(l)//n_split + (i < len(l)%n_split)
		yield l[prev_ptr:(prev_ptr + n_data)]
		prev_ptr += n_data

def run_mr(mapper_script, reducer_script, input, output, extra_files = []):
	global stdout_r, stderr_r

	input = input.strip("/")
	output = output.strip("/")

	try:
		subprocess.check_call(["hdfs", "dfs", "-rmr", "-skipTrash", "./" + input, "./mr_output"], stdout = stdout_r, stderr = stderr_r)
	except subprocess.CalledProcessError:
		pass

	subprocess.check_call(["hdfs", "dfs", "-copyFromLocal", input, "./"], stdout = stdout_r, stderr = stderr_r)

	cmd = [
			"hadoop", "jar", "/usr/hdp/current/hadoop-mapreduce-client/hadoop-streaming.jar", 
			"-file", mapper_script, 
			"-file", reducer_script
		]

	for file in extra_files:
		cmd.append("-file")
		cmd.append(file)

	cmd = cmd + [
		"-mapper", "python %s"%mapper_script,
		"-reducer", "python %s"%reducer_script,
		"-input", "./" + input,
		"-output", "./mr_output"
	]

	subprocess.check_call(cmd, stdout = stdout_r, stderr = stderr_r)

	try:
		subprocess.check_call(["rm", "-f", output], stdout = stdout_r, stderr = stderr_r)
	except subprocess.CalledProcessError:
		pass

	subprocess.check_call(["hdfs", "dfs", "-copyToLocal", "./mr_output/part-00000"], stdout = stdout_r, stderr = stderr_r)
	FNULL.close()

def run_local(mapper_script, reducer_script, input, output):
	mapper_input = open(input, "r")
	mapper_output = open("tmp.txt", "w")
	mapper_status = subprocess.check_call(["python", mapper_script], stdin = mapper_input, stdout = mapper_output)
	mapper_input.close()
	mapper_output.close()

	reducer_input =  open("tmp.txt", "r")
	reducer_output = open(output, "w")
	reducer_status = subprocess.check_call(["python",  reducer_script], stdin = reducer_input, stdout = reducer_output)
	reducer_input.close()
	reducer_output.close()