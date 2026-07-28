---
title: OWASP Secure Coding Dojo
source: owasp.org
url: https://owasp.org/www-project-secure-coding-dojo/
collector: owasp
category: web-security
tags:
- web-security
- dojo
- secure
- coding
- software
date_collected: '2026-07-26T12:44:38.417511Z'
language: unknown
---

# OWASP Secure Coding Dojo

### Description

The Secure Coding Dojo is a training platform which can be customized to integrate with custom vulnerable websites and other CTF challenges. The project was initially developed at Trend Micro and was donated to OWASP in 2021.

Here are some of the features:

- Integrates with Enterprise environments using Slack, Google and LDAP for authentication
- It allows grouping of participants according to their development teams
- It allows teams to track progress and compete with each other
- Each lesson is built as an attack/defence pair. Developers can observe the software weaknesses by conducting the attack and after solving the challenge they learn about the associated software defenses
- Predefined lessons are based on the MITRE most dangerous software errors (also known as SANS 25) so the focus is on software errors rather than attack techniques
- The predefined hacking challenges are created for entry level and keep the developers engaged. Only a browser is needed.
- With CTFs there is a puzzle aspect to the challenges which is great for pen-tester audiences but can make some developers lose interest. In the Secure Coding Dojo the focus is on demonstrating the vulnerability.
- There are tips that help the developers as they are exploiting the issue to avoid getting stuck

### Licensing

This program is free software: you can redistribute it and/or modify it under the terms of the Apache License 2.0

### Roadmap

As of *December, 2020*, the highest priorities for the next 6 months are:

- Dockerize the Second Degree Blackbelt
- Multi-language support
- New training module with focus on containers

### Getting Involved

Involvement in the development and promotion of **Secure Coding Dojo** is actively encouraged!
You do not have to be a security expert or a programmer to contribute.

Some of the ways you can help are as follows:

- Try it out
- Have your development team try it out
- Submit feedback via Github issues
- Submit pull requests

### Training Portal Front Page

### Leaderboard

### Secure Coding Practices (Code Blocks)

### Training modules

### Code Review training module

Check it out from OWASP Coding Dojo static page: [Security Code Review 101](https://owasp.org/SecureCodingDojo/codereview101/)

### Common Software flaws training module

### Detailed description for a challenge

### Common Software flaws - Insecure.Inc Vulnerable site

### XSS challenge

### Buffer overflow challenge

### Hosted by OWASP

<https://securecodingdojo.owasp.org/>

### Host it locally

The following steps will get you the basic configuration for the Dojo. For advanced configuration and integrations check the [wiki](https://github.com/trendmicro/SecureCodingDojo/wiki/Deploying-with-Docker)

- Install Docker latest version.
- Git clone the repository
- Change directory to the repo root directory
- Configure an environment variable DATA\_DIR as a mount point for the dojo files. On \*nix/mac modify .bash\_profile as follows
  ```
  export DATA_DIR="/YOUR_DATA_DIR"
  ```
- On Mac you must allow Docker access to this directory in Docker > Preferences > File Sharing
- Restart your terminal
- Run with
  ```
  docker-compose up
  ```

### Running a Secure Coding Workshop using the Dojo

Bringing Software Security training to schools can have a positive impact on the security of future software. The Secure Coding Dojo project was created to bring knowledge about software weaknesses and security best practices to classrooms of all sizes: from universities to large companies. This workshop package is intended to facilitate security advocates to deliver training sessions using the dojo.

The workshop package is based on an event organized by the OWASP Ottawa Chapter and Secure that Cert at the University of Ottawa. Special thanks to the workshop organizers: Nancy Gariche, Garth Boyd, Miguel Garzon, Abdulwahaab Ahmed, Scott Kelly and Dave Petrasovic.

### Package Contents

The following resources are being provided with the package:

- Prerequisites
- Suggested agenda and workshop structure
- Presentation material
- Recording of a lecture at the University of Ottawa using the presentation material
- Dojo deployment instructions

### Prerequisites

Students will be asked to bring the following:

- Laptop with Internet access
- Optional: Docker and latest version of the Secure Coding Dojo per the install instructions below.
- Browser: Chrome or Firefox latest version
- No other software is required.

Organizers should consider the following:

- Event planning platform
- Room size based on registration
- AV and Internet access for participants
- Consider hosting for the Secure Coding Dojo platform: cloud account, host names, certificates
- Workshop staff. 1 tutor to 50 students. Workshop staff should complete all exercises in advance and be familiar with the content.
- Catering if applicable

### Suggested Agenda

The following agenda is based on a full day workshop including lecture.

- 10:00 Registration
- 10:30 Lecture: Attack-Grams
- 11:00 Lecture: Secure Coding Practices
- 12:00 Lunch break
- 12:30 Dojo Practice Setup, Accounts, Urls
- 13:00 Dojo Practice: Security Code Review Master Module
- 13:30 Dojo Practice: Secure Coding Dojo Black Belt Module
- 17:00 End of workshop

### Presentation Material

Slides for the lecture portion are available [here](https://github.com/trendmicro/SecureCodingDojo/tree/master/workshop)
and can be distributed under the licensing of this project.
Please give credit to the content creator and graphics creators.

### Lecture Recording

A lecture recording using the provided presentation material can be found at the following [link](https://www.youtube.com/watch?v=1ghIH_Myu4U&feature=youtu.be&t=929)

### Deploying Secure Coding Dojo

The Secure Coding Dojo runs from Docker containers. Students could easily deploy their own instance using docker-compose as described below.
Deploying a common permanent production instance of the Dojo requires a bit more setup with instructions available on the [wiki](https://github.com/trendmicro/SecureCodingDojo/wiki/Deploying-with-Docker) .

You may also find useful the AppSec DC 2019 presentation of the project: [AppSeC Presentation](https://github.com/trendmicro/SecureCodingDojo/tree/master/AppSecDC%20Secure%20Coding%20Dojo%20Presentation)

Costs for a permanent deployment may vary from $30/month to more depending on the number of participants.

#### Basic Setup

- Install Docker latest version.
- Git clone the repository
- Change directory to the repo root directory
- Configure an environment variable DATA\_DIR as a mount point for the dojo files. On \*nix/mac modify .bash\_profile as follows
  ```
  export DATA_DIR="/YOUR_DATA_DIR"
  ```
- On Mac you must allow Docker access to this directory in Docker > Preferences > File Sharing
- Restart your terminal
- Run with
  ```
  docker-compose up
  ```
