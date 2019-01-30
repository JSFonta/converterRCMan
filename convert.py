#!/usr/bin/python

# Ensure that your YAML file use 2 white spaces or 1 tab for each indent. Do not mix tab and white space

import sys, re

# Define classes

# All items created by this script is based on the Entity class
# Each entity has its own and unique id, whatever the final type
class Entity:
	id = 1
	def __init__(self, name, parent):
		self.id 	= Entity.id
		self.name 	= name
		self.parent	= parent
		Entity.id 	+= 1

# Leaves of the tree, inheritance of Entity
class Server(Entity):
	def __init__(self, name, parent, ip, protocol):
		Entity.__init__(self, name, parent)
		self.ip 		= ip
		self.protocol	= protocol



# Verify that basics looks okay
if len(sys.argv) != 3:
	print("Need path to the YAML file to parse.")
	print("python convert.py --path PATH/TO/THE/YAML/FILE.yaml")
	sys.exit(0)


# Regular expression used after to define if it is category or server
regexCategory = re.compile(r"^([\s\t]*)(\w{1,}):$")
regexServer = re.compile(r"^[\t\s]*-[\s\t]*(\w{1,})[\s\t](\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})[\s\t]([sS][sS][hH]|[rR][dD][pP])$")

# Read only the file in text based mode
# Aim is to create linked and defined objects
file = open(sys.argv[2], "rt")

for line in file:

	# Category case
	if regexCategory.match(line):
		print(regexCategory.search(line).groups())

	# Server case
	if regexServer.match(line):
		print(regexServer.search(line).groups())