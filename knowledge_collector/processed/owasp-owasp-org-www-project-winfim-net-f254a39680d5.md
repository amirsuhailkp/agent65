---
title: OWASP WinFIM.NET
source: owasp.org
url: https://owasp.org/www-project-winfim.net/
collector: owasp
category: web-security
tags:
- web-security
- winfim
- net
- file
- txt
date_collected: '2026-07-26T12:44:51.613564Z'
language: unknown
---

# OWASP WinFIM.NET

# WinFIM.NET

WinFIM.NET - File Integrity Monitoring For Windows

**#Introduction**
There are plenty of commercial tools to do file integrity monitoring (FIM). But, for freeware / Open Source, especially for Windows, it seems not much options.

A small Windows Service named [“WinFIM.NET”](https://github.com/OWASP/www-project-winfim.net) was developed trying to fill up this gap.

**#characteristics**
The characteristics of this small application are:

**#Installation (single machine)**

1) Manual download all files to destination computer

2) Configure the parameters to fill your own environment
```
```
a) ‘monlist.txt‘ – put your in-scope monitoring files / directories (Absolute path) line by line under this file<br>
b) ‘exclude_path.txt‘ – put your exclusion (Absolute path) line by line under this file (the exclusion should be overlapped with the paths in ‘monlist.txt’ (e.g. Sub-directory of the in-scope directory)<br>
c) ‘exclude_extension.txt‘ – put all whitelisted file extension (normally, those extensions should be related to some frequent changing files, e.g. *.log, *.tmp)<br>
d) ‘scheduler.txt‘ – This file is to control whether the WinFIM.NET will be run in schedule mode or continuous mode.<br>
  -  Put a number ‘0’ to the file, if you want the WinFIM.NET keep running.
  -  Put a number (in minute) for the time separation of each run. e.g. 30 (that means file checksum will be run every 30 minutes).```
```

3) Unblock the “WinFIM.NET Service.exe”

4) Install the Windows Service - Bring up an Administrator command prompt and navigate to the deployed folder, then execute “install\_service.bat”

5) Verify if the Windows Service is up and running

6) Please make sure maximum log size is configured according to your deployment environment. By default, it only reserves around 1MB for it. - %SystemRoot%\System32\Winevt\Logs\WinFIM.NET.evtx

**#Uninstallation**
Bring up an Administrator command prompt and navigate to the deployed folder, then execute “uninstall\_service.bat”

**#Windows Event ID for file / directory changes**

Enjoy!

Cheers
Henry

## Deployment Illustration

For detail introduction, please visit my [Cyber Security Corner](https://redblueteam.wordpress.com/2020/03/11/winfim-net-windows-file-integrity-monitoring/) technical blog.
