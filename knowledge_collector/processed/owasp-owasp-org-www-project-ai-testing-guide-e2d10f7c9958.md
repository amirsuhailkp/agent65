---
title: OWASP AI Testing Guide
source: owasp.org
url: https://owasp.org/www-project-ai-testing-guide/
collector: owasp
category: web-security
tags:
- web-security
- testing
- owasp
- guide
- systems
date_collected: '2026-07-26T12:45:02.166566Z'
language: unknown
---

# OWASP AI Testing Guide

# 📢 26 November 2025 — Version 1 Published

The **OWASP AI Testing Guide v1** is officially released.
This milestone marks the first open, community-driven standard for trustworthiness testing of AI systems.

👉 **Download the PDF**

👉 **Browse it on GitHub**

# AI Testing as the Foundation of AI Trustworthiness

Artificial Intelligence has shifted from an innovative technology to a critical component of modern digital infrastructure. AI systems now support high-stakes decisions in healthcare, finance, mobility, public services, and enterprise automation. As these systems grow in reach and autonomy, organizations need a standardized and repeatable way to verify that AI behaves safely as intended.

The OWASP AI Testing Guide fills this gap by establishing a practical standard for trustworthiness testing of AI systems, offering a unified, technology-agnostic methodology that evaluates not only security threats but the broader trustworthiness properties required by responsible and regulatory-aligned AI deployments.

AI testing is no longer just about security, it is a multidisciplinary discipline focused on maintaining trust in autonomous and semi-autonomous systems. The OWASP AI Testing Guide establishes the missing standard: a unified, practical, and comprehensive framework for trustworthiness testing of AI systems, grounded in real attack patterns, emerging global standards, and the lived experience of the AI security community.

### Why AI Testing is Unique

Traditional software testing focuses on protecting systems from unauthorized access, code flaws, and system vulnerabilities. AI systems require more. Because AI models learn, adapt, generalize, and fail in non-deterministic ways, they introduce risks that cannot be addressed with conventional security testing.

From the evidence documented in the NIST AML Taxonomy and the OWASP Top 10 for LLM Applications 2025 , we know that AI systems fail for reasons that go far beyond security:

- Adversarial manipulation (prompt injection, jailbreaks, model evasion)
- Bias and fairness failures
- Sensitive information leakage
- Hallucinations and misinformation
- Data/model poisoning across the supply chain
- Excessive or unsafe agency
- Misalignment with user intent or organizational policies
- Non-transparent or unexplainable outputs
- Model drift and degradation over time

Because of these complexities, the industry is converging on the principle that: Security is not sufficient, AI Trustworthiness is the real objective. This OWASP AI Testing Guide operationalizes these principles into a practical testing framework.

AI models can be fooled or manipulated by carefully crafted inputs (adversarial examples): organizations must employ dedicated adversarial robustness testing methodologies that extend well beyond standard functional tests. Without these specialized security assessments, AI systems remain vulnerable to subtle attacks that can compromise their integrity, reliability, and overall trustworthiness.

### Purpose and Scope of the OWASP AI Testing Guide

The OWASP AI Testing Guide provides:

- A standardized methodology for trustworthiness testing of AI and LLM-based systems
- Repeatable test cases that evaluate risks across:
  - AI Application Layer
  - AI Model Layer
  - AI Infrastructure Layer
  - AI Data Layer

This Guide is designed to serve as a comprehensive reference for software developers, architects, data analysts, researchers, auditors and risk officers, ensuring that AI risks are systematically addressed throughout the product development lifecycle.

### Start contributing [HERE](https://github.com/OWASP/www-project-ai-testing-guide)

### Road Map

- Phase 0: Marco Morana and Matteo Meucci wrote a first draft (APRIL-JUNE 2025)

  [here](https://github.com/MatOwasp/AI-Testing-Guide)
- Phase 1: Initial Draft and Community Formation (JUNE 2025) Publish an initial project outline clearly defining the scope, mission, and testing categories. Establish an OWASP GitHub repository and set up a dedicated community team:

  [OWASP AI Testing Guide Table of Contents](https://github.com/OWASP/www-project-ai-testing-guide/blob/main/Document/README.md)Conduct initial outreach to invite contributions from the OWASP and AI communities.
- Phase 2: Refinement, Release, and Promotion (NOVEMBER 2025) Incorporate community and industry feedback to finalize the first official release of the OWASP AI Testing Guide v1. Present the guide at global OWASP conferences, including hosting workshops and interactive sessions to encourage broader adoption and continuous improvement. Establish a structured update cycle to ensure ongoing relevance with advancements in AI.

## Start Contributing

The OWASP projects are an open source effort, and we enthusiastically welcome all forms of contributions and feedback.

- 📥 Send your suggestion, propose your concepts to the [project leader](/cdn-cgi/l/email-protection#c8a5a9bcbcada7e6a5adbdababa188a7bfa9bbb8e6a7baaf).
- 👋 Join OWASP in our Slackworkspace.
- Start contributing here: [OWASP AI Testing Guide Table of Contents](https://github.com/OWASP/www-project-ai-testing-guide/blob/main/Document/README.md)
