import elasticsearch

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
        #print ("domain: %s \n" % elt['_source']['author_domain'])
        domain_output.add(elt['_source']['author_domain'])

for elt in domain_output:
    print("%s \n" % elt)

print(len(domain_output))