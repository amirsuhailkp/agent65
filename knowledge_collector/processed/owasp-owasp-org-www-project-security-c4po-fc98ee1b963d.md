---
title: OWASP Security-C4PO
source: owasp.org
url: https://owasp.org/www-project-security-c4po/
collector: owasp
category: web-security
tags:
- web-security
- security-c4po
- c4po
- docker
- run
date_collected: '2026-07-26T12:44:40.623433Z'
language: unknown
---

# OWASP Security-C4PO

Welcome to the OWASP page for Security-C4PO, an open-source pentest reporting tool.
Security-C4PO is an open-source web-application for managing and documenting penetration tests.
It aims to streamline and automate the often time-consuming task of creating comprehensive reports by providing an intuitive web-based interface that facilitates the content of the [OWASP TESTING GUIDE](https://owasp.org/www-project-web-security-testing-guide/v42/).

## Description

C4PO provides pentesters the perfect solution when it comes to reporting security vulnerabilities and other risk-related findings. It makes the pain of copy and paste a thing of the past. The interface is designed to guide you through your pentests in the style of the OWASP Testing Guide. Before creating your report we show you a summary through visualizing findings and their statuses.

Interested? Checkout our [Official Release Trailer](https://www.youtube.com/watch?v=DXVx4BFckmY)!

### What can it do for you?

- Great starting point for beginners
- Easy way to do pentests without prior knowledge of hacking
- Designed to avoid “Analysis Paralysis”
- Central overview and organisation of pentests
- Saves money compared to hiring third-party pentesters or tools
- Completely open-source under the Apache-2.0 license
- Accelerate your pentest delivery to better serve clients
- Boost margins by slashing report creation time
- Automatically build actionable reports

## Licensing

Security C4PO is licensed under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) License. Please see the [LICENSE](https://github.com/marcel-haag/security-c4po/blob/main/LICENSE.md) file for more information.

We hope you find Security C4PO useful for managing and generating pentest reports. If you encounter any issues or have suggestions for improvement, please feel free to create an issue on the [issue tracker](https://github.com/Marcel-Haag/security-c4po/issues).

## Techstack

### Development server

Execute
```
c4po-dev.sh
```

and all services will run on a dev server.
You can reach the application by entering http://localhost:4200 in you browser.

### Testuser Credentials

- Username: c4po
- Password: Test1234!

## Application Architecture

## Data Structure

## Docker Hub Setup

- Pull all images:
  - ```
    docker image pull --all-tags cellecram/security-c4po
    ```
- Create network:
  - ```
    docker network create -d bridge c4po
    ```
- Start images:
  - ```
    docker run --network=c4po --name c4po-keycloak -d -p 8080:8080 cellecram/security-c4po:keycloak
    ```
  - ```
    docker run --network=c4po --name c4po-db -d -p 27017:27017 cellecram/security-c4po:mongo
    ```
  - ```
    docker run --network=c4po --name c4po-angular -d -p 4200:4200 cellecram/security-c4po:angular
    ```
  - ```
    docker run --network=c4po -e "SPRING_PROFILES_ACTIVE=COMPOSE" --name c4po-api -d -p 8443:8443 cellecram/security-c4po:api
    ```
  - ```
    docker run --network=c4po -e "SPRING_PROFILES_ACTIVE=COMPOSE" --name c4po-reporting -d -p 8444:8444 cellecram/security-c4po:reporting
    ```

### OR: Run Script (Docker Hub)

Execute
```
c4po-prod.sh
```

and all services will be pulled from Docker Hub and started.
You can reach the application by entering
```
http://localhost:4200
```

in you browser.

## Contributing to Security-C4PO

First off, thanks for taking the time to contribute! 👍

The following is a set of guidelines for contributing to this project and its packages, which are hosted on GitHub. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

### Issue Board

## How Can I Contribute?

### Reporting Bugs

This section guides you through submitting a bug report. Following these guidelines helps maintainers and the community understand your report.

Explain the problem and include additional details to help maintainers reproduce the problem:

- **Use a clear and descriptive title**for the issue to identify the problem.
- **Describe the exact steps which reproduce the problem**in as many details as possible. For example, start by explaining how you started the application, e.g. which command exactly you used in the terminal, or how you started the application otherwise. When listing steps,**don’t just say what you did, but explain how you did it**.
- **Describe the behavior you observed after following the steps**and point out what exactly is the problem with that behavior.
- **Explain which behavior you expected to see instead and why.**
- **Include screenshots and animated GIFs**which show you following the described steps and clearly demonstrate the problem.
- **If the problem wasn’t triggered by a specific action**, describe what you were doing before the problem happened.

### Suggesting Enhancements

This section guides you through submitting an enhancement suggestion, including completely new features and minor improvements to existing functionality. Following these guidelines helps maintainers and the community understand your suggestion :pencil: and find related suggestions :mag\_right:.

- **Use a clear and descriptive title**for the issue to identify the suggestion.
- **Provide a step-by-step description of the suggested enhancement**in as many details as possible.
- **Include screenshots, mock-ups or animated GIFs**which help you demonstrate the steps or point out the part which the suggestion is related to.
- **Explain why this enhancement would be useful**

## Code of Conduct

Use the following conventions:

- Branch:
  ```
  <initial>_c4po_<issuenumber>
  ```
- Commit:
  ```
  feat: <What was implemented?>
  ```

  or
  ```
  fix: <What got fixed?>
  ```

  By participating, you are expected to uphold this code.

## Local development

Security-C4PO and all it’s included micorservices can be developed locally.
Execute
```
c4po-dev.sh
```

and all services will run on a dev server.

#### Testuser Credentials:

- Username: c4po
- Password: Test1234!

#### Technical Environment Requirements

- Docker / Docker-compose
- OpenJDK 11
- Node 14.15.1 / npm 6.14.8

#### Helpfull Tools

- mongoDB Compass
- Postman
