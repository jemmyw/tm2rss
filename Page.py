import logging
from google.appengine.ext import db
from google.appengine.api import urlfetch
from google.appengine.api import memcache

class Page(db.Model):
	date = db.DateTimeProperty(auto_now_add=True)
	content = db.TextProperty()
	url = db.StringProperty()
	
	rpcs = {}
	timeouts = {}
	urls = {}
	
def fetch(url, timeout = 0, async = False):
	logging.debug('fetch: ' + url)
	
	data = memcache.get(url)
	if(data is not None):
		logging.debug('fetched from memcached')
		return data
	else:
		if(timeout == 0):
			page = Page.gql('WHERE url = :1', url).get()
			if(page):
				logging.debug('fetched from db') 
				return page.content	
	
		try:
			rpc = urlfetch.create_rpc()
			urlfetch.make_fetch_call(rpc, url)
			
			Page.rpcs[url] = rpc
			Page.timeouts[url] = timeout
			
			if(async):
				return rpc
			else:
				return wait(url)

		except urlfetch.Error, e:
			return None
		
	return None
		
def wait(url):
	return store_result(url)
	
def store_result(url):
	if(url not in Page.rpcs): return None
	rpc = Page.rpcs[url]
	
	timeout = 0	
	if(url in Page.timeouts): timeout = Page.timeouts[url]

	try:
		response = rpc.get_result()	
		if(response.status_code == 200):
			result = unicode(response.content, 'utf-8')
				
			if(timeout == 0):
				memcache.add(url, result)
				page = Page(url=url, content=result)
				page.put()
			else:								
				memcache.add(url, result, timeout * 60)
				
			return result
	except urlfetch.Error, e:
		return None
	return None
	