#!/usr/bin/python

import sys

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


# Read only the file in text based mode
# 
f = open("config.yaml", "rt")
for x in f:
  print(x)