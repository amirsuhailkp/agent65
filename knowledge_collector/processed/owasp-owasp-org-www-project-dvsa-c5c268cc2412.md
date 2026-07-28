---
title: OWASP DVSA
source: owasp.org
url: https://owasp.org/www-project-dvsa/
collector: owasp
category: web-security
tags:
- web-security
- dvsa
- serverless
- application
- email
date_collected: '2026-07-26T12:44:07.807653Z'
language: unknown
---

# OWASP DVSA

# DVSA

### a Damn Vulnerable Serverless Application

Damn Vulnerable Serverless Application (DVSA) is a deliberately vulnerable application aiming to be an aid for security professionals to test their skills and tools in a legal environment, help developers better understand the processes of securing serverless applications and to aid both students & teachers to learn about serverless application security in a controlled class room environment.

The aim of DVSA is to practice some of the most common serverless vulnerabilities, with a simple straightforward interface.

Please note, there are both documented and undocumented vulnerabilities with this software. This is intentional. You are encouraged to try and discover as many issues as possible.

# Disclaimer

*Do not install DVSA on a production account*

We do not take responsibility for the way in which any one uses this application (DVSA). We have made the purposes of the application clear and it should not be used maliciously. We have given warnings and taken measures to prevent users from installing DVSA on to production accounts.

# How to use?

See [Deployment](https://www2.owasp.org/www-project-dvsa/#div-deployment) tab

# Cheat-Sheet

See instructions and demonstrations in the [LESSONS](https://github.com/OWASP/DVSA/tree/master/AWS) section.

# License

Damn Vulnerable Serverless Application (DVSA) is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Damn Vulnerable Serverless Application (DVSA) is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Damn Vulnerable Serverless Application (DVSA). If not, see http://www.gnu.org/licenses/.

## Founder

[Tal Melamed](/cdn-cgi/l/email-protection#a9ddc8c587c4ccc5c8c4cccde9c6dec8dad987c6dbce)[OWASP](https://www.owasp.org/index.php/User:Tal_Mel)[LinkedIn](https://www.linkedin.com/in/talmelamed/)

## Sponsors

# Deployment

#### [Application Repository](AWS/VIDEOS/reo_deploy.mp4)

- Deploy DVSA from the

  [AWS Serverless Application Repository](https://serverlessrepo.aws.amazon.com/applications/arn:aws:serverlessrepo:us-east-1:674087993380:applications~OWASP-DVSA)
- After deployment is complete. Click on ‘View CloudFormation Stack’
- Under ‘Outputs’ you will find the URL for the application (DVSA Website URL)

#### [Serverless Framework](AWS/VIDEOS/serverless_deploy.mp4)

You must run serverless deploy commands with an environment variable profile (e.g.
```
AWS_PROFILE=<aws-profile-name>
```

) instead of the serverless argument.

##### Clone Project

- ```
  git clone  ```

  [[email protected]](/cdn-cgi/l/email-protection):OWASP/DVSA.git

##### Install Serverless

- ```
  npm install -g serverless
  ```

##### Install AWS-CLI

- ```
  pip install awscli --upgrade --user  ```

##### Verify AWS-CLI Installation

- ```
  aws --version
  ```

If you get a “command not found” error, see the “Steps to Take after Installation” section [here](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html#install-tool-pip).

##### Configure AWS-CLI for your Account

- ```
  aws configure  ```

##### Install dependencies

- ```
  npm i
  ```

##### Deploy Backend

- ```
  sls deploy  ```

##### Build Client

- ```
  npm run-script client:build
  ```

##### Deploy Client

- ```
  sls client deploy  ```

## Running locally

#### Run Client

- ```
  npm run-script client:start
  ```

**Note**: This will only work if you previously deployed the backend. If this fails, confirm you still have a
```
be-stack.json
```

file at the root of this project.

#### Run Backend

- ```
  npm start  ```

If you want to point your local client to your local backend, edit your

```
be-stack.json```

and set

```
ServiceEndpoint```

to

```
http://localhost:3000```

. Note that you will still be using the Cognito pools in AWS.

## Email subscription

DVSA sends receipts in the email (which will help you in hacking it). You can use the built-in **Inbox** page within the application to get the emails and obtain the receipts.

**Note**: each user will be assigned an email from

```
mailsac.com```

which will be automatically verified. Real emails will be sent to their account and will appear in the application Inbox page. All this is

**transparent**to the user and the deployer).

**Note**: to make the email verification script work your default AWS region has to be “US East (N. Virginia)”, for example by setting

```
region = us-east-1```

in your ~/.aws/config file

**Alternatively**, if you want users to receive emails to their registered email account (e.g. gmail), use one of the followings:

- Send an email verification link to email address, by running the following command (after clicking on the received link, emails will **also**be sent to their actual email address):

```
aws ses verify-email-identity --email-address <your_email>```

- [Request a sending limit increase](https://console.aws.amazon.com/support/v1#/case/create?issueType=service-limit-increase&limitType=service-code-ses). This will allow your entire cloud account to send emails to any address.

## Example

Put whatever you like here: news, screenshots, features, supporters, or remove this file and don’t use tabs at all.

# Get Involved

Get involved in **DVSA**!

You do not have to be a security expert or a programmer to contribute.

Contact the Project Leader(s) to get involved, we welcome any type of suggestions and comments.

## Slack

Join out [Slack channel](https://join.slack.com/t/owasp/shared_invite/enQtNDI5MzgxMDQ2MTAwLTEyNzIzYWQ2NDZiMGIwNmJhYzYxZDJiNTM0ZmZiZmJlY2EwZmMwYjAyNmJjNzQxNzMyMWY4OTk3ZTQ0MzFhMDY)

## GitHub

The project is maintained in the [DVSA](https://github.com/OWASP/DVSA/).

Feel free to open or solve an [issue](https://github.com/OWASP/DVSA//issues).

# Roadmap

- 25 DEC 2018: http://serverless.fail (official website) was launched.
- 08 JAN 2019: v1.0 beta release [GitHub](https://github.com/OWASP/DVSA/)
- 01 FEB 2019: v1.0 official version.
- 01 APR 2019: Serverless is available trough the [AWS Serverlesss Repository](https://serverlessrepo.aws.amazon.com/applications/arn:aws:serverlessrepo:us-east-1:889485553959:applications~DVSA)
- 15 JAN 2020: v1.2 available on [Github](https://github.com/OWASP/DVSA/)and[AWS Serverless Repository](https://serverlessrepo.aws.amazon.com/applications/arn:aws:serverlessrepo:us-east-1:889485553959:applications~DVSA)

- 15 Oct 2018: Hello world! - DVSA was created by [Tal Melamed](https://www.linkedin.com/in/talmelamed/)
- 25 Dec 2018: http://serverless.fail - Launched
- 01 Jan 2019: Project was donated by [Protego Labs](https://protego.io)
- 03 Jan 2019: [The Register](https://www.theregister.co.uk/2019/01/03/damn_vulnerable_serverless_application/)
- 04 Jan 2019: [SDTimes](https://sdtimes.com/cloud/sd-times-news-digest-protegos-dvsa-quicklogic-acquires-ai-company-and-iot-interoperability/)
- 07 Jan 2019: [eWEEK](http://www.eweek.com/security/protego-labs-boosts-serverless-security-with-open-source-project)
- 08 Jan 2019: [Computer Weekly](https://www.computerweekly.com/news/252455429/Protego-Labs-launches-serverless-app-security-tool)
- 08 Jan 2019: [Technical.ly](https://technical.ly/baltimore/2019/01/08/protego-has-a-new-open-source-tool-to-provide-serverless-security-training/)
