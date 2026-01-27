# Linux Server Health Monitor

## Overview
A lightweight Python-based health monitoring tool for Linux servers. The script continuously checks CPU usage, memory usage, disk utilization, and mount integrity. Mount paths are configurable through a YAML file, allowing new paths to be monitored without modifying code. The monitor runs automatically at system startup and logs results to a centralized log file, simulating industry-standard data center monitoring behavior.

---

## Features
- Monitors CPU, memory, and disk usage  
- Validates mount points (exists, mounted, writable)  
- YAML-based configuration for dynamic mount path management  
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
Recommended directory: opt/healthcheck
```bash
git clone https://github.com/DallinM1/Linux-Server-Health-Monitor.git
```

### 2. Install Python dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install psutil pyyaml
```

### 3. Set up mounts directory
```bash
sudo mkdir -p /etc/healthcheck
```
### 3. Create mounts.yaml file
```bash
cd /etc/healthcheck
sudo nano mounts.yaml
```
```yaml
mounts:
 - path: /desired_path_here
 - path: /desired_path_2_here
```
- Each path must be a valid mount point
- New paths can be added without modifying the Python script

### 4. Set up logging directory
```bash
sudo mkdir -p /var/log/healthcheck
sudo chown youruser:youruser /var/log/healthcheck
```
- Log file is created automatically when script runs

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
ExecStart=/usr/bin/python3 /opt/healthcheck/health_monitor.py
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
