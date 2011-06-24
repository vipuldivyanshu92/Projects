# All math functions return the square of the distance to avoid float values and then speed up the code processing

def math_h(i):		 # Return the Euclidean distance from node I to the goal Node
	return (pos_goal[0]-i[0])**2+((pos_goal[1]-i[1])**2)
	
def math_g(i):		  # Return the real length used to go come to the current point
	return len(GetReversePath(l_close[i]["parent"]))**2

def GetLowestF():
	lowest = None
	for i in l_open.keys():
		v = l_open[i]["F"]
		if lowest == None or l_open[lowest]["F"] > v:
			lowest = i
	return lowest
						
	
def GetAdjacentNodes(i):		# Return adjacent Nodes of Node i, diagonal are ignored here
	nodes = []
	if i[0]-1 >=  0:
		nodes += [(i[0]-1, i[1])]
	if i[0]+1 <=  map_height:
		nodes += [(i[0]+1, i[1])]
	if i[1]-1 >= 0:
		nodes += [(i[0], i[1]-1)]
	if i[1]+1 <= map_width:
		nodes += [(i[0], i[1]+1)]
	return nodes

def GetReversePath(i):		  # Return the path from one point to another using the parents of closed list
	path = []
	v = i
	while v != None:
		path += [v]
		v = l_close[v]["parent"]
	return path

def GetPath(i):				 # Return the path in the correct way
	path = GetReversePath(i)
	path.reverse()
	return path

# Map
map = [
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0],
[1,1,1,1,1,1,1,1,0,1,1,0,1,1,0,1,1,1,1,1,1,1,1,0,1,1,0,1,1,0,1,1,1,1,1,1,1,1],
[1,1,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,1,1],
[1,1,0,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,1,1],
[1,1,0,0,0,0,1,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,1,1,0,0,0,0,1,1],
[1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0,1,1,1,1,1,0,1,1,0,1,1,1,1,1],
[0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0],
[0,0,0,1,1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,1,0,0,0],
[0,0,0,1,1,0,1,1,1,1,1,0,1,1,0,0,0,0,0,0,0,0,0,0,1,1,0,1,1,1,1,1,0,1,1,0,0,0],
[1,1,1,1,1,0,1,1,1,1,1,0,1,1,0,1,1,1,0,0,1,1,1,0,1,1,0,1,1,1,1,1,0,1,1,1,1,1],
[1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
[1,1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,1],
[1,1,0,1,1,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,1,0,1,1],
[1,1,0,1,1,0,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,1,1,0,1,1],
[1,1,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,1,1],
[1,1,0,1,1,0,1,1,1,1,1,0,1,1,0,1,1,0,1,1,0,1,1,0,1,1,0,1,1,1,1,1,0,1,1,0,1,1],
[1,1,0,1,1,0,0,0,0,0,0,0,1,1,0,1,1,0,0,0,0,1,1,0,1,1,0,0,0,0,0,0,0,1,1,0,1,1],
[1,1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,1],
[1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
[1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1],
[0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

map_width = len(map[0])-1
map_height = len(map)-1

pos_start = (1, 0)
pos_goal = (21, 4)

l_open = {}			 # Create a dictionnary for open list
l_close = {}			# Create a dictionnary for closed list

# Format of the lists:
# {
#	   (posx, posy) : {"parent" : (posx, posy), "H" : math_h(), "G" : math_g(), "F" : math_g()+math_h()}
#		...  
# }

# Add start Node to the Open List:
tmp_h = math_h(pos_start)
l_open[pos_start] = {"parent" : None, "H" : tmp_h, "G" : 0, "F" : tmp_h}

while len(l_open) > 0:
	current_node = GetLowestF()						 # Find the Node with the lowest F
	#print "Current node :", current_node
	l_close[current_node] = l_open[current_node]		# Copy this Node into the closed list
	del l_open[current_node]							# Delete it from the open list
	if current_node == pos_goal:						# If we have added to goal position to the close list we have finished
		break									   # Leave the loop

	AdjacentNodes = GetAdjacentNodes(current_node)	  # Get a list of the adjacent nodes
	for n in AdjacentNodes:							 # for each of this nodes
		if (l_close.has_key(n)) or (map[n[0]][n[1]] == 1):	  # If this case is in closed list or a barrier
			pass										 	# Ignore it
		else:
			if not l_open.has_key(n):						# If current node is not on the open list
				tmp_h = math_h(n)
				tmp_g = math_g(current_node)
				tmp_f = tmp_h + tmp_g
				l_open[n] = {"parent" : current_node, "H" : tmp_h, "G" : tmp_g, "F" : tmp_f} # Add it to the open list
			else:
				# If node is already on the open list
				# Check if the new G is less than the current one
				# if It is change the parent to the current node
				# Recalculate G and then F
				tmp_g = math_g(current_node)
				if tmp_g < l_open[n]["G"]:
					l_open[n]["parent"] = current_node
					l_open[n]["G"] = tmp_g
					l_open[n]["F"] = l_open[n]["H"] + tmp_g

print GetReversePath(pos_goal)
print
print GetPath(pos_goal)

raw_input()
