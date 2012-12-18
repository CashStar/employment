#!/usr/bin/env python
from anvil import Anvil
from autojenkins import Jenkins
from readconfig import EmploymentConfig

class Project(object):
	'''
	Represents a project
	'''

	def __init__(self, project_name, repo_url,stage,job_type=None, version=None):
		self.name = project_name

		if version != None:
			self.PROJECT = project_name + '_' + version
			self.VERSION = version
		else:
			self.PROJECT = project_name
			self.VERSION = None

		self.REPO_URL = repo_url
		self.STAGE = stage
		self.job_type=job_type

		c = EmploymentConfig('employment.conf')

		self.TEST_SCRIPT = c.getJenkinsScript('test')
		self.PACKAGE_SCRIPT = c.getJenkinsScript('package')
		self.UPLOAD_SCRIPT = c.getJenkinsScript('upload')
		self.JENKINS_URL = c.getJenkinsURL()
		self.PKG_prefix = c.getPacakgePrefix()

		self.KILN_PREFIX = c.getKilnPrefix()
		self.KILN_USERNAME = c.getKilnUsername()
		self.KILN_PASSWORD = c.getKilnPassword()
		self.k = Anvil(self.KILN_PREFIX)
		self.k.create_session(self.KILN_USERNAME, self.KILN_PASSWORD)

		self.EMAIL_TO = c.getJenkinsEmail()

		if self.job_type == 'package':
			if self.STAGE == 'dev':
				self.JENKINS_STRING = self.PKG_prefix + "_" + project_name + "_" + self.VERSION
			else:
				self.JENKINS_STRING = self.PKG_prefix + "_" + project_name
		else:
			if self.STAGE == 'dev':
				self.JENKINS_STRING = project_name + "_" + self.VERSION
			else:
				self.JENKINS_STRING = project_name

		if self.STAGE == 'dev':
			self.KILN_STRING = project_name + "_" + self.VERSION
		else:
			self.KILN_STRING = project_name

	def kiln_connect():
		anvil = Anvil(self.KILN_PREFIX)
		anvil.create_session(self.KILN_USERNAME, self.KILN_PASSWORD)
		return anvil

	def kiln_repos():
		anvil = kiln_connect()
		repos = anvil.get_repos()
		return repos

	def _jenkins_connect(self):
		return Jenkins(self.JENKINS_URL)

	def _kiln_check(self,check_project):
		anvil = self.kiln_connect()
		repos = anvil.get_repos()
		for repo in repos:
		    if repo.name == check_project:
		    	return True

	def jenkins_create_job(self):
		'''
		Create Jenkins job based on object. If it is a package job the corresponding
		template xml file will be used.
		'''
		j = self._jenkins_connect()
		if self.k.check_repo(self.KILN_STRING):
			if self.job_type == 'package':
				if j.job_exists(self.JENKINS_STRING):
					print "Job " + self.JENKINS_STRING + " already exists in Jenkins."
				else:
					response = j.create(self.JENKINS_STRING, 'templates/PKG_template.xml',
										repo_url=self.REPO_URL,
										project_name=self.name, 
										email_notify=self.EMAIL_TO,
										test_script=self.TEST_SCRIPT,
										package_script=self.PACKAGE_SCRIPT,
										stage=self.STAGE,
										version=self.VERSION,
										upload_script=self.UPLOAD_SCRIPT)
					print response
			else:
				if j.job_exists(self.JENKINS_STRING):
					print "Job " + self.JENKINS_STRING + " already exists in Jenkins."
				else:
					response = j.create(self.JENKINS_STRING, 'templates/template.xml',
										repo_url=self.REPO_URL,
										project_name=self.name,
										email_notify=self.EMAIL_TO,
										test_script=self.TEST_SCRIPT)
					print response
		else:
			print "Project " + self.PROJECT + " not found in kiln."

	def jenkins_remove_job(self):
		j = self._jenkins_connect()
		if j.job_exists(self.JENKINS_STRING):
			j.delete(self.JENKINS_STRING)
		else:
			print "Skipping, doesn't exist in Jenkins"
		
	def jenkins_build(self):
		j = self._jenkins_connect()
		j.build(self.JENKINS_STRING)

	def write_jenkins_xml(self):
        '''
        Output xml file of job.
        '''
		j = self._jenkins_connect()
		xml_output = self.JENKINS_STRING + ".xml"
		f = open(xml_output, 'w')
		f.write(j.get_config_xml(self.JENKINS_STRING))
		f.close()
