---
title: OWASP VulnerableApp
source: owasp.org
url: https://owasp.org/www-project-vulnerableapp/
collector: owasp
category: web-security
tags:
- web-security
- vulnerableapp
- project
- run
- will
date_collected: '2026-07-26T12:44:47.518702Z'
language: unknown
---

# OWASP VulnerableApp

# OWASP VulnerableApp

## Break it. Scan it. Reproduce it. Improve it.

OWASP VulnerableApp is a modular deliberately vulnerable application designed primarily for validating and benchmarking security scanners through reproducible test scenarios, while also supporting learning and experimentation.

### 🔍 What makes it different

Unlike traditional vulnerable applications, VulnerableApp is designed as a testable security ecosystem, not a static training app.

### It enables:

- 🔬 Scanner benchmarking for tools like Burp Suite, OWASP ZAP, and custom DAST engines
- 🧩 Modular vulnerability design that allows new scenarios without modifying core services
- 📊 Security regression testing across releases and environments
- 🎯 Realistic attack surface simulation for modern web application patterns
- 🧪 Deterministic vulnerability behavior for repeatable scanning results
- 🧠 Built for security engineers, researchers, and educators

### VulnerableApp helps you:

- Validate how security tools behave across known vulnerability patterns
- Build controlled environments for security experimentation
- Extend vulnerability coverage as new attack techniques emerge
- Run consistent, repeatable security testing pipelines

### ⚙️ Why it matters

Most vulnerable apps are:

- Static
- Hard to extend
- Designed only for manual learning

### VulnerableApp is built for:

automation, reproducibility, and evolution

### User Interface

## Running the project

There are 2 ways to run the project:

- The simplest way to run the project is using Docker containers which will run the full-fleged VulnerableApplication with all the components. For running as Docker application, follow following steps:
  - Download and Install [Docker Compose](https://docs.docker.com/compose/install/)
  - Clone this Github repository
  - Open the terminal and Navigate to the Project root directory
  - Run the command

    ```
    docker-compose pull && docker-compose up
    ```
  - Navigate to browser and visit

    ```
    http://localhost
    ```

    and this will give the User Interface for VulnerableApp.**Note**: The above steps will run the latest unreleased VulnerableApp version. If you want to run the latest released version, please use docker**latest**tag.
- Download and Install
- Another way to run the VulnerableApp is as standalone Vulnerable Application is:
  - Navigate to [Releases Section](https://github.com/SasanLabs/VulnerableApp/releases)in github and download the Jar for the latest released version
  - Open the terminal and navigate to the project root directory
  - Run the command

    ```
    java -jar VulnerableApp-*
    ```
  - Navigate to browser and visit

    ```
    http://localhost:9090/VulnerableApp
    ```

    . This will give the Legacy User Interface for the VulnerableApp.
- Navigate to

## Building the project

There are 2 ways in which this project can be built and used:

- As a Docker application which will help in running the full-fledged VulnerableApplication. For running as Docker application, follow following steps:
  - Build the docker image by running

    ```
    ./gradlew jibDockerBuild
    ```
  - Download [Docker-Compose](https://github.com/SasanLabs/VulnerableApp-facade/blob/main/docker-compose.yml)and run in the same directory

    ```
    docker-compose up
    ```
  - Navigate to browser and visit

    ```
    http://localhost
    ```

    and this will give the User Interface for VulnerableApp.
- Build the docker image by running
- As a SpringBoot application which will run with the Legacy UI or Rest API but gives the benefit of debugging and solving issues. This is the simple way,
  - Import the project into your favorite IDE and run it
  - Navigate to browser and visit:

    ```
    http://localhost:9090/VulnerableApp
    ```

    and this will give the Legacy User Interface for VulnerableApp which you can use to debug and test.

## Contributing to Project

There are multiple ways in which you can contribute to the project:

- If you are a developer and trying to start on to the project, then the suggestion is to go through the list of [issues](https://github.com/SasanLabs/VulnerableApp/issues)which contains
  ```
  good first issue
  ```

  which can be a good starter.
- If you are a developer or a security professional looking to add new Vulnerability type then you can Generate the Sample Vulnerability by running
  ```
  ./gradlew GenerateSampleVulnerability
  ```

  . It will generate the Sample Vulnerability template which has placeholders and comments. Modified files can be seen in the logs of the command or in the github history. You can navigate to those files, fill in the placeholders and then build the project to see the effect of the changes.
- In case you are looking to contribute to the project by publicising it or working on the growth of the project, please feel free to add your thoughts to discussions section or issues and we can discuss over them.

## Technologies used

- Java17
- Spring Boot
- ReactJS
- Javascript/TypeScript

### Connecting to embedded H2 database

For accessing database from browser, visit:
```
http://localhost:9090/VulnerableApp/h2
```

Database Connection properties:
```
```
JDBC Url: jdbc:h2:mem:testdb
User Name: admin
Password: hacker```
```

## Testing with Modern UI

VulnerableApp-facade provides a modern UI for VulnerableApp. To test your local changes with the Modern UI:

- **Prerequisite**: Ensure you have Docker and Docker-Compose installed.
- **Run Testing Script**:
  - On Windows:

    ```
    .\scripts\testWithModernUI.bat
    ```
  - On Linux/Mac:

    ```
    ./scripts/testWithModernUI.sh
    ```
- On Windows:

This script will build your local changes into a Docker image (
```
sasanlabs/owasp-vulnerableapp:unreleased
```

) and start the full stack (including facade, jsp, and php services) using
```
docker-compose.local.yml
```

.

- **Access the UI**: Navigate to
  ```
  http://localhost
  ```

  to see the modern UI with your changes.

## Currently handled Vulnerability types

- [JWT Vulnerability](https://github.com/SasanLabs/VulnerableApp/blob/master/src/main/java/org/sasanlabs/service/vulnerability/jwt/)
- [Command Injection](https://github.com/SasanLabs/VulnerableApp/tree/master/src/main/java/org/sasanlabs/service/vulnerability/commandInjection)
- [Cryptography Failures](https://github.com/SasanLabs/VulnerableApp/tree/master/src/main/java/org/sasanlabs/service/vulnerability/cryptographicFailures)
- [File Upload Vulnerability](https://github.com/SasanLabs/VulnerableApp/tree/master/src/main/java/org/sasanlabs/service/vulnerability/fileupload)
- [Path Traversal Vulnerability](https://github.com/SasanLabs/VulnerableApp/tree/master/src/main/java/org/sasanlabs/service/vulnerability/pathTraversal)
- [SQL Injection](https://github.com/SasanLabs/VulnerableApp/tree/master/src/main/java/org/sasanlabs/service/vulnerability/sqlInjection)
- [XSS](https://github.com/SasanLabs/VulnerableApp/tree/master/src/main/java/org/sasanlabs/service/vulnerability/xss)
- [XXE](https://github.com/SasanLabs/VulnerableApp/tree/master/src/main/java/org/sasanlabs/service/vulnerability/xxe)
- [Open Redirect](https://github.com/SasanLabs/VulnerableApp/tree/master/src/main/java/org/sasanlabs/service/vulnerability/urlRedirection)
- [SSRF](https://github.com/SasanLabs/VulnerableApp/tree/master/src/main/java/org/sasanlabs/service/vulnerability/ssrf)
- [IDOR](https://github.com/SasanLabs/VulnerableApp/tree/master/src/main/java/org/sasanlabs/service/vulnerability/idor)
- [Clickjacking](https://github.com/SasanLabs/VulnerableApp/tree/master/src/main/java/org/sasanlabs/service/vulnerability/clickjacking)
- [LDAP Injection](https://github.com/SasanLabs/VulnerableApp/tree/master/src/main/java/org/sasanlabs/service/vulnerability/ldapInjection)
- [Authentication Vulnerability](https://github.com/SasanLabs/VulnerableApp/tree/master/src/main/java/org/sasanlabs/service/vulnerability/authentication)

## Contact

In case you are stuck with any of the steps or understanding anything related to project and its goals, feel free to shoot a mail at [[email protected]](/cdn-cgi/l/email-protection) or raise an [issue](https://github.com/SasanLabs/VulnerableApp/issues) and we will try our best to help you.

## Documentation and References

- [Documentation](https://sasanlabs.github.io/VulnerableApp)
- [Design Documentation](https://sasanlabs.github.io/VulnerableApp/DesignDocumentation.html)
- [Owasp VulnerableApp](https://owasp.org/www-project-vulnerableapp/)
- [Overview video for OWASP Spotlight series](https://www.youtube.com/watch?v=HRRTrnRgMjs)
- [Overview Video](https://www.youtube.com/watch?v=AjL4B-WwrrA&ab_channel=OwaspVulnerableApp)

### Blogs

- [Overview of Owasp-VulnerableApp - Medium article](https://hussaina-begum.medium.com/an-extensible-vulnerable-application-for-testing-the-vulnerability-scanning-tools-cc98f0d94dbc)
- [Overview of Owasp-VulnerableApp - Blogspot post](https://hussaina-begum.blogspot.com/2020/10/an-extensible-vulnerable-application.html)
- [Introduction to Owasp VulnerableApp by Kenji Nakajima](https://jpn.nec.com/cybersecurity/blog/220520/index.html)
- [Gen AI based platform Shannon exploiting VulnerableApp](https://qiita.com/fiord/items/9351bcff6d646862f181)

### Usage of OWASP VulnerableApp

### Troubleshooting references

### Readme in other languages

## Roadmap

### Vision for the project:

The overall vision for the project is to implement a Platform capability such that it is easier to write vulnerable code and exposing that through an API and UI.

### Usage of the project:

This Project mainly targets 4 type of audience:

- Developers of Vulnerability Scanning tools
- New Vulnerability finders (for faster demonstration of the vulnerability)
- Security enthusiasts, Students who want to learn more about Security
- CTF organizers (A Platform to Host CTF by choosing vulnerabilities present in the project)

### Initial high level plan:

Basic idea for this project is to build an extensible framework which is driven by the configuration and developers who want to introduce new vulnerable code into the project need to do minimal boilerplate code and also the learning curve for configurations is minimum.

Looking at it, the first approach which comes into my mind is to give a framework similar to Spring i.e. something like annotation driven framework for including a vulnerability type and also for adding a new vulnerability to existing vulnerability type and also adding User Interface for the same.

- Milestone 1: Alpha release - Building extensible backend Platform
- Milestone 2: Beta release - Building extensible User Interface
- Milestone 3: Gamma release - Addition of 50 vulnerabilities using the above mentioned Platform
- Milestone 4: Release 1
- Milestone 5: Dev lifecycle integration

### Current State

For know about the current state please go to [Git Repository](https://github.com/SasanLabs/VulnerableApp) and also visit issues section for new enhancements,tech-debts and bugs.

### Timeframes

This is hard to estimate as this depends on the number of contributers but as of now i had already build some of the pieces of Backend platform and i have started building frontend platform but addition of 50 vulnerabilities can take quite a lot time. So Plan is to release this Project is near July 31 2020.

### Technology

Technologies used in this project are:

Majorly:

- Java-8
- SpringBoot
- Vanilla Javascript
- Vanilla CSS

But we are not limited to above technologies and can extend to new Horizons.
Incase you have any idea on technology and how it can suit us, please reach out to us on our [Slack-Channel](https://owasp.slack.com/messages/#owasp-vulnerableapp/).

### Challenges

There are many, please visit [Issues](https://github.com/SasanLabs/VulnerableApp/issues) for more information.
