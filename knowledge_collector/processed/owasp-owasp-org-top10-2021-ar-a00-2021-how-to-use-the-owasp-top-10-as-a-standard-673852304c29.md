---
title: How to use the OWASP Top 10 as a standard
source: owasp.org
url: https://owasp.org/Top10/2021/ar/A00_2021_How_to_use_the_OWASP_Top_10_as_a_standard/
collector: owasp
category: web-security
tags:
- web-security
- owasp
- top
- standard
- use
date_collected: '2026-07-25T14:26:09.312457Z'
language: unknown
---

# How to use the OWASP Top 10 as a standard

The OWASP Top 10 is primarily an awareness document. However, this has not stopped organizations from using it as a de facto industry AppSec standard since its inception in 2003. If you want to use the OWASP Top 10 as a coding or testing standard, know that it is the bare minimum and just a starting point.

One of the difficulties of using the OWASP Top 10 as a standard is that we document AppSec risks, and not necessarily easily testable issues. For example, A04:2021-Insecure Design is beyond the scope of most forms of testing. Another example is testing whether in-place, in-use, and effective logging and monitoring are implemented, which can only be done with interviews and requesting a sampling of effective incident responses. A static code analysis tool can look for the absence of logging, but it might be impossible to determine if business logic or access control is logging critical security breaches. Penetration testers may only be able to determine that they have invoked incident response in a test environment, which is rarely monitored in the same way as production.

Here are our recommendations for when it is appropriate to use the OWASP Top 10:

Use CaseOWASP Top 10 2021OWASP Application Security Verification StandardAwarenessYesTrainingEntry levelComprehensiveDesign and architectureOccasionallyYesCoding standardBare minimumYesSecure Code reviewBare minimumYesPeer review checklistBare minimumYesUnit testingOccasionallyYesIntegration testingOccasionallyYesPenetration testingBare minimumYesTool supportBare minimumYesSecure Supply ChainOccasionallyYes

We would encourage anyone wanting to adopt an application security
standard to use the [OWASP Application Security Verification Standard](https://owasp.org/www-project-application-security-verification-standard/)
(ASVS), as it’s designed to be verifiable and tested, and can be used in
all parts of a secure development lifecycle.

The ASVS is the only acceptable choice for tool vendors. Tools cannot comprehensively detect, test, or protect against the OWASP Top 10 due to the nature of several of the OWASP Top 10 risks, with reference to A04:2021-Insecure Design. OWASP discourages any claims of full coverage of the OWASP Top 10, because it’s simply untrue.
