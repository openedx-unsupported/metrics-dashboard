"""
Gathers all author domains from the index in elasticsearch that stores information from 7 edX repositories
"""

import elasticsearch

def reverse(word):
    return word[::-1]

# ElasticSearch instance (url)
es = elasticsearch.Elasticsearch(['http://localhost:9200/'])

# Initialize the scroll
page = es.search(
    index = 'git_grimoirelab',
    scroll = '2m',
    search_type = 'query_then_fetch',
    size = 10000)

sid = page['_scroll_id']
scroll_size = page['hits']['total']

domain_output = set()

# Start scrolling
while (scroll_size > 0):
    print("Scrolling...")
    page = es.scroll(scroll_id = sid, scroll = '2m')
    # Update the scroll ID
    sid = page['_scroll_id']
    # Get the number of results that we returned in the last scroll
    scroll_size = len(page['hits']['hits'])
    print("scroll size: " + str(scroll_size))
    for elt in page['hits']['hits']:
        #print ("domain: %s \n" % elt)
        domain_output.add(reverse(str(elt['_source']['author_domain']))) #reverse so that you can sort by the ending of a domain

sorted_output = sorted(domain_output)

for index, elt in enumerate(sorted_output): #revert back to original string, but keep sorted order
    sorted_output[index] = reverse(elt)

for elt in sorted_output:
    print("%s\n" % elt)