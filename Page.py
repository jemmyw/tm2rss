import datetime
import logging
from google.appengine.ext import db
from google.appengine.api import urlfetch
from google.appengine.api import memcache

class Page(db.Model):
	date = db.DateTimeProperty(auto_now_add=True)
	content = db.TextProperty()
	url = db.StringProperty()
	
def fetch(url, timeout = 0):
	logging.debug('fetch: ' + url)
	
	data = memcache.get(url)
	if(data is not None): 
		return data
	else:
		if(timeout == 0):
			page = Page.gql('WHERE url = :1', url).get()
			if(page): return page.content	
	
		try:
			response = urlfetch.fetch(url)
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