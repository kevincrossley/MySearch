from bs4 import BeautifulSoup
import time

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


def soup_crawl(page):
	soupLinks = []
	soup = BeautifulSoup(page, 'html.parser')

	for link in soup.find_all('a'):
	    soupLinks.append(link.get('href'))
	    
	return soupLinks


def crawl_web(seed, max_pages, max_depth):
	toCrawl = [seed]
	crawled = []
	next_depth = []
	depth = 0
	index = {}
	while toCrawl and depth <= max_depth:
		page = toCrawl.pop()
		if page not in crawled and len(crawled) < max_pages:
			content = get_page(page)
			add_page_to_index(index, page, content)
			union(next_depth, get_all_links(content))
			crawled.append(page)
		if not toCrawl:
			toCrawl, next_depth = next_depth, []
			depth = depth + 1

	return index


def record_user_click(index, keyword, url):
    urls = lookup(index, keyword)
    if urls:
        for entry in urls:
            if entry[0] == url:
                entry[1] = entry[1]+1


def add_to_index(index, keyword, url):
    # dictionary version - does not check for duplicate urls
    if keyword in index:
    	if url not in index[keyword]:
    		index[keyword].append(url)
    else:
    	index[keyword] = [url]

    # # old list version- checks for duplicate urls 
    # # format of index: [[keyword, [[url, count], [url, count],..]],...]
    # for entry in index:
    #     if entry[0] == keyword:
    #         for urls in entry[1]:
    #             if urls[0] == url:
    #                 return
    #         entry[1].append([url,0])
    #         return
    # # not found, add new keyword to index
    # index.append([keyword, [[url,0]]])


def lookup(index,keyword):
    if keyword in index:
    	return index[keyword]
    else:
    	return None


def add_page_to_index(index, url, content):
	words = content.split()
	# splitlist = [' ', '(', ')',':',';',',','.','!','?','"']
	# words = split_string(content, splitlist)
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
	return result, run_time


max_pages = 10
max_depth = 3
seed = "https://udacity.github.io/cs101x/index.html"
# seed = input("Enter your crawler seed url:")
database = crawl_web(seed, max_pages, max_depth)

result = lookup(database, 'I')
print_nice_list(result)

# Example Seeds
# https://udacity.github.io/cs101x/index.html
# https://en.wikipedia.org/wiki/Main_Page
# https://www.google.com/





