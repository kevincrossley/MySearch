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
	while toCrawl and depth <= max_depth:
		page = toCrawl.pop()
		if page not in crawled and len(crawled) < max_pages:
			union(next_depth, get_all_links(get_page(page)))
			crawled.append(page)
		if not toCrawl:
			toCrawl, next_depth = next_depth, []
			depth = depth + 1

	return crawled

max_pages = 100
max_depth = 1
seed = input("Enter your crawler seed url:")
links = crawl_web(seed, max_pages, max_depth)
print_nice_list(links)

''' Example Seeds '''
# https://udacity.github.io/cs101x/index.html
# https://en.wikipedia.org/wiki/Main_Page
# https://www.google.com/






