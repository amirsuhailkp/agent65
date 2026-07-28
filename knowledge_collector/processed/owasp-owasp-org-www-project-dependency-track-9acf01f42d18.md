---
title: OWASP Dependency-Track
source: owasp.org
url: https://owasp.org/www-project-dependency-track/
collector: owasp
category: web-security
tags:
- web-security
- dependency-track
- risk
- vulnerability
- owasp
date_collected: '2026-07-26T12:43:42.624737Z'
language: unknown
---

# OWASP Dependency-Track

For more details about Dependency-Track see the projects website at [dependencytrack.org](https://dependencytrack.org/)

Dependency-Track is an intelligent [Component Analysis](https://owasp.org/www-community/Component_Analysis) platform that allows organizations to
identify and reduce risk in the software supply chain. Dependency-Track takes a unique
and highly beneficial approach by leveraging the capabilities of [Software Bill of Materials](https://owasp.org/www-community/Component_Analysis#software-bill-of-materials-sbom) (SBOM). This approach
provides capabilities that traditional Software Composition Analysis (SCA) solutions cannot achieve.

Dependency-Track monitors component usage across all versions of every application in its portfolio in order to proactively identify risk across an organization. The platform has an API-first design and is ideal for use in CI/CD environments.

## Features

- Consumes and produces [CycloneDX](https://cyclonedx.org)Software Bill of Materials (SBOM)
- Consumes and produces CycloneDX Vulnerability Exploitability Exchange (VEX)
- Full-stack component support for:
  - Applications
  - Libraries
  - Frameworks
  - Operating systems
  - Containers
  - Firmware
  - Files
  - Hardware
  - Services
- Tracks component usage across every application in an organizations portfolio
- Quickly identify what is affected, and where
- Identifies multiple forms of risk including
  - Components with known vulnerabilities
  - Out-of-date components
  - Modified components
  - License risk
  - More coming soon…
- Integrates with multiple sources of vulnerability intelligence including:
  - [National Vulnerability Database](https://nvd.nist.gov)(NVD)
  - [GitHub Advisories](https://www.github.com/advisories)
  - [Sonatype OSS Index](https://ossindex.sonatype.org)
  - [VulnDB](https://vulndb.cyberriskanalytics.com)from[Risk Based Security](https://www.riskbasedsecurity.com)
  - More coming soon.
- Helps to prioritize mitigation by incorporating support for the [Exploit Prediction Scoring System (EPSS)](https://www.first.org/epss/)
- Maintain a private vulnerability database of vulnerability components
- Robust policy engine with support for global and per-project policies
  - Security risk and compliance
  - License risk and compliance
  - Operational risk and compliance
- Ecosystem agnostic with built-in repository support for:
  - Cargo (Rust)
  - Composer (PHP)
  - Gems (Ruby)
  - Hex (Erlang/Elixir)
  - Maven (Java)
  - NPM (Javascript)
  - NuGet (.NET)
  - Pypi (Python)
  - More coming soon.
- Identifies APIs and external service components including:
  - Service provider
  - Endpoint URIs
  - Data classification
  - Directional flow of data
  - Trust boundary traversal
  - Authentication requirements
- Includes a comprehensive auditing workflow for triaging results
- Configurable notifications supporting Slack, Microsoft Teams, WebEx, Webhooks, and Email
- Supports standardized SPDX license ID’s and tracks license use by component
- Easy to read metrics for components, projects, and portfolio
- Native support for Kenna Security, Fortify SSC, ThreadFix, and DefectDojo
- API-first design facilitates easy integration with other systems
- API documentation available in OpenAPI format
- OAuth 2.0 + OpenID Connect (OIDC) support for single sign-on (authN/authZ)
- Supports internally managed users, Active Directory/LDAP, and API Keys
- Simple to install and configure. Get up and running in just a few minutes

## Integrations

## Installation

Dependency-Track is distributed as Docker containers.

### Docker Compose
```
```
curl -LO https://dependencytrack.org/docker-compose.yml
docker-compose up -d```
```

### Docker Swarm
```
```
curl -LO https://dependencytrack.org/docker-compose.yml
docker swarm init
docker stack deploy -c docker-compose.yml dtrack```
```

## News

The latest releases of Dependency-Track are published on GitHub.

👉 **View all releases:**
https://github.com/DependencyTrack/dependency-track/releases

For detailed release notes and documentation, please visit:

📖 **Release announcements & documentation:**
https://docs.dependencytrack.org/

To stay up to date:

- Watch the project on GitHub for release notifications
- Follow the OWASP Dependency-Track project page
- Join the OWASP Slack (#dependency-track channel)

## Supporters

Dependency-Track is developed by a worldwide team of volunteers.

But we have also been helped by many organizations, either financially or by encouraging their employees to work on Dependency-Track:

## U.S. Executive Order 14028

Since its inception in 2013, OWASP Dependency-Track has been at the forefront of analyzing bill of materials for cybersecurity
risk identification and reduction. Dependency-Track allows organizations and governments to operationalize SBOM in
conformance with [U.S. Executive Order 14028](https://www.whitehouse.gov/briefing-room/presidential-actions/2021/05/12/executive-order-on-improving-the-nations-cybersecurity/).

- Supports the OWASP CycloneDX BOM format specifically defined in the [NTIA Minimum Elements For a Software Bill of Materials(SBOM)](https://www.ntia.gov/files/ntia/publications/sbom_minimum_elements_report.pdf)
- Consumes and analyzes SBOMs for known security, operational, and license risk
- Ideal for use in [procurement](https://docs.dependencytrack.org/usage/procurement/)and[continuous integration and delivery](https://docs.dependencytrack.org/usage/cicd/)environments
- Supports the OWASP CycloneDX VEX format exceeding the [Vulnerability Exploitability Exchange requirements defined by CISA](https://www.cisa.gov/sites/default/files/publications/VEX_Use_Cases_Document_508c.pdf)

### For software consumers

- Tracks all systems and applications that have SBOMs
- Upload SBOMs through the user interface or via automation
- Components defined in SBOMs will be analyzed for known vulnerabilities using multiple sources of vulnerability intelligence, including the [NVD](https://nvd.nist.gov/)
- Displays all identified vulnerabilities and vulnerable components for every SBOM analyzed
- Upload CycloneDX VEX obtained from suppliers to gain insight into the vulnerable components that pose risk, and the ones that don’t
- Quickly identify all systems and applications that have a specific component or are affected by a specific vulnerability
- Helps to prioritize mitigation by incorporating support for the [Exploit Prediction Scoring System (EPSS)](https://www.first.org/epss/)
- Evaluate the portfolio of systems and applications against user-configurable security, operational, and license policies

### For software producers

- Create and consume CycloneDX SBOMs in development pipelines
- SBOMs will be analyzed for known security, operational, and license risk
- Evaluates the portfolio of applications against user-configurable security, operational, and license policies
- Inspect security findings and make audit decisions about the relevance and exploitability of each vulnerability
- CycloneDX BOMs can be dynamically generated from current inventory for any application
- CycloneDX VEX is dynamically generated from audit decisions for each application
- An API-first design allows software producers to extract SBOMs for released products, produce VEX whenever updated audit decisions are made, and make data available to internal systems responsible for SBOM and VEX distribution.

### Other considerations

- Both CycloneDX and Dependency-Track are full-stack solutions supporting software, hardware, and services. The CycloneDX standard and use with Dependency-Track is not limited to SBOM use cases.
- Software consumers may optionally audit security findings from vendor SBOMs. If consumers discover discrepancies in vendor supplied VEX, consumers can share their own auto-generated VEX with suppliers, completing a bi-directional exchange of vulnerability and exploitability information.
