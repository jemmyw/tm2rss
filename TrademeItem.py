import Page
import re
import os
import logging
from dateutil.parser import *
from dateutil.tz import *
from datetime import *
from BeautifulSoup import BeautifulSoup
from google.appengine.ext.webapp import template
from google.appengine.api import memcache

class TrademeItem:
	def __init__(self, html):
		self.title = ""
		self.link = ""
		self.image = ""
		self.description = ""
		self.date = None
		self.rss = None
		self.details = False
		self.html = html
		self.load()
		
	def load(self):
		logging.debug('load')

		title_link = self.html.find('a')
		image = self.html.find('img')
		
		self.title = title_link.string
		self.link = 'http://www.trademe.co.nz' + title_link['href']

		if(re.match('http', image['src'])):
			self.image = image['src']
		
		self.rss = memcache.get(self.memcache_key())
		if(self.rss is not None):
			self.details = True
		else:
			self.rss = self.to_rss()
		
	def load_details(self):
		self.process_details(Page.fetch(self.link, 0, False))	
			
	def process_details(self, result):
		if(self.details): return	
	
		soup = BeautifulSoup(result)
		desc = soup.find('div', id=re.compile('DetailsContentColumn'))
		del(desc['style'])
		del(desc['id'])
		self.description = desc.prettify()
        
		listed_at = soup.find('li',  id=re.compile('ListingTitle_titleTime'))
		if(listed_at):
			matches = re.search('Listed:\s*(.*)', listed_at.string)
			self.date = parse(matches.group(1))
			
		self.rss = self.to_rss()
		memcache.add(self.memcache_key(), self.rss)
		self.details = True
			
	def rss_date(self):
		return self.date.strftime('%a, %d %b %Y %H:%M:%S %z')
		
	def memcache_key(self):
		return self.link + '_item'
			
	def to_rss(self):
		template_variables = {'item': self}
		if(self.date): template_variables['date'] = self.rss_date()
	
		path = os.path.join(os.path.dirname(__file__), 'item_rss.rss')
		return template.render(path, template_variables)