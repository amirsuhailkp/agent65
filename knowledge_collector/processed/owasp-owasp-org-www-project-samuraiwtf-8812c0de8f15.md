---
title: OWASP SamuraiWTF
source: owasp.org
url: https://owasp.org/www-project-samuraiwtf/
collector: owasp
category: web-security
tags:
- web-security
- katana
- samuraiwtf
- environment
- web
date_collected: '2026-07-26T12:43:53.920390Z'
language: unknown
---

# OWASP SamuraiWTF

SamuraiWTF (Web Training Framework) is not just another vulnerable application - it’s a complete, robust framework for learning application security testing. It’s a project of OWASP (Open Web Application Security Project) and is designed to help individuals boost their cyber security skills. The framework is based on an Ubuntu-based basebox, making it fairly lightweight and easy to manage.

SamuraiWTF is a build system made up of multiple projects. It is best known for building a virtual machine that has been pre-configured to function as a web penetration testing and training environment. This environment is supported on Hyper-V, VirtualBox, and VMWare. It is built using Vagrant and Ansible to provide the most cross-platform mechanism to build and enhance the learning environment.

## Licensing

The scripts and resources belonging to this project itself are licensed under the Lesser GNU Public License version 3 (LGPL3). All software loaded into the VM, including the tools, targets, utilities, and operating system itself retain their original license agreements.

## Getting Involved

Contributors are very welcome and the contribution process is standard:

fork this project make your contribution submit a pull request Substantial or Regular contributors may also be brought in as full team members. This includes those who have made substantial contributions to previous versions of SamuraiWTF with the assumption they will continue to do so.

## Example

Put whatever you like here: news, screenshots, features, supporters, or remove this file and don’t use tabs at all.

# Katana

Katana is the package management tool and interface for SamuraiWTF 5.0+. Specifically Katana is intended to be used by instructors to set up a classroom lab that will be distrubuted to their students, or by self-study students to install the tools and targets they desire to use.

*IMPORTANT NOTES:*

- *Katana runs as root. It is intended only to be used in a temporary classroom environment. Don’t install it on any network that is important to you.*
- *Katana is installed as part of the*[SamuraiWTF Distribution](https://github.com/SamuraiWTF/samuraiwtf)and is not intended to be installed or run on a non-SamuraiWTF build.

## Using Katana

There are two ways to use Katana:

### Using Katana with the Web User Interface

By default, Katana should be running at
```
http://katana.wtf
```

from within your SamuraiWTF environment. Simply visit the Katana URL from any web browser inside the
environment. From the. GUI you will be able to install, stop, and start any of the Katana-defined tools and targets. Note that an internet connection is required to
install tools and targets.

### Using Katana from the Command Line

From a command line terminal inside your SamuraiWTF environment, simply type katana and the desired arguments. Katana supports the following arguments:

ArgumentDescription
```
list
```

List all available modules that are currently supported by Katana.
```
install <name>
```

Install the supplied module by name.
```
remove <name>
```

Remove the supplied module by name.
```
start <name>
```

Start the supplied module, assuming it is startable.
```
stop <name>
```

Stop the supplied module, assuming it is stopable.
```
status <name>
```

Output the status of the supplied module. This will include whether or not it is installed and if it is running (if it is runnable).
```
lock
```

Lock the current set of modules. This will require a restart of Katana.
```
--update
```

This is a special argument for updating katana to the latest version from this repo. For development purposes, an optional second parameter to pull from a specific branch.

## Samurai-Dojo

Samurai-Dojo is a set of vulnerable web applications created by and for the Samurai security training and testing distributions like SamuraiSTFU and SamuraiWTF. These vulnerable applications include:

- Dojo Basic: A simple PHP app that can be used for demos and exercises
- Dojo Scavenger: A student CTF-like challenge to test pentesting skills

### Vagrant

For ease of development a Vagrant configuration are available. The Vagrant configuration and deployment are stored in the following files:

- ```
  Vagrantfile  ```

  : contains a standard Vagrant config (no plugins required)
- ```
  bootstrap.sh
  ```

  : contains the installation script to get Samurai-Dojo up and running on Apache

## Development

The SamuraiWTF project team is currently rewriting dojo-basic. This effort is to
modify the project codebase to be a complete modern application. It is being worked on
in the [dojo-basic-2](https://github.com/SamuraiWTF/dojo-basic-2) repo.
