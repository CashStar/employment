#!/usr/bin/env python
import optparse
from JobChunks import JobChunks
import Project
import string

def main():
	def app_description():
		"""
		Create a set of jobs representing a type of job, stage of developement,and version.
		----------------------
		Examples:		
		./run.py -s dev -v 4_0 -d -c
		Delete and create development jobs for the 4_0 branch.

		./run.py -s dev -v 4_0 -t package -d -c
		Delete and create development package jobs for the 4_0 branch.

		./run.py -s production -v 4_0 -d -c
		Delete and create production jobs for the master branch.

		./run.py -s production -v 4_0 -d -c
		Delete and create production jobs for the master branch.

		./run.py -s production -v 4_0 -t package -d -c
		Delete and create production package jobs for the master branch.
		"""
		return str(string.replace(app_description.__doc__,'\n\t','\n'))[1:]

	p = optparse.OptionParser(usage=app_description())
	p.add_option('--type', '-t', default=None, help="Type of jobs (ex. package, or default normal)")
	p.add_option('--stage', '-s', default="production", help="Stage jobs will represent [production/dev]")
	p.add_option('--version', '-v', default="", help="Version of jobs (ex. 4_0")
	p.add_option('--delete', '-d', default=False, dest="do_delete", action="store_true", help="Delete jobs")
	p.add_option('--create', '-c', default=False, dest="do_create", action="store_true", help="Create jobs")

	options, arguments = p.parse_args()

	if (options.do_delete == False) and (options.do_create == False):
		p.error("Must specify an action (ex. -d or -c)")

	def Jobs():
		jobs = JobChunks(stage=options.stage,job_type=options.type,version=options.version)
		return jobs

	if options.do_delete:
		jobs = Jobs()
		jobs.delete()
		jobs.delete_trig()

	if options.do_create:
		jobs = Jobs()
		jobs.create()
		jobs.create_trig()

if __name__ == '__main__':
	main()
