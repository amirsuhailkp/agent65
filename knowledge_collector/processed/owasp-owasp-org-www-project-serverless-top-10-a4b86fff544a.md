---
title: OWASP Serverless Top 10
source: owasp.org
url: https://owasp.org/www-project-serverless-top-10/
collector: owasp
category: web-security
tags:
- web-security
- serverless
- top
- owasp
- security
date_collected: '2026-07-26T12:45:49.754275Z'
language: unknown
---

# OWASP Serverless Top 10

# Main

The [OWASP Top 10: Serverless Interpretation](https://github.com/OWASP/Serverless-Top-10-Project/raw/master/OWASP-Top-10-Serverless-Interpretation-en.pdf) is now available.

## Introduction

When adopting serverless technology, we eliminate the need to develop a server to manage our application. By doing so, we also pass some of the security threats to the infrastructure provider such as [AWS](https://aws.amazon.com/serverless), [Azure](https://azure.microsoft.com/en-us/services/functions/) and [GCP](https://cloud.google.com/functions/). In addition to the many advantages of serverless application development, such as cost and scalability, some security aspects are also handed to our service provider. Serverless services run code without provisioning or managing servers and the code is executed only when needed.

However, even if these applications are running without a managed server, they still execute code. If this code is written in an insecure manner, it can still be vulnerable to application-level attacks.

The interpretation report examines the differences in attack vectors, security weaknesses, and the business impact of application attacks on in the serverless world, and, most importantly, the report will suggest ways to to prevent them. As we will be able to see in the report, attack and defense techniques are different from what we used to in the traditional application world.

After that, an open-call will be established to collect data in the wild and establishing the official Serverless Top 10 Report.

## Purpose

OWASP Serverless Top 10 aims at educating practitioners and organizations about the consequences of the most common serverless application security vulnerabilities, as well as providing basic techniques to identify and protect against them.

## License

The OWASP Serverless Top 10 is free to use. It is licensed under the [Creative Commons Attribution-ShareAlike 4.0 license (CC BY-SA 4.0)](http://creativecommons.org/licenses/by-sa/4.0/).

## Founder

[Tal Melamed](/cdn-cgi/l/email-protection#7b0f1a1755161e171a161e1f3b140c1a080b5514091c)[OWASP](https://www.owasp.org/index.php/User:Tal_Mel)[LinkedIn](https://www.linkedin.com/in/talmelamed/)

## Sponsors

## Contributors

*Report Reviewers* Assaf Hefetz, SnykErez Metula, AppSec LabsErez Yalon, CheckmarxFrank M. Catucci, OWASPGuy Bernhart-Magen, IntelHemed Gur Ary, OWASPJeff Williams, Contrast SecurityJim DelGrosso, SynopsysJochanan Sommerfeld, RDuckKobi Lechner, INFINIDATLimor Sylvie Kessem, IBMMarcin Hoppe, Auth0Mark Johnston, GoogleMartin Knobloch, OWASPMatthew Henderson, MicrosoftMatteo Meucci, Minded SecurityOwen Pendlebury, OWASPPaco Hope, AWSPatrick Laverty, Rapid7Rupack Ganguly, Serverless Inc.Tanya Janca, MicrosoftTash Norris, Capital OneTom Brennan, IOActiveYan Cui, DAZNYoussef Elmalty, AWS

# Get Involved

Get involved in  **OWASP Serverless Top 10**!

You do not have to be a security expert or a programmer to contribute. Contact the Project Leader(s) to get involved, we welcome any type of suggestions and comments.

Possible ways to get contribute:

- We are actively looking for organizations and individuals that will provide vulnerability prevalence data.
- Translation efforts (later stages)
- Assisting in the development of related and relevant tools (e.g. DVSA)

## Slack

Join out [Slack channel](https://join.slack.com/t/owasp/shared_invite/enQtNDI5MzgxMDQ2MTAwLTEyNzIzYWQ2NDZiMGIwNmJhYzYxZDJiNTM0ZmZiZmJlY2EwZmMwYjAyNmJjNzQxNzMyMWY4OTk3ZTQ0MzFhMDY)

## GitHub

The project is maintained in the [OWASP Serverless Top 10](https://github.com/OWASP/Serverless-Top-10-Project/).

Feel free to open or solve an [issue](https://github.com/OWASP/Serverless-Top-10-Project/issues).

Ready to contribute directly into the repo? Great! Just make sure you read the
[How to Contribute guide](https://github.com/OWASP/Serverless-Top-10-Project/blob/master/CONTRIBUTING.md).

## News & Events

- [01 Sep 2018]: Hello World! Project was donated by [Protego Labs](https://protego.io)
- [18 Sep 2018]: Join our [Slack-channel](https://join.slack.com/t/owasp/shared_invite/enQtNDI5MzgxMDQ2MTAwLTEyNzIzYWQ2NDZiMGIwNmJhYzYxZDJiNTM0ZmZiZmJlY2EwZmMwYjAyNmJjNzQxNzMyMWY4OTk3ZTQ0MzFhMDY)**#project-sls-top-10**.
- [22 Sep 2018]: Follow our [Git Repo](https://github.com/OWASP/Serverless-Top-10-Project/).
- [25 Oct 2018]: **First Release!**
- [02 Nov 2018]: OWASP [Official Announcement](https://owasp.blogspot.com/2018/11/serverless-top-10-added-to-project.html)

# Translation Efforts

- **Chinese:**[OWASP Top 10 - Serverless Interpretation 中文版（PDF)](https://github.com/OWASP/Serverless-Top-10-Project/raw/master/2018/cn/OWASP-Top-10-Serverless-Interpretation-cn-v1.0.pdf)

项目牵头人：肖文棣、王颉（[[email protected]](/cdn-cgi/l/email-protection)）
项目组成员：刘晓辉、李宇全、明敏、王斌（排名不分先后，按姓氏拼音排列）

## Planned Projects

- Serverless Security Top 10
- [DVSA](https://github.com/OWASP/DVSA)-**D**amn**V**ulnerable**S**erverless**A**pplication

## Roadmap

Coming soon!
