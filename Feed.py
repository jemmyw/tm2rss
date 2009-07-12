import datetime
import Page
from TrademeItem import *
from google.appengine.ext import db

class Feed(db.Model):
	created_at = db.DateTimeProperty(auto_now_add=True)
	url = db.StringProperty()
	title = db.StringProperty()

	def load(self):
		self.start_time = datetime.now()
		self.max_time = timedelta(seconds=2)

		self.page = Page.fetch(self.url, 5)
		
		if(self.page):
			soup = BeautifulSoup(self.page)
			items = soup.findAll('li', {"class": re.compile('.*listingCard.*')})
			self.items = map(self.process_item, items)

			for item in self.items:
				item.load_details()
				time = datetime.now()
				if(time > self.start_time + self.max_time):
					# Stop due to time contraint
					break

		return self.items

	def process_item(self, item):
		titem = TrademeItem(item)
		return titem