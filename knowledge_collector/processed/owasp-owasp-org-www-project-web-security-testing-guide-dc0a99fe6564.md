---
title: OWASP Web Security Testing Guide
source: owasp.org
url: https://owasp.org/www-project-web-security-testing-guide/
collector: owasp
category: web-security
tags:
- web-security
- version
- web
- guide
- testing
date_collected: '2026-07-26T12:42:52.750133Z'
language: unknown
---

# OWASP Web Security Testing Guide

The Web Security Testing Guide (WSTG) Project produces the premier cybersecurity testing resource for web application developers and security professionals.

The WSTG is a comprehensive guide to testing the security of web applications and web services. Created by the collaborative efforts of cybersecurity professionals and dedicated volunteers, the WSTG provides a framework of best practices used by penetration testers and organizations all over the world.

## Contributions

Any contributions to the guide itself should be made via the [guide’s project repo](https://github.com/OWASP/wstg).

Contributions should only be made in the proper repo against the latest content. Please don’t open PRs here for versioned or stable content, they represent point-in-time state.

## Stable

View the always-current stable version at [stable](stable/).

## Latest

We are currently developing release version 5.0.

You can [read the latest development documents in our official GitHub repository](https://github.com/OWASP/wstg/tree/master/document) or view the bleeding-edge content at [latest](latest/).

## Versioned Releases

[v4.2](v42/) is currently available as a web-hosted release and PDF. Previous releases are available as PDFs and in some cases web content via the **Release Versions** tab.

## How To Reference WSTG Scenarios

Each scenario has an identifier in the format
```
WSTG-<category>-<number>
```

, where: ‘category’ is a 4 character upper case string that identifies the type of test or weakness, and ‘number’ is a zero-padded numeric value from 01 to 99. For example:
```
WSTG-INFO-02
```

is the second Information Gathering test.

The identifiers may change between versions therefore it is preferable that other documents, reports, or tools use the format:
```
WSTG-<version>-<category>-<number>
```

, where: ‘version’ is the version tag with punctuation removed. For example:
```
WSTG-v41-INFO-02
```

would be understood to mean specifically the second Information Gathering test from version 4.1.

If identifiers are used without including the
```
<version>
```

element then they should be assumed to refer to the latest Web Security Testing Guide content. Obviously as the guide grows and changes this becomes problematic, which is why writers or developers should include the version element.

### Linking

Linking to Web Security Testing Guide scenarios should be done using versioned links not
```
stable
```

or
```
latest
```

which will definitely change with time. However, it is the project team’s intention that versioned links not change. For example:
```
https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/01-Information_Gathering/02-Fingerprint_Web_Server
```

. Note: the
```
v42
```

element refers to version 4.2.

## Stable

View the always-current stable version at [stable](stable/).

## [Unreleased 4.3]

## [Version 4.2] - 2020-12-03

[Version 4.2](v42/) introduces new testing scenarios, updates existing chapters, and offers an improved writing style and chapter layout.

[Download the v4.2 PDF](https://github.com/OWASP/wstg/releases/download/v4.2/wstg-v4.2.pdf) here.

## [Version 4.1] - 2020-04-21

[Version 4.1](v41/) serves as a post-migration stable version under the new GitHub repository workflow.

[Download the v4.1 PDF](https://github.com/OWASP/wstg/releases/download/v4.1/wstg-v4.1.pdf) here.

## [Version 4.0] - 2014-09-17

[Download the v4 PDF](assets/archive/OWASP_Testing_Guide_v4.pdf) here.

A printed book is also made [available for purchase](https://www.lulu.com/shop/matteo-meucci-and-andrew-muller/testing-guide-40-release/paperback/product-22294314.html).

## [Version 3.0] - 2008-12-16

[Download the v3 PDF](assets/archive/OWASP_Testing_Guide_v3.pdf) here.

### [Pre-release 3.0] - 2008-11-06

[View a presentation (PPT)](assets/archive/OWASP_EU_Summit_2008_OWASP_Testing_Guide_v3.ppt) previewing the release at the OWASP EU Summit 2008 in Portugal.

## [Version 2.0] - 2007-02-10

[Download the v2 PDF](assets/archive/OWASP_Testing_Guide_v2.pdf) here.

The guide is also available in [Word Document format in English (ZIP)](assets/archive/OWASP_Testing_Guide_v2_doc.zip) as well as [Word Document format translation in Spanish (ZIP)](assets/archive/OWASP_Testing_Guide_v2_spanish_doc.zip).

## [Version 1.1] - 2004-08-14

Version 1.1 is released as the *OWASP Web Application Penetration Checklist*.

[Download the v1.1 PDF](assets/archive/OWASP_Web_Application_Penetration_Checklist_v1_1.pdf) here.

## [Version 1.0] - 2004-12-10

[Download the v1 PDF](assets/archive/OWASP_Testing_Guide_v1.pdf) here.

## Archives

Historical [archives of the Mailman owasp-testing mailing list](https://lists.owasp.org/pipermail/owasp-testing/index) are available to view or download.

## How can I help?

We are actively inviting new contributors to help keep the WSTG up to date! You can get started at [our official GitHub repository](https://github.com/OWASP/wstg).

## How can I contact you?

To report issues or make suggestions for the WSTG, please use [GitHub Issues](https://github.com/OWASP/wstg/issues).

For everything else, we’re easy to find on Slack:

- Join the OWASP Group Slack with this [invitation link](https://owasp-slack.herokuapp.com/).
- Join this project’s [channel, #testing-guide](https://app.slack.com/client/T04T40NHX/CJ2QDHLRJ).

You can @ us on Twitter [@owasp\_wstg](https://twitter.com/owasp_wstg).
