---
title: OWASP secureCodeBox
source: owasp.org
url: https://owasp.org/www-project-securecodebox/
collector: owasp
category: web-security
tags:
- web-security
- securecodebox
- security
- owasp
- project
date_collected: '2026-07-26T12:44:57.007266Z'
language: unknown
---

# OWASP secureCodeBox

> The OWASP secureCodeBox Project is a
>
> *kubernetes based, modularized toolchain*for*continuous security scans of your software project*. Its goal is to*orchestrate*and easily*automate*a bunch of*security-testing tools*out of the box. With secureCodeBox we provide a toolchain for continuous scanning of applications to find the low-hanging fruit issues early in the development process and free the resources of the penetration tester to concentrate on the major security issues.

## Description

The purpose of secureCodeBox is not to replace the penetration testers or make them obsolete. We strongly recommend to run extensive tests by experienced penetration testers on all your applications. For more information about this project, please have look at our [GitHub Repo secureCodeBox](https://github.com/secureCodeBox/secureCodeBox) or [online documentation](https://docs.securecodebox.io/).

Our *main goal* is to implement a major security testing platform and framework which enables developers and teams to integrate a bunch of security testing tools in their CI/CD environment or kubernetes environment as easy as possible. The flexibility and scalability of the platform architecture leads to features like *multi tenancy support*, *large scale (multi-) project testing*, support of distributed and private networks, customizable security test flows, which enables projects to test complex environments without implementing the complete security testing infrastructure on their own.

Secondly we try to foster a broad range of security tools to be easily integrated. Also we will try to integrate existing OWASP Projects as building blocks in our platform.

### Architecture

The secureCodeBox architecture is based on Kubernetes Custom Ressource Definitions (CRDs) and follows a function as a service (FaaS) principle. Therefore we implemented a Kubernetes operator which schedules *security scans* as *kubernetes jobs*. This architecture is much more resource efficient. Instead of long running microservices (SCB v1 Architecture), scans only consume cluster resources for a short amount of time.

## Roadmap

Our [project roadmap](https://docs.securecodebox.io/docs/architecture/#road-map) is documented on our [documentation site](https://docs.securecodebox.io/) in the [architecture section](https://docs.securecodebox.io/docs/architecture/)

## Quickstart secureCodeBox

For a quickstart see our [installation documentation](https://docs.securecodebox.io/docs/getting-started/installation) and the [starting your first scan documentation](https://docs.securecodebox.io/docs/getting-started/first-scans) on our comprehensive [documentation site](https://docs.securecodebox.io/).

## Community

You are welcome, please join us on… 👋

### Contributors

## Licensing

This Project is free software: you can redistribute it and/or modify it under the terms of the [Apache License 2.0](https://github.com/secureCodeBox/secureCodeBox/blob/master/LICENSE). OWASP secureCodeBox Project and any contributions are Copyright by the secureCodeBox authors.
