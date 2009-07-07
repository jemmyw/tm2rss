import datetime
import logging
from google.appengine.ext import db
from google.appengine.api import urlfetch

class Page(db.Model):
	date = db.DateTimeProperty(auto_now_add=True)
	content = db.TextProperty()
	url = db.StringProperty()
	
def fetch(url, timeout = 60):
	logging.debug('fetch: ' + url)
	cached = Page.gql('WHERE url = :1', url).get()

	if(cached):
		if(cached.date < datetime.datetime.now() - datetime.timedelta(minutes = timeout)):
			logging.debug('fetch cache expired')
			cached.delete()
		else:	
			logging.debug('fetch from cache')
			return cached.content
	
	try:
		response = urlfetch.fetch(url)
		if(response.status_code == 200):
			result = unicode(response.content, 'utf-8')
			cached = Page()
			cached.url = url
			cached.content = result			
			cached.put()
			return response.content
	except urlfetch.Error, e:
		return None
		
	return None