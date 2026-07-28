---
title: OWASP Cervantes
source: owasp.org
url: https://owasp.org/www-project-cervantes/
collector: owasp
category: web-security
tags:
- web-security
- cervantes
- email
- protected
- owasp
date_collected: '2026-07-26T12:44:05.976045Z'
language: unknown
---

# OWASP Cervantes

Cervantes is an opensource collaborative platform for pentesters or red teams who want to save time to manage their projects, clients, vulnerabilities and reports in one place.

## Technologies

## Supported

OWASP FoundationSnykA2SECURE

## Features

- OpenSource
- Multiplatform
- Multilanguage
- Team Collaboration
- BuiltIn dashbaords and analytics
- Manage your clients and Offensive Security projects
- One click reports creation
- And more

## Contributors

Cervantes has been created, developed and maintained by [Ruben Mesquida](/cdn-cgi/l/email-protection#15676077707b3b78706664607c7174557a627466653b7a6772)

## Licensing

This program is free software: You can modify it under the terms of the Apache-2.0 License. OWASP Cervantes and any contributions are Copyright © by Ruben Mesquida

# Try Cervantes

There is a live demo running on <http://demo.cervantessec.org>.

The demo server has 3 users to show the different permission levels. The credentials for these users are:

UsernamePasswordRole[[email protected]](/cdn-cgi/l/email-protection)Admin123.Administrator[[email protected]](/cdn-cgi/l/email-protection)SuperUser123.SuperUser[[email protected]](/cdn-cgi/l/email-protection)User123.User

## Runtime requirements

- Docker
- Docker compose

## How to run it locally with Docker compose

- First you need to clone this repository
```
```
git clone https://github.com/CervantesSec/docker.git```
```

- After that you need to start your docker containers:
```
```
docker-compose -p cervantes -f docker-compose.yml up -d```
```

- After this, open your browser at http://localhost
- Default User is:
```
```
[email protected] - Admin123.```
```

## How to run it locally from source

- Install dotnet sdk from https://dotnet.microsoft.com/en-us/download
- Install PostgreSQL https://www.postgresql.org/download/
- Clone this repository
```
```
git clone https://github.com/CervantesSec/cervantes.git```
```

- In Cervantes.Web -> appsettings.json edit the DefaultConnection with your database parameters
```
```
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=localhost;Database=cervantes;Username=postgres;Password=postgres"
  },
  "Logging": {
    "LogLevel": {
      "Default": "Trace",
      "Microsoft": "Warning",
      "Microsoft.Hosting.Lifetime": "Information",
      "Cervantes.*": "Trace"
    }
  },
  "AllowedHosts": "*",
  "EmailConfiguration": {
    "Enabled": false,
    "Name": "Cervantes",
    "From": "[email protected]",
    "SmtpServer": "localhost",
    "SmtpPort": 1025,
    "SmtpUsername": "[email protected]",
    "SmtpPassword": "cervantes"
  },
  "JiraConfiguration": {
    "Enabled": false,
    "Auth": "Basic",
    "Url": "",
    "Project": "",
    "User": "",
    "Password": "",
    "ConsumerKey": "",
    "ConsumerSecret": "",
    "OAuthAccessToken": "",
    "OAuthTokenSecret": ""

  }
}```
```

- Run the project
```
```
dotnet run --project /CERVANTES_PATH/Cervantes.Web/```
```

- After this, open your browser at http://localhost:5001
- Default User is:
```
```
[email protected] - Admin123.```
```

## Alpha 0.5

**Note**: This is a alpha release. Please file new issues for any bugs you find in it.

### Changes

- Multilanguage Improvements
- Notifications Improvements
- SMTP Email support
- Minor bug fixes
- Fixed UI Bugs
- Checklists support OWASP MASTG & WSTG
- Report compliance OWASP WSTG & MASTG
- Implemented OWASP Score
- Basic Jira Integration
- Import vulns from CSV
- Data Vault Added
- Vuln Id Autogeneration
- Added Executive Summary Section
- Dark Mode Implemented

And more…

## Alpha 0.4

**Note**: This is a alpha release. Please file new issues for any bugs you find in it.

### Changes

- Report Generation Reworked
- Nmap Parser
- Import XML nmap scans
- Added Email Service
- Search Module
- Fixed Application Logs
- Project Languages
- Language
- Minor bug fixes
- Fixed UI Bugs
- Security Improvements
- Account Lockout Implementation
- Implemented Anti-XSS
- File Validation

And more…

## Alpha 0.3

**Note**: This is a alpha release. Please file new issues for any bugs you find in it.

### Changes

- Reformat Data Model
- Added Backup/Resore system
- Added Data Vault on Workspace
- Added feature to assign various targets to one vulnerability
- Added feature to added various targets to one task
- Project/Vuln Templates Improvements
- Fixed Login verification
- User creation improvements
- Fixed Date picker on Project/Task creation
- Fixed ORM problem on duplicate IDs
- Fixed minor UI bugs
- Minor UI Improvements
- Fixed. verification on some forms

## Contributing guidelines

- If you are contributing with code, make sure you have fork the project, and create a pull requests that contains amongst other things a description of your changes.
- Keep your changes small. The smaller the changeset the more likely to be merged. This applies to code an documentation.

# Contributor Covenant Code of Conduct

## Our Pledge

In the interest of fostering an open and welcoming environment, we as contributors and maintainers pledge to making participation in our project and our community a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, sex characteristics, gender identity and expression, level of experience, education, socio-economic status, nationality, personal appearance, race, religion, or sexual identity and orientation.

## Our Standards

Examples of behavior that contributes to creating a positive environment include:

- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

Examples of unacceptable behavior by participants include:

- The use of sexualized language or imagery and unwelcome sexual attention or advances
- Trolling, insulting/derogatory comments, and personal or political attacks
- Public or private harassment
- Publishing others’ private information, such as a physical or electronic address, without explicit permission
- Other conduct which could reasonably be considered inappropriate in a professional setting

## Our Responsibilities

Project maintainers are responsible for clarifying the standards of acceptable behavior and are expected to take appropriate and fair corrective action in response to any instances of unacceptable behavior.

Project maintainers have the right and responsibility to remove, edit, or reject comments, commits, code, wiki edits, issues, and other contributions that are not aligned to this Code of Conduct, or to ban temporarily or permanently any contributor for other behaviors that they deem inappropriate, threatening, offensive, or harmful.

## Scope

This Code of Conduct applies both within project spaces and in public spaces when an individual is representing the project or its community. Examples of representing a project or community include using an official project e-mail address, posting via an official social media account, or acting as an appointed representative at an online or offline event. Representation of a project may be further defined and clarified by project maintainers.

## Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be reported by contacting the project team lead. All complaints will be reviewed and investigated and will result in a response that is deemed necessary and appropriate to the circumstances. The project team is obligated to maintain confidentiality with regard to the reporter of an incident. Further details of specific enforcement policies may be posted separately.

Project maintainers who do not follow or enforce the Code of Conduct in good faith may face temporary or permanent repercussions as determined by other members of the project’s leadership.

## Attribution

This Code of Conduct is adapted from the [Contributor Covenant](https://www.contributor-covenant.org), version 1.4,
available at https://www.contributor-covenant.org/version/1/4/code-of-conduct.html

For answers to common questions about this code of conduct, see https://www.contributor-covenant.org/faq
