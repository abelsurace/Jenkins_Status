from jenkinsapi.jenkins import Jenkins
from jenkinsapi.custom_exceptions import NoBuildData
import logging
import sys
log = logging.getLogger('jenkins_indicator')

class JenkinsWrapper(object):
    def __init__(self, jenkins_url, username, password):
        self.jenkins_url = jenkins_url
        self.jenkins = Jenkins(jenkins_url, username=username, password=password)
        self.jobs_names = []

    def observe_jobs_checked(self, jobs_names):
        log.info( 'ALL JENKINS JOBS:')
        allJobs = self.jenkins.get_jobs_list()
        badJobNames = []
        for name in jobs_names:
            log.debug(name)
            if name not in allJobs:
                badJobNames.append(name)
        if len(badJobNames)>0:
            log.error('\033[1;31;40m Invalid job name provided in indicator_config')
            for badname in badJobNames:
                print("\033[1;31;40m" + badname + " \n") 
            sys.exit()

        self.observe_jobs(jobs_names)
        return True

    def observe_jobs(self, jobs_names):
        self.jobs_names = jobs_names

    def fetch_project_data(self, project_name):
        return self.jenkins.get_job(project_name).get_last_build()

    def fetch_observed_projects_data(self):
        builds = {}
        completed_builds = {}
        #log.debug(self.jenkins.get_jobs_list())
        log.debug('OBSERVED JENKINS JOBS:')
        for name in self.jobs_names:
            log.debug("fetch_observed" + name)
            try:
                builds[name] = self.jenkins.get_job(name).get_last_build()
                completed_builds[name] = self.jenkins.get_job(name).get_last_completed_build()
            except NoBuildData:
                builds[name] = None
                completed_builds[name] = None

        return builds, completed_builds
