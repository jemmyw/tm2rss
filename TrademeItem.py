import Page
from BeautifulSoup import BeautifulSoup

class TrademeItem:
	def __init__(self):
		self.title = ""
		self.link = ""
		self.image = ""
		self.description = ""
		
	def load_item(self, item):
		title_link = item.find('a', id = re.compile('listingTitle'))
		image = item.find('img')
		
		self.title = title_link.string
		self.link = 'http://www.trademe.co.nz' + title_link['href']
		self.image = image['src']
		
		self.load_page()
		
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