---
title: OWASP WAF-A-MoLE
source: owasp.org
url: https://owasp.org/www-project-waf-a-mole/
collector: owasp
category: web-security
tags:
- web-security
- waf-a-mole
- admin
- payload
- operators
date_collected: '2026-07-26T12:44:49.288955Z'
language: unknown
---

# OWASP WAF-A-MoLE

# Project Overview

WAF-A-MoLE is a guided mutation-based fuzzer for Web Application Firewalls.

Given an input attack payload, it tries to produce a semantic invariant query that bypasses detection rules for the target WAF. You can use this tool for assessing the robustness of your product by letting WAF-A-MoLE explore the solution space to find dangerous “blind spots” left uncovered by the target classifier.

## WAF-A-MoLE Architecture

WAF-A-MoLE takes an initial payload and inserts it in the payload Pool, which manages a priority queue ordered by the WAF confidence score over each payload.

During each iteration, the head of the payload Pool is passed to the Fuzzer, where it gets randomly mutated, by applying one of the available mutation operators. Mutation operators Mutations operators are all semantics-preserving and they leverage the expressive power of the target grammar.

Below are the SQL mutation operators available in the current version of WAF-A-MoLE.

MutationExampleCase Swappingadmin’ OR 1=1# ⇒ admin’ oR 1=1#Whitespace Substitutionadmin’ OR 1=1# ⇒ admin’\t\rOR\n1=1#Comment Injectionadmin’ OR 1=1# ⇒ admin’/\*\*/OR 1=1#Comment Rewritingadmin’/*\*/OR 1=1# ⇒ admin’/*xyz\*/OR 1=1#abcInteger Encodingadmin’ OR 1=1# ⇒ admin’ OR 0x1=(SELECT 1)#Operator Swappingadmin’ OR 1=1# ⇒ admin’ OR 1 LIKE 1#Logical Invariantadmin’ OR 1=1# ⇒ admin’ OR 1=1 AND 0<1#Number Shufflingadmin’ OR 1=1# ⇒ admin’ OR 2=2#

How to Contribute Questions, bug reports and pull requests are always welcome. In particular, if you are interested in expanding this project, we are currently interested in the following contributions:

- New WAF adapters
- New mutation operators (both for SQL and other vulnerability classes, XSS in particular)
- New search algorithms

## Project Road Map

🎯**August 2024 - WAF-A-MoLE becomes a OWASP project!**

This version supports SQL mutations and contains drivers for ModSecurity and a selection of ML-based WAFs The ModSecurity driver leverages on a custom fork for the pymodsecurity module.

🎯**March 2024 - September 2024**

Testing + Feedback + Improvements These tests will include assessing how effective the current strategy is at bypassing ModSecurity (with a focus on the CoreRuleSet), also by gathering real experiences from users. Compare and add optimization algorithms to the WAF-A-MoLE strategy selection.

🎯**September 2024: Integrate WAF-A-MoLE in the FTW framework**

FTW currently uses static payloads, we want to add dynamic payload generation.

🎯**March 2025: XSS support**

WAF-A-MoLE includes mutation operators and strategies for Cross-Site Scripting payloads

## Example

Put whatever you like here: news, screenshots, features, supporters, or remove this file and don’t use tabs at all.
