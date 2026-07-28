---
title: OWASP DevSecOps Guideline
source: owasp.org
url: https://owasp.org/www-project-devsecops-guideline/
collector: owasp
category: web-security
tags:
- web-security
- project
- owasp
- devsecops
- guideline
date_collected: '2026-07-26T12:45:21.351804Z'
language: unknown
---

# OWASP DevSecOps Guideline

The OWASP DevSecOps Guideline explains how we can implement a secure pipeline and use best practices and introduce tools that we can use in this matter. Also, the project is trying to help us promote the shift-left security culture in our development process. This project helps any companies of each size that have a development pipeline or, in other words, have a DevOps pipeline. We try to draw a perspective of a secure DevOps pipeline during this project and then improve it based on our customized requirements.

The Ideal goal is “detect security issues (by design or application vulnerability) as fast as possible.”

### Initial steps:

At first, we consider to implement the following steps in a basic pipeline:

- Scan git repositories for finding potential credentials leakage.
- SAST (Static Application Security Test)
- SCA (Software Composition Analysis)
- IAST (Interactive Application Security Testing)
- DAST (Dynamic Application Security Test)
- IaC Scanning (Scanning Terraform, HelmChart code to find misconfiguration)
- Infrastructure scanning
- Compliance check

## Latest

You can [read the latest development documents in our official GitHub repository](https://github.com/OWASP/DevSecOpsGuideline/tree/master/documents) or view the latest content at [latest](latest/).

### Contributions

Feel free to contribute to this project; any contributors are welcome to make a pull request on [the project repo](https://github.com/OWASP/DevSecOpsGuideline).

### Related Project[s]:

## Contributing

Contributing to this project is so simple. Please go to the project’s [GitHub repo](https://github.com/OWASP/DevSecOpsGuideline) and send a new pull request.

Please do not hesitate to create an issue if you have any ideas or recommendations.[Share your opinion or recommandation](https://github.com/OWASP/DevSecOpsGuideline/issues)
