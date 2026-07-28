---
title: OWASP Threat Model Library
source: owasp.org
url: https://owasp.org/www-project-threat-model-library/
collector: owasp
category: web-security
tags:
- web-security
- threat
- owasp
- model
- modeling
date_collected: '2026-07-26T12:44:43.093190Z'
language: unknown
---

# OWASP Threat Model Library

## Our Mission

> 🎯
>
>
> To enable secure software architectures by democratising threat modeling through open-source, community engagement and AI advancements with clean, vetted and reliable data.

Welcome to the first, open-sourced, structured, peer-reviewed threat modeling dataset. By generating this open-source curated dataset of real-world threat models, we aim to:

- Promote and contribute to the standardization of threat modelling
- Contribute to the knowledge exchange between peers by reviewing every model.
- Improve the security of open-source applications by having them openly threat modeled. Death to security via obscurity!
- Create a dataset to fine-tune existing pre-trained LLMs to achieve more reliable threat modeling results

## News

[OWASP Threat Dragon](https://owasp.org/www-project-threat-dragon/) to support OWASP Threat Model Library Schema export by end of the year! With also the fact that threat models in the [OWASP Threat Model Cookbook](https://github.com/OWASP/threat-model-cookbook) are imported as examples in Threat Dragon, this will help produce more threat models to push to the library!

## Events

Project was presented at the OWASP Global AppSec in Barcelona on 29th of May 2025, along with the v1.0 release of the schema!

## Road Map

- **Start Receiving Contributions!**
  - See the schema, uploaded examples and start threat modelling!
- **Community Engagement:**
  - Workshops and [hackathons](https://airtable.com/appwu5c5wt1zJXhIQ/pagnNjTTHWSMQJIer/form)will be organized to promote collaboration and encourage community involvement.
- Workshops and
- **Threat Modeling for Popular Open Source Software:**
  - Initiatives will be launched to model the security threats of widely used open-source software.

## FAQs

- **How do I contribute?**

  See our Conributing Tab on the

  [project page](https://owasp.org/www-project-threat-model-library/)!
- **What is the CycloneDx TM-BOM?**

  CycloneDx TM-BOM (Threat Model Bill of Materials) is an industry-standard specification that provides a way to describe threat models. The official release is pending! Once TM-BOM is released, there will be another version released of the Threat Model Library Schema to ensure compatibility.
- **What tools can I use for threat modeling?**

  There are several tools available for threat modeling, both open-source and commercial. Some popular options include:

  - **OWASP Threat Dragon**(open-source)
  - **OWASP pytm**(open-source)
  - **Microsoft Threat Modeling Tool**(free, proprietary)

  You can use any tool you’re comfortable with as long as the output can be converted into the JSON format once the schema is published.
- **How will threat models be reviewed and validated?**

  Threat models submitted to the repository will be reviewed by the maintainers and the community. The review process will ensure that the model adheres to the schema, follows best practices, and provides meaningful insights. Reviewers may request adjustments or additional details before merging.
- **What happens after I submit a threat model?**

  After submission, the maintainers and community will review the model. If it meets the standards, it will be merged into the library. We encourage contributors to continuously update and refine threat models as new information or threats emerge.
- **Will there be support or training for beginners in threat modeling?**

  Yes, we plan to offer training resources, workshops, and tutorials for those who are new to threat modeling. These resources will help you understand the key concepts, tools, and best practices in threat modeling.
- **How do I report issues or suggest improvements to the project?**

  If you encounter any issues or have suggestions for improvement, you can open an issue in the project’s GitHub repository. Be sure to provide as much detail as possible, and if applicable, a proposed solution or workaround.

## Thank You Notes

Thank you to our sponsors from DevArmor!

Contributions will be used for organising hackathons and community engagement.
Register interest for a hackathon [here](https://airtable.com/appwu5c5wt1zJXhIQ/pagnNjTTHWSMQJIer/form).

Thank you to the [CycloneDX](https://owasp.org/www-project-cyclonedx/) TM-BOM workgroup - including:

## Contact Us

> ### ⭐ Key Contributors
>
> *Izar Tarandach*—*pytm Project Leader and just a guy that talks a lot and wears funny conference t-shirts*
> *Jon Gadsden*—*Threat Dragon & DevGuide Co-Leader*
> *Steve Springett*—*OWASP Dependency-Track Leader, OWASP SCVS Co-Author, Chair of the OWASP CycloneDX Core Working Group, Chair of Ecma TC54, Core Member of the PackageURL specification, Member of the OWASP Global Board of Directors, and Security Leader at ServiceNow*

# Contributing Guidelines

Thank you for your interest in contributing to the Threat Model Library - an OWASP project. We welcome all contributions and appreciate your efforts to improve our projects.

## Getting Started

To get started with contributing to any OWASP project, please follow these steps:

- [Join](https://owasp.org/slack/invite)the[OWASP Slack workspace](https://owasp.slack.com)to connect with the OWASP community and get help with any questions you may have.
- Head over to our

  [OWASP Slack channel - #project-threat-model-library](https://owasp.slack.com/archives/C08UNEQTPUY)if any questions.
- Fork the repository and clone it to your local machine.
- To understand the schema better head over to the schema

  [specification tab on our page](https://owasp.org/www-project-threat-model-library/)!
- Go ahead and create a threat model in the json format!
- Validate against the json schema.
- Submit a pull request with your changes. You can ping the reviewers on the Slack channel, or just sit tight and wait - we will review!

## Pull Request Guidelines

Before submitting a pull request, please make sure:

- Your changes are consistent with the project’s goals and objectives.
- Your changes are well-documented and follow the project’s coding standards.
- Your changes do not introduce new bugs or break existing functionality.
- Your changes are accompanied by tests, if applicable.
- Your pull request includes a clear and concise description of the changes you have made.

## Code of Conduct

We ask that all contributors to OWASP projects abide by our [Code of Conduct](https://owasp.org/www-policy/operational/code-of-conduct). This code outlines our expectations for behavior within the project community and helps us maintain a welcoming and inclusive environment for all contributors.

## Hackathon Interest

Register interest for a hackathon [here](https://airtable.com/appwu5c5wt1zJXhIQ/pagnNjTTHWSMQJIer/form).

# **OWASP Threat Model Library Schema Specification**

This specification explains each major element defined in the OWASP Threat Model Library JSON Schema. It is designed to help understand the purpose and relationships of various schema components.

## **Document Metadata**

### **``` version ```**
```
version
```

A structured version number (e.g., “1.0”) representing the current version of the threat model. Helps track evolution of the model over time.

### **``` $schema ```**
```
$schema
```

Specifies the Threat Model Library schema, and its specific version, the threat model document conforms to. For example:
```
“$schema”: “https://github.com/OWASP/www-project-threat-model-library/blob/v1.0.0/threat-model.schema.json”
```

## **System Description**

The following top-level properties describe the system being threat-modeled.

### **``` scope ```**
```
scope
```

Defines the boundary and criticality of what is being modeled. This is foundational to any threat modeling exercise, as it determines what is included/excluded - “scoping the work” is a common terminology used in threat modelling or other security domains like pentesting.

- ```
  title  ```

  : Name of the system being modeled.
- ```
  description
  ```

  : Describes what’s in scope and what’s out of scope. This is distinct from the description of the system’s purpose and behavior, which goes in the*top-level*
  ```
  description
  ```

  property, separate from
  ```
  scope
  ```

  .
- ```
  business_criticality  ```

  : Indicates how important the system is to business operations. This helps prioritize risk mitigation.
- ```
  data_sensitivity
  ```

  : Flags if the system handles sensitive data types (e.g., credentials, PII). Critical for compliance and privacy.
- ```
  exposure  ```

  :

  ```
  internal  ```

  or

  ```
  external  ```

  access. Externally facing systems are at higher risk.
- ```
  tier
  ```

  : Prioritization tier used to guide depth of modeling, risk exposure and review frequency.
  - ```
    mission_critical:
    ```

    - business criticality maximal + external
    - business critical maximal + stores sensitive data
    - business criticality high + stores sensitive data + external
  - ```
    business_critical
    ```

    - business criticality maximal and no sensitive data, internal
    - business criticality high + external but no sensitive data
    - business criticality high + sensitive data + internal
    - business criticality moderate but sensitive data + external
  - ```
    important
    ```

    - business criticality moderate and below + sensitive data
    - business criticality moderate + external, no sensitive data
  - ```
    non_critical
    ```

    - business criticality moderate and below + internal and no sensitive data
    - business criticality low and minimal, no sensitive data, can be external

### ``` description ```

Describes the system’s purpose and behavior and any other business context not otherwise captured.

## **Architecture Modeling**

### **``` trust_zones ```**
```
trust_zones
```

Logical areas with uniform trust assumptions (e.g., public internet, internal VPC, secure enclave). Used to define boundaries of exposure and control. Each
```
component
```

is assigned to a
```
trust zone
```

.

### **``` trust_boundaries ```**
```
trust_boundaries
```

Interfaces where data crosses from one trust zone to another. These are high-risk areas in any architecture:

- Controls (e.g., authentication, access control) must be explicitly modeled here.
- To exist they must be defined with controls such as encryption, authentication, token management, session security …
- If a trust boundary is not defined then that is a threat modelling finding - the root cause of potential threats!

### **``` actors ```**
```
actors
```

These are commonly known as entities. Human or machine entities that interact with the system. Key to identifying external threats and misuse scenarios.

### **``` components ```**
```
components
```

Building blocks of the system (e.g., APIs, backend services). Central to threat modeling since most threats target specific components.

### **``` data_stores ```**
```
data_stores
```

Where data is stored or persisted. Important for identifying risks like unauthorized access, data corruption, and backups.

### **``` data_sets ```**
```
data_sets
```

Logical groupings of data. Mapping datasets to their stores helps clarify data flow, exposure, and sensitivity.

### **``` data_flows ```**
```
data_flows
```

Represents communication between components, actors, and data stores. Data flows are key to STRIDE-based threat modeling and attack path analysis.

### **``` diagrams ```**
```
diagrams
```

Enables visual system modeling using PlantUML, Mermaid, or similar. Essential for collaboration and reviewing architecture.

## **Security Modeling**

### **``` assumptions ```**
```
assumptions
```

Things you take as true about your system (e.g., “TLS terminates at the load balancer”). Helps clarify model boundaries and gaps.

- ```
  description  ```

  : An arbitrary statement about the system.
- ```
  topics
  ```

  : A list of topics on which the assumption makes a statement. These topics will be of a standardized taxonomy and must not be arbitrarily chosen. As of right now, no topics have been standardized, so this property must not be specified.
- ```
  validity  ```

  : Whether the assumption is

  ```
  unconfirmed  ```

  (proposed/assumed by a stakeholder),

  ```
  confirmed  ```

  (definitely true), or

  ```
  rejected  ```

  (proposed but known to be false).

### **``` threat_personas ```**

```
threat_personas```

Adversary profiles that inform how and why threats might be realized. Useful for risk assessment and simulating realistic attacker behavior.

Aids in justifying and validating threats. Supports structured persona-based modeling and possible support for integration with threat detection tools in the future.

### **``` threats ```**

```
threats```

Individual threat events. Each threat references its persona, attack vector (CAPEC), and weakness (CWE). They are the core unit of security concern in the model.

### **``` controls ```**

```
controls```

Implementations of mitigations tied to specific threats. Helps ensure your model leads to actionable recommendations.

**Effectiveness of controls:** Added as a property (e.g., minimal to maximal scale) to assess relative control strength.

Distinguished from mitigations which is the process of implementing countermeasures. A mitigation is the **effect** or **strategy** of reducing risk, rather than the specific tool or mechanism.

We chose the term “controls” over alternatives like “mitigations” or “countermeasures” because:

- controls is more aligned with risk and governance frameworks such as ISO 27001, NIST, CIS, and SOC2
- it reflects the language used in security audits, risk treatment plans, and governance reporting
- it’s broader and implementation-agnostic, a control can be preventive, detective, or corrective - not just a technical fix
- “mitigation” often implies reduction in risk, but not full prevention
- “countermeasure” is more military/technical and less used in enterprise security governance
- it enables clearer mapping between threat models and control libraries, using controls makes it easier to link threat model outputs to control catalogs like NIST 800-53, OWASP ASVS, or CIS Controls

In short, “control” unifies threat modeling with risk governance and enterprise security frameworks — making threat models more actionable and aligned with business processes.

### **``` risks ```**

```
risks```

Risk is a function of the likelihood of a threat event / scenario’s occurrence and potential adverse impact should the event occur. A risk should be present only if a vulnerability or weakness are present that could lead to a threat event. Ties the threat model to risk management practices and governance. Enables prioritization.

Even though risks are influenced by org-specific factors (impact context, likelihood drivers), the schema retains this optional element to support linkage with enterprise risk registers.

#### **``` summary ```**

```
summary```

To formulate a risk summary consider how a threat with an exploitable weakness or vulnerability leads to a risk event and certain impact.

#### **``` likelihood ```**

```
likelihood```

Likelihood is a factor of risk. To estimate the likelihood consider the applicability of the threat persona to the business context, threat source, threat scenario, existing vulnerabilities or pre-existing conditions.

#### **``` impact ```**

```
impact```

Impact is a factor of Risk. Key considerations for impact are:

- **Operational Impact**: How the threat affects business processes.
- **Financial Impact**: The potential monetary loss.
- **Reputation Impact**: Public perception and long-term trust.
- **Regulatory/Legal Impact**: Fines, penalties, or legal consequences.

#### **``` level ```**

```
level```

- **Methodology**:

  ```
  Likelihood x Impact  ```
- **Output**:
  - **Score**: Numerical
  - **Descriptive**: Text label (e.g., Low, Medium, High)

#### **``` score ```**

```
score```

The cross product of impact and likelihood yields the risk score, a scale from 1 to 25:

#### 5x5 Risk Level Matrix

The cross product of impact and likelihood yields the risk score (1–25). Color-coded with emojis to reflect severity bands:

#### 5x5 Risk Level Matrix

The cross product of impact and likelihood yields the risk score (1–25). The matrix below is color-coded with square emojis to reflect severity bands:

*Likelihood \ Impact**1 (Negligible)**2 (Minor)**3 (Moderate)**4 (Major)**5 (Severe)**1 (Rare)*🟩 1 *(Very Low)*🟩 2 *(Very Low)*🟨 3 *(Low)*🟨 4 *(Low)*🟧 5 *(Medium)**2 (Unlikely)*🟩 2 *(Very Low)*🟨 4 *(Low)*🟧 6 *(Medium)*🟧 8 *(Medium)*🟥 10 *(High)**3 (Possible)*🟨 3 *(Low)*🟧 6 *(Medium)*🟧 9 *(Medium)*🟥 12 *(High)*🟪 15 *(Very High)**4 (Likely)*🟨 4 *(Low)*🟧 8 *(Medium)*🟥 12 *(High)*🟪 16 *(Very High)*🔴 20 *(Critical)**5 (Almost Certain)*🟧 5 *(Medium)*🟥 10 *(High)*🟪 15 *(Very High)*🔴 20 *(Critical)*🔴 25 *(Critical)*

Based on the numerical value of the risk score, we define the following risk levels:

*Risk Score Range**Risk Level*🟩 1–2Very Low🟨3–4Low🟧 5–9Medium🟥 10–12High🟪13–16Very High🔴20–25Critical

#### Likelihood and impact assesment guidance

*Value**Likelihood**Definition*1RareVery unlikely to occur; may happen only in exceptional circumstances, such as once in 10+ years.2UnlikelyCould occur but not expected; has happened once in 5–10 years.3PossibleMight occur under some circumstances; happens every 2–5 years.4LikelyExpected to occur in some situations; happens at least once a year.5Almost CertainExpected to occur regularly; happens multiple times a year or more frequently.

#### Impact Severity Definitions

*Value**Impact Severity**Operational Impact**Financial Impact**Reputation Impact**Regulatory/Legal Impact*1InsignificantMinimal disruption, no noticeable effect on business operations.<0.1% of annual revenue.No damage to reputation.No legal or regulatory implications.2MinorSome minor disruption, but recoverable with little effort.0.1% to 0.5% of annual revenue.Small, localized damage to reputation, quickly recoverable.Minor compliance issues, no fines or legal action.3ModerateNoticeable operational impact, moderate recovery efforts required.0.5% to 1% of annual revenue.Moderate reputation damage; some negative press, recoverable.Possible fines or legal action; warning from regulators.4MajorSignificant operational disruption; requires substantial resources.1% to 5% of annual revenue.Significant damage to reputation; major loss of customer trust.Substantial legal issues; fines and regulatory penalties.5SevereCritical operational impact; operations cease or major losses.>5% of annual revenue.Severe reputation damage; long-term loss of market position.Major legal action; large fines; potential shutdown.

## **Extensions**

### **``` extensions ```**

```
extensions```

Allows custom fields while enforcing namespace uniqueness. Enables organizations to capture additional data relevant to their threat modeling workflows. For example:

```
```
{
  ...
  "extensions": {
    "example.com/owasp-threat-model-foobar-extension": {
      // Whatever schema is needed, whereas the schema should be clearly
      // documented at https://example.com/owasp-threat-model-foobar-extension.
      ...
    },
    "example.net/other-extension": {
      // Analogously.
      ...
    }
  }
}
```
```

This schema enables traceable, evidence-backed, and enterprise-ready threat modeling for modern systems. It is optimized for structured outputs, tool integration, and supports formal risk analysis through linkage of threats, risks, and mitigations.

For implementation guidance or examples, refer to <https://github.com/OWASP/www-project-threat-model-library>.

# 🌟 Demonstrate Your Brand’s Commitment to Innovation

### Sponsor the OWASP Threat Model Library (TML)

## 🚀 Shaping the Future of Threat Modeling

The **OWASP Threat Model Library (TML)** is the first open, community-driven dataset that collects real-world threat models.  
It lowers the barriers to entry for developers, engineers, and security teams by providing **reusable examples, structured schemas, and practical templates**.

By supporting this project, you help move threat modeling from a niche activity to a **widely adopted practice**, embedded in how systems are designed and built.

## 🎯 Incentives to Support the OWASP Threat Model Library

### 🌍 Global Outreach

Stand alongside OWASP in creating the world’s most comprehensive open dataset of threat models — a resource that will influence organizations, regulators, and security research for years to come.

### 💡 Drive Innovation

Help drive innovation in threat modeling: from standardising schemas to building the pre-requisite for threat modelling / security AI development.

### 🤝 Join the Community

Your support powers **events, workshops, and hackathons**, where practitioners share hard-won lessons and refine models together.

## 🔧 Supporting the Evolution of TML

The OWASP Threat Model Library is powered by passionate volunteers.  
Your sponsorship ensures ongoing improvements, outreach, and innovation, including:

- Development of new threat models for emerging technologies
- Threat modeling data model innovation support
- Community events and workshops
- Talks, training, and publications that spread adoption
- Building bridges with standards bodies and other OWASP projects (e.g., )*CycloneDX*

👉 **Your contribution helps make threat modeling accessible to everyone — from developers to CISOs.**

## 🏢 Benefits for Your Organization

- **Visibility with Purpose**: Be recognized at OWASP events, on project pages, and in research outputs as a company that invests in open source and transparent security.
- **Reputation Boost**: Show customers and partners that you are committed to systemic security improvements, not just proprietary solutions.
- **Access to Experts**: Engage with a diverse network of researchers, engineers, and industry leaders advancing the state of threat modeling.

## 💎 Sponsorship Tiers

### 🏆 Gold – $10,000+

- High-visibility sponsorship with **prominent logo placement**on the project page
- Logo placement on the project Sponsorship Tab as a **Gold Sponsor**
- Recognition in co-leader and key-contributor talks/presentations
- Prominent logo placement at project events and hackathons
- Additional visibility of your organisation’s product

### 🥈 Silver – $5,000+

- Placement as **Silver Sponsor**on the sponsorship tab
- Strong visibility in project communications
- Participation in project events, workshops, and hackathons with brand visibility

### 🥉 Bronze – $1,000+

- Acknowledgment on sponsor project pages
- Inclusion as a **Bronze supporter**

## 🌱 Startup Discounts & Alternatives

- **Startups with < $30M funding**receive a**$2,500 discount**on Silver and Gold sponsorships.
- In certain cases, we can substitute part of the funding with resources such as:
  - Hackathon or workshop planning
  - Direct project contributions
  - Community outreach
  - Event venues, speakers, and platforms

📩 **Interested? Let’s talk!**
