import os
import logging
import inspect
from google.appengine.ext.webapp import template

class Template:
	def render(self, variables={}):
		path = os.path.dirname(inspect.getmodule(self).__file__)
		file = os.path.basename(inspect.getmodule(self).__file__)
		className = self.__class__.__name__.lower()		
		
		fe = os.path.splitext(file)
		file = fe[0]		
		file = os.path.join(path, 'templates', file, className + '.html')
		
		logging.debug(file)
		
		self.response.out.write(template.render(file, variables))