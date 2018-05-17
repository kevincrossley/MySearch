import json


def lookup(index,keyword):
    if keyword in index:
    	return index[keyword]
    else:
    	return None


def lucky_search(index, ranks, keyword):
	pages  = lookup(index, keyword)
	if not pages:
		return None
	best_page = pages[0]
	for candidate in pages:
		if ranks[candidate] > ranks[best_page]:
			best_page = candidate
	return best_page


def ordered_search(index, ranks, keyword):
	# using quicksort algorithm
	pages = lookup(index, keyword)
	return quicksort_pages(pages, ranks)


def quicksort_pages(pages, ranks):
	if not pages or len(pages) <= 1:
		return pages
	else:
		pivot = ranks[pages[0]] # find pivot point
		worse = []
		better = []
		for page in pages[1:]: # note: starting at 1 bc used 0 as pivot point, so its already accounted for
			if ranks[page] <= pivot:
				worse.append(page)
			else:
				better.append(page)
		return quicksort_pages(better, ranks) + [pages[0]] + quicksort_pages(worse, ranks)


# Read in index.txt and rank.txt

# ifile = open('index.txt','r')
# rfile = open('rank.txt','r')
# index = ifile.read()
# ranks = rfile.read()

with open('index.txt') as ifile:
    	index = json.load(ifile)
with open('rank.txt') as rfile:
    	ranks = json.load(rfile)

# assign searchterm
searchterm = 'Kevin'
# searchterm = input("Enter your search term:")

# Execute a search for a keyword and see ranked list of pages with that term
result = ordered_search(index, ranks, searchterm)

if result == None:
	result = None
else:
	lucky = result[0] # could also call lucky_search if all you want is top option

print result

# Close Files
ifile.close()
rfile.close()


