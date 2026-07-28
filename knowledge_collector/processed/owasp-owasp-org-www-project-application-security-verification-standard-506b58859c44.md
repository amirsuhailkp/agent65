---
title: OWASP Application Security Verification Standard ASVS
source: owasp.org
url: https://owasp.org/www-project-application-security-verification-standard/
collector: owasp
category: web-security
tags:
- web-security
- asvs
- owasp
- security
- standard
date_collected: '2026-07-25T14:25:49.411283Z'
language: unknown
---

# OWASP Application Security Verification Standard (ASVS)

## What is the ASVS?

The OWASP Application Security Verification Standard (ASVS) Project provides a basis for testing web application technical security controls and also provides developers with a list of requirements for secure development.

## Support the ASVS

For more details on how to financially support the ASVS, see our [Supporters Page](https://appsecg.host/fundasvs).

## Stay up to date with the ASVS

Follow us on social media to ensure you don’t miss updates about the ASVS:

## More Details on the ASVS

The primary aim of the **OWASP Application Security Verification Standard (ASVS) Project** is to normalize the range in the coverage and level of rigor available in the market when it comes to performing Web application security verification using a commercially-workable open standard. The standard provides a basis for testing application technical security controls, as well as any technical security controls in the environment, that are relied on to protect against vulnerabilities such as Cross-Site Scripting (XSS) and SQL injection. This standard can be used to establish a level of confidence in the security of Web applications. The requirements were developed with the following objectives in mind:

- **Use as a metric**- Provide application developers and application owners with a yardstick with which to assess the degree of trust that can be placed in their Web applications,
- **Use as guidance**- Provide guidance to security control developers as to what to build into security controls in order to satisfy application security requirements, and
- **Use during procurement**- Provide a basis for specifying application security verification requirements in contracts.

Get the latest stable version of the ASVS (5.0.0) from the [Downloads](https://github.com/OWASP/ASVS/tree/v5.0.0#latest-stable-version---500) page.

## How To Reference ASVS Requirements

Each requirement has an identifier in the format
```
<chapter>.<section>.<requirement>
```

, where each element is a number. For example,
```
1.11.3
```

.

- The
  ```
  <chapter>
  ```

  value corresponds to the chapter from which the requirement comes; for example, all
  ```
  1.#.#
  ```

  requirements are from the ‘Encoding and Sanitization’ chapter.
- The
  ```
  <section>
  ```

  value corresponds to the section within that chapter where the requirement appears, for example: all
  ```
  1.2.#
  ```

  requirements are in the ‘Injection Prevention’ section of the ‘Encoding and Sanitization’ chapter.
- The
  ```
  <requirement>
  ```

  value identifies the specific requirement within the chapter and section, for example,
  ```
  1.2.5
  ```

  which as of version 5.0.0 of this standard is:

> Verify that the application protects against OS command injection and that operating system calls use parameterized OS queries or use contextual command line output encoding.

Since the identifiers may change between versions of the standard, it is preferable for other documents, reports, or tools to use the following format:
```
v<version>-<chapter>.<section>.<requirement>
```

, where: ‘version’ is the ASVS version tag. For example:
```
v5.0.0-1.2.5
```

would be understood to mean specifically the 5th requirement in the ‘Injection Prevention’ section of the ‘Encoding and Sanitization’ chapter from version 5.0.0. (This could be summarized as
```
v<version>-<requirement_identifier>
```

.)

Note: The
```
v
```

preceding the version number in the format should always be lowercase.

If identifiers are used without including the
```
v<version>
```

element then they should be assumed to refer to the latest Application Security Verification Standard content. As the standard grows and changes this becomes problematic, which is why writers or developers should include the version element.

ASVS requirement lists are made available in [CSV, JSON, and other formats](https://github.com/OWASP/ASVS) which may be useful for reference or programmatic use.

## Related Projects

OWASP Resources:

## Example

Put whatever you like here: news, screenshots, features, supporters, or remove this file and don’t use tabs at all.

# Jump to an event

# Meet the ASVS team at Global AppSec San Francisco 2024

You can meet some of the ASVS team and hear about using the ASVS at OWASP Global AppSec San Francisco 2024 happening between 23-27 September.

### Get updated on the ASVS

Two of our working group, [Shanni Prutchi](https://www.linkedin.com/in/shanni-prutchi/) and [Ryan Armstrong](https://www.linkedin.com/in/ryarmst/) will be delivering a short talk about the ASVS project and the latest developments and plans.

You can catch them at 14:15 on Friday afternoon in the Bayview A room. Add it to your conference schedule [here](https://sched.co/1lIO2).

(Ryan and Shanni are also doing their own excellent talks at the conference so dont forget to check those out [here](https://sched.co/1g3Wd) and [here](https://sched.co/1g3aZ)!)

### Hear about using the ASVS

Shortly afterwards, [Aram Hovsepyan](https://www.linkedin.com/in/aramhovsep/) will be giving a talk about “Maturing Your Application Security Program with ASVS-Driven Development”. In the talk Aram explains how leveraging ASVS for deriving security test cases can create a common theme across all stages of the software development lifecycle.

If you are interested in how to apply ASVS in your development teams, add it to your conference schedule [here](https://sched.co/1g3ac).

### Engage with the Community

Our new Community Manager [Matthew Aderhold](https://www.linkedin.com/in/matthewaderhold/) will also be at the conference so make sure you catch him to grab some stickers, talk to him about how you are using ASVS and get more information on how you can engage with the ASVS community! He will be there from day 1 of the training so you have plenty of time to catch him!

If you have contributed to the ASVS, make sure you let him know as he will have some special shiny stickers for contributors!

### We hope to see you there at Global AppSec San Francisco 2024

# OWASP ASVS Community Meetup - Lisbon 2024

We held a community meetup for the ASVS project as part of Global AppSec Lisbon on 27th June 2024!

Jim Manico gave the opening keynote to reintroduce the ASVS and the background behind the project and we had some [other great talks](#full-agenda) as well!

There was also an update on the current status of the standard and time allocated to work on the upcoming version 5.0.

You can see full details in the blog post we published about it: <https://owasp.org/blog/2024/07/03/asvs-community-meetup.html>

Additionally, we would love to get more community members involved in the ASVS and other than working on the standard we also have information about other volunteering opportunities to help develop and promote the project! See the “[Get Involved](https://appsecg.host/asvsgetinvolved)” tab above!.

## Full Agenda

You can see the current agenda we had here.

[View the ASVS Community Meetup schedule.](https://owaspglobalappseclisbon2024.sched.com/type/ASVS+Community+Meetup/)

## Meetup Supporter

Thanks to our friends at [Jit](https://jit.io) for supporting this exciting initiative!

# ASVS Supporters

## Introduction

Within the ASVS project, we gratefully recognise the following organizations who support the OWASP Application Security Verification Standard project through monetary donations or allowing contributors to spend significant time working on the standard as part of their work with the organization.

We recognise various tiers of support and the amount of time the supporter is recognised for depends on the supporter level.

On this page and the project web page, we will display the supporter’s logo and link to their website and we will publicise via Social Media as well.

## Maintaining Supporters (through time provision)

Organizations who have allowed contributors to spend significant time working on the standard as part of their working day with the organization. This will be evaluated at the sole discretion of the project leaders. Supporter will be listed 2 years from the end of the time provision.

## Primary supporters

## Secondary supporters

## Tertiary supporters

## Associate supporters

## News and Events

- [30 May 2025] ASVS Version 5.0.0 is released LIVE at Global AppSec EU Barcelona 2025!
- [31 March 2025] Release Candidate 1 of the ASVS version 5.0 is announced!
- [04 November 2024] Some of the ASVS team got together at the [OWASP Project Summit](https://web.archive.org/web/20250000000000*/https://owaspprojectsummit.org/)to make major progress on getting towards version 5.0!
- [01 June 2024] Announcing the first [OWASP ASVS Community Meetup](https://owasp.org/www-project-application-security-verification-standard/#div-meetup)at Global AppSec Lisbon!
- [22 May 2022] Started recognising [time and financial supporters](https://owasp.org/www-project-application-security-verification-standard/#div-supporters)of the ASVS.
- [15 May 2022] The [plan and roadmap](https://owasp.org/blog/2022/05/15/asvs-5.0-roadmap.html)towards ASVS version 5.0 was announced!
- [28 October 2021] [ASVS 4.0.3](https://github.com/OWASP/ASVS/tree/v4.0.3#latest-stable-version---403)released!
- [27 October 2020] [ASVS 4.0.2](https://github.com/OWASP/ASVS/tree/v4.0.2#latest-stable-version---402)released!
- [2 March 2019] [ASVS 4.0.1](https://github.com/OWASP/ASVS/tree/v4.0.1/4.0)released!
- [9 March 2018] [OWASP ASVS 3.1 Spreadsheet](https://docs.google.com/spreadsheets/d/1ic7gsib--Cn4ujrA8rhvzuUmMFpQ2Jkl96SZDCEtqJg/edit?ts=5a6bafe1#gid=950526877)created by August Detlefsen
- [29 June 2016] Version 3.0.1 released
- [9 Oct 2015] Version 3.0 released
- [20 May 2015] “First Cut” Version 3.0 released
- [11 Aug 2014] Version 2.0 released

# Acknowledgements

Note that since 4.x, contributors have been acknowledged in the “Frontispiece” section at the start of the ASVS document itself.

Time and financial supporters are recognised on the “[Supporters](https://owasp.org/www-project-application-security-verification-standard/#div-supporters)” tab.

## Volunteers

### Version 3 (2015)

Project Leaders

- Daniel Cuthbert
- Andrew van der Stock

Lead Author

- Jim Manico

Other reviewers and contributors

- Boy Baukema
- Ari Kesäniemi
- Colin Watson
- François-Eric Guyomarc’h
- Cristinel Dumitru
- James Holland
- Gary Robinson
- Stephen de Vries
- Glenn Ten Cate
- Riccardo Ten Cate
- Martin Knobloch
- Abhinav Sejpal
- David Ryan
- Steven van der Baan
- Ryan Dewhurst
- Raoul Endres
- Roberto Martelloni

### Version 2 (2014)

Project leaders

- Sahba Kazerooni
- Daniel Cuthbert

Lead authors

- Andrew van der Stock
- Sahba Kazerooni
- Daniel Cuthbert
- Krishna Raja

Other reviewers and contributors

- Jerome Athias
- Boy Baukema
- Archangel Cuison
- Sebastien.Deleersnyder
- Antonio Fontes
- Evan Gaustad
- Safuat Hamdy
- Ari Kesäniemi
- Scott Luc
- Jim Manico
- Mait Peekma
- Pekka Sillanpää
- Jeff Sergeant
- Etienne Stalmans
- Colin Watson
- Dr. Emin İslam Tatlı

Translators

- Abbas Javan Jafari (Persian)
- Sajjad Pourali (Persian)

### Version 2009

Project leader

- Mike Boberski

Lead authors

- Mike Boberski
- Jeff Williams
- Dave Wichers

Other reviewers and contributors

Pierre Parrend (OWASP Summer of Code), Andrew van der Stock, Nam Nguyen, John Martin, Gaurang Shah, Theodore Winograd, Stan Wisseman, Barry Boyd, Steve Coyle, Paul Douthit, Ken Huang, Dave Hausladen, Mandeep Khera Scott Matsumoto, John Steven, Stephen de Vries, Dan Cornell, Shouvik Bardhan, Dr. Sarbari Gupta, Eoin Keary, Richard Campbell, Matt Presson, Jeff LoSapio, Liz Fong, George Lawless, Dave van Stein, Terrie Diaz, Ketan Dilipkumar Vyas, Bedirhan Urgun, Dr. Thomas Braun, Colin Watson, Jeremiah Grossman.

## OWASP Summer of Code 2008

The OWASP Foundation sponsored the OWASP Application Security Verification Standard Project during the OWASP Summer of Code 2008.

# Volunteer for the ASVS

## Building the standard

We are always looking for people to help out with building the standards and discussing what should be in there.

You can find information on contributing to the standard in the [Contribution Guide](https://github.com/OWASP/ASVS/blob/master/CONTRIBUTING.md).

## Helping in other ways

We are looking for volunteers to help with the following tasks. We are working on the ASVS all year around and you should expect to have to spend a few hours a week working on your tasks on average. Some of the tasks may be more intensive such as building scripts or GitHub actions.

If any of these roles sound like a good fit for you, please get in touch! Students and non-tech people are welcome to apply, especially folks in the community who are trying to get into the security space but don’t know how, as being involved in an OWASP project like this can provide valuable experience.

The latest list of roles is here:

You can submit your interest here:

## ASVS Users

### CREST OWASP Verification Standard (OVS) Programme

The [CREST OWASP OVS Programme](https://www.crest-approved.org/membership/crest-ovs-programme/) accredits companies that provide app security testing services to the application development industry. The testing to be performed is based on the ASVS (and MASVS) projects.

### App Defense Alliance

The [App Defense Alliance](https://www.appdefensealliance.org/) has based its [Web App Profile](https://www.appdefensealliance.org/profiles/web-app-profile) on the ASVS project.

### Other users

A broad range of companies and agencies around the globe have added ASVS to their software assurance tool boxes, including:

- [Booz Allen Hamilton](https://www.boozallen.com)
- [CGI Federal](https://www.cgi.com/us/en-us/federal)
- [Denim Group](https://denimgroup.com)
- [Etebaran Informatics](https://etebaran.com)
- [Inspectiv](https://www.inspectiv.com/)- “We use ASVS in our pen tests in order to have a comprehensive, vendor neutral, guideline for testing the security of applications and websites.”
- [Minded Security](https://www.mindedsecurity.com)
- [Nixu](https://www.nixu.com)
- [NVISO](https://nviso.eu)- “We use the ASVS as a baseline for our Web Application Penetration Tests.”
- [Pensive Security](https://pensivesecurity.io)
- [ps\_testware](https://www.pstestware.com/)
- [Proactive Risk](https://www.proactiverisk.com)
- [Quince Associates Limited (SeeMyData)](https://quince.co.uk)
- [ReqView](https://www.reqview.com/)- “We use the ASVS as a document template in ReqView requirements management tool and demonstrate its usage in our Example project.”
- [Serviço Federal de Processamento de Dados (SERPRO)](https://www.serpro.gov.br/)
- [Universidad Distrital Francisco José de Caldas](https://www.udistrital.edu.co/)

Organizations listed are not accredited by OWASP. Neither their products or services have been endorsed by OWASP. Use of ASVS may include for example providing verification services using the standard. Use of ASVS may also include for example performing internal evaluation of products with the OWASP ASVS in mind, and NOT making any claims of meeting any given level in the standard. Please let us know how your organization is using OWASP ASVS. Include your name, organization’s name, and brief description of how you use the standard. The project leads can be reached using the contact details on the main page.
