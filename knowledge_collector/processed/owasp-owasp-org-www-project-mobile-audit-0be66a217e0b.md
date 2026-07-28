---
title: OWASP Mobile Audit
source: owasp.org
url: https://owasp.org/www-project-mobile-audit/
collector: owasp
category: web-security
tags:
- web-security
- mobile
- audit
- api
- info
date_collected: '2026-07-26T12:44:21.535463Z'
language: unknown
---

# OWASP Mobile Audit

## Mobile Audit - Static Analysis and detecting malware in Android APKs

### Who is Mobile Audit for?

Mobile Audit focuses not only in the security testing and defensive use cases, the goal of the project is to become a complete homologation for Android APKs, which includes:

- Static Analysis (SAST): It will perform a full decompilation of the APK and extract all the possible information of it. It reports the different vulnerabilities and findings in the source code grouped by different categories. Also, it has full support on finding triage (change status and criticality).
- Malware Analysis: finds dangerous permissions and suspicious code.
- Best Practices of Secure Android Coding: tells developers in which parts of the code they are coding securely and where they are not.

It is aimed to different user profiles:

- Developers
- System Administrators
- Security Engineers

In each of the scans, it would have the following information:

- Application Info
- Security Info
- Components
- SAST Findings
- Best Practices Implemented
- Virus Total Info
- Certificate Info
- Strings
- Databases
- Files

For easy access there is a sidebar on the left page of the scan:

### Components

- **db**: PostgreSQL 3.11.5
- **nginx**: Nginx 1.23.3
- **rabbitmq**: RabbitMQ 3.11.5
- **worker**: Celery 5.2.2
- **web**: Mobile Audit App[3.0.0](https://github.com/mpast/mobileAudit)

### Main features

- Uses Docker for easy deployment in multiplatform environment
- Extract all information of the APK
- Analyze all the source code searching for weaknesses
- All findings are categorized and follows CWE standards
- Also highlight the Best Practices in Secure Android Implementation in the APK
- The findings can be edited and the false positives can be triaged and deleted
- All scan results can be exported to PDF
- User authentication and user management
- API v1 with Swagger and ReDoc
- TLS
- Dynamic page reload (WIP)
- Export to Markdown
- Export to CSV
- LDAP integration

### Integrations

#### Virus Total (API v3)

It checks if there has been an scan of the APK and extract all its information. Also, there is the possibility of uploading the APK is selected a property in the environment (Disabled by default).

#### Defect Dojo (API v2)

It is possible to upload the findings to the defect manager.

#### MalwareDB & Maltrail

It checks in the database if there are URLs in the APK that are related with Malware.

## Contribution

If you are interested in contributing with Mobile Audit:

- **Fork**this repo
- **Clone**the project to your own machine
- **Commit**changes to your own branch
- **Push**your work back up to your fork
- Submit a **Pull request**so that we can review your changes

## Licensing

This project is distributed under [GPL-3.0 License](https://github.com/mpast/mobileAudit/raw/main/LICENSE).

## Quickstart

### Installation

Using Docker-compose:

The provided
```
docker-compose.yml
```

file allows you to run the app locally in development. To start the container, run:
```
```
docker-compose up```
```

If there are changes to the local Application Dockerfile, you can build the image with
```
```
docker-compose build```
```

Once the application has launched, you can test the application by navigating to: http://localhost:8888/ to access the dashboard.

Also, there is a TLS version running in port 443, so you can test the application by navigating to: https://localhost/ to access the dashboard.

In each of the scans, it would have the following information:

- Application Info
- Security Info
- Components
- SAST Findings
- Best Practices Implemented
- Virus Total Info
- Certificate Info
- Strings
- Databases
- Files

For easy access there is a sidebar on the left page of the scan:

### API v1

REST API integration with Swagger and ReDoc.

#### Usage

- Endpoint to authenticate and get token:
  ```
  /api/v1/auth-token/
  ```
- Once authenticated, use header in all requests:
  ```
  Authorization: Token <ApiKey>
  ```

#### Swagger

#### ReDoc

#### Endpoints

- A JSON view of the API specification at
  ```
  /swagger.json
  ```
- A YAML view of the API specification at
  ```
  /swagger.yaml
  ```
- A swagger-ui view of your API specification at
  ```
  /swagger/
  ```
- A ReDoc view of your API specification at
  ```
  /redoc/
  ```

### Configuration

#### Nginx configuration

- TLS - port 443:
  ```
  nginx/app_tls.conf
  ```
- Standard - port 8888:
  ```
  nginx/app.conf
  ```

#### Docker configuration

There are two volumes in
```
docker-compose.yml
```

with the configurations. By default both 443 and 8888 ports will be available, but **use only TLS configuration for production deployments**.
```
```
- ./nginx/app.conf:/etc/nginx/conf.d/app.conf
- ./nginx/app_tls.conf:/etc/nginx/conf.d/app_tls.conf```
```

#### Environment variables

All the environment variables are in a
```
.env
```

file, there is an
```
.env.example
```

with all the variables needed. Also there are collected in
```
app/config/settings.py
```

:
```
```
CWE_URL = env('CWE_URL', 'https://cwe.mitre.org/data/definitions/')

MALWAREDB_ENABLED = env('MALWAREDB_ENABLED', True)
MALWAREDB_URL = env('MALWAREDB_URL', 'https://www.malwaredomainlist.com/mdlcsv.php')

VIRUSTOTAL_ENABLED = env('VIRUSTOTAL_ENABLED', False)
VIRUSTOTAL_URL = env('VIRUSTOTAL_URL', 'https://www.virustotal.com/')
VIRUSTOTAL_FILE_URL = env('VIRUSTOTAL_FILE_URL', 'https://www.virustotal.com/gui/file/')
VIRUSTOTAL_API_URL_V3 = env('VIRUSTOTAL_API_URL_V3', 'https://www.virustotal.com/api/v3/')
VIRUSTOTAL_URL_V2 = env('VIRUSTOTAL_API_URL_V2', 'https://www.virustotal.com/vtapi/v2/file/')
VIRUSTOTAL_API_KEY = env('VIRUSTOTAL_API_KEY', '')
VIRUSTOTAL_UPLOAD = env('VIRUSTOTAL_UPLOAD', False)

DEFECTDOJO_ENABLED = env('DEFECTDOJO_ENABLED', False)
DEFECTDOJO_URL = env('DEFECTDOJO_URL', 'http://defectdojo:8080/finding/')
DEFECTDOJO_API_URL = env('DEFECTDOJO_API_URL', 'http://defectdojo:8080/api/v2/')
DEFECTDOJO_API_KEY = env('DEFECTDOJO_API_KEY', '')```
```
