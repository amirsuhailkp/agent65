---
title: OWASP Threat Modeling Project
source: owasp.org
url: https://owasp.org/www-project-threat-modeling/
collector: owasp
category: web-security
tags:
- web-security
- threat
- modeling
- owasp
- security
date_collected: '2026-07-26T12:45:55.734230Z'
language: unknown
---

# OWASP Threat Modeling Project

**Status:** Maintained Project Guidance

This documentation project is the maintained entry point for OWASP Threat Modeling Project resources. It connects current guidance, community references, tools, examples, and historical material while recognizing that there are various threat modeling methodologies.

This project provides information on threat modeling techniques for applications of all types, with a focus on current and emerging techniques.

## New to threat modeling? Start here

Use [Shostack’s Four Question Framework](https://github.com/adamshostack/4QuestionFrame) as a methodology-neutral starting point:

- **What are we working on?**Understand the project scope, and possibly the system, users, dependencies, assumptions, or trust boundaries.
- **What can go wrong?**Identify threats, misuse cases, design assumptions, and security or privacy concerns.
- **What are we going to do about it?**Prioritize risks and define mitigations, design changes, tests, or follow-up work.
- **Did we do a good job?**Review outcomes, track decisions and assumptions, and revisit remaining risks over time.

The [Threat Modeling tab](https://owasp.org/www-project-threat-modeling/#div-threatmodeling) introduces the practice, the [Application Threat Modeling tab](https://owasp.org/www-project-threat-modeling/#div-application-tm) describes a practical application workflow, and the [Resources tab](https://owasp.org/www-project-threat-modeling/#div-resources) lists tools, references, and related OWASP projects.

This project will gather techniques, methodologies, tools and examples. We will group these using the four questions. This will allow people to easily find advice they can use.

Example: if you are looking for different diagramming techniques you will want to look for all the techniques answering the question “What are we working on.”

### Methodology-neutral positioning

The OWASP Threat Modeling Project does not define a single official OWASP threat modeling methodology. The project documents a wide range of approaches, including STRIDE, PASTA, LINDDUN, attack trees, abuse cases, and other community practices.

Different methods may be appropriate depending on system context, security and privacy goals, team maturity, delivery model, and regulatory needs. Contributions should explain their scope, assumptions, and intended use so practitioners can choose and adapt approaches responsibly.

### Guiding principles:

This project follows a number of principles that all contributions must adhere to:

- We are vendor, methodology and tool independent: we strive to have examples in as many methodologies and/or tools as possible.
- Open discussion is promoted: all topics are open for discussion with just one rule: don’t be a jerk. If you feel information is lacking or missing, let us know via the OWASP #threat-modeling slack channel.
- We come to an agreement: we discuss things mainly in google docs and on slack, if the project leaders feel a consensus is made, we will publish the content to our main website. All published content can be changed by submitting change requests on the Github repository that serves the website.

## Overview

The term “Threat Modeling” has become quite popular. The “[State Of Threat Modeling Report](https://www.threatmodelingconnect.com/state-of-threat-modeling-2024-25)” points at a robust and improving practice across companies and enterprises of all sizes, embracing a growing number of tools and methodologies.

In 2020, a group of threat modeling practitioners, researchers and authors got together to write the [Threat Modeling Manifesto](https://www.threatmodelingmanifesto.org/) in order to “…share a distilled version of our collective threat modeling knowledge in a way that should inform, educate, and inspire other practitioners to adopt threat modeling as well as improve security and privacy during development”. The Manifesto contains values and principles connected to the practice and adoption of Threat Modeling, as well as identified patterns and anti-patterns to facilitate it.

One of the outputs of the Manifesto was this consensus-driven definition:

“Threat modeling is analyzing representations of a system to highlight concerns about security and privacy characteristics.”

A threat model is essentially a structured representation of all the information that affects the security of an application. In essence, it is a view of the application and its environment through security glasses.

Threat modeling is a process for capturing, organizing and analyzing all of this information. Threat modeling enables informed decision-making about application security risk. In addition to producing a model, typical threat modeling efforts also produce a prioritized list of security threats identified, and possibly mitigations to the risk they create.

## Why Threat Model?

Threat modeling embodies a family of activities for improving security by identifying threats, understanding their criticality, and then defining countermeasures to prevent, or mitigate the effects of these threats to the system, functionality and user. A threat is a potential or actual undesirable event that may be malicious (such as CSRF attack) or incidental (thunderstorm knocking the power down). Threat modeling is a planned activity for identifying and assessing application threats and vulnerabilities. It can also encompass fields related to Security, like Safety and Privacy.

## Threat Modeling Across the Lifecycle

Threat modeling is best applied continuously throughout a software development project - at whatever resolution may be practical for that specific project.

The process is essentially the same at different levels of abstraction, although the information gets more and more granular throughout the lifecycle. Ideally, a high-level threat model should be defined in the ideation or design phase, and then refined throughout the lifecycle. As more details are added to the system, new attack vectors may be created and exposed. The ongoing threat modeling process examines, diagnoses, and addresses these threats.

Note that it is a natural part of refining a system for new threats to be exposed. For example, when you select a particular technology – such as Java for example – you take on the responsibility to identify the new threats that are created by that choice. Even implementation choices such as using regular expressions for validation introduce potential new threats to deal with.

Threat modeling can be divided into two closely related activities: system modeling and threat elicitation. It is very important that all participants in a threat model be able to recognize the system under analysis in whatever representation (diagram, textual, etc.) is chosen, as that recognition will be the basis of the threat elicitation phase.

## Benefits

Done right, threat modeling provides visibility across a project that helps justify and support security efforts. The threat model allows security decisions to be made rationally, with all the information on the table. The alternative is to make ad-hoc security decisions with no support in real data, scenarios and outcomes. The threat modeling process naturally produces an assurance argument, or artifact, that can be used to explain and defend the security of an application. An assurance argument starts with a few high level claims, and justifies them with either sub-claims or evidence.

## Where to go from here?

Check the [Resources tab](https://owasp.org/www-project-threat-modeling/#div-resources) for more extensive documentation, books and tools to start you on your journey!

## Application Threat Modeling

Threat modeling works to identify, communicate, and understand threats and mitigations within the context of protecting something of value.

Threat modeling can be applied to a wide range of things, including software, applications, systems, networks, distributed systems, things in the Internet of things, business processes, etc. There are very few technical products which cannot be threat modeled; more or less rewarding, depending on how much it communicates, or interacts, with the world. Threat modeling can be done at any stage of development, preferably early - so that the findings can inform the design.

### What

Most of the time, a threat model includes:

- A description / design / model of what you’re worried about
- A list of assumptions that can be checked or challenged in the future as the threat landscape changes
- A list of potential threats to the system
- A list of actions to be taken for each threat
- A way of validating the model and threats, and verification of success of actions taken

Our motto is: Threat modeling: the sooner the better, but never too late.

### Why

The inclusion of threat modeling in the SDLC can help

- Build a secure design
- Efficient investment of resources; appropriately prioritize security, development, and other tasks
- Bring Security and Development together to collaborate on a shared understanding, informing development of the system
- Identify threats and compliance requirements, and evaluate their risk
- Define and build required controls.
- Balance risks, controls, and usability
- Identify where building a control is unnecessary, based on acceptable risk
- Document threats and mitigation
- Ensure business requirements (or goals) are adequately protected in the face of a malicious actor, accidents, or other causes of impact
- Identification of security test cases / security test scenarios to test the security requirements

### 4 Questions

The Threat Modeling Manifesto has adopted the [4 Questions Framework](https://github.com/adamshostack/4QuestionFrame) as the seminal framework to direct threat modeling efforts. Most threat model methodologies answer one or more of the following questions in the technical steps which they follow:

#### What are we building?

As a starting point you need to define the scope of the Threat Model. To do that you need to understand the application you are building, examples of helpful techniques are:

- Architecture diagrams
- Dataflow transitions
- Data classifications
- You will also need to gather people from different roles with sufficient technical and risk awareness to agree on the framework to be used during the Threat modeling exercise.

#### What can go wrong?

This is a “research” activity in which you want to find the main threats that apply to your application. There are many ways to approach the question, including brainstorming or using a structure to help think it through. Structures that can help include STRIDE, Kill Chains, CAPEC and others.

#### What are we going to do about that?

In this phase you turn your findings into specific actions.

#### Did we do a good enough job?

Finally, carry out a retrospective activity over the work you have done to check quality, feasibility, progress, and/or planning. Review needed changes to your process, your methodology, and how you communicate results to your stakeholders.

### Process

The effort, work, and timeframes spent on threat modeling relate to the process in which engineering is happening and products/services are delivered. The idea that threat modeling is waterfall or ‘heavyweight’ is based on threat modeling approaches from the early 2000s. Modern threat modeling building blocks fit well into agile and are in wide use.

#### When to Threat Model

When the system changes, you need to consider the security impact of those changes. Sometimes those impacts are not obvious.

Threat modeling integrates into Agile by asking “what are we working on, now, in this sprint/spike/feature?”; trying to answer this can be an important aspect of managing security debt, but trying to address it per-sprint is overwhelming. When the answer is that the system’s architecture isn’t changing, no new processes or dataflows are being introduced, and there are no changes to the data structures being transmitted, then it is unlikely that the answers to ‘what can go wrong’ will change. When one or more of those changes, then it’s useful to examine what can go wrong as part of the current work package, and to understand designs trade-offs you can make, and to understand what you’re going to address in this sprint and in the next one. The question of did we do a good job is split: the “did we address these threats” is part of sprint delivery or merging, while the broader question is an occasional saw-sharpening task.

After a security incident, going back and checking the threat models can be an important process.

#### Threat Modeling: Engagement Versus Review

Threat modeling at a whiteboard can be a fluid exchange of ideas between diverse participants. Using the whiteboard to construct a model that participants can rapidly change based on identified threats is a high-return activity. The models created there (or elsewhere) can be meticulously transferred to a high-quality archival representation designed for review and presentation. Those models are useful for documenting what’s been decided and sharing those decisions widely within an organization. These two activities are both threat modeling, yet quite different.

> *Status:*Resource Index / Community References

The best resource to start learning about threat modeling or improving your existing process, is the [Threat Modeling Manifesto](https://www.threatmodelingmanifesto.org/). This Manifesto was created by a group of leading threat modeling professionals.

## Ecosystem Navigation

Use this page as a map across threat modeling resources:

- Tools and project guidance: OWASP projects listed below, including modeling tools, libraries, playbooks, and AI-assisted tooling.
- Reference charts and frameworks: classification aids such as the Threat Severity Chart.
- Related OWASP guidance: community pages, Security Culture, and DevSecOps guidance.
- External references: books, process guidance, and practice material from the wider threat modeling community.
- Future ecosystem areas: examples, benchmarks, interoperability formats, and reference architectures can be added as they become available.

## Reference Charts & Frameworks

## Threat Modeling OWASP Projects (Tools and Guidance)

- [OWASP Threat Dragon](https://owasp.org/www-project-threat-dragon/)
- [OWASP PyTM](https://owasp.org/www-project-pytm/)
- [OWASP Ontology Driven Threat Modeling](https://owasp.org/www-project-ontology-driven-threat-modeling-framework/)
- [OWASP Threat Model Library](https://owasp.org/www-project-threat-model-library/)
- [OWASP SAP Threat Modeling Builder](https://owasp.org/www-project-sap-threat-modeling-builder/)
- [OWASP Cumulus - gamified threat modeling for the cloud](https://owasp.org/www-project-cumulus/)
- [OWASP Cornucopia - gamified threat modeling](https://owasp.org/www-project-cornucopia/)
- [OWASP Threat Modelling Guide](https://owasp.org/www-project-threat-modelling-guide/)
- [OWASP Threat Modeling Playbook](https://owasp.org/www-project-threat-modeling-playbook/)
- [OWASP Dragon GPT](https://owasp.org/www-project-dragon-gpt/)
- [OWASP Precogly](https://precogly.github.io/precogly/)

## Additional OWASP References

These links include related OWASP project and community resources. Some of these pages may include historical material and should be read according to this status shown below.

- [Threat Modeling in OWASP Security Culture](https://owasp.org/www-project-security-culture/v10/6-Threat_Modelling/)
- [Threat Modeling in OWASP Community Pages](https://owasp.org/www-community/Threat_Modeling)
- [Threat Modeling Process in OWASP Community Pages (historical)](https://owasp.org/www-community/Threat_Modeling_Process)
- [Threat Modeling at the OWASP DevSecOps Guideline Project](https://owasp.org/www-project-devsecops-guideline/latest/00b-Threat-modeling)

## Additional References

- [Adam Shostack - “Threat Modeling: Designing for Security”](https://shostack.org/books/threat-modeling-book)
- [Tony Uceda-Velez - “Risk Centric Threat Modeling: Process for Attack Simulation and Threat Analysis”](https://versprite.com/author/tony-ucedavelez/)
- [Brook Schoenfield - “Securing Systems: Applied Security Architecture and Threat Modeling”](http://brookschoenfield.com/?page_id=245)
- [Microsoft’s Security Development Process](https://www.microsoft.com/en-us/securityengineering/sdl)
- [Microsoft Threat Modeling & Tool](https://www.microsoft.com/en-us/securityengineering/sdl/threatmodeling)
- [SAFECode - “Tactical Threat Modeling”](https://safecode.org/tactical-threat-modeling/)
- [Matt Coles & Izar Tarandach - “Threat Modeling: A Practical Guide For Development Teams”](https://threatmodeling.dev)
