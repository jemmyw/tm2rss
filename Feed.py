import datetime
import logging
from google.appengine.ext import db
from google.appengine.api import urlfetch
from google.appengine.api import memcache

class Feed(db.Model):
	created_at = db.DateTimeProperty(auto_now_add=True)
	url = db.StringProperty()
	title = db.StringProperty()