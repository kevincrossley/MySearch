import json


def compute_ranks(graph):
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
					newrank = newrank + d * (ranks[node] / len(graph[node]))

			newranks[page] = newrank
		ranks = newranks
	return ranks


# Read in the graph 
with open('graph.txt') as gfile:
    	graph = json.load(gfile)

# Compute the rank of each page indexed (Page Rank algorithm)
ranks = compute_ranks(graph)

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