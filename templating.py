import os
import logging
import inspect
from google.appengine.ext.webapp import template
from google.appengine.api import memcache

class Template:
	def render(self, variables={}):
		self.response.out.write(self.render_as_string(variables))

	def render_and_cache(self, variables = {}, timeout = 60):
		template = self.render_as_string(variables)
		memcache.add(self.request.uri, template, timeout)
		self.response.out.write(template)

	def render_as_string(self, variables={}):
		path = os.path.dirname(inspect.getmodule(self).__file__)
		file = os.path.basename(inspect.getmodule(self).__file__)
		className = self.__class__.__name__.lower()

		fe = os.path.splitext(file)
		file = fe[0]
		file = os.path.join(path, 'templates', file, className + '.html')

		logging.debug(file)

		return template.render(file, variables)
		