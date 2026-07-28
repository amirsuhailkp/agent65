---
title: OWASP SecureTea Project
source: owasp.org
url: https://owasp.org/www-project-securetea/
collector: owasp
category: web-security
tags:
- web-security
- securetea
- owasp
- project
- sudo
date_collected: '2026-07-26T12:44:39.946536Z'
language: unknown
---

# OWASP SecureTea Project

Welcome to the home of the OWASP SecureTea Project !
The OWASP SecureTea Project is an application designed to help secure a person’s laptop or computer / server with IoT (Internet Of Things) and notify users (via various communication mechanisms), whenever someone accesses their computer / server.

This application uses the touchpad/mouse/wireless mouse to determine activity and is developed in Python and tested on various machines (Linux, Mac & Windows). The software have it’s own IDS(Intrusion Detection System) / IPS(Instrusion Prevention System), firewall, anti-virus, intelligent log monitoring capabilities with web defacement detection, and support for much more communication medium.

**The OWASP SecureTea Project** provides a one-stop security solution for various devices (personal computers / servers / IoT devices).

## Installation

Before installing, please make sure to install the  **pre-requisites**.

You can install SecureTea from PyPi package manager using the following command:
```
$ sudo python3 -m pip install securetea
```

**or**

You can install SecureTea using the latest repository:
```
```
git clone https://github.com/OWASP/SecureTea-Project.git
cd SecureTea-Project/
sudo python3 -m pip install -r requirements.txt
sudo python3 setup.py install```
```

Please make sure all dependencies are installed if anyone of the above fails.

For more detailed information, refer to the [installation guide](/doc/en-US/user_guide.md#installation).

## Quick Start

- Start SecureTea using one or more

  :**integrations**

  For example, running Intrusion Detection System only:
  ```
  $ sudo securetea --ids
  ```
- Start SecureTea in

  :**server mode**
  ```
  $ sudo securetea-server
  ```
- Start SecureTea in

  :**system mode**
  ```
  $ sudo securetea-system
  ```
- Start SecureTea in

  :**IoT mode**
  ```
  $ sudo securetea-iot
  ```

For more detailed information, refer to the [usage guide](https://github.com/OWASP/SecureTea-Project/blob/master/doc/en-US/user_guide.md#usage).

## Example

Put whatever you like here: news, screenshots, features, supporters, or remove this file and don’t use tabs at all.

## Features

- [Intrusion Detection System](https://github.com/OWASP/SecureTea-Project/blob/master/doc/en-US/user_guide.md#intrusion-detection-system)
- [Firewall](https://github.com/OWASP/SecureTea-Project/blob/master/doc/en-US/user_guide.md#firewall)
- [AntiVirus](https://github.com/OWASP/SecureTea-Project/blob/master/doc/en-US/user_guide.md#antivirus)
- [Server Log Monitor](https://github.com/OWASP/SecureTea-Project/blob/master/doc/en-US/user_guide.md#server-log-monitor)
- [System Log Monitor](https://github.com/OWASP/SecureTea-Project/blob/master/doc/en-US/user_guide.md#system-log-monitor)
- [Local Web Deface Detection & Prevention System](https://github.com/OWASP/SecureTea-Project/blob/master/doc/en-US/user_guide.md#web-deface-detection)
- [Auto Web Server Patcher](https://github.com/OWASP/SecureTea-Project/blob/master/doc/en-US/user_guide.md#auto-server-patcher)
- [Insecure Headers Detection](https://github.com/OWASP/SecureTea-Project/blob/master/doc/en-US/user_guide.md#insecure-headers)
- [IoT Anonymity Checker](https://github.com/OWASP/SecureTea-Project/blob/master/doc/en-US/user_guide.md#iot-anonymity-checker)
- [Auto Report Generation Using OSINT](https://github.com/OWASP/SecureTea-Project/blob/master/doc/en-US/user_guide.md)
- [Notifying Suspicious Activities Using Various Mediums (Twitter, Telegram, Slack, Gmail, SMS, AWS)](https://github.com/OWASP/SecureTea-Project/blob/master/doc/en-US/user_guide.md#setting-up-notifiers)
- [Interactive GUI For Ease Of Setting Up](https://github.com/OWASP/SecureTea-Project/blob/master/doc/en-US/user_guide.md#configuring-using-web-ui)

## Contributors

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

*Abhishek Sharma*[💻](https://github.com/OWASP/SecureTea-Project/commits?author=abhisharma404)[📖](https://github.com/OWASP/SecureTea-Project/commits?author=abhisharma404)*Rejah Rehim* [💻](https://github.com/OWASP/SecureTea-Project/commits?author=rejahrehim)[📖](https://github.com/OWASP/SecureTea-Project/commits?author=rejahrehim)*adeyosemanputra*[💻](https://github.com/OWASP/SecureTea-Project/commits?author=adeyosemanputra)[📖](https://github.com/OWASP/SecureTea-Project/commits?author=adeyosemanputra)*Ananthu S*[💻](https://github.com/OWASP/SecureTea-Project/commits?author=ananthus)*Sunny Dhoke*[🐛](https://github.com/OWASP/SecureTea-Project/issues?q=author%3Asunn-e)[📖](https://github.com/OWASP/SecureTea-Project/commits?author=sunn-e)*MajAK*[💻](https://github.com/OWASP/SecureTea-Project/commits?author=kUSHAL0601)*Mishal Shah*[💻](https://github.com/OWASP/SecureTea-Project/commits?author=mishal23)*sam@ukjp*[💻](https://github.com/OWASP/SecureTea-Project/commits?author=sam-aldis)

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!

# Latest News

Securetea Project Graduate as OWASP Lab Status on Thu, Sep 9, 2021. see more at https://owasp.org/projects/ </br>
