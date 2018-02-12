import argparse
import re

# IDENTIFIER - HOSTNAME PAIRS
MACHINES = [
	("m", "master"), 
	("s1", "slave01"), 
	("s2", "slave02"), 
	("s3", "slave03")
]
HOSTNAMES = [m.lower() for _, m in MACHINES]
HOSTFILE_DIR = "/etc/hosts"

def parse_args():
	parser = argparse.ArgumentParser(description = "Modify the host file for easy access to the clusters")
	parser.add_argument("action", type = str, choices = ["update", "reset"])
	for identifer, hostname in MACHINES:
		parser.add_argument("address_%s"%identifer, type = str, nargs = "?", default = None, help = "IP address of %s"%hostname)
	args = parser.parse_args()

	host_map = None
	if args.action == "update":
		host_map = {}
		for identifier, hostname in MACHINES:
			address = args.__dict__["address_%s"%identifier]
			if address is None:
				raise argparse.ArgumentTypeError("Missing argument address_%s"%identifier)
			host_map[hostname] = address

	return args.action, host_map


def read_and_clean_hostfile():
	contents = []
	with open(HOSTFILE_DIR, "r") as f:
		for line in f.readlines():
			tokens = re.split(r"\s|\t", line)
			is_remove = False
			for token in tokens:
				if token.lower() in HOSTNAMES:
					is_remove = True
					break

			if not is_remove:
				contents.append(line.rstrip("\n"))
	return contents

def save_host_file(contents):
	try:
		with open(HOSTFILE_DIR, "w") as f:
			f.write("\n".join(contents) + "\n")
	except PermissionError:
		print("PermissionError: run me in sudo")
		exit(-1)

def update(contents, host_map):
	for hostname, address in host_map.items():
		contents.append("%s\t%s"%(address, hostname))
	return contents

if __name__ == "__main__":
	action, host_map = parse_args()
	contents = read_and_clean_hostfile()
	if action == "update":
		update(contents, host_map)
	save_host_file(contents)
