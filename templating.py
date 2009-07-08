import os
import logging
from google.appengine.ext.webapp import template

def render(variables={}):
	logging.debug(__file__)