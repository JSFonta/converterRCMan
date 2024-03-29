#!/usr/bin/python

# Ensure that your YAML file use 2 white spaces for each indent. Do not mix tab and white space
# Developped by JSFonta (https://github.com/JSFonta), 2019
# This tool is designed for RCMan (https://github.com/nikolayarhangelov/rcman)
# The aim is to convert a simple and easy readable YAML file to a json which works into RCMan as configuration

import sys, re

# Define classes

# All items created by this script is based on the Entity class
# Each entity has its own and unique id, whatever the final type
class Entity:
	id = 1
	def __init__(self, name, parent):
		self.id 		= Entity.id
		self.name 		= name
		self.parent		= parent
		self.children 	= []
		Entity.id 	   += 1

# Leaves of the tree, inheritance of Entity
class Server(Entity):
	def __init__(self, name, parent, conn, protocol):
		Entity.__init__(self, name, parent)
		self.conn 		= conn
		self.protocol	= protocol
		# Keep 2 ID for each server
		Entity.id 	   += 1





# This method determine the depth of an YAML object : 2 white spaces = 1 depth
def depthOf(expression):
	return(int(len(expression)/2))

# Hydrate all items with children
def hydrateAllChildren(items):

	for item in items:
		for ite in items:

			if ite.parent == item:

				item.children.append(ite)


# Convert recursively the whole objects tree to a json file
# Must start with the tree's root
def jsonify(item):

	# Display all the JSON, with right parameters
	returnValue 	= "{\n"
	if len(item.children) == 0 :
		returnValue    += "\"$id\": \""+str(item.id)+"\",\n"
		returnValue    += "\"DisplayName\": \""+item.name+"\",\n"
		returnValue    += "\"IsExpanded\": false,\n"
		if isinstance(item, Server) :
			returnValue+= "\"ConnectionSettings\": {\n"
			returnValue+= "\"$id\": \""+str(item.id+1)+"\",\n"
			returnValue+= "\"Protocol\": \""+item.protocol+"\",\n"
			returnValue+= "\"Server\": \""+item.conn+"\"\n"
			returnValue+= "},\n"
			returnValue+= "\"Items\": []\n"
		returnValue    += "}"

		return returnValue

	returnValue    += "\"$id\": \""+str(item.id)+"\",\n"
	returnValue    += "\"DisplayName\": \""+item.name+"\",\n"
	returnValue    += "\"IsExpanded\": false,\n"
	returnValue    += "\"Items\": [\n"

	# Avoid coma after the last children
	count = 0
	for child in item.children:

		# Call the same function for every children
		returnValue += jsonify(child)
		count += 1
		if count < len(item.children):  
			returnValue += ","

	returnValue    += "]\n}\n"

	return returnValue

####################################
# Welcome into the main program :) #
####################################

# Verify that basics looks okay
if len(sys.argv) != 3:
	print("Need path to the YAML file to parse.")
	print("python convert.py --path PATH/TO/THE/YAML/FILE.yaml")
	sys.exit(-1)

# Regular expression used after to define if it is category or server
regexCategory = re.compile(r"^[\s\t]*([\w\d\-]{1,}):$")
regexServer = re.compile(r"^[\t\s]*-[\s\t]*([\w\-+_\.\d]{1,})[\s\t](.+)[\s\t]([sS][sS][hH]|[rR][dD][pP])$")
regexDepth = re.compile(r"^(\s{0,}).*$")

# Read only the file in text based mode
# Aim is to create linked and defined objects
try:
	file = open(sys.argv[2], "rt")
except Exception as e:
	print(e)
	sys.exit(-1)

# Init the tree
root 			= Entity("root", "no")
previousElem 	= root
previousDepth 	= -1

allItems = []

# Read line by line until the EOF
for line in file:

	# Category case
	if regexCategory.match(line):
		# Catch category information
		rawCategory = regexCategory.search(line).groups()
		e = Entity(rawCategory[0], root)

	# Server case
	if regexServer.match(line):
		rawServer = regexServer.search(line).groups()
		e = Server(rawServer[0], root, rawServer[1], rawServer[2])

	# Keep in memory the whole list
	allItems.append(e)

	# Compute the depth
	depth = depthOf(regexDepth.search(line).groups()[0])

	if depth == previousDepth:
		# Same parent
		e.parent = previousElem.parent

	elif depth < previousDepth:
		# Shallower
		# Find the right parent
		i = previousDepth - depth + 1
		lastParent = previousElem
		while i != 0 and lastParent != root:
			lastParent = lastParent.parent
			i -= 1
		e.parent = lastParent

	else:
		# Deeper
		e.parent = previousElem

	# Update for next line
	previousElem = e
	previousDepth = depth

file.close()

allItems.insert(0, root)

# Now, construct the output, JSON file
hydrateAllChildren(allItems)

output = jsonify(root)

# Create or just write into the file if it already exists
try:
	file = open("connections.json", "w")
	file.write(output)
	file.close()
except Exception as e:
	print("Cant write the output file, let's print it !")
	print(e)
	print("--------------")
	print(output)