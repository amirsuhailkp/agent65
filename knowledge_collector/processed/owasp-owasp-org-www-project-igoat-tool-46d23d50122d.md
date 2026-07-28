---
title: OWASP iGoat Tool
source: owasp.org
url: https://owasp.org/www-project-igoat-tool/
collector: owasp
category: web-security
tags:
- web-security
- igoat
- owasp
- tool
- ios
date_collected: '2026-07-26T12:44:55.739663Z'
language: unknown
---

# OWASP iGoat Tool

## OWASP iGoat - A Learning Tool for iOS App Pentesting and Security

iGoat is a learning tool for iOS developers (iPhone, iPad, etc.) and mobile app pentesters. It was inspired by the WebGoat project, and has a similar conceptual flow to it.

As such, iGoat is a safe environment where iOS developers can learn about the major security pitfalls they face as well as how to avoid them. It is made up of a series of lessons that each teach a single (but vital) security lesson.

### The lessons are laid out in the following steps:

- Brief introduction to the problem.
- Verify the problem by exploiting it.
- Brief description of available remediations to the problem.
- Fix the problem by correcting and rebuilding the iGoat program.

Step 4 is optional, but highly recommended for all iOS developers. Assistance is available within iGoat if you don’t know how to fix a specific problem.

## OWASP iGoat (Swift) - A Damn Vulnerable Swift Application for iOS

**Vulnerabilities Covered (version 1.0):** [Documentation: https://docs.igoatapp.com/](https://codeload.github.com/OWASP/iGoat-Swift/zip/master)

**Documentation:**[iGoat Wiki](https://github.com/OWASP/iGoat-Swift/wiki)

**iGoat Quick Setup**
```
git clone https://github.com/OWASP/iGoat-Swift.git
```

and open iGoat-Swift.xcodeproj with xcode.
**Setup iGoat Server** Navigate to server > docker\_packaging and then use command
```
docker compose up
```

**Using Cydia Repo** - Open Cydia -> Sources -> Edit and add source http://swiftigoat.yourepo.com/ and then search for iGoat and install it.

**Project Lead** - Swaroop Yermalkar

## Architecture

## Example

Put whatever you like here: news, screenshots, features, supporters, or remove this file and don’t use tabs at all.
