---
title: OWASP SEDATED®
source: owasp.org
url: https://owasp.org/www-project-sedated/
collector: owasp
category: web-security
tags:
- web-security
- sedated
- sensitive
- owasp
- data
date_collected: '2026-07-26T12:44:35.322980Z'
language: unknown
---

# OWASP SEDATED®

The **SEDATED®** Project (Sensitive Enterprise Data Analyzer To Eliminate Disclosure) focuses in on preventing sensitive data such as user credentials and tokens from being pushed to Git. Developers are constantly pushing changes to GitHub and will most likely eventually try pushing a commit that contains sensitive information and we want to help catch and prevent that. The **SEDATED®** application will run on the Git server and review all incoming code changes. If it identifies sensitive data it will reject the push otherwise it will allow it.

## Purpose

With the myriad of code changes required in today’s CICD environment developers are constantly pushing code that could unintentionally contain sensitive information. This potential sensitive data exposure represents a huge risk to organizations ([2021 OWASP Top Ten #2 - Cryptographic Failures](https://owasp.org/Top10/A02_2021-Cryptographic_Failures)). **SEDATED®** addresses this issue by automatically reviewing all incoming code changes and providing instant feedback to the developer. If it identifies sensitive data it will prevent the commit(s) from being pushed to the Git server.

## Latest Version

[Version 1.2.0](https://github.com/OWASP/SEDATED/releases/tag/v1.2.0) is the latest version!

## Getting Involved

We are looking for community support with this project as there is a lot more we can do! Feel free to checkout the  **OWASP/SEDATED®** repository and contribute any ideas you may have to make

**SEDATED®**even better!

## Example

Put whatever you like here: news, screenshots, features, supporters, or remove this file and don’t use tabs at all.
