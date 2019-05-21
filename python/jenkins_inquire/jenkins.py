#!/usr/bin/python

from jenkinsapi.jenkins import Jenkins
from jenkinsapi.custom_exceptions import NoBuildData
import logging
log = logging.getLogger('jenkins_indicator')

class JenkinsWrapper(object):
    def __init__(self, jenkins_url, username, password):
        self.jenkins_url = jenkins_url
        self.jenkins = Jenkins(jenkins_url, username=username, password=password)
        self.jobs_names = []

    def observe_jobs_checked(self, jobs_names):
        log.info( 'ALL JENKINS JOBS:')
        for j in self.jenkins.get_jobs():
            self.jobs_names.append(j[0])
            log.info(j[0])

        for name in jobs_names:
            if name not in self.jobs_names:
                raise Exception('Invalid job name provided in indicator_config', name)

        self.observe_jobs(jobs_names)
        return True

    def observe_jobs(self, jobs_names):
        self.jobs_names = jobs_names

    def fetch_project_data(self, project_name):
        return self.jenkins.get_job(project_name).get_last_build()

    def fetch_observed_projects_data(self):
        builds = {}
        completed_builds = {}
        log.debug('OBSERVED JENKINS JOBS:')
        for name in self.jobs_names:
            log.debug(name)
            try:
                builds[name] = self.jenkins.get_job(name).get_last_build()
                completed_builds[name] = self.jenkins.get_job(name).get_last_completed_build()
            except NoBuildData:
                builds[name] = None
                completed_builds[name] = None

        return builds, completed_builds
