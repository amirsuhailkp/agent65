---
title: OWASP VXDF Validated Exploitable Data Flow Format
source: owasp.org
url: https://owasp.org/www-project-vxdf/
collector: owasp
category: web-security
tags:
- web-security
- vxdf
- owasp
- security
- schema
date_collected: '2026-07-26T12:44:45.627390Z'
language: unknown
---

# OWASP VXDF (Validated Exploitable Data Flow) Format

# 🛡️ VXDF: Evidence-Based Vulnerability Intelligence

The first standardized format for reporting **validated exploitable** vulnerabilities with proof

## What is VXDF?

**OWASP VXDF (Validated Exploitable Data Flow)** is a revolutionary approach to vulnerability reporting that focuses on **confirmed exploitable** code vulnerabilities with mandatory validation evidence. Unlike traditional vulnerability scanners that generate noise, VXDF provides actionable intelligence that security teams can trust.

### The Alert Fatigue Problem

Security teams are drowning in vulnerability alerts from scanning tools (SAST, DAST, SCA). The overwhelming majority are false positives or theoretical vulnerabilities with no practical exploit path, resulting in:

- 🚨 **Alert Fatigue:**Teams waste 70%+ of their time on non-critical issues
- ⏰ **Delayed Response:**Real threats get buried in the noise
- 😤 **Developer Frustration:**Constant interruptions for non-exploitable findings
- 📊 **Inconsistent Data:**Incompatible formats across security tools

### 🔍 Evidence-Based

Every vulnerability includes concrete proof of exploitability - no more guessing if threats are real

### ⚙️ Machine-Readable

JSON format enables seamless automation in security tools and CI/CD pipelines

### 🎯 Actionable Intelligence

Clear exploitation paths and concrete proof help teams prioritize effectively

### 🔗 Standards-Aligned

Compatible with SARIF, SPDX, and other security frameworks

## What VXDF Contains

- **🆔 Vulnerability Identification:**CWE mapping and comprehensive weakness details
- **📦 Affected Components:**Precise software/library/code segment information
- **🛤️ Exploitation Path:**Step-by-step attack flow from source to sink
- **✅ Validation Evidence:**Working PoC scripts, HTTP requests/responses, or other verifiable proof
- **⚖️ Impact Assessment:**Contextualized severity and business impact analysis

## Who Benefits from VXDF?

- **🛡️ Security Teams:**Cut through the noise and focus on real threats
- **👨‍💻 Developers:**Receive clear, actionable reports with evidence
- **🏢 Tool Vendors:**Provide high-fidelity results that teams actually trust
- **🕵️ Security Researchers:**Submit findings with verifiable proof of concept
- **🏛️ Organizations:**Dramatically improve security posture efficiency

## 📚 Project Resources

### 🔗 Official Links

- **Project Website:**[vxdf.org](https://vxdf.org)
- **GitHub Repository:**[mihir-shah99/vxdf](https://github.com/mihir-shah99/vxdf)
- **Schema Explorer:**[Interactive Schema](https://vxdf.org/schema-explorer)

### 📖 Documentation & Tools

- **Normative Schema:**[JSON Schema v0.2](https://github.com/mihir-shah99/vxdf/blob/main/docs/normative-schema.json)
- **Example Files:**[Sample VXDF](https://github.com/mihir-shah99/vxdf/blob/main/test-data/example1_flow_based.vxdf.json)
- **Integration Guide:**[Tool Integration](https://vxdf.org/integration)

### 👥 Community & Support

- **Weekly Meetings:**Tuesdays 8 AM PT
- **Discussions:**[GitHub Discussions](https://github.com/mihir-shah99/vxdf/discussions)
- **Issues:**[Bug Reports & Features](https://github.com/mihir-shah99/vxdf/issues)

### 🔧 Current Development

- **SDK Status:**Python ✅, JavaScript & Go 🔄
- **Parser Support:**Snyk, Semgrep, OWASP ZAP 🔄
- **Intelligence Engine:**Enhanced correlation 🔄

## 🚀 Get Involved Today!

### 💻 For Contributors

- Review the [Contributing Guide](https://github.com/mihir-shah99/vxdf/blob/main/CONTRIBUTING.md)
- Check [Good First Issues](https://github.com/mihir-shah99/vxdf/labels/good%20first%20issue)
- Join our [Slack channel](https://owasp.slack.com/archives/C08T85605RS)

### 🏢 For Tool Vendors

- Implement VXDF in your security products
- Access our [Partnership Program](https://vxdf.org/partners)
- Contact us for integration support

### 🏛️ For Organizations

- Pilot VXDF in your security workflow
- Join our [Advisory Board](https://vxdf.org/advisory-board)
- Share feedback and use cases

### Related OWASP Projects

- [OWASP SARIF](https://owasp.org/www-project-sarif/)- Static Analysis Results Interchange Format
- [OWASP Dependency Check](https://owasp.org/www-project-dependency-check/)- Software Composition Analysis
- [OWASP ZAP](https://owasp.org/www-project-zap/)- Web Application Security Scanner

**VXDF:**

*Making vulnerability intelligence actionable, not overwhelming*

# VXDF Project Roadmap

## Current Status (Q2 2025)

### ✅ Completed (2024-Q1 2025)

- **Foundational Schema Definition**- Base VXDF JSON schema with validation rules
- **Normative Schema Documentation**- Complete schema specification v0.1-v0.2
- **GitHub Repository & Community**- Project infrastructure and OWASP integration
- **Schema Validation Tools**- Production-ready validation tools and CLI
- **Documentation Website**- Comprehensive project documentation at vxdf.org

### 🔄 In Progress (Q2 2025)

- **OWASP Top 10 2024 Mapping**- Mapping VXDF to OWASP Top 10 2024
- **Enhancing Correlation Engine**- Enhancing the correlation engine to support more complex and nuanced correlations.
- **Enhanced SDK Development**- JavaScript and Go library implementations
- **Adding more parser support**- Adding more parser support for more tools - Snyk, Semgrep, OWASP ZAP etc.

## Q3 2025 Milestones

### Core Platform Enhancement

- **Multi-Language SDK Suite**- Complete JavaScript, Go, and .NET SDKs
- **Intelligence Engine v1.0**- Mature validation and scoring engine.
- **Advanced Analytics Dashboard**- Real-time vulnerability management metrics
- **API Gateway**- Centralized VXDF processing and validation service

## Contribution Opportunities

### For Developers

- **SDK Development**- Contributing to multi-language library implementations
- **Intelligence Engine**- Mature coreelation and validation improvements
- **Tool Integrations**- Building connectors for security tools and platforms
- **Open Source Tools**- Community-driven utilities and extensions

### For Organizations

- **Enterprise Pilots**- Production deployment and feedback programs
- **Industry Standards Work**- Contributing to standardization efforts
- **Academic Research**- University collaboration and research projects
- **Conference Speaking**- Sharing implementation experiences and use cases

### For Vendors

- **Certified Integrations**- Building official VXDF support into security tools
- **Partnership Program**- Commercial collaboration and co-marketing opportunities
- **Technical Advisory**- Contributing to technical direction and standards
- **Marketplace Presence**- Featuring integrations in VXDF ecosystem

## Get Involved

**Current Priorities:**

- Join our [roadmap discussions](https://github.com/mihir-shah99/vxdf/discussions/categories/roadmap)
- Participate in weekly Tuesday meetings
- Contribute to [GitHub Issues](https://github.com/mihir-shah99/vxdf/issues)and development

**Partnership Inquiries:**

- **Enterprise Pilots:**Contact[[email protected]](/cdn-cgi/l/email-protection)
- **Vendor Integrations:**Join[#project-vxdf](https://owasp.slack.com/archives/C08T85605RS)
- **Academic Research:**Submit proposals via GitHub Discussions

*Roadmap Updated: June 2025 | Next Review: September 2025*

# VXDF Project Meetings

## Weekly Project Call

**Every Tuesday, 8:00 AM - 9:00 AM Pacific Time**

- **Next Meeting:**June 10, 2025 at 8:00 AM PT
- **Join:**[Google Meet](https://meet.google.com/sxb-tjao-ucp)
- **Add to Calendar:**[Google Calendar Event](https://calendar.google.com/calendar/event?action=TEMPLATE&tmeid=NTBxdDlwbWpmdXMxM29rYzFxanJmdGJkYjZfMjAyNTA2MTBUMTUwMDAwWiBtaWhpci5zaGFoQG93YXNwLm9yZw&tmsrc=mihir.shah%40owasp.org&scp=ALL)
- **Agenda:**[Google Docs](https://docs.google.com/document/d/1Hc5nmbVnyr5gExA9Z0rJSzXYhTYdQv0NBgve7UXdnHM/edit?usp=sharing)

### Time Zone Conversions

- **UTC:**4:00 PM (Winter) / 3:00 PM (Summer)
- **Eastern:**11:00 AM EST / 12:00 PM EDT
- **Central European:**5:00 PM CET / 4:00 PM CEST
- **India:**9:30 PM IST
- **Australia:**3:00 AM AEDT / 2:00 AM AEST

## Working Groups

### Schema & Standards Working Group

- **Focus:**Schema evolution, validation rules, standards alignment

### Tool Integration Working Group

- **Focus:**SDK development, Maturing Intelligence engine, and other tooling

## How to Participate

- **Join Slack:**[#project-vxdf](https://owasp.slack.com/archives/C08T85605RS)for announcements
- **Add Meeting:**Use the[calendar link](https://calendar.google.com/calendar/event?action=TEMPLATE&tmeid=NTBxdDlwbWpmdXMxM29rYzFxanJmdGJkYjZfMjAyNTA2MTBUMTUwMDAwWiBtaWhpci5zaGFoQG93YXNwLm9yZw&tmsrc=mihir.shah%40owasp.org&scp=ALL)above
- **Review Agenda:**Check the[Google Doc](https://docs.google.com/document/d/1Hc5nmbVnyr5gExA9Z0rJSzXYhTYdQv0NBgve7UXdnHM/edit?usp=sharing)before meetings

## Meeting Resources

- **Meeting Recordings:**[GitHub Repository](https://github.com/mihir-shah99/vxdf/tree/main/meeting-notes)
- **Action Items:**[GitHub Projects](https://github.com/mihir-shah99/vxdf/projects/1)
- **Technical Support:**[GitHub Issues](https://github.com/mihir-shah99/vxdf/issues)
- **General Questions:**[GitHub Discussions](https://github.com/mihir-shah99/vxdf/discussions)

*Weekly meetings every Tuesday 8:00 AM Pacific Time*
