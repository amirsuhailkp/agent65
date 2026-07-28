---
title: OWASP HACTU8
source: owasp.org
url: https://owasp.org/www-project-hactu8/
collector: owasp
category: web-security
tags:
- web-security
- testing
- security
- owasp
- systems
date_collected: '2026-07-26T12:44:15.989639Z'
language: unknown
---

# OWASP HACTU8

## Overview

HACTU8 is an OWASP Incubator Project focused on advancing security testing for modern, interconnected systems. The platform supports ethical hacking, validation, and assurance across environments that combine artificial intelligence, Internet of Things (IoT), robotics, and distributed software systems.

HACTU8 takes a holistic, system-level approach to security testing, incorporating agent-based systems, Model Context Protocol (MCP)-enabled integrations, and extensible architectures for autonomous and embedded environments. The platform enables testing across AI agents, robotic systems, edge devices, and consumer technologies, supporting modular and interoperable security tooling aligned with emerging AI execution models.

## Objectives

- Provide a structured platform for testing AI-enabled, IoT, and autonomous systems
- Enable ethical hacking and security validation of complex, interconnected environments
- Support modular, extensible security tooling and orchestration
- Promote secure design and implementation practices for emerging technologies
- Foster community collaboration and research in next-generation security testing

## Key Features

- AI-Driven Testing

  Leverage generative AI and machine learning techniques to simulate attack scenarios and identify vulnerabilities
- Agent-Based Execution

  Support testing of AI agents and autonomous workflows, including multi-agent interactions and decision chains
- MCP Integration Support

  Enable interoperability through Model Context Protocol (MCP)-compatible interfaces for context sharing and tool orchestration
- System & Device Coverage

  Assess security across IoT devices, robotics platforms, embedded systems, edge environments, and distributed services
- Extensible Architecture

  Provide plugin-based mechanisms for integrating tools, attack modules, and test scenarios
- Modular Framework

  Allow independent development and integration of testing components for flexibility and scalability

## Scope

HACTU8 focuses on security testing across:

- Artificial intelligence systems and AI agents
- IoT ecosystems and connected devices
- Robotics and autonomous systems
- Edge and embedded environments
- Distributed and agent-orchestrated systems (including MCP-enabled architectures)

## Roadmap

### Phase 1: Research and Planning

- Define requirements for AI, IoT, and autonomous system security testing
- Identify relevant attack surfaces and threat models
- Establish architecture for modular and extensible design

### Phase 2: Platform Development

- Develop modular tools for AI-driven security testing
- Implement agent-based execution models for orchestration
- Introduce MCP-compatible integrations for interoperability and context sharing
- Extend testing scenarios to robotics, edge, and embedded environments

### Phase 3: Testing and Validation

- Conduct real-world testing across AI, IoT, and autonomous systems
- Validate effectiveness of agent-based and AI-assisted testing approaches
- Refine tools and methodologies based on findings

### Phase 4: Documentation and Community Engagement

- Publish documentation, guides, and best practices
- Encourage contributions from security researchers and developers
- Collaborate with OWASP and the broader security community

## Emerging Focus: Agents and Extensibility

HACTU8 continues to evolve to address:

- AI agents and autonomous workflows
- Model Context Protocol (MCP)-enabled interoperability
- Extensible plugin architectures for tools, tests, and attack modules
- Robotics, edge systems, and constrained embedded devices

This reflects the growing importance of non-human identities and autonomous systems in modern security environments.

## Get Involved

We welcome contributions from:

- Security researchers
- AI/ML engineers
- Hardware and embedded systems developers
- Ethical hackers and penetration testers

To contribute, visit the project repository and follow the contribution guidelines.

## Project Links

- GitHub Repository: https://github.com/OWASP/www-project-hactu8
- OWASP Project Page: https://owasp.org/www-project-hactu8/

## Licensing

This project is licensed under the OWASP Foundation License.

## Acknowledgements

HACTU8 is part of the OWASP Foundation’s mission to improve software security through open collaboration, education, and innovation.

## Roadmap (As Of January 2026)

This roadmap outlines the development plan for the OWASP HACTU8 reference platform. Phase 1 focuses on building a foundational system to support AI assurance testing through UI scaffolding, test agent integration, registry design, and a lightweight scanner.

## Project Phases

PhaseNameObjective*1*Foundation and IntegrationEstablish a running UI, test orchestration, extension architecture, and registry/discovery foundation*2*Platform DevelopmentExpand into a fully functional MVP with integrated models, test automation, and extension marketplace*3*Community EngagementPromote contribution, support external tools, and build adoption with documentation and collaboration models

## Phase 1: Foundation and Integration

### M1: Mockup

> Scaffold the UI, engine shell, scanner, and API endpoints for initial visualization.

- Scaffold Streamlit UI Shell
- Build FastAPI Interface Skeleton
- Create Engine Module Skeleton (agents/orchestrator)
- Create Scanner CLI Skeleton

### M2: Requirements Documentation

> Define all core schemas, specifications, and architectural references.

- Define Initial Architecture Document
- Create Test Spec Template (JSON/YAML)
- Document OWASP Top 10 Test Concepts
- Describe Signature Format for Scanners
- Define Registry API Contract

### M3: Running Demo

> Deliver a working vertical slice using mock data to demonstrate test execution flow.

- Wire UI to Dummy API
- Run Simulated Prompt Injection Agent
- Display Result in Assurance Viewer
- Integrate Registry View from API

### M4: Extension Model

> Implement a plugin system for test extensions, aligned to the OWASP LLM Top 10.

- Define Extension Plugin Base Class
- Implement Prompt Injection Extension Stub
- Define Extension Metadata Format
- Render Extension Output in UI

### M5: Discovery Architecture

> Define and implement how LLMs, tools, and endpoints are discovered or registered.

- Design Discovery Interface (API + check-in)
- Create Signature Loader Logic
- Connect CLI Scanner to Registry
- Simulate Local Ollama/Foundry Detection
- Document Discovery Modes and Architecture

### Phase Closeout: Retrospective

> Evaluate Phase 1 and scope Phase 2 deliverables.

- Conduct Phase 1 Retrospective
- Define Milestones for Phase 2: Platform Development

## Diagrams

### Component Diagram
```
```
graph TD
  subgraph UI Layer
    A[Streamlit UI]
    A1[Workbench]
    A2[Assurance Viewer]
    A3[Registry Viewer]
    A4[Extension Panel]
  end

  subgraph Services
    S1[API Gateway / FastAPI]
    S2[Registry Service]
    S3[Identity / Auth]
  end

  subgraph Engine
    E1[Orchestrator]
    E2[Extension Loader]
    E3[Agent Runner]
  end

  subgraph Extensions
    X1[Prompt Injection Ext]
    X2[RAG Poisoning Ext]
    X3[Custom Test Ext]
  end

  subgraph Scanner CLI
    C1[AI Port Scanner]
    C2[Signature Loader]
  end

  %% UI to Services
  A -->|REST| S1
  A1 -->|Run Remote Test| S1
  A2 -->|Fetch Results| S1
  A3 -->|Get Registry| S2
  A4 -->|Run Local Extension| X1
  A4 -->|Run Local Extension| X2
  A4 -->|Run Local Extension| X3

  %% Services to Engine
  S1 -->|Invoke| E1
  E1 --> E2
  E2 -->|Load| X1
  E2 -->|Load| X2
  E2 -->|Load| X3
  E1 --> E3

  %% Extensions to Agent Runner
  X1 --> E3
  X2 --> E3
  X3 --> E3

  %% Registry and Scanner
  S2 --> E1
  S2 --> C1
  C1 --> C2
  C2 --> S2

  %% Identity
  A --> S3
  S3 --> S1```
```
