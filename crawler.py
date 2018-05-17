import time
import json
from bs4 import BeautifulSoup

def get_page(url): 
	try: 
		import urllib 
		return urllib.urlopen(url).read() 
	except: 
		return ''


def gen_next_target(page):
	start_link = page.find('<a href=')

	if start_link == -1:
		return None, 0

	else:
		start_quote = page.find('"',start_link)
		end_quote = page.find('"',start_quote + 1)
		url = page[start_quote + 1 : end_quote]
		return url, end_quote


def get_all_links(page):
	links = []
	while True:
		url, endpos = gen_next_target(page)
		if url:
			links.append(url)
			page = page[endpos:]
		else:
			break
	return links


def union(p,q):
    for e in q:
        if e not in p:
            p.append(e)


def print_nice_list(p):
	i = 0
	print '\n************ Start of List ************\n' 
	
	while i < len(p):
		print p[i]
		i = i + 1

	print '\n************  End of List  ************\n'


def crawl_web(seed, max_pages, max_depth):
	toCrawl = [seed]
	crawled = []
	next_depth = []
	depth = 0
	index = {}
	graph = {}
	while toCrawl and depth <= max_depth:
		page = toCrawl.pop()
		if page not in crawled and len(crawled) < max_pages:
			content = get_page(page)
			add_page_to_index(index, page, content)
			outlinks = get_all_links(content)
			graph[page] = outlinks
			union(next_depth, outlinks)
			crawled.append(page)
		if not toCrawl:
			toCrawl, next_depth = next_depth, []
			depth = depth + 1

	return index, graph

'''
def record_user_click(index, keyword, url):
    urls = lookup(index, keyword)
    if urls:
        for entry in urls:
            if entry[0] == url:
                entry[1] = entry[1]+1


def soup_crawl(page):
	soupLinks = []
	soup = BeautifulSoup(page, 'html.parser')

	for link in soup.find_all('a'):
	    soupLinks.append(link.get('href'))
    return soupLinks
'''

def add_to_index(index, keyword, url):
    # dictionary version - does not check for duplicate urls
    if keyword in index:
    	if url not in index[keyword]: 
    		# comment out the above if statement to include duplicate entries
    		index[keyword].append(url)
    else:
    	index[keyword] = [url]


def add_page_to_index(index, url, content):
	# words = content.split()
	splitlist = [' ', '(', ')',':',';',',','.','!','?','"','<','>']
	words = split_string(content, splitlist)
	for word in words:
		add_to_index(index, word, url)


def split_string(source, splitlist):
	output = []
	atsplit = True
	for char in source:
		if char in splitlist:
			atsplit = True
		else:
			if atsplit:
				output.append(char)
				atsplit = False
			else:
				output[-1] = output[-1] + char
	return output


def stopwatch(code):
	start = time.clock()
	result = eval(code)
	run_time = time.clock() - start
	return run_time


max_pages = 10
max_depth = 3
seed = "https://udacity.github.io/cs101x/urank/"
# seed = input("Enter your crawler seed url:")

# Example Seeds
# https://udacity.github.io/cs101x/index.html
# https://en.wikipedia.org/wiki/Main_Page
# https://www.google.com/
# https://udacity.github.io/cs101x/urank/
# https://www.udacity.com/cs101x/urank/index.html

# Crawl Web to create an index of all content on page
# 	and a graph documenting connections of links
index, graph = crawl_web(seed, max_pages, max_depth)

# Write index and graph to output files
# 	for now, overwrite every time
# 	should append unless already indexed
# 	probably can incoporate read/write to file inside crawl_web function

# Write to file using json
with open('index.txt', 'w') as ifile:
	json.dump(index, ifile)
with open('graph.txt', 'w') as gfile:
	json.dump(graph, gfile)


# # file-append.py
# f = open('helloworld.txt','a')
# f.write('\n' + 'hello world')
# f.close()

# Close files 
ifile.close()
gfile.close()


