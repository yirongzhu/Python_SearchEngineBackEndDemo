import random


# This is the cache we get. There are a lot of urls and the corresponding web pages. We get one random of them. 
# Get the cache in the key value pairs here. The keys are urls, the values are the html web pages corresponding to it.
cache = {
   
}



def get_page(url):
    if url in cache:
        return cache[url]
    return ""



def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote



def get_all_links(page):
    links = []
    while True:
        url, endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links



def union(a, b):
    for e in b:
        if e not in a:
            a.append(e)
            
            
            
def add_page_to_index(index, url, content):
    words = content.split()
    for word in words:
        add_to_index(index, word, url)
        
        

def add_to_index(index, keyword, url):
    if keyword in index:
        index[keyword].append(url)
    else:
        index[keyword] = [url]



def lookup(index, keyword):
    if keyword in index:
        return index[keyword]
    else:
        return None



# Use BFS to construct the whole index in the hashmap and get a graph of outlinks for implementing the pagerank algorithm
def crawl_web(seed): # returns index, graph of inlinks
    tocrawl = [seed]
    crawled = []
    graph = {}  # <url>, [list of pages it links to]
    index = {}
    while tocrawl:
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page(page)
            add_page_to_index(index, page, content)
            outlinks = get_all_links(content)
            graph[page] = outlinks
            union(tocrawl, outlinks)
            crawled.append(page)
    return index, graph



# Based on Rank = 1 / n * (1 - d) + d * sum(Rank[inlinks] / num of inlinks), then loop to update for a lot of times and the ranking becomes more accurate. 
def compute_ranks(graph):
    d = 0.8 # damping factor
    numloops = 10

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



def quicksort(l):
    if len(l) == 0 or len(l) == 1:
        return l
    else:
        pivot = l.pop( random.randint( 0, len(l)-1 ) )
        left = []
        right = []
        for e in l:
            if e <= pivot:
                right.append(e)
            else:
                left.append(e)
        return quicksort(left) + [pivot] + quicksort(right)
    
    

# Get the ordered search result from the pagerank and the index. 
def ordered_search(index, ranks, keyword):
    if keyword in index:
        urllist = index[keyword]
        ranklist = []
        for url in urllist:
            ranklist.append(ranks[url])
        newranklist = quicksort(ranklist)
        finlist = []
        for val in newranklist:
            for e in urllist:
                if ranks[e] == val:
                    finlist.append(e)
        return finlist
    else:
        return None
    
    

index, graph = crawl_web('')
ranks = compute_ranks(graph)

print ordered_search(index, ranks, 'Keyword')