#!/usr/bin/env python
from anvil import Anvil
from autojenkins import Jenkins
from Project import Project
from readconfig import EmploymentConfig

class JobChunks(object):
	'''
	Represents a group of projects that exist in our repo and are being created in Jenkins. These groups vary
	by environment and depending on if they are for packaging.

	For instance, if the repo has a _version at the end it's a dev environment. Similarly, if the job is for 
	packaging it will be created accordingly.
	'''

	def __init__(self, stage, job_type=None, version=None):
		c = EmploymentConfig('employment.conf')
		self.JENKINS_URL=c.getJenkinsURL()
		self.KILN_PREFIX = c.getKilnPrefix()
		self.JOB_TYPE = job_type
		self.STAGE = stage
		self.VERSION = version

		c = EmploymentConfig('employment.conf')
		self.KILN_PREFIX = c.getKilnPrefix()
		self.KILN_USERNAME = c.getKilnUsername()
		self.KILN_PASSWORD = c.getKilnPassword()
		self.k = Anvil(self.KILN_PREFIX)
		self.k.create_session(self.KILN_USERNAME, self.KILN_PASSWORD)
		#self.k.create_session_by_prompting()

		group1 = c.getGroupProjects('group1')
		self.group1name = c.getGroupName('group1')

		group2 = c.getGroupProjects('group2')
		self.group2name = c.getGroupName('group2')

		self.app_groups = [group1, group2]

	def _jenkins_connect(self):
		'''
		Create a object holding a connection to jenkins. Assign this function to a variable.

		Ex. j = _jenkins_connect()
		'''
		return Jenkins(self.JENKINS_URL)

	def _build_project_string(self, app_name):
		'''
		Build the project string. Should this just be a variable?
		'''

		if self.JOB_TYPE == 'package':
			if self.STAGE == 'dev':
				string_return = "PKG_" + app_name + "_" + self.VERSION
			else:
				string_return = "PKG_" + app_name
		else:
			if self.STAGE == 'dev':
				string_return = app_name + "_" + self.VERSION
			else:
				string_return = app_name
		return string_return

	def _build_trig_string(self):
		'''
		Create the name of the job that will trigger all the others.
		'''
		if self.JOB_TYPE == 'package':
			if self.STAGE == 'dev':
				string_return = "PKG_dev_" + self.VERSION
			else:
				string_return = "PKG_master"
		else:
			if self.STAGE == 'dev':
				string_return = "TEST_dev_" + self.VERSION
			else:
				string_return = "TEST_master"
		return string_return

	def _build_kiln_string(self, app_name):
		'''
		Build the string for the name of the app as it would appear in kiln.
		'''
		if self.STAGE == 'dev':
			string_return = app_name + "_" + self.VERSION
		else:
			string_return = app_name
		return string_return

	def _get_repo_base(self, group):
		'''
		Create the base repo url based on the group.
		'''

		if group == 0:
			base_url = "https://%s.kilnhg.com/Code/src/%s/" % (self.KILN_PREFIX, self.group1name)
		elif group == 1:
			base_url = "https://%s.kilnhg.com/Code/src/%s/" % (self.KILN_PREFIX, self.group2name)
		else:
			base_url=None
		return base_url

	def _jobs_in_jenkins(self):
		'''
		Returns an array of all jobs from config that are in Jenkins.
		'''
		j = self._jenkins_connect()
		jobs = []
		for group in self.app_groups:
			base_url = self._get_repo_base(self.app_groups.index(group))
			for project in group:
				project_name = self._build_project_string(project)
				repo_url = base_url + project
				if j.job_exists(project_name):
					jobs.append(Project(project, repo_url, self.STAGE, self.JOB_TYPE, self.VERSION))
		return jobs

	def _job_in_kiln(self):
		'''
		Returns array of projects in kiln
		'''
		jobs = []
		for group in self.app_groups:
			base_url = self._get_repo_base(self.app_groups.index(group))
			for project in group:
				project_name = self._build_kiln_string(project)
				repo_url = base_url + project_name
				if self.k.check_repo(project_name):
					print "Found %s in kiln" % project_name
					jobs.append(Project(project, repo_url, self.STAGE, self.JOB_TYPE, self.VERSION))
		return jobs

	def _build_app_list(self):
		'''
		Return a comma  of projects that we will pass to a trigger job.
		'''
		apps = self._jobs_in_jenkins()
		app_string = ''
		for app in apps:
			if apps.index(app) < (len(apps)-1):
				app_string = app_string + self._build_project_string(app.name) + ', '
			else:
				app_string = app_string + self._build_project_string(app.name)
		return app_string

	def delete(self):
	    print "*" * 60
	    print "Doing delete"
	    print "*" * 60
	    jobs = self._jobs_in_jenkins()
	    for job in jobs:
	    	print "Removing Jenkins job for " + self._build_project_string(job.name)
	        jobs[jobs.index(job)].jenkins_remove_job()

	def create(self):
	    print "*" * 60
	    print "Creating jobs"
	    print "*" * 60
	    jobs = self._job_in_kiln()
	    for job in jobs:
	    	print "Creating Jenkins job for " + self._build_project_string(job.name)
	        jobs[jobs.index(job)].jenkins_create_job()

	def create_trig(self):
		build_apps = self._build_app_list()
		print "Using app list: " + build_apps
		j = self._jenkins_connect()
		trigger_job = self._build_trig_string()
		if j.job_exists(trigger_job):
			print "Job " + trigger_job + " already exists!"
		else:
			print "Creating trigger job " + trigger_job
			response = j.create(trigger_job, 'templates/trigger.xml',
							job_list=build_apps)
			print response

	def delete_trig(self):
		j = self._jenkins_connect()
		trigger_job = self._build_trig_string()
		if j.job_exists(trigger_job):
			print "Deleting trigger job " + trigger_job
			return j.delete(trigger_job)
		else:
			print trigger_job + " doesn't seem to exist."

	def init_build(self):
		'''
		Hit the trigger job. Not really necessary right now.
		'''

