from Feed import Feed
import re
from templating import *
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users

def loginRequired(func):
	def wrapper(self, *args, **kw):
		user = users.get_current_user()
		if not user:
			self.redirect(users.create_login_url(self.request.uri))
		else:
			func(self, *args, **kw)
	return wrapper

class New(webapp.RequestHandler, Template):
	def get(self):
		user = users.get_current_user()
		logged_in = user is not None
		login_url = users.create_login_url(self.request.uri)
		feeds = Feed.gql('ORDER BY created_at DESC').fetch(20)

		self.render({'user': user, 'logged_in': logged_in, 'login_url': login_url, 'feeds': feeds})
		
class Create(webapp.RequestHandler, Template):
	@loginRequired
	def post(self):
		url = self.request.get('url')
		matches = re.search('v=([A-Za-z]*)', url)

		if(matches is None or matches.group(1) is None):
			url = url + '&v=List'
		elif(matches.group(1) != 'List'):
			url = string.replace(url, matches.group(0), 'v=List')

		feed = Feed(url=self.request.get('url'),title=self.request.get('title'))
		feed.put()
		self.redirect('/show/' + str(feed.key()))
		
class Show(webapp.RequestHandler, Template):
	@loginRequired
	def get(self, key):
		self.response.headers['Content-Type'] = 'application/rss+xml'
		
		feed = Feed.get(key)
		feed.load()
		self.render({'feed': feed, 'items': feed.items, 'url': self.request.uri})


application = webapp.WSGIApplication(
												[('/', New),
												('/new', New),
												('/create', Create),
												('/show/(.*)', Show)],
												debug=True)

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
    main()
