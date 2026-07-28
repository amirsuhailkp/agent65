---
title: OWASP VulnerableApp-Facade
source: owasp.org
url: https://owasp.org/www-project-vulnerableapp-facade/
collector: owasp
category: web-security
tags:
- web-security
- vulnerable
- vulnerableapp-facade
- applications
- application
date_collected: '2026-07-26T12:44:48.118779Z'
language: unknown
---

# OWASP VulnerableApp-Facade

# Owasp VulnerableApp-facade

As we are seeing a lot of technological enhancements in the industry in the past few years, these technical enhancements are solving one or the other problem however, with that they also bring few different vulnerabilities. Vulnerable Applications are generally written in one of the tech stacks like either Node.js or Java with a SQL or NoSQL database etc. and hence they are not able to expand to a whole new set of vulnerabilities that are present in other technologies. Also adding more vulnerabilities in a single vulnerable application makes it heavier and complex which finally makes it unmaintainable. So VulnerableApp-facade is built to solve this problem by building a distributed farm of Vulnerable Applications such that they can be built agnostic to tech stacks.

## High Level Design Details

**VulnerableApp-facade** is a small component which acts as a webserver and a gateway. It routes the calls to different Vulnerable Applications which are registered with it based on an url pattern. It also exposes a schema/contract (Vulnerability Definition) and if a vulnerable application adhere to that then it will be able to interact and route the traffic to that vulnerable application. It also provides the generic skeleton UI which it builds by reading the provided schema (Vulnerability Definition) from the vulnerable application and then loads the UI specific to vulnerable application inside the skeleton UserInterface.

### Glimpse of the Owasp VulnerableApp-Facade

## How to run the project

VulnerableApp-facade is a farm of vulnerable applications where each application runs as a docker container. VulnerableApp-facade has
```
docker-compose.yml
```

file which contains docker configuration of other vulnerable applications along with docker configuration of VulnerableApp-facade.

### Simple Start

In order to run entire suit please follow the below steps:

- Download and Install [Docker Compose](https://docs.docker.com/compose/install/).
- Clone the github repository
- Open the terminal and navigate to the Project root directory
- Run the command:
  ```
  docker-compose pull && docker-compose up
  ```
- Navigate to browser and visit
  ```
  http://localhost
  ```

  to play with the application.

### Advanced Start

As [docker-compose.yml](https://github.com/SasanLabs/VulnerableApp-facade/blob/main/docker-compose.yml) contains all the applications which adhere to the schema of VulnerableApp-facade so in case you are looking for specific vulnerable applications like only Java related vulnerable applications then remove other vulnerable applications from [docker-compose.yml](https://github.com/SasanLabs/VulnerableApp-facade/blob/main/docker-compose.yml) and then run steps as mentioned in the [Simple start step](#simple-start).

## How to Contribute to the project

VulnerableApp-facade have majorly 2 components:

- React UI component
- Lua module

**React UI component** is used to load the skeleton UserInterface and Lua module is used to merge the Vulnerability Definitions exposed by different vulnerable applications.
In order to do changes in React UI component,

- Start the VulnerableApplication-facade using steps mentioned at [Simple Start](#simple-start). This is an important step as it will start the underlying VulnerableApplications which will be invoked by the Facade UI internally. Consider the underlying VulnerableApplications as the backend for Facade application.
- Navigate to
  ```
  facade-app
  ```

  folder
- Do the code changes
- Run
  ```
  npm run start
  ```

  which will start the npm server.
- Navigate to
  ```
  http://localhost:3000
  ```

  to verify/view the changes

**Lua module** is used for handling the Nginx configuration and communication between facade application and VulnerableApplications which is the backend for facade application.
In order to make changes in Lua module, the easy way is to add the changes in the lua files and build the docker image with those changes
by executing command:
```
docker build . -t sasanlabs/owasp-vulnerableapp-facade:latest
```

and then run the project as mentioned at [How to run the project](#how-to-run-the-project)

Before raising the PR with UI changes please execute
```
npm run pretty
```

command in
```
facade-app
```

folder to auto handle formatting of javascript/typescript files.

## Integrated Vulnerable Applications

## Contact

Please raise a github issue for enhancement/issues in VulnerableApp-facade or send email to [[email protected]](/cdn-cgi/l/email-protection) regarding queries
we will try to resolve issues asap.

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

### Troubleshooting references

## Other links

## Example

Put whatever you like here: news, screenshots, features, supporters, or remove this file and don’t use tabs at all.
