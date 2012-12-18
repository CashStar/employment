import ConfigParser
import re

class EmploymentConfig(object):
	'''
	Object to get values out of config file and write new values to config file.
	'''
	def __init__(self, filename):
		self.filename = filename
		self.general_section = 'general'

	def ConfigSectionMap(self, section):
		dict1 = {}
		Config = ConfigParser.ConfigParser()
		Config.read(self.filename)
		options = Config.options(section)
		for option in options:
			try:
				dict1[option] = Config.get(section, option)
				if dict1[option] == -1:
					DebugPrint("skip: %s" % option)
			except:
				print("exception on %s!" % option)
				dict1[option] = None
		return dict1

	def getPacakgePrefix(self):
		return self.ConfigSectionMap('jenkins')['package_prefix']

	def getJenkinsEmail(self):
		return self.ConfigSectionMap('jenkins')['email']

	def getJenkinsURL(self):
		return self.ConfigSectionMap('jenkins')['url']

	def getJenkinsScript(self, script):
		return self.ConfigSectionMap('jenkins')["%s_script" % script]

	def getKilnPrefix(self):
		return self.ConfigSectionMap('kiln')['prefix']

	def getKilnUsername(self):
		return self.ConfigSectionMap('kiln')['username']

	def getKilnPassword(self):
		return self.ConfigSectionMap('kiln')['password']

	def getGroupName(self, group):
		return self.ConfigSectionMap(group)['group_name']

	def getGroupProjects(self, group):
		return self.ConfigSectionMap(group)['projects'].split(', ')