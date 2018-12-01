#!/usr/bin/env python3.7

import csv
import re
import os
import sys
import pdb
import subprocess

def extract_data(device, location):

	# take Location and go back 200 bytes to grab relevant data.
	location -= 200

	# generate strings we will be sending to DD
	if_str = 'if=%s' % device
	skip_str = 'skip=%s' % location

	# Pipe output to HexDump for readability.
	cmd = "dd %s bs=1 count=500 %s | hd" % (if_str, skip_str)

	# Run , put stderror on STDOUT as DD doesn't output to STDOUT.
	ps = subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	
	# Grab output and put in file.
	output = ps.communicate()[0]

	if not os.path.exists('output'):
		os.makedirs('output')

	# create files named after their location. Don't forget to subtract 200 ;)
	f = open("output/" + str(location + 200) + ".txt", "a")
	f.write(output)
	f.close()

# Open Bulk Extractor CCN results file.
f = open("ccn.txt")

# Create  dictionary for holding lines.
lines = {}

# Loop through the lines , and add to dictionary. Enumerating for organization.
for counter, content in enumerate(f.readlines()):
	lines.update({counter : content})

# Grab our device / filename.
device = lines[3].replace('# Filename: ', '').strip()

i = 5
locations = []

#  Loop through the lines, split , and pull first index. Assign to seperate list of data locations.
while i < ( len(lines) - i ):
	locations.append(lines[i].split()[0])
	i += 1

for location in locations:
	extract_data(device, int(location))

