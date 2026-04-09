# Linux Server Health Monitor

## Overview
A lightweight Python-based health monitoring tool for Linux servers. The script continuously checks CPU usage, memory usage, disk utilization, and mount integrity. Warning and critical thresholds, along with mount paths, are configurable through a single YAML file, allowing the monitor to be tuned without modifying code. The monitor runs automatically at system startup and logs results to a centralized log file, simulating industry-standard data center monitoring behavior.

---

## Features
- Monitors CPU, memory, and disk usage  
- Validates mount points (exists, mounted, writable)  
- YAML-based configuration for alert thresholds and mount path management  
- Runs continuously using `systemd`  
- Centralized logging to `/var/log/healthcheck/healthcheck.log`  
- Tested using simulated CPU, memory, and disk load  

---

## Requirements
- Linux (tested on Ubuntu)  
- Python 3.8+  
- Python libraries:
  - psutil
  - pyyaml
- systemd  

---

## Setup Instructions

### 1. Clone the Repository
Recommended directory: `/opt/healthcheck`
```bash
git clone https://github.com/DallinM1/Linux-Server-Health-Monitor.git
```

### 2. Install Python Dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install psutil pyyaml
```

### 3. Create the Config Directory and config.yaml
```bash
sudo mkdir -p /etc/healthcheck
sudo nano /etc/healthcheck/config.yaml
```
```yaml
thresholds:
  warning: 80
  critical: 90

mounts:
  - path: /desired_path_here
  - path: /desired_path_2_here
```
- `warning` and `critical` are percentage thresholds applied to CPU, memory, and disk checks
- Each mount path must be a valid mount point
- Thresholds and paths can be updated at any time without modifying the Python script

### 4. Set up Logging Directory
```bash
sudo mkdir -p /var/log/healthcheck
sudo chown youruser:youruser /var/log/healthcheck
```
- The log file is created automatically when the script runs

---

## Automation Instructions

### 1. Create the systemd Service File
```bash
sudo nano /etc/systemd/system/healthcheck.service
```
```ini
[Unit]
Description=Linux Server Health Monitor
After=network.target

[Service]
Type=simple
User=youruser
ExecStart=/usr/bin/python3 /opt/healthcheck/healthcheck.py
Restart=always
RestartSec=5
StandardOutput=append:/var/log/healthcheck/healthcheck.log
StandardError=append:/var/log/healthcheck/healthcheck.log

[Install]
WantedBy=multi-user.target
```

### 2. Enable and Start the Service
```bash
sudo systemctl daemon-reload
sudo systemctl enable healthcheck
sudo systemctl start healthcheck
```
