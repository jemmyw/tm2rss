from BeautifulSoup import BeautifulSoup
import Page
import TrademeItem
import os
import re
import urllib2
import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.ext import db

class MainPage(webapp.RequestHandler):
	def get(self):
		url = 'http://www.trademe.co.nz/Browse/CategoryAttributeSearchResults.aspx?keyval=1022858&from=fav&sort_order=expiry_desc&v=List&Y=0'
		result = Page.fetch(url, 5)
		
		if(result):		
			self.response.headers['Content-Type'] = 'application/rss+xml'
			items_rss = self.processResults(result)
			
			template_values = {
				'items_rss': items_rss
			}
			
			path = os.path.join(os.path.dirname(__file__), 'index.rss')
			self.response.out.write(template.render(path, template_values))
			
		else:
			self.response.headers['Content-Type'] = 'text/plain'
			self.response.out.write('Hello, webapp world!')
		
	def processResults(self, result):
		soup = BeautifulSoup(result)	
		items = soup.findAll('li', {"class": re.compile('.*listingCard.*')})
		items = map(self.processResult, items)
		
		return "\n".join(items)
		
	def processResult(self, item):
		titem = TrademeItem()
		titem.load_item(item)
		
		path = os.path.join(os.path.dirname(__file__), 'item_rss.rss')
		return template.render(path, {'item': titem})
		


application = webapp.WSGIApplication(
												[('/', MainPage)],
												debug=True)
												
def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()