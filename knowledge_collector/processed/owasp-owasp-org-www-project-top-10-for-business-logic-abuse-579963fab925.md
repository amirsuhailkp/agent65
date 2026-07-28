---
title: OWASP Top 10 for Business Logic Abuse
source: owasp.org
url: https://owasp.org/www-project-top-10-for-business-logic-abuse/
collector: owasp
category: web-security
tags:
- web-security
- logic
- business
- vulnerabilities
- issues
date_collected: '2026-07-26T12:45:59.704642Z'
language: unknown
---

# OWASP Top 10 for Business Logic Abuse

Modern applications rely heavily on complex business logic to manage workflows, data, and user interactions. Unlike traditional vulnerabilities such as SQL injection or misconfigurations, business logic abuse exploits design flaws in how applications operate. These attacks manipulate application workflows, state transitions, and decision-making processes to gain unauthorized access, bypass restrictions, or disrupt operations.

The OWASP Business Logic Abuse Top 10 complements and enhances existing OWASP Top 10 projects by providing a cross-domain focus on business logic vulnerabilities that transcend technology stacks. Whether applied to web applications, APIs, mobile apps, firmware, supply chain systems, or even hardware platforms, these issues remain universal as they target the fundamental logic governing workflows and state transitions. By addressing flaws like workflow step skipping, broken object-level authorization, and business constraint bypasses, this Top 10 bridges gaps in domain-specific lists, ensuring that logic abuse risks are identified and mitigated regardless of the implementation medium. This unifying approach fosters better integration of security practices across diverse OWASP projects, strengthening overall application security frameworks.

The OWASP Business Logic Abuse Top 10 provides a structured methodology for identifying and prioritizing the most critical business logic vulnerabilities. This project introduces an innovative, open approach based on Turing machine principles, modeling applications as finite states, transitions, and memory operations. This approach allows the broader security community to understand, simulate, and mitigate business logic vulnerabilities systematically.

# Purpose of the Project

- Raise Awareness: Highlight the prevalence and impact of business logic flaws in modern applications.
- Create a Reproducible Methodology: Provide an open framework based on computational principles for identifying, modeling, and analyzing these vulnerabilities.
- Empower Developers and Architects: Equip technical stakeholders with tools and insights to design secure workflows and logic.
- Define Top 10 Issues: Establish a comprehensive, prioritized list of the most critical business logic abuses, supported by real-world case studies and a computational model.

# Releases

- First Release, May 30th, 2025 OWASP AppSec Global EU, Barcelona.
- Second Release, August 2nd, 2025.

# Unique Approach

This project departs from traditional vulnerability frameworks by leveraging the Turing machine model to define and categorize business logic abuse. Applications are viewed as abstract machines with:

- Tape: Representing memory or data storage (e.g., databases, in-memory objects).
- Head: Representing data access mechanisms (e.g., API calls, queries).
- States: Representing application workflows (e.g., authentication, transaction approval).
- Transitions: Representing the logic that moves the application between states (e.g., user actions, API responses).

# Key Innovations

- Computational Foundation: Modeling vulnerabilities through Turing machine components provides a systematic approach to understanding flaws.
- Open Methodology: Every step of the vulnerability identification process is documented, allowing the community to validate and expand the research.
- Focus on Root Causes: Identifies and classifies vulnerabilities by their underlying computational flaws (e.g., state mismanagement, transition errors, memory corruption).
- Practical Outcomes: Provides actionable guidance for preventing, detecting, and mitigating business logic abuse.

# Methodology

## 1. Vulnerability Modeling with Turing Machines

Applications are modeled as Turing machines to abstract their behavior:

- Tape: Stores the application’s data (e.g., user inputs, transaction logs).
- Head: Accesses and modifies data on the tape.
- States: Represent stages in application workflows.
- Transitions: Define how the application moves between states based on conditions.

Business logic vulnerabilities are identified by simulating flaws in these components:

- Tape Issues: Data inconsistencies, corruption, or unauthorized modifications.
- State Issues: Improper initialization, transitions, or management of states.
- Transition Issues: Workflow bypasses, race conditions, or weak validations.

## 2. Open and Reproducible Process

The project adopts a transparent research methodology:

Data Sources: Analysis of real-world incidents, penetration testing reports, and industry publications.

Root Cause Analysis: Vulnerabilities are traced back to fundamental issues in Turing machine components.

Community Collaboration: Contributions and feedback from the OWASP community are integral to the project.

## 3. Vulnerability Prioritization

The Top 10 vulnerabilities are selected based on:

Frequency: How often they are encountered in real-world applications.

Impact: The potential damage to confidentiality, integrity, and availability.

Exploitability: The ease with which attackers can exploit the flaw.

## Road Map

- July-November 2024: analytical work for modeling business logic in terms of Turing machines
- December 2024 : mapping CVE data with issues classes by the model, open submissions
- March 2025: first draft release
- April 2025: public feedback gathering to decide of GA

## Overview

We modelled business-logic vulnerabilities as automata by mapping the Turing-machine primitives to real-world logic flows. We chose this framing because any business rule can be expressed as a Turing machine, guaranteeing that our taxonomy can represent every possible logic flaw.

## Data collection and analysis

We used a large language model to validate that the proposed model provides sufficient coverage by classifying all CVEs from 2023 to 2025, clustered the classification results, and verified the model against a sample of 25k GitHub security issues. This confirms that the model is both theoretically complete and practically aligned with real-world vulnerabilities.

The analysis was performed in four steps:

### Stage 1: Model definition and initial classification

We started with the basic groups of issues in regards to the Turing-machine primitives: Tape, State, Transition. For each group, we introduced around 20 root causes which resulted in 63 distinct classes of vulnerabilities.

To validate the coverage, we used an LLM to classify all CVEs from 2023 to 2025 (76k CVE in total).

### Stage 2: Clustering of existing CVE and publicly known exploits

We took the high-confidence classifications from Stage 1 and removed any CVE with a low correlation score. We then applied several clustering algorithms using the initial root-cause labels as feature vectors, and selected configurations that maximized cohesion and silhouette score.

Next, we discarded clusters whose silhouette fell below our threshold and excluded individual CVE with low classification confidence. Similar clusters were then merged to eliminate redundancy.

Finally, we removed clusters that are not related to business logic attacks and are covered with other Top 10s, such as:

- Issues with cryptography.
- Security misconfigurations.
- Injection attacks.
- Improper API and asset inventory management including unsafe API consumption.

Result: 12 tightly-bound, high-confidence clusters of real-world exploits.

### Stage 3: Clustering of existing CVE and publicly known exploits

As the next step, we removed any clusters whose coverage fell below our threshold. We then added three additional clusters (Race Condition and Concurrency Issues, Logic Bomb, Loops and Halting Issues, Resource Quota Violations) to cover gaps in the taxonomy.

After merging similar groups and polishing definitions, we arrived at ten cohesive clusters of vulnerabilities.

### Stage 4: Clustering of existing CVE and publicly known exploits

We recognized that CVE records emphasize impact and exploit details rather than root-cause insights. To fill that gap, we drew a random sample of 25k security-related issues from GitHub.

We mapped issue descriptions and tags back to our ten clusters and measured how well each cluster captured real-world problem reports. Based on alignment rates, we refined cluster definitions, merged or split groups to match patterns seen in developer discussions, and validated that our taxonomy holds outside the CVE corpus.

# OWASP Top 10 for Business Logic Abuse – 2025

Class nameSummary[BLA1:2025 - Action Limit Overrun (ALO)](docs/the-top-10/action-limit-overrun.html)Overrun Limit of Idempotent Operations arises when unsynchronized concurrent requests exploit a TOCTOU gap to bypass single-use checks and repeatedly execute operations like coupon redemptions or refunds.[BLA2:2025 - Concurrent workflow order bypass (CWOB)](docs/the-top-10/workflow-order-bypass.html)Workflow Order Bypass is a race-condition attack that runs a workflow’s final step before its required prior steps complete, either across distributed commands or within unguarded internal sub-states.[BLA3:2025 - Object state manipulations (OSM)](docs/the-top-10/object-state-manipulations.html)Object state manipulation flaws occur when APIs bind unfiltered user input into internal objects without validating fields or types, allowing attackers to override protected properties, such as roles or permissions.[BLA4:2025 - Malicious Logic Loop (MLL)](docs/the-top-10/malicious-logic-loop.html)APIs lacking proper gating, loop exit checks, input validation, or recursion limits can be exploited to trigger hidden routines and exhaust resources, leading to service crashes, financial loss, or denial of service.[BLA5:2025 - Artifact Lifetime Exploitation (ALE)](docs/the-top-10/artifact-lifetime-exploitation.html)Abuse of one-time or short-lived resources, like tokens, sessions, or temporary files left valid beyond their intended lifecycle, lets attackers replay stale artifacts to access sensitive operations or data.[BLA6:2025 - Missing Transition Validation (MTV)](docs/the-top-10/missing-transition-validation.html)Transition validation flaws occur when APIs defer or omit essential checks in multi-step state workflows, letting attackers call later endpoints and enabling unauthorized workflows.[BLA7:2025 - Resource Quota Violation (RQV)](docs/the-top-10/resource-quota-violation.html)Without proper rate limits, business endpoints triggering heavy operations can be abused to exhaust resources, degrade services, or cause financial harm in AI systems where one user’s token overuse can DoS others.[BLA8:2025 - Internal State Disclosure (ISD)](docs/the-top-10/internal-state-disclosure.html)When systems show different messages, codes, visuals, delays for valid vs invalid inputs they leak internal states, enabling attackers to lay groundwork for targeted intrusion or fraud.[BLA9:2025 - Broken Access Control (BAC)](docs/the-top-10/broken-access-control.html)Flawed or missing role and permission checks in critical workflows let attackers spoof roles, bypass controls, and execute unauthorized actions, causing privilege escalation and data integrity breaches.[BLA10:2025 - Shadow Function Abuse (SFA)](docs/the-top-10/shadow-function-abuse.html)Shadow functions are unprotected hidden features in production code, like internal APIs or test utilities, which attackers find via code inspection or discovery tools to bypass security and access restricted data.

1 Of the analyzed security issues on Github. Referer to the Methodology section for further information.
