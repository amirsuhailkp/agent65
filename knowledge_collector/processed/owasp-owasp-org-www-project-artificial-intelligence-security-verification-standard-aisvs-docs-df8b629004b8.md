---
title: OWASP Artificial Intelligence Security Verification Standard AISVS Docs
source: owasp.org
url: https://owasp.org/www-project-artificial-intelligence-security-verification-standard-aisvs-docs/
collector: owasp
category: web-security
tags:
- web-security
- security
- aisvs
- verification
- systems
date_collected: '2026-07-26T12:45:05.382451Z'
language: unknown
---

# OWASP Artificial Intelligence Security Verification Standard AISVS Docs

The **Artificial Intelligence Security Verification Standard (AISVS)** is an
open catalogue of testable security requirements for AI-enabled systems. It
helps developers, architects, security engineers, and auditors design, build,
test, and verify AI applications throughout their lifecycle, from data
collection and model training to deployment, monitoring, and retirement.

Every requirement is verifiable, testable, and implementable.

> ### Project Status
>
> *AISVS Version 1.0 is live!*Released June 24, 2026, it is available now in the[OWASP/AISVS](https://github.com/OWASP/AISVS)repository.[Download the AISVS 1.0 PDF](https://github.com/OWASP/AISVS/blob/main/1.0/dist/AISVS-1.0.pdf).

This site is the public documentation wrapper for the main
[OWASP/AISVS](https://github.com/OWASP/AISVS) content repository.

### How to use AISVS

- **Design.**Use it as a security checklist when architecting AI systems.
- **Development.**Integrate it into CI/CD pipelines, code reviews, and tests.
- **Assessment.**Apply it as a verification framework for pen testing and audits.
- **Procurement.**Reference specific requirements when evaluating AI vendors and third-party models.

### Verification Levels

Each requirement is assigned a level (1, 2, or 3) indicating depth of assurance.

LevelDescriptionWhen to use*1*Essential baseline controls every AI system should implement.All AI applications, including internal tools and low-risk systems.*2*Standard controls for systems handling sensitive data or making consequential decisions.Production systems, customer-facing AI, systems processing personal data.*3*Advanced controls for high-assurance environments facing sophisticated threats.Critical infrastructure, safety-critical AI, regulated industries.

Most production systems should aim for at least Level 2.

### Requirement Chapters

- [Training Data Governance & Bias Management](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C01-Training-Data-Integrity-and-Traceability.md)
- [User Input Validation](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C02-Input-Validation.md)
- [Model Lifecycle Management & Change Control](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C03-Model-Lifecycle-Management.md)
- [Infrastructure, Configuration & Deployment Security](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C04-Infrastructure.md)
- [Access Control & Identity](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C05-Access-Control-and-Identity.md)
- [Supply Chain Security for Models, Frameworks & Data](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C06-Supply-Chain.md)
- [Model Behavior, Output Control & Safety Assurance](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C07-Model-Behavior.md)
- [Memory, Embeddings & Vector Database Security](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C08-Memory-Embeddings-and-Vector-Database.md)
- [Autonomous Orchestration & Agentic Action Security](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md)
- [MCP Security](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C10-MCP-Security.md)
- [Adversarial Robustness & Attack Resistance](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C11-Adversarial-Robustness.md)
- [Monitoring, Logging & Anomaly Detection](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C12-Monitoring-and-Logging.md)

### Appendices

- [Appendix A: Glossary](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x90-Appendix-A_Glossary.md)
- [Appendix B: AI Security Controls Inventory](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x91-Appendix-B_AI_Security_Controls_Inventory.md)
- [Appendix C: AI-Assisted Secure Coding](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x92-Appendix-C_AI_for_Code_Generation.md)

### Road Map

PhaseStatusFocusPhase 1: Research and Category List CreationDoneEstablish the research base and define the AISVS category structure.Phase 2: Requirement CreationDoneCreate requirements for each category and refine them with community, partner, and subject matter expert input.Phase 3: Beta Release and Pilot TestingDoneRelease a beta version of AISVS and gather feedback from early adopters using it on real-world AI applications.Phase 4: Final 1.0 ReleaseDoneIncorporate pilot feedback and publish Version 1.0 with full documentation and a lightweight checklist.Phase 5: Continuous ImprovementCurrent PhaseMaintain AISVS as an open source project and update it to address emerging threats, new AI approaches, and regulatory change.

## Example

Put whatever you like here: news, screenshots, features, supporters, or remove this file and don’t use tabs at all.
