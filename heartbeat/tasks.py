from __future__ import absolute_import, unicode_literals
import time, random, json
from .celery import app

@app.task
def execute_check_tasks(config, hosts, services):
    config = json.loads(config)[0].get('fields', [])
    hosts_task = do_host_checks.delay(json.loads(hosts),
        config.get('period_fixed'))
    services_task = do_service_checks.delay(json.loads(services),
        config.get('period_min'), config.get('period_max'))
    return [hosts_task.id, services_task.id]
    
@app.task
def terminate_check_tasks(id_list):
    for id in id_list:
        app.control.revoke(id, terminate=True)
        print("  Successfully Stopped Task[{}]".format(id))
        


@app.task
def do_host_checks(hosts, period):
    print("  Starting to Check Hosts")
    # while schedule.visible:
    # while True:
        # time.sleep(period)
        # [check_host(host) for host in hosts]
        # schedule.refresh_from_db()
    print("  Finished Checking Hosts")
    
@app.task
def do_service_checks(services, lo, hi):
    print("  Starting to Check Services")
    # while schedule.visible:
    # while True:
        # time.sleep(random.randint(lo, hi))
        # [check_service(service) for service in services]
        # schedule.refresh_from_db()
    print("  Finished Checking Services")
    
# class Checks:
    
        
    
        
def check_host(host):
    print("    Starting to Check the Host: {}".format(host))
    check = HostCheck(host=host)
    (status, details) = check.execute()
    check.update_status(status)
    print("    Finished Checking the Host: {}".format(host))

def check_service(service):
    print("    Starting to Check the Service: {}".format(service))
    check = ServiceCheck(service=service, point_value=service.point_value)
    (status, details) = check.execute()
    print(status)
    print(details)
    check.update_status(status)
    print("    Finished Checking the Service: {}".format(service))