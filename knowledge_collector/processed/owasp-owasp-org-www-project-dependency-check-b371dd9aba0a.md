---
title: OWASP Dependency-Check
source: owasp.org
url: https://owasp.org/www-project-dependency-check/
collector: owasp
category: web-security
tags:
- web-security
- dependency-check
- owasp
- known
- data
date_collected: '2026-07-26T12:43:42.004512Z'
language: unknown
---

# OWASP Dependency-Check

Dependency-Check is a Software Composition Analysis (SCA) tool that attempts to detect publicly disclosed vulnerabilities contained within a project’s dependencies. It does this by determining if there is a Common Platform Enumeration (CPE) identifier for a given dependency. If found, it will generate a report linking to the associated CVE entries.

## Introduction

The OWASP Top 10 2013 contained a new entry: A9-Using Components with Known Vulnerabilities. Dependency-Check was created as one of the earliest SCA tools to scan applications (and their dependent libraries) and identify any known vulnerable components.

The problem with using known vulnerable components was described very well in a paper by Jeff Williams and Arshan Dabirsiaghi titled, “[Unfortunate Reality of Insecure Libraries](https://www.scribd.com/document/175866686/Aspect-Security-the-Unfortunate-Reality-of-Insecure-Libraries)”. The gist of the paper is that we as a development community include third party libraries in our applications that contain well known published vulnerabilities (such as those at the [National Vulnerability Database](https://nvd.nist.gov/vuln/search)).

Dependency-Check has a command line interface, a Maven plugin, a Gradle plugin, an Ant task and a number of integrations with build tooling such as Jenkins, GitHub Actions and Azure DevOps. The core engine contains a series of analyzers that inspect the project dependencies, collect pieces of information about the dependencies (referred to as evidence within the tool). The evidence is then used to identify the [Common Platform Enumeration (CPE)](https://nvd.nist.gov/products/cpe) for the given dependency. If a CPE is identified, a listing of associated [Common Vulnerability and Exposure (CVE)](https://www.cve.org/) entries are listed in a report. Other 3rd party services and data sources such as the NPM Audit API, the OSS Index, RetireJS, and Bundler Audit are utilized for specific technologies.

Dependency-Check automatically updates itself using the [NVD Data Feeds](https://nvd.nist.gov/vuln/data-feeds) hosted by NIST. ‘'’IMPORTANT NOTE:’’’ The initial download of the data may take ten minutes or more. If you run the tool at least once every seven days, only a small JSON file needs to be downloaded to keep the local copy of the data current.
