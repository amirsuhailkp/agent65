---
title: OWASP ThreatAtlas
source: owasp.org
url: https://owasp.org/www-project-threatatlas/
collector: owasp
category: web-security
tags:
- web-security
- threatatlas
- threat
- threats
- diagrams
date_collected: '2026-07-26T12:44:43.693418Z'
language: unknown
---

# OWASP ThreatAtlas

**OWASP ThreatAtlas** is an open-source web application for team-based threat modeling. Organizations run structured sessions by inviting developers, DevOps, architects, and security engineers to map systems, record threats and mitigations, and review risk in one place—instead of scattering notes across documents and slides.

The project is **Apache 2.0** licensed. The [application source](https://github.com/OWASP/www-project-threatatlas/tree/main/threatatlas-app) ships as a modern stack (FastAPI, PostgreSQL, React) and is designed to be **self-hosted** so data stays under your control.

## 🌟 Mission

Bridge the gap between security frameworks and real architectures: make it easy to **draw** data flows, **attach** threats and mitigations from recognized knowledge bases, **collaborate** with clear ownership and history, and **review** how risk changes over time.

## 🧭 What ThreatAtlas offers

- **Data Flow Diagrams (DFDs)**— Interactive diagrams for processes, data stores, external entities, flows, and trust boundaries, with**Draw.io / .drawio import**and diagram templates for fast onboarding.
- **Component Library**— Drag pre-built security components into diagrams and use the Component Threat Library to browse, edit, and revert predefined threat/mitigation mappings per framework.
- **Threats, mitigations, and risk**— Link mitigations to threats; record likelihood, impact, and risk score; see risk-oriented views in**analytics**and heatmap overlays.
- **Knowledge base**— Browse and apply content from multiple frameworks (e.g. STRIDE, PASTA, LINDDUN, OWASP references, MITRE-oriented material, CVSS-oriented guidance—see the app and docs for the current catalog).
- **Collaboration**— Products shared with teammates;**RBAC**, invitations, live cursor tracking, real-time diagram sync, auto-save, and visibility controls aligned with how teams actually work.
- **Approvals and risk acceptance**— Formal approval workflows, justification tracking, a dedicated approvals dashboard, and notifications for reviewers and collaborators.
- **Notifications and search**— In-app bell with unread badges plus global search (⌘K / Ctrl+K) for products, diagrams, KB threats, and mitigations.
- **DevOps integration**— API Tokens for machine access, JIRA issue creation from threat cards, and a CI/CD Security Gate endpoint for pass/fail checks.
- **History**—**Diagram versioning**with comparison, including visibility into threat and mitigation changes—not only canvas edits.
- **Comments**— Discussion on threats and mitigations for async review.
- **Custom frameworks**— Define organization-specific methodology and reuse it across diagrams.
- **Optional AI assistant**— When enabled by an administrator, a**conversational AI assistant**in the diagram editor can help explore threats and proposals; provider and keys are configured in-app (see deployment and security notes in the docs).

## 🏗 Why OWASP ThreatAtlas?

- **Open source and self-hosted**— Inspect the code, adapt it, and run it in your environment.
- **Many frameworks, one workspace**— Combine diagramming, a structured threat/mitigation model, and a growing knowledge base instead of maintaining separate spreadsheets and diagrams.
- **Built as a product, not a static site**— Authentication, teams, persistence, and UI workflows for day-to-day threat modeling—not only reference pages.
- **Extensible methodology**— Custom frameworks sit alongside built-in catalogs so teams can encode their own standards.
- **Practical outputs**— Analytics, versioning, and structured data (e.g. diagram export) support reviews, onboarding, and continuous refinement of a threat model.

## 🌳 Repository layout

- — Backend, frontend, Docker Compose, and tool documentation.[ThreatAtlas application (](https://github.com/OWASP/www-project-threatatlas/tree/main/threatatlas-app)
  ```
  threatatlas-app/
  ```

  )

## 📖 Documentation

### 🛠 Installation & setup

Run ThreatAtlas locally or in your infrastructure:

### 💻 Development & contributing

Build, test, and submit changes:

### 👤 User guide

Learn the main UI flows (products, diagrams, threats, mitigations, settings):

### 📋 Releases

What changed in each version:

## Contributors

ThreatAtlas is a community-driven project. We are grateful to all our contributors who help make threat modeling more accessible and effective.

### Core Team

- **Ali Yazdani**- Project Leader

### How to Become a Contributor

We welcome contributions of all kinds!

- **Code**: Check our[GitHub Repository](https://github.com/OWASP/www-project-threatatlas).
- **Threat Models**: Help us expand the knowledge base for cloud-native services.
- **Feedback**: Join our Slack channel and share your thoughts.

See our [Development & Contributing Guide](threatatlas-app/docs/development.md) for more details.

## Documentation

Comprehensive guides for using and deploying ThreatAtlas.

### 🚀 Getting Started

- : How to set up ThreatAtlas using Docker or production deployment.[Installation Guide](threatatlas-app/docs/installation.md)
- : A step-by-step tutorial on creating products, diagrams, and managing threats.[User Guide](threatatlas-app/docs/user-guide.md)
- : Technical setup for codebase contributors.[Development Guide](threatatlas-app/docs/development.md)

### 🛠 Technical Reference

- **Backend API**: The FastAPI backend provides interactive Swagger documentation at
  ```
  /docs
  ```

  when running the application.
- **Data Models**: Documentation for our service-specific threat models and mitigation mappings.

### 🤝 Contribution Docs

- : How to set up your environment and submit Pull Requests.[Development Guide](threatatlas-app/docs/development.md)
- : How to report security vulnerabilities.[Security Policy](SECURITY.md)
