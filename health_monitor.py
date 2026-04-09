import os
import time
import logging

import psutil
import yaml

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

CONFIG_PATH = "/etc/healthcheck/config.yaml"
LOG_PATH = "/var/log/healthcheck/healthcheck.log"
CHECK_INTERVAL_SECONDS = 60

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

def load_config(config_path: str) -> dict:
    """Load and return the full YAML configuration file."""
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

# ---------------------------------------------------------------------------
# Disk
# ---------------------------------------------------------------------------

def get_disk_usage() -> list[tuple[psutil._common.sdiskpart, float]]:
    """Return a list of (partition, usage_percent) tuples for all disk partitions."""
    return [
        (partition, psutil.disk_usage(partition.mountpoint).percent)
        for partition in psutil.disk_partitions()
    ]

def check_disk_usage(warning_threshold: int, critical_threshold: int) -> None:
    """Log a warning or critical message for any partition exceeding the given thresholds."""
    for partition, usage_percent in get_disk_usage():
        if usage_percent >= critical_threshold:
            logging.critical(f'Mount point "{partition.mountpoint}" disk usage at {usage_percent}%')
        elif usage_percent >= warning_threshold:
            logging.warning(f'Mount point "{partition.mountpoint}" disk usage at {usage_percent}%')

# ---------------------------------------------------------------------------
# CPU
# ---------------------------------------------------------------------------

def check_cpu_usage(
    warning_threshold: int,
    critical_threshold: int,
    interval: int = 1,
) -> None:
    """Log a warning or critical message if CPU usage exceeds the given thresholds."""
    cpu_usage = psutil.cpu_percent(interval)
    if cpu_usage >= critical_threshold:
        logging.critical(f"CPU usage at {cpu_usage}%")
    elif cpu_usage >= warning_threshold:
        logging.warning(f"CPU usage at {cpu_usage}%")

# ---------------------------------------------------------------------------
# Memory
# ---------------------------------------------------------------------------

def check_memory_usage(warning_threshold: int, critical_threshold: int) -> None:
    """Log a warning or critical message if memory usage exceeds the given thresholds."""
    mem_usage = psutil.virtual_memory().percent
    if mem_usage >= critical_threshold:
        logging.critical(f"Memory usage at {mem_usage}%")
    elif mem_usage >= warning_threshold:
        logging.warning(f"Memory usage at {mem_usage}%")

# ---------------------------------------------------------------------------
# Mount integrity
# ---------------------------------------------------------------------------

def check_path_exists(path: str) -> bool:
    """Return True if the given path exists on the filesystem."""
    return os.path.exists(path)

def check_path_is_mount(path: str) -> bool:
    """Return True if the given path is a mount point."""
    return os.path.ismount(path)

def check_mount_is_writable(path: str) -> bool:
    """Return True if the given path is writable by the current process."""
    return os.access(path, os.W_OK)

def check_mount(path: str) -> None:
    """Verify that a path exists, is a mount point, and is writable; log any failures."""
    if not check_path_exists(path):
        logging.error(f"{path} does not exist")
    elif not check_path_is_mount(path):
        logging.error(f"{path} is not a mount point")
    elif not check_mount_is_writable(path):
        logging.error(f"{path} is not writable")

# ---------------------------------------------------------------------------
# Main health check
# ---------------------------------------------------------------------------

def health_check(config: dict) -> None:
    """Run all health checks using thresholds and mount paths from config."""
    warning = config["thresholds"]["warning"]
    critical = config["thresholds"]["critical"]

    check_disk_usage(warning, critical)
    check_cpu_usage(warning, critical)
    check_memory_usage(warning, critical)

    for mount in config.get("mounts", []):
        check_mount(mount["path"])

# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    config = load_config(CONFIG_PATH)
    while True:
        try:
            health_check(config)
        except Exception as e:
            logging.exception(f"Health check failed: {e}")
        time.sleep(CHECK_INTERVAL_SECONDS)

