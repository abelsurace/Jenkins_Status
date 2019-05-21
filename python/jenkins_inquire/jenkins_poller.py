import datetime
import time
from jenkins_inquire.jenkins import JenkinsWrapper
from requests.exceptions import ConnectionError, HTTPError
import logging

log = logging.getLogger('jenkins_indicator')


def poll(server=None, user=None, password=None, configuration=None, observers=None, interval=None):
    jenkinsserver = JenkinsWrapper(
        jenkins_url=server,
        username=user,
        password=password
    )

    jenkinsserver.observe_jobs(configuration.keys())

    while True:
        try:
            (builds, completed_builds) = jenkinsserver.fetch_observed_projects_data()
            for name, build in builds.items():
                if build is None:
                    for o in observers:
                        o.on_no_info_available(name)
                else:
                    was_good_previously = completed_builds[name].is_good()
                    is_running = build.is_running()
                    is_success = build._data['result'] == 'SUCCESS'
                    is_faliure = build._data['result'] == 'FAILURE'
                    start_time = build.get_timestamp()
                    estimated_time = datetime.timedelta(milliseconds=build._data['estimatedDuration'])
                    description = build.job.get_description()
                    log.info(build.job)
                    state = {"running": is_running, "is_success": is_success,"is_falure": is_faliure, "result": build._data['result']}
                    log.debug("Project '{}' status : {}".format(name, str(state)))
                    for o in observers:
                        o.on_new_build_info(name, description, is_success,is_faliure, was_good_previously, is_running, start_time,
                                            estimated_time)
            log.debug("Round complete waiting for next pull round in {} seconds".format(interval))
            time.sleep(interval)
        except (ConnectionError, HTTPError) as e:
            log.warning("Connectivity error " + str(e))
        except Exception as e:
            log.error("Unhandled exception due to error: " + str(e))
