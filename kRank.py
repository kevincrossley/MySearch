import json


def compute_ranks(graph, k):
	d = 0.8 # damping factor - propability of selecting link on current page or randomly jumping
	numloops = 10 # number of iterations
	
	ranks = {}
	npages = len(graph)
	for page in graph:
		ranks[page] = 1.0 / npages
	
	for i in range(0, numloops):
		newranks = {}
		for page in graph:
			newrank = (1 - d) / npages
			
			for node in graph:
				if page in graph[node]:
					# next line is about reciprocal links
					# line below if statement is indented when if statement active
					if not is_reciprocal_link(graph, node, page, k):
						newrank = newrank + d * (ranks[node] / len(graph[node]))

			newranks[page] = newrank
		ranks = newranks
	return ranks


def is_reciprocal_link(graph, source, destination, k):
	if k == 0:
		if destination == source:
			return True
		return False
	if source in graph[destination]:
		return True
	for node in graph[destination]:
		if is_reciprocal_link(graph, source, node, k - 1):
			return True
	return False

# Read in the graph 
with open('graph.txt') as gfile:
    	graph = json.load(gfile)

# Compute the rank of each page indexed (Page Rank algorithm)
k = 0 # threshold for reciprocal link calculation. setting to zero should only include links to itself
ranks = compute_ranks(graph, k)

# Write to ranks output file
# 	should probably also adapt this to append newly indexed pages 
#	potentially to be done in the compute_ranks function??
with open('rank.txt', 'w') as rfile:
	json.dump(ranks, rfile)


# # file-append.py
# f = open('helloworld.txt','a')
# f.write('\n' + 'hello world')
# f.close()

# Close files
rfile.close()
gfile.close()