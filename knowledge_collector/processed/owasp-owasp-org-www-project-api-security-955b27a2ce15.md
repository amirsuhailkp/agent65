---
title: OWASP API Security Project
source: owasp.org
url: https://owasp.org/www-project-api-security/
collector: owasp
category: web-security
tags:
- web-security
- api
- security
- owasp
- project
date_collected: '2026-07-26T12:43:48.177800Z'
language: unknown
---

# OWASP API Security Project

Check out the new
[OWASP API Security Top 10 2023](https://owasp.org/API-Security/editions/2023/en/0x00-header/)!

## What is API Security?

A foundational element of innovation in today’s app-driven world is the API. From banks, retail and transportation to IoT, autonomous vehicles and smart cities, APIs are a critical part of modern mobile, SaaS and web applications and can be found in customer-facing, partner-facing and internal applications. By nature, APIs expose application logic and sensitive data such as Personally Identifiable Information (PII) and because of this have increasingly become a target for attackers. Without secure APIs, rapid innovation would be impossible.

API Security focuses on strategies and solutions to understand and mitigate the unique vulnerabilities and security risks of Application Programming Interfaces (APIs).

## API Security Top 10 2023

Here is a sneak peek of the 2023 version:

- [API1:2023 - Broken Object Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/)

  APIs tend to expose endpoints that handle object identifiers, creating a wide attack surface of Object Level Access Control issues. Object level authorization checks should be considered in every function that accesses a data source using an ID from the user.

  [Continue reading](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/).
- [API2:2023 - Broken Authentication](https://owasp.org/API-Security/editions/2023/en/0xa2-broken-authentication/)

  Authentication mechanisms are often implemented incorrectly, allowing attackers to compromise authentication tokens or to exploit implementation flaws to assume other user’s identities temporarily or permanently. Compromising a system’s ability to identify the client/user, compromises API security overall.

  [Continue reading](https://owasp.org/API-Security/editions/2023/en/0xa2-broken-authentication/).
- [API3:2023 - Broken Object Property Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa3-broken-object-property-level-authorization/)

  This category combines

  [API3:2019 Excessive Data Exposure](https://owasp.org/API-Security/editions/2019/en/0xa3-excessive-data-exposure/)and[API6:2019 - Mass Assignment](https://owasp.org/API-Security/editions/2019/en/0xa6-mass-assignment/), focusing on the root cause: the lack of or improper authorization validation at the object property level. This leads to information exposure or manipulation by unauthorized parties.[Continue reading](https://owasp.org/API-Security/editions/2023/en/0xa3-broken-object-property-level-authorization/).
- [API4:2023 - Unrestricted Resource Consumption](https://owasp.org/API-Security/editions/2023/en/0xa4-unrestricted-resource-consumption/)

  Satisfying API requests requires resources such as network bandwidth, CPU, memory, and storage. Other resources such as emails/SMS/phone calls or biometrics validation are made available by service providers via API integrations, and paid for per request. Successful attacks can lead to Denial of Service or an increase of operational costs.

  [Continue reading](https://owasp.org/API-Security/editions/2023/en/0xa4-unrestricted-resource-consumption/).
- [API5:2023 - Broken Function Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa5-broken-function-level-authorization/)

  Complex access control policies with different hierarchies, groups, and roles, and an unclear separation between administrative and regular functions, tend to lead to authorization flaws. By exploiting these issues, attackers can gain access to other users’ resources and/or administrative functions.

  [Continue reading](https://owasp.org/API-Security/editions/2023/en/0xa5-broken-function-level-authorization/).
- [API6:2023 - Unrestricted Access to Sensitive Business Flows](https://owasp.org/API-Security/editions/2023/en/0xa6-unrestricted-access-to-sensitive-business-flows/)

  APIs vulnerable to this risk expose a business flow - such as buying a ticket, or posting a comment - without compensating for how the functionality could harm the business if used excessively in an automated manner. This doesn’t necessarily come from implementation bugs.

  [Continue reading](https://owasp.org/API-Security/editions/2023/en/0xa6-unrestricted-access-to-sensitive-business-flows/).
- [API7:2023 - Server Side Request Forgery](https://owasp.org/API-Security/editions/2023/en/0xa7-server-side-request-forgery/)

  Server-Side Request Forgery (SSRF) flaws can occur when an API is fetching a remote resource without validating the user-supplied URI. This enables an attacker to coerce the application to send a crafted request to an unexpected destination, even when protected by a firewall or a VPN.

  [Continue reading](https://owasp.org/API-Security/editions/2023/en/0xa7-server-side-request-forgery/).
- [API8:2023 - Security Misconfiguration](https://owasp.org/API-Security/editions/2023/en/0xa8-security-misconfiguration/)

  APIs and the systems supporting them typically contain complex configurations, meant to make the APIs more customizable. Software and DevOps engineers can miss these configurations, or don’t follow security best practices when it comes to configuration, opening the door for different types of attacks.

  [Continue reading](https://owasp.org/API-Security/editions/2023/en/0xa8-security-misconfiguration/).
- [API9:2023 - Improper Inventory Management](https://owasp.org/API-Security/editions/2023/en/0xa9-improper-inventory-management/)

  APIs tend to expose more endpoints than traditional web applications, making proper and updated documentation highly important. A proper inventory of hosts and deployed API versions also are important to mitigate issues such as deprecated API versions and exposed debug endpoints.

  [Continue reading](https://owasp.org/API-Security/editions/2023/en/0xa9-improper-inventory-management/).
- [API10:2023 - Unsafe Consumption of APIs](https://owasp.org/API-Security/editions/2023/en/0xaa-unsafe-consumption-of-apis/)

  Developers tend to trust data received from third-party APIs more than user input, and so tend to adopt weaker security standards. In order to compromise APIs, attackers go after integrated third-party services instead of trying to compromise the target API directly.

  [Continue reading](https://owasp.org/API-Security/editions/2023/en/0xaa-unsafe-consumption-of-apis/).

## Licensing

**The OWASP API Security Project documents are free to use!**

The OWASP API Security Project is licensed under the [Creative Commons
Attribution-ShareAlike 4.0 license](https://creativecommons.org/licenses/by-sa/4.0/), so you can copy, distribute and
transmit the work, and you can adapt it, and use it commercially, but all
provided that you attribute the work and if you alter, transform, or build upon
this work, you may distribute the resulting work only under the same or similar
license to this one.

## Founders

## Leaders

## 2023 Sponsors

## 2023 Contributors

247arjun, abunuwas, Alissa Knight, Arik Atar, aymenfurter, Corey J. Ball, cyn8, d0znpp, Dan Gordon, donge, Dor Tumarkin, faizzaidi, gavjl, guybensimhon, Inês Martins, Isabelle Mauny, Ivan Novikov, jmanico, Juan Pablo, k7jto, LaurentCB, llegaz, Maxim Zavodchik, MrPRogers, planetlevel, rahulk22, Roey Eliyahu, Roshan Piyush, securitylevelup, sudeshgadewar123, Tatsuya-hasegawa, tebbers, vanderaj, wenz, xplo1t-sec, Yaniv Balmas, ynvb

## 2019 Contributors

007divyachawla, Abid Khan, Adam Fisher, anotherik, bkimminich, caseysoftware, Chris Westphal, dsopas, DSotnikov, emilva, ErezYalon, flascelles, Guillaume Benats, IgorSasovets, Inonshk, JonnySchnittger, jmanico, jmdx, Keith Casey, kozmic, LauraRosePorter, Matthieu Estrade, nathanawmk, PauloASilva, pentagramz, philippederyck, pleothaud, r00ter, Raj kumar, Sagar Popat, Stephen Gates, thomaskonrad, xycloops123, Raphael Hagi, Eduardo Bellis, Bruno Barbosa

## Google Group

Join the discussion on the [OWASP API Security Project Google group](https://groups.google.com/a/owasp.org/d/forum/api-security-project).

This is the best place to introduce yourself, ask questions, suggest and discuss any topic that is relevant to the project.

## GitHub Discussions

You can also use [GitHub Discussions](https://github.com/OWASP/API-Security/discussions) as a place to connect with other community
members, asking questions or sharing ideas.

## GitHub

The project is maintained in the [OWASP API Security Project repo](https://github.com/OWASP/API-Security).

**The latest changes are under the** .
```
develop
```

branch

Feel free to open or solve an [issue](https://github.com/OWASP/API-Security/issues).

Ready to contribute directly into the repo? Great! Just make sure you read the
[How to Contribute guide](https://github.com/OWASP/API-Security/blob/master/CONTRIBUTING.md).

- **Jun 28th, 2024**

  OWASP API Security Project - Past Present and Future @ OWASP Global AppSec Lisbon 2024 (

  [YouTube](https://www.youtube.com/watch?v=hn4mgTu5izg))
- **Jun 3rd, 2024**
- **Jun 5th, 2023**[OWASP API Security Top 10 2023](https://owasp.org/API-Security/editions/2023/en/0x00-header/)stable version was publicly released.
- **Feb 14, 2023**[OWASP API Security Top 10 2023 Release Candidate](announcements/2023/02/api-top10-2023rc)is now available.
- **Aug 30, 2022**
- **Oct 30, 2020**[GraphQL Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/GraphQL_Cheat_Sheet.html)release. A truly community effort whose[log and contributors list are available at GitHub](https://github.com/OWASP/CheatSheetSeries/pull/434).
- **Apr 4, 2020**
- **Mar 27, 2020**
- **Dec 26, 2019**

  OWASP API Security Top 10 2019 stable version release.
- **Sep 30, 2019**

  The RC of API Security Top-10 List was published during

  [OWASP Global AppSec Amsterdam](https://ams.globalappsec.org/)([slide deck](https://github.com/OWASP/www-project-api-security/raw/master/assets/presentations/api-security-top10-rc-global-appsec-ams.pdf))
- **Sep 13, 2019**

  The RC of API Security Top-10 List was published during

  [OWASP Global AppSec DC](https://dc.globalappsec.org/)([slide deck](https://github.com/OWASP/www-project-api-security/raw/master/assets/presentations/api-security-top10.pdf))
- **May 30, 2019**

  The API Security Project was Kicked-Off during

  [OWASP Global AppSec Tel Aviv](https://telaviv.appsecglobal.org/)([slide deck](https://github.com/OWASP/www-project-api-security/raw/master/assets/presentations/owasp-api-security-project-kick-off.pdf))

## Planned Projects

- API Security Top 10
- API Security Cheat Sheet
- crAPI - **C**ompletely**R**idiculous**API**, an intentionally vulnerable API project)

## Roadmap

## OWASP API Security Top 10 2023

## OWASP API Security Top 10 2019

- [Arabic](https://owasp.org/API-Security/editions/2019/ar/0x00-header/)(also available in[PDF](https://owasp.org/API-Security/editions/2019/ar/dist/owasp-api-security-top-10-ar.pdf),[ODT](https://owasp.org/API-Security/editions/2019/ar/dist/owasp-api-security-top-10-ar.odt))[Malek Aldossary](https://twitter.com/malajab),[Sabri Hassanyah](https://twitter.com/kingsabri),[Mostafa Alaqsm](https://twitter.com/malaqsm),[Fahad Alduraibi](https://twitter.com/fahad_alduraibi),[Thamer Alshammeri](https://twitter.com/t44t_),[Mohammed Alsuhaymi](https://twitter.com/msuhaymi)
- [Persian](https://owasp.org/API-Security/editions/2019/fa/0x00-header/)(also available in[PDF](https://owasp.org/API-Security/editions/2019/fa/dist/owasp-api-security-top-10.pdf),[ODT](https://owasp.org/API-Security/editions/2019/fa/dist/owasp-api-security-top-10.odt))[Alireza Mostame](https://www.linkedin.com/in/alireza-mostame-29970b242),[Mohammad Reza Ismaeli Taba](https://www.linkedin.com/in/rezataba),[Amirmahdi Nowbakht](https://www.linkedin.com/in/amirmahdi-nowbakht-3b8865200),[RNPG](https://www.linkedin.com/company/raspina-net-pars/)
- [Portuguese (Brazil)](https://owasp.org/API-Security/editions/2019/pt-BR/0x00-header/)(also available in[PDF](https://owasp.org/API-Security/editions/2019/pt-BR/dist/owasp-api-security-top-10-pt-br.pdf),[ODT](https://owasp.org/API-Security/editions/2019/pt-BR/dist/owasp-api-security-top-10-pt-br.odt))
- [Portuguese (Portugal)](https://owasp.org/API-Security/editions/2019/pt-pt/0x00-header/)(also available in[PDF](https://owasp.org/API-Security/editions/2019/pt-pt/dist/owasp-api-security-top-10.pdf),[ODT](https://owasp.org/API-Security/editions/2019/pt-pt/dist/owasp-api-security-top-10.odt))
- [Russian](https://owasp.org/API-Security/editions/2019/ru/0x00-header/)(also available in[PDF](https://owasp.org/API-Security/editions/2019/ru/dist/owasp-api-security-top-10.pdf),[ODT](https://owasp.org/API-Security/editions/2019/ru/dist/owasp-api-security-top-10.odt))[Eugene Rojavski](https://twitter.com/eugenerojavski),[act1on3](https://twitter.com/act1on3), keni0k
