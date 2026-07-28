---
title: OWASP WebGoat
source: owasp.org
url: https://owasp.org/www-project-webgoat/
collector: owasp
category: web-security
tags:
- web-security
- webgoat
- security
- web
- vulnerabilities
date_collected: '2026-07-26T12:44:50.307221Z'
language: unknown
---

# OWASP WebGoat

## Learn the hack - Stop the attack

WebGoat is a deliberately insecure application that allows interested developers just like you to test vulnerabilities commonly found in Java-based applications that use common and popular open source components.

## Description

Web application security is difficult to learn and practice. Not many people have full blown web applications like online book stores or online banks that can be used to scan for vulnerabilities. In addition, security professionals frequently need to test tools against a platform known to be vulnerable to ensure that they perform as advertised. All of this needs to happen in a safe and legal environment.

Even if your intentions are good, we believe you should never attempt to find vulnerabilities without permission. The primary goal of the WebGoat project is simple: create a de-facto interactive teaching environment for web application security. In the future, the project team hopes to extend WebGoat into becoming a security benchmarking platform and a Java-based Web site Honeypot.

**WARNING 1:***While running this program your machine will be extremely
vulnerable to attack. You should disconnect from the Internet while using
this program.* WebGoat’s default configuration binds to localhost to minimize
the exposure.

**WARNING 2:***This program is for educational purposes only. If you attempt
these techniques without authorization, you are very likely to get caught. If
you are caught engaging in unauthorized hacking, most companies will fire you.
Claiming that you were doing security research will not work as that is the
first thing that all hackers claim.*

## Goals

Web application security is difficult to learn and practice. Not many people have full blown web applications like online book stores or online banks that can be used to scan for vulnerabilities. In addition, security professionals frequently need to test tools against a platform known to be vulnerable to ensure that they perform as advertised. All of this needs to happen in a safe and legal environment.

Even if your intentions are good, we believe you should never attempt to find vulnerabilities without permission. The primary goal of the WebGoat project is simple: create a de-facto interactive teaching environment for web application security. In the future, the project team hopes to extend WebGoat into becoming a security benchmarking platform and a Java-based Web site Honeypot.

## Learn in three steps

### Explain the vulnerability

Teaching is now a first class citizen of WebGoat, we explain the vulnerability. Instead of ‘just hacking’ we now focus on explaining from the beginning what for example a SQL injection is.

### Learn by doing

During the explanation of a vulnerability we build assignments which will help you understand how it works.

### Explain mitigation

At the end of each lesson you will receive an overview of possible mitigations which will help you during your development work.

## Lessons

WebGoat contains lesson for almost all OWASP Top 10 vulnerabilities and more…

### Future lessons

The following lessons are on our wish list:

- Lesson about cryptography (in progress)
- Lesson about path traversal (in progress)
- Session management
- More password reset lessons
- etc

See our [Github page](https://github.com/WebGoat/WebGoat/issues) for more information.

## Getting started

### 1. Run using Docker

Already have a browser and ZAP and/or Burp installed on your machine in this case you can run the WebGoat image directly using Docker.

Every release is also published on [DockerHub](https://hub.docker.com/r/webgoat/webgoat).
```
```
docker run -it -p 127.0.0.1:8080:8080 -p 127.0.0.1:9090:9090 webgoat/webgoat```
```

If you want to reuse the container, give it a name:
```
```
docker run --name webgoat -it -p 127.0.0.1:8080:8080 -p 127.0.0.1:9090:9090 webgoat/webgoat```
```

As long as you don’t remove the container you can use:
```
```
docker start webgoat```
```

This way, you can start where you left off. If you remove the container, you need to use
```
docker run
```

again.

### 2. Run using Docker with complete Linux Desktop

Instead of installing tools locally we have a complete Docker image based on running a desktop in your browser. This way you only have to run a Docker image which will give you the best user experience.
```
```
docker run -p 127.0.0.1:3000:3000 webgoat/webgoat-desktop```
```

### 3. Standalone

Download the latest WebGoat release from <https://github.com/WebGoat/WebGoat/releases>
```
```
java -Dfile.encoding=UTF-8 -Dwebgoat.port=8080 -Dwebwolf.port=9090 -jar webgoat-2023.5.jar```
```

Click the link in the log to start WebGoat.

## WebWolf the small helper

WebWolf is a separate web application which simulates an attackers machine. It makes it possible for us to make a clear distinction between what takes place on the attacked website and the actions you need to do as an “attacker”. WebWolf was introduced after a couple of workshops where we received feedback that there was no clear distinction between what was part of the “attackers” role and what was part of the “users” role on the website. The following items are supported in WebWolf:

### Host a file

Upload a file needed to be downloaded during an assignment

### E-mail client

WebWolf serves a mail client with which we can easily simulate sending an e-mail.

### Landing page for incoming requests

WebWolf can serve as a landing page to which you can make a call from inside an assignment, giving you as the attacker
information about the complete request. Think of it as a very simple form of
```
netcat
```

.

## Running

### 1. Docker

If you started the Docker image, WebWolf is already running. Please point your browser to: http://localhost:9090/WebWolf

### 2. Standalone

If you want to use the standalone version, you will need to download the jar file and start it:
```
```
java -jar webwolf-<<version>>.jar [--server.port=9090] [--server.address=localhost]```
```

By default, WebWolf starts on port 9090 with
```
--server.port
```

you can specify a different port. With
```
server.address
```

you
can bind it to a different address (default localhost)
