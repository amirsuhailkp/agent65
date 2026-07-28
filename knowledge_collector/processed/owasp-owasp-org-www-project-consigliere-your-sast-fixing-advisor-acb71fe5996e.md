---
title: OWASP Consigliere - Your SAST Fixing Advisor
source: owasp.org
url: https://owasp.org/www-project-consigliere---your-sast-fixing-advisor/
collector: owasp
category: web-security
tags:
- web-security
- sast
- fixing
- techniques
- consigliere
date_collected: '2026-07-26T12:45:15.916572Z'
language: unknown
---

# OWASP Consigliere - Your SAST Fixing Advisor

**Welcome to Consigliere, your SAST fixing advisor!**

### Project Goal

Standardization of the available fixing techniques of code issues detected by the industry-leading SAST tools.

### Project Description

There are usually many ways to fix security vulnerabilities to eliminate risk. However, when it comes to Static Code Analysis, different SAST tools expect different mitigation techniques. As a result, developers do not have a clear path to fixing a finding in a way that assures the SAST tool will not recognize the issue anymore.

This document is aimed to standardize the valid techniques available for fixing common SAST findings. It has two main consumers:

- Developers and security teams - will be able to fix SAST findings easily and with a clear path to ensure the issue isn’t re-detected after the fix.
- SAST tools - will be able to support the different valid fix techniques available for the findings they produce, and by that eliminate mass amounts of false positive issues they report to their customers.

### Project Roadmap

- Create a document with guidelines and code samples of vulnerable codes and valid techniques to fix, for common findings - SQLi, XSS, Path Traversal, CMDi, SSRF, XXE, and more.
- Invite developers and security enthusiasts to add their feedback and contribute more issue types and/or mitigation techniques.
- Collaborate with the industry SAST leaders to promote the idea of a clear path for fixing SAST findings, so everyone can benefit and save precious time.

### Additional Comments

This is an open-source, free project, that’s aimed to help anyone who writes or maintains code. This project will be executed in full collaboration with any actor in the industry that manages vulnerability detection or auto-remediation, who is interested in participating.
