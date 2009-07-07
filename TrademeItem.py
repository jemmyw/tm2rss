import Page
import re
import os
import logging
from dateutil.parser import *
from dateutil.tz import *
from datetime import *
from BeautifulSoup import BeautifulSoup
from google.appengine.ext.webapp import template

class TrademeItem:
	def __init__(self):
		self.title = ""
		self.link = ""
		self.image = ""
		self.description = ""
		self.date = None
		self.rss = None
		
	def load_item(self, item):
		title_link = item.find('a', id = re.compile('listingTitle'))
		image = item.find('img')
		
		self.title = title_link.string
		self.link = 'http://www.trademe.co.nz' + title_link['href']
		self.image = image['src']
		
		self.load_page()
		self.rss = self.to_rss()
		
	def load_page(self):
		result = Page.fetch(self.link)
		if(result):
			self.process_page(result)
			
	def process_page(self, result):
		soup = BeautifulSoup(result)
		desc = soup.find('div', id=re.compile('DetailsContentColumn'))
		del(desc['style'])
		del(desc['id'])
		self.description = desc.prettify()
        
		listed_at = soup.find('li',  id=re.compile('ListingTitle_titleTime'))
		if(listed_at):
			matches = re.search('Listed:\s*(.*)', listed_at.string)
			self.date = parse(matches.group(1))
			
	def rss_date(self):
		return self.date.strftime('%a, %d %b %Y %H:%M:%S %z')
			
	def to_rss(self):
		template_variables = {'item': self}
		if(self.date): template_variables['date'] = self.rss_date()
	
		path = os.path.join(os.path.dirname(__file__), 'item_rss.rss')
		return template.render(path, template_variables)