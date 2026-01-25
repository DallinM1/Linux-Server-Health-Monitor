import psutil
import os
import time
import logging
from datetime import datetime

logging.basicConfig(
    filename="/var/log/healthcheck/healthcheck.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

def get_disk_usage():
    disk_parts = psutil.disk_partitions()
    usage_list = []
    for part in disk_parts:
        u = psutil.disk_usage(part.mountpoint).percent
        usage_list.append((part, u))
    return usage_list

def check_disk_usage(warning_flag, critical_flag):
    disk_usage_list = get_disk_usage()
    for i in disk_usage_list:
        if i[1] >= critical_flag:
            logging.critical(f"Mount point \"{i[0].mountpoint}\" disk usage at {i[1]}%")
        elif i[1] >= warning_flag:
            logging.warning(f"Mount point \"{i[0].mountpoint}\" disk usage at {i[1]}%")

def check_cpu_usage(warning_flag, critical_flag, interval=1):
    cpu_usage = psutil.cpu_percent(interval)
    if cpu_usage >= critical_flag:
        logging.critical(f"CPU usage at {cpu_usage}%")
    elif cpu_usage >= warning_flag:
        logging.warning(f"CPU usage at {cpu_usage}%")
    
def check_memory_usage(warning_flag, critical_flag):
    mem_usage = psutil.virtual_memory().percent
    if mem_usage >= critical_flag:
        logging.critical(f"Memory usage at {mem_usage}%")
    elif mem_usage >= warning_flag:
        logging.warning(f"Memory usage at {mem_usage}%")
    
def check_path_exists(path):
    return os.path.exists(path)
    
def check_path_is_mount(path):
    return os.path.ismount(path)
    
def check_mount_is_writable(path):
    return os.access(path, os.W_OK)

def check_mount(path):
    if check_path_exists(path) is False:
        logging.error(f"{path} does not exist")
    elif check_path_is_mount(path) is False:
        logging.error(f"{path} is not a mount point")
    elif check_mount_is_writable(path) is False:
        logging.error(f"{path} is not writable")

def health_check():
    check_disk_usage(80, 90)
    check_cpu_usage(80, 90)
    check_memory_usage(80, 90)

if __name__ == "__main__":
    while True:
        health_check()
        time.sleep(60)