# Linux-Server-Health-Monitor
A lightweight Python-based monitoring script designed to track system performance and log vital health events every minute. This tool ensures that administrators have a persistent, structured record of system warnings, errors, and critical failures.
Features

    Continuous Monitoring: Runs every 60 seconds via cron for near real-time oversight.
    Hierarchical Logging: Separates system events into WARNING, ERROR, and CRITICAL levels.
    Metric Tracking: Monitors core system resources, including CPU Load, Memory (RAM) Consumption, and Disk Space Availability.
    Minimal Footprint: Designed to run with low overhead on any modern Linux distribution.

Prerequisites

    Python 3.x
    psutil library (can be installed via: pip install psutil)

