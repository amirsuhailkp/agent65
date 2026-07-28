---
title: OWASP Auto DevSecOps
source: owasp.org
url: https://owasp.org/www-project-auto-devsecops/
collector: owasp
category: web-security
tags:
- web-security
- devsecops
- owasp
- auto
- sast
date_collected: '2026-07-26T12:44:04.430668Z'
language: unknown
---

# OWASP Auto DevSecOps

DevSecops is a python package that can be used at CI/CD for SAST and DAST. I am using opensource scanners in a serverless style. No need to host sonarqube or purchase semgrep pro. I am also writing own semgrep rules, that will be maintained over the time by community.

it will work something like
```
pip install devsecops
```

$devsecops sast –all –slack-token <> –output report.pdf

### Road Map

v0.0.1 - SAST, Secret Detection, DAST using the opensource tools and custom scripts. Slack Integration. (Completed)

v0.0.2 - Differential Scan, JIRA integration, Github Action (In Progress)

v0.0.3 - Trivy support to perform Dependency Scan.

v0.0.4 - Dastardly support

## Example

Put whatever you like here: news, screenshots, features, supporters, or remove this file and don’t use tabs at all.
