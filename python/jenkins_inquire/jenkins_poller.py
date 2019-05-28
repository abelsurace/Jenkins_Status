import datetime
import time
import sys
from jenkins import JenkinsWrapper
from requests.exceptions import ConnectionError, HTTPError
import logging

log = logging.getLogger('jenkins_indicator')


def poll(server=None, user=None, password=None, configuration=None, observers=None, interval=None, list_jobs=None):
    try:
        jenkinsserver = JenkinsWrapper(
        jenkins_url=server,
        username=user,
        password=password
    )
    except HTTPError:
        log.error ("\033[1;31;40m invalid server URL")
        sys.exit(1)
    except ConnectionError:
        log.info ("\033[1;31;40m Cant connect to provided server, verify the Username and password")
        sys.exit(1)

    if list_jobs == True:
        all_jobs=jenkinsserver.jenkins.get_jobs_list()
        log.info("\033[1;32;35m All mavailable jobs")
        j=0
        for j in range (0, len(all_jobs), 2):
            print("\033[1;32;40m" + '"' + all_jobs[j] +'": '+ str(j/2) + ",")
        sys.exit(1)
        

    jenkinsserver.observe_jobs(configuration.keys())
    jenkinsserver.observe_jobs_checked(configuration.keys())

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
