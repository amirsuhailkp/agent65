---
title: OWASP FIASSE
source: owasp.org
url: https://owasp.org/www-project-fiasse/
collector: owasp
category: web-security
tags:
- web-security
- security
- software
- fiasse
- system
date_collected: '2026-07-26T12:45:26.980537Z'
language: unknown
---

# OWASP FIASSE

## “The Securable Framework”

Use an attribute model with principles and processes to guide agentic software development (or manual software engineering) to secure outcomes. The Framework for Integrating Application Security into Software Engineering (FIASSE) is a vendor-neutral approach to embedding security directly into the software engineering discipline, without “Shoveling Left”. FIASSE (pronounced /feiz/ like ‘phases of the moon’) is a light weight framework that adapts to your existing software development processes. FIASSE provides a model and principles to create truly securable software by focusing on software attributes and promoting fundamental Software Engineering capabilities that make secure operation over time possible. This makes your security efforts more effective, sustainable, and integrated with the development team.

It reframes developments relationship with security in terms software engineers already understand and can execute on. This gives development clear expectations for the involvement of the security team, reducing the aggravation that comes from last-minute or after-the-fact security demands. These approaches work regardless if the code is agentic generated or manually written.

## Fundamentals

While this framework attempts to give structure to the relationship between security and software engineering, the primary audience is Software Engineers. Therefore, the fundamentals are framed from that perspective to set expectations for development.

The core FIASSE tenets are:

- The Securable Principle: There is no static state of “secure”. Software engineers need to understand what is needed to create securable code without the years of extra training and experience it would take to understand the security practice.
- Derived Integrity Principle: The Derived Integrity Principle states that an application must not implicitly trust or adopt unmanaged external context, such as client-supplied data or other untrusted inputs, when making critical decisions. Instead, it should derive important facts (like identity, permissions, pricing, and state) from authoritative, controlled sources to preserve integrity.
- Canonical Input Handling: The practice of converting all incoming data into a validated and well-defined state before it is used anywhere in the system. This supports the Securable and Derived Integrity principles by making sure that every decision is based on normalized, predictable input instead of raw, inconsistent, or attacker-shaped data.
- The Transparency Principle: How the system works should be perceptible so engineers and stakeholders can see what it is doing, why it is doing it, and how. In software engineering terms, it pushes teams to design systems whose behavior is visible.

### Scope

FIASSE does not intend to replace existing security assurance advice like OWASP PSCF, OWASP SAMM, OWASP ASVS, etc. Instead, it aims to complement other projects by providing a developer-centric framework. It does this by providing a structured approach to securing code through engineering practices.

## Road Map

- Establishment of project governance and contribution guidelines.
- Use feedback to refine the framework and its components.
- Formal publication of FIASSE and SSEM specifications, including their core attributes and integration strategies.
- Development of an SSEM Primer/Introduction Guide to help software engineers understand the model and its application.
- Create a guide for Application Security practitioners on using and teaching FIASSE with relevant security requirements and code examples.
- Collection of SSEM adoption use cases or patterns to illustrate practical applications and benefits.
- Development of additional agentic guidance for protecting the developer and creating code that is securable.
- Gather additional software engineering principles that apply to security and include examples to demonstrate them.

## Core Principles

- The Securable Principle: The Securable Principle says that software is never in a final, fixed state of “secure”; instead, it must be built so it can be secured and kept secure over time. Security is treated as an ongoing property of the system’s design, code, and operations.
- The Derived Integrity Principle: The Derived Integrity Principle states that an application must not implicitly trust or adopt unmanaged external context, such as client-supplied data or other untrusted inputs, when making critical decisions. Instead, it should derive important facts (like identity, permissions, pricing, and state) from authoritative, controlled sources to preserve integrity.
- Canonical Input Handling: The practice of converting all incoming data into a validated and well-defined state before it is used anywhere in the system. This supports the Securable and Derived Integrity principles by making sure that every decision is based on normalized, predictable input instead of raw, inconsistent, or attacker-shaped data.
- The Transparency Principle: How the system works should be perceptible so engineers and stakeholders can see what it is doing, why it is doing it, and how. In software engineering terms, it pushes teams to design systems whose behavior is visible..

## Software Engineering Principles

- Boundary \*Control Principle: Flexibility within a system’s interior is an engineering asset to be preserved; control at every trust boundary is a security requirement to be enforced. These objectives are complementary, not competing. \*Control in this principle refers to its software-engineering sense of the word.
- Request Surface Minimization: The smaller and more intentional the surface that accepts external input, the fewer assumptions the rest of the system has to defend. Accept only what the operation needs, and reject everything else explicitly.
- Principle of Least Astonishment: A system should behave the way a reasonable user, operator, or developer expects. Surprise is a source of defects, including security defects, because behavior that diverges from expectation is behavior that is not being reviewed or defended.
- Actionable Security Intelligence Principle Security output becomes valuable only once it has been translated into prioritized, engineering-grounded direction calibrated to the developer’s context. Raw tool output, exploit-centric narratives, and unfiltered vulnerability lists are information, not yet intelligence.

## Core Values

- Securable Attributes over Security Controls: Rather than focusing on security controls, checklists, or gates, the emphasis is on building software with inherent qualities that make it easier to analyze, modify, test, and trust. Keeping the system defensible matters more than tests that will fail without preparation. Security controls remain valid where they are meant to work, which includes requirements and assurance. Building defensible software is a different job, and it needs performed with intention.
- Participation over Assessment: Structured participation by the security team in the development process yields better results than security assessment alone, which tends to be late and expensive. This means security participation in architecture, design and requirements in whatever form that takes. This makes assessment part of an iterative and empirical process.

> It is ok to give development the answers to the security test because they have to implement it functionally to pass. In software engineering terms this is called requirements.

- First Principle Alignment: While the Security discipline works to ‘reduce the probability of material impact’, the Software Engineering discipline works to ‘resiliently add computing value’. FIASSE provides the structure and knowledge to dovetail these two efforts.
- Business Alignment: FIASSE facilitates Application Security’s understanding of business needs as given to software development. This ensures that security concerns are addressed without disrupting development workflows. Structured alignment allows security to increase their impact on the security outcomes of development.

## The Model

SSEM identifies all the fundamental attributes that are the building blocks of securable software in an evolving landscape (FIASSE RFC Section 2.1). These attributes are not merely abstract concepts but represent tangible characteristics that directly contribute to its overall security and resilience.

### **Maintainability**: Maintainability is the degree of effectiveness and efficiency with which a product or system can be modified by the intended maintainers

- *Analyzability*The ability to quickly assess the impact of changes, diagnose issues, and identify what needs to be modified.
- *Modifiability*The ability to safely and quickly modify a system without causing defects or reducing quality or securability.
- *Testability*The ability to verify that a system meets its requirements and is free of defects.
- *Observability*The degree to which the internal state of a system can be inferred from its external outputs.

### **Trustworthiness**: Trustworthiness is the degree to which a system can be trusted to behave in a predictable manner

- *Confidentiality*The ability to keep sensitive information secure and private.
- *Accountability*The ability to uniquely trace actions to the responsible entity.
- *Authenticity*The ability to confirm the identity of a user or system.

### **Reliability**: Reliability is the degree to which a system, product or component performs specified functions under specified conditions for a specified period of time

- *Availability*The ability of a system to remain accessible and operational when needed.
- *Integrity*The ability to ensure that a system’s data is accurate and uncorrupted.
- *Resilience*The ability to recover from failures and continue operating.

The detail and structure of the SSEM are designed to align with the realities of software development, focusing on creating systems that are securable and adaptable to future changes. The SSEM aims to enhance security, maintain developer velocity, and improve software systems’ ability to adapt to a changing security landscape while maintaining usability and performance.

**For more information** on the Securable Software Engineering Model (SSEM) and its usage, please refer to the [FIASSE RFC](https://github.com/OWASP/FIASSE/blob/main/docs/FIASSE-RFC.md#3-the-securable-software-engineering-model-ssem) or visit the [FIASSE website](https://owaspfiasse.org/#ssem/model).

Tell us what you think!

## Feedback

Please use the [Github Discussions](https://github.com/Xcaciv/securable_software_engineering/discussions) for feedback:

- What do like?
- What don’t you like?
- How can we make FIASSE/SSEM easier to use?
- How could FIASSE/SSEM be improved?

## Contributing Guidelines

Thank you for your interest in contributing to an OWASP project. We welcome all contributions and appreciate your efforts to improve our projects.

### Getting Started

To get started with contributing to any OWASP project, please follow these steps:

- [Join](https://owasp.org/slack/invite)the[OWASP Slack workspace](https://owasp.slack.com)to connect with the OWASP community and get help with any questions you may have.
- Review the

  [OWASP Projects](https://owasp.org/projects/)page to browse the list of OWASP projects and find a project that aligns with your interests and skills.
- Visit the project’s individual page and repository to familiarize yourself with the project goals and objectives.
- Fork the repository and clone it to your local machine.
- Make your changes and review them locally.
- Submit a pull request with your changes.

### Pull Request Guidelines

Before submitting a pull request, please make sure:

- Your changes are consistent with the project’s goals and objectives: this isn’t an assurance framework.
- Your changes are well-documented and follow the project’s standards and styles.
- Your pull request includes a clear and concise description of the changes you have made.

## Code of Conduct

We ask that all contributors to OWASP projects abide by our [Code of Conduct](https://owasp.org/www-policy/operational/code-of-conduct). This code outlines our expectations for behavior within the project community and helps us maintain a welcoming and inclusive environment for all contributors.

Thank you for your interest in contributing to an OWASP project. We appreciate your efforts to help us improve and grow our projects.
