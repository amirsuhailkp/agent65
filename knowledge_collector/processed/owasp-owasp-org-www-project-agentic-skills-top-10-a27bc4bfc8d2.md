---
title: OWASP Agentic Skills Top 10
source: owasp.org
url: https://owasp.org/www-project-agentic-skills-top-10/
collector: owasp
category: web-security
tags:
- web-security
- security
- skills
- skill
- agentic
date_collected: '2026-07-26T12:45:00.005078Z'
language: unknown
---

# OWASP Agentic Skills Top 10

> *Security Risks and Mitigations for AI Agent Skills*
>
> Covering OpenClaw (SKILL.md YAML), Claude Code (skill.json), Cursor/Codex (manifest.json), and VS Code (package.json) ecosystems.

**Breadcrumb:**[OWASP](https://owasp.org/) > [Projects](https://owasp.org/projects/) > Agentic Skills Top 10

**Public review (v1):** Please review and comment on the merged v1 draft in the [Google Doc](https://docs.google.com/document/d/1A5d2OnT8h8oZo7MSde4TOT3sg3AkXJgTGQwVrAga1aE/edit?usp=drivesdk). Previous GitHub issues and pull requests remain available for historical reference, but v1 publication comments should be submitted in the Google Doc.

**Tutorial videos:** Use the [AST10 tutorial video library](/www-project-agentic-skills-top-10/videos?video=ast01) to play each risk video from selectable cards or share direct links with
```
?video=ast01
```

through
```
?video=ast10
```

.

## Table of Contents

- [Overview](#overview)
- [📊 Visual Top 10 Overview](/www-project-agentic-skills-top-10/top10)
- [Tutorial Videos](/www-project-agentic-skills-top-10/videos?video=ast01)
- [The Problem: A Crisis Already in Progress](#the-problem-a-crisis-already-in-progress)
- [What Are Agentic Skills?](#what-are-agentic-skills)
- [Incident Timeline (2026)](#incident-timeline-2026)
- [Summary Table](#summary-table)
- [Universal Skill Format Proposal](#universal-skill-format-proposal)
- [Case Studies](/www-project-agentic-skills-top-10/case-studies.html)
- [Threat Intelligence](/www-project-agentic-skills-top-10/threat-intelligence.html)
- [Interactive Risk Assessment Tool](/www-project-agentic-skills-top-10/risk-assessment.html)
- [Skill Scanner Integration](/www-project-agentic-skills-top-10/skill-scanner-integration.html)
- [API Documentation](/www-project-agentic-skills-top-10/api-documentation.html)
- [Skill Development Guide](/www-project-agentic-skills-top-10/skill-development-guide.html)
- [Platform Comparison](/www-project-agentic-skills-top-10/platform-comparison.html)
- [Community & Contribution](/www-project-agentic-skills-top-10/community-contribution.html)
- [Training & Certification](/www-project-agentic-skills-top-10/training-certification.html)
- [Incident Response Playbook](/www-project-agentic-skills-top-10/incident-response.html)
- [Security Metrics & Monitoring](/www-project-agentic-skills-top-10/metrics-monitoring.html)
- [Getting Started](#getting-started)
- [Target Audience](#target-audience)
- [Project Status and Timeline](#project-status-and-timeline)
- [Leadership and Governance](#leadership-and-governance)
- [Key Research and References](#key-research-and-references)
- [License](#license)

## Overview

The **OWASP Agentic Skills Top 10 (AST10)** documents the 10 most critical security risks in agentic AI skills across all major AI agent platforms. Skills represent the execution layer that gives agents real-world impact: they define not just what resources agents can access, but *how* they orchestrate multi-step workflows autonomously.

While significant attention has been devoted to securing large language models (LLMs) and the Model Context Protocol (MCP) tool layer, the intermediate **behavior layer**—embodied in agentic skills—has emerged as a particularly vulnerable and under-protected component of the AI agent ecosystem. This project exists to close that gap.

**Mental Model**: *MCP = how the model talks to tools; AST10 = what those tools actually do.*

## Quick Security Checklist

Use this checklist to assess your agent skill security posture:

### Registry & Installation

- Only install skills from verified publishers with code signing
- Enable automated scanning for all skill installations
- Review skill permissions before installation
- Pin skill versions to prevent automatic malicious updates

### Runtime Security

- Run agents in isolated environments (containers/sandbox)
- Implement network restrictions for agent processes
- Monitor agent file system and network activity
- Regularly audit installed skills and their dependencies

### Governance & Monitoring

- Maintain inventory of all deployed agent skills
- Implement approval workflows for skill installations
- Enable comprehensive audit logging for agent actions
- Establish incident response procedures for skill compromises

### Development Practices

- Sign all published skills with cryptographic keys
- Include comprehensive permission manifests
- Test skills in isolated environments before publishing
- Document security considerations in skill metadata

*See the complete Security Assessment Checklist for detailed guidance.*

## The Problem: A Crisis Already in Progress

This is not a theoretical future risk. The AI agent skill ecosystem is under active attack as of Q1 2026.

**By the numbers:**

MetricFigureSourceSkills scanned3,984Snyk ToxicSkills (Feb 2026)Skills with security flaws1,467 (36.82%)Snyk ToxicSkills (Feb 2026)Skills with critical issues534 (13.4%)Snyk ToxicSkills (Feb 2026)Confirmed malicious payloads76+Snyk ToxicSkills (Feb 2026)ClawHavoc campaign: malicious skills1,184Antiy CERT (Feb 2026)OpenClaw instances internet-exposed135,000+SecurityScorecard (Feb 2026)CVEs disclosed (OpenClaw alone)9 (3 with public exploits)Endor Labs (Feb 2026)Skills analyzed across all registries30,000+National CIO Review / Cisco (2026)Skills containing at least one vulnerability>25%National CIO Review (2026)

The ClawHub registry—the primary marketplace for OpenClaw skills—became the **first AI agent registry to be systematically poisoned at scale**. Five of the top seven most-downloaded skills at peak infection were confirmed malware. The registry has since implemented automated scanning and partnered with VirusTotal, but the broader ecosystem remains largely unprotected.

Check Point Research disclosed two critical vulnerabilities in Claude Code (CVE-2025-59536, CVSS 8.7; CVE-2026-21852, CVSS 5.3) demonstrating that **repository-level configuration files now function as part of the execution layer**—simply cloning and opening an untrusted project can trigger remote code execution and API key exfiltration before any user consent dialog appears.

No comprehensive security framework or dedicated guidance for agent skills existed before this project. That gap is what AST10 addresses.

## What Are Agentic Skills?

Agentic AI skills are reusable, named behaviors that encode complete workflows, including:

- Task understanding and goal decomposition
- Multi-step planning and tool orchestration
- File system, network, and shell access
- Safety guardrails and output formatting
- Persistent memory and cross-session state

Unlike MCP tools (which define *what* resources and actions are available), skills define *how* to use those tools in sequence to accomplish user goals. This behavioral abstraction layer creates unique security challenges that cannot be addressed by securing either the model or the protocol layer alone.

**The “Lethal Trifecta” (Simon Willison / Palo Alto Networks, 2026):**
An AI agent skill is especially dangerous when it simultaneously has:

- **Access to private data**(SSH keys, API credentials, wallet files, browser data)
- **Exposure to untrusted content**(skill instructions, memory files, email)
- **Ability to communicate externally**(network egress, webhook calls, curl)

Most production agent deployments today satisfy all three conditions.

### Skill Formats by Platform

PlatformSkill FormatPrimary Risk FileOpenClaw
```
SKILL.md
```

(YAML frontmatter + Markdown)
```
SKILL.md
```

,
```
SOUL.md
```

,
```
MEMORY.md
```

Claude Code
```
skill.json
```

/
```
YAML
```

+
```
scripts/
```
```
.claude/settings.json
```

, hooks configCursor / Codex
```
manifest.json
```

+ handler scripts
```
manifest.json
```

, tool configsVS Code
```
package.json
```

+ extensions
```
package.json
```

,
```
extension.ts
```

## Incident Timeline (2026)

The following is a condensed timeline of confirmed real-world incidents involving AI agent skill security, drawn from publicly disclosed research and CVE records.

### January 2026

- **Jan 27–29**:**ClawHavoc campaign**launches. Attackers register as ClawHub developers and flood the registry with 341 malicious skills in a 3-day window. All 335 AMOS-delivering skills share a single C2 IP (
  ```
  91.92.242[.]30
  ```

  ). Target data includes exchange API keys, wallet private keys, SSH credentials, browser passwords, and
  ```
  .env
  ```

  files. Skills also write malicious instructions directly into
  ```
  MEMORY.md
  ```

  and
  ```
  SOUL.md
  ```

  for session-persistent backdooring.
- **Jan 31**: ClawHavoc surge peaks. Koi Security names the campaign and begins coordinated removal effort. Some packages persist for weeks.

### February 2026

- **Feb 1**: Koi Security publishes first public ClawHavoc analysis.
- **Feb 3**: Snyk publishes “From SKILL.md to Shell Access in Three Lines of Markdown” threat model, documenting how three lines of markdown in a
  ```
  SKILL.md
  ```

  file can instruct an agent to read SSH keys and exfiltrate them.
- **Feb 4**: Alice publishes findings on several published OpenClaw skills found to be actively malicious while in use by over 6,000 users — detected via behavioral analysis.
- **Feb 5**: Snyk publishes**ToxicSkills**— the first comprehensive security audit of the AI agent skill ecosystem. Key findings: 36% of skills contain security flaws; 13.4% contain critical-level issues; 76 confirmed active malicious payloads; 8 malicious skills still live at time of publication.
- **Feb 5**: Snyk publishes “280+ Leaky Skills: How OpenClaw & ClawHub Are Exposing API Keys and PII” — a parallel finding showing credential exposure at scale through over-permissioned skills.
- **Feb 10**: Snyk documents “How a Malicious Google Skill on ClawHub Tricks Users Into Installing Malware” — typosquatting and fake brand impersonation confirmed as active tactics.
- **Feb 11**: Snyk publishes “Why Your Skill Scanner Is Just False Security (and Maybe Malware)” — demonstrating that pattern-matching scanners miss the majority of critical threats, which rely on natural-language instruction manipulation rather than code signatures.
- **Feb 14**: OpenClaw patches**log poisoning vulnerability**(version 2026.2.13). Attackers could write malicious content to agent log files via WebSocket requests; since the agent reads its own logs for troubleshooting, injected text could influence decisions and trigger indirect prompt injection.
- **Feb 25**: Check Point Research publicly discloses**CVE-2025-59536**(CVSS 8.7) and**CVE-2026-21852**(CVSS 5.3) in Claude Code. Both were patched months earlier but the disclosure confirms: repository-controlled configuration files can silently execute arbitrary shell commands and exfiltrate API keys at project open time, before any trust dialog.
- **Feb 26**:**ClawJacked**disclosed by Oasis Security (CVE-2026-28363, CVSS 9.9). Malicious websites can brute-force localhost WebSocket connections with no rate limiting to silently hijack local OpenClaw instances, register new devices without user prompts, and exfiltrate data through existing agent integrations. OpenClaw patches within 24 hours (version 2026.2.25).
- **Feb 2026**: Antiy CERT publishes**ClawHavoc Campaign Analysis**, classifying malware as
  ```
  Trojan/OpenClaw.PolySkill
  ```

  . Final tally: 1,184 malicious skills across 12 publisher accounts. Hudson Rock separately identifies Vidar infostealer variants specifically targeting OpenClaw agent identity files (
  ```
  openclaw.json
  ```

  ,
  ```
  device.json
  ```

  ,
  ```
  soul.md
  ```

  ,
  ```
  memory.md
  ```

  ).
- **Feb 2026**: Microsoft Defender Security Research Team issues advisory:*“Because of these characteristics, OpenClaw should be treated as untrusted code execution with persistent credentials. It is not appropriate to run on a standard personal or enterprise workstation.”*
- **Feb 2026**: BlueRock Security analyzes 7,000+ MCP servers; finds 36.7% potentially vulnerable to SSRF. Proof-of-concept against Microsoft’s MarkItDown MCP server retrieves AWS IAM keys from EC2 metadata endpoint.

### March 2026

- **Mar 2026**: SecurityScorecard confirms 135,000+ OpenClaw instances publicly internet-exposed with insecure defaults; 53,000+ correlated with prior breach activity. Bitdefender telemetry confirms employees deploying OpenClaw on corporate devices with no SOC visibility.
- **Mar 2026**: Snyk and Tessl announce registry-level skill security scanning partnership. Snyk and Vercel previously partnered to scan skills on
  ```
  skills.sh
  ```

  at install time.
- **NIST / CAISI**: Federal Register RFI on AI Agent Security (published Jan 8, 2026, comments closed Mar 9, 2026) — the first formal US government solicitation specifically addressing AI agent security risks.

### June 2026

- **Jun 3**: Trail of Bits publishes “The Sorry State of Skill Distribution” — every public skill scanner tested (ClawHub’s VirusTotal + LLM guard model, Cisco’s
  ```
  skill-scanner
  ```

  , the skills.sh scanners) is bypassed in under an hour, via payload padding that forces truncation, logic hidden in binary and archive formats, and prompt-injecting the scanner’s own LLM judge.
- **Jun 22–24**: Air Security publishes “The Story of Skills” and “The Circus of Skills” — a researcher-built malicious skill reaches over 26,000 agents while every scanner clears it, its payload served from an attacker-controlled external documentation URL; a follow-up scan of 142,836 live skills finds 17,822 (12.4%, 6.7M installs) resting on at least one untrusted external instruction source.

### July 2026

- **Jul 2**: Air Security publishes “SkillJacking” — 925 skills serving ~134K agents sit on instantly hijackable dependencies (deleted GitHub accounts, unregistered packages, expired domains, freed cloud-app slots); researchers take over the most popular video-generation skill on skills.sh (11,483 installs) by re-registering its deleted owner account.

## Summary Table

Each of the 10 risks is documented in a separate file. Click on the risk name to view the full details.

> 📊
>
> *Prefer a visual map?*See the*— a skill-lifecycle diagram plus a colour-coded card for every risk.*[Top 10 Visual Overview](/www-project-agentic-skills-top-10/top10)

# RiskSeverityKey MitigationReal-World Evidence[AST01](/www-project-agentic-skills-top-10/ast01.html)Malicious SkillsCriticalMerkle root signing, registry scanningClawHavoc (1,184 skills), ToxicSkills (76 payloads)[AST02](/www-project-agentic-skills-top-10/ast02.html)Supply Chain CompromiseCriticalRegistry transparency, provenance trackingClawHub collapse, Claude Code CVE-2025-59536[AST03](/www-project-agentic-skills-top-10/ast03.html)Over-Privileged SkillsHighLeast-privilege manifests, schema validation280+ credential-leaking skills (Snyk, Feb 2026)[AST04](/www-project-agentic-skills-top-10/ast04.html)Insecure MetadataHighStatic analysis, safe parsers, sandboxed loadingFake “Google” skill impersonation; YAML payload delivery in SKILL.md[AST05](/www-project-agentic-skills-top-10/ast05.html)Untrusted External InstructionsHighSource inventory, content pinning, continuous rescanningAir PoC bypassed all scanners; 26,000 agents at risk[AST06](/www-project-agentic-skills-top-10/ast06.html)Weak IsolationHighContainerization, Docker sandboxingOpenClaw host-mode execution, 135K exposed instances[AST07](/www-project-agentic-skills-top-10/ast07.html)Update DriftMediumImmutable pinning, hash verificationClawJacked (CVE-2026-28363), patch-lag exploitation[AST08](/www-project-agentic-skills-top-10/ast08.html)Poor ScanningMediumSemantic + behavioral multi-tool pipelinePattern-matcher bypass via natural-language injection[AST09](/www-project-agentic-skills-top-10/ast09.html)No GovernanceMediumSkill inventories, agentic identity controls53K exposed instances with no SOC visibility[AST10](/www-project-agentic-skills-top-10/ast10.html)Cross-Platform ReuseMediumUniversal YAML formatMalicious skills ported across ClawHub, skills.sh

## MAESTRO Mapping

The Cloud Security Alliance (CSA) MAESTRO framework provides a structured threat modeling approach for agentic AI systems across 7 interconnected layers. This mapping aligns each AST10 risk with relevant MAESTRO layers to enable targeted threat localization and cross-layer risk analysis.
```
```
graph TD
    A[Layer 7: Agent Ecosystem] --> B[Layer 6: Security & Compliance]
    B --> C[Layer 5: Evaluation & Observability]
    C --> D[Layer 4: Deployment & Infrastructure]
    D --> E[Layer 3: Agent Frameworks]
    E --> F[Layer 2: Data Operations]
    F --> G[Layer 1: Foundation Models]

    style A fill:#ffcccc
    style B fill:#ffcccc
    style C fill:#ffffcc
    style D fill:#ccffcc
    style E fill:#ccccff
    style F fill:#ffccff
    style G fill:#ccffff```
```

ASTRiskMAESTRO LayersAST01Malicious Skills7, 3, 6, 4, 5AST02Supply Chain Compromise7, 3, 6, 4AST03Over-Privileged Skills6, 4, 3, 7AST04Insecure Metadata7, 3, 4, 6AST05Untrusted External Instructions3, 2, 7, 6AST06Weak Isolation4, 6, 3AST07Update Drift4, 6, 7AST08Poor Scanning5, 6, 3AST09No Governance6, 7, 5AST10Cross-Platform Reuse7, 3, 6

*The MAESTRO layer mapping helps teams align AST10 risks with CSA’s 7-layer threat model for agentic AI.*

*For detailed descriptions, attack scenarios, preventive mitigations, and OWASP mappings, see each individual risk file.*

## Contribute

We welcome contributions from the community! Here’s how you can help:

### Ways to Contribute

- **Report New Risks**: Found a security issue in agent skills? Submit it as a GitHub issue with evidence and impact analysis.
- **Improve Mitigations**: Have better prevention strategies or real-world examples? Update the relevant AST file.
- **Add Examples**: Share anonymized attack scenarios or mitigation case studies.
- **Translate**: Help localize this guide for non-English speakers.
- **Code**: Contribute to scanning tools, format validators, or automation scripts.
- **Research**: Analyze skills in your environment and share findings (anonymized).

### Getting Started

- Fork the repository on GitHub.
- Create a feature branch for your changes.
- Make your edits following our [contributing guidelines](/www-project-agentic-skills-top-10/CONTRIBUTING.md).
- Submit a pull request with a clear description of your changes.

### Submit New Risk Entries

Use our **interactive web form** to submit new AST risk entries:

**🔀 AST10 metadata loss simulator** — Compare two skill manifests to see which security metadata is lost or weakened after a cross-platform port.

The form generates properly formatted markdown and provides multiple submission options:

- Direct GitHub file creation
- Create GitHub Issue
- Download and manual PR

### Community Guidelines

- Be respectful and constructive in discussions.
- Provide evidence for security claims.
- Respect contributor privacy when sharing examples.
- Follow OWASP’s Code of Conduct.

*See CONTRIBUTING.md for detailed guidelines.*

## Universal Skill Format Proposal

The following YAML format is proposed as a cross-platform standard that mitigates AST10 and provides the metadata foundation required to address AST01 through AST09. It is designed to be a superset of all current platform-specific formats.
```
```
---
# Universal Agentic Skill Format v1.0
# Compatible with: OpenClaw, Claude Code, Cursor/Codex, VS Code

name: example-skill
version: 1.0.0
platforms: [openclaw, claude, cursor, vscode]

description: "Safe example skill — concise, honest statement of function"
author:
  name: "Author Name"
  identity: "did:web:example.com"         # Decentralized identity anchor
  signing_key: "ed25519:pubkey_hex_here"

permissions:
  files:
    read:
      - ~/.config/app.json                 # Explicit paths only; no wildcards
    write:
      - ~/.config/app.json
    deny_write:
      - SOUL.md
      - MEMORY.md
      - AGENTS.md                          # Identity files require explicit grant
  network:
    allow:
      - api.example.com                    # Domain allowlist, not binary on/off
    deny: "*"                              # Default deny all other egress
  shell: false                             # Explicit shell access declaration
  tools:
    - web_fetch
    - read_file

requires:
  binaries: [jq, curl]
  min_runtime_version: "2026.1.0"

risk_tier: L1                              # L0=safe, L1=low, L2=elevated, L3=destructive
scan_status:
  scanner: "[email protected]"
  last_scanned: "2026-02-15"
  result: "pass"

signature: "ed25519:ABCDEF1234567890..."   # Signs the canonical hash of this manifest
content_hash: "sha256:abcdef1234..."       # Hash of the complete skill package

changelog:
  - version: "1.0.0"
    date: "2026-02-01"
    notes: "Initial release"
---```
```

**Format design rationale:**

- ```
  permissions.deny_write  ```

  protects identity files (

  ```
  SOUL.md  ```

  ,

  ```
  MEMORY.md  ```

  ) by default — must be explicitly overridden.
- ```
  network.allow
  ```

  is a domain allowlist, not a boolean — closing the “network: true” over-permission gap (AST03).
- ```
  signature  ```

  and

  ```
  content_hash  ```

  together enable Merkle-root registry verification (AST01/AST02).
- ```
  scan_status
  ```

  creates a machine-readable provenance trail (AST08/AST09).
- ```
  risk_tier  ```

  enables automated governance policies without per-skill review (AST09/AST10).

## Getting Started

### For Security Teams

- Review this document and the [complete Top 10 detail pages](/www-project-agentic-skills-top-10/top10)for full risk descriptions, attack scenarios, and OWASP mappings.
- Conduct a skill inventory across all agent platforms in use — treat this as an immediate priority given active exploitation confirmed in 2026.
- Use the [Security Assessment Checklist](/www-project-agentic-skills-top-10/checklist.html)for reviewing installed skills.
- Implement the governance framework described in AST09: inventory, approval workflow, audit logging, and agentic identity controls.
- Subscribe to ClawHub, skills.sh, and platform-specific security advisories.

### For Skill Developers

- **Least privilege**: Declare a minimal permission manifest; request only what your skill genuinely needs (AST03).
- **Safe parsing**: Use safe YAML/JSON loaders; never deserialize untrusted skill configs without sandboxing (AST04).
- **Sign your skills**: Implement ed25519 signing before publication; include

  ```
  content_hash  ```

  in your manifest (AST01/AST02).
- **Pin dependencies**: Lock all nested dependencies to immutable hashes — never version ranges (AST07).
- **Honest metadata**: Accurately declare

  ```
  risk_tier  ```

  , permissions, and

  ```
  requires  ```

  ; do not understate scope (AST04).
- **Protect identity files**: Never request write access to

  ```
  SOUL.md  ```

  ,

  ```
  MEMORY.md  ```

  , or

  ```
  AGENTS.md  ```

  unless your skill’s core function requires it — and document why (AST03).

### For Platform Developers

- **Default sandbox**: Make container/Docker isolation the default for skill execution; make host-mode an explicit opt-in (AST06).
- **Safe deserialization**: Disable dangerous YAML/JSON tags in all skill loaders by default; validate against a schema before execution (AST04).
- **Registry scanning**: Implement behavioral scanning at publish time and at install time; pattern matching alone is insufficient (AST08).
- **Provenance infrastructure**: Support the Universal Skill Format; implement Merkle-root transparency logs for your registry (AST01/AST02/AST10).
- **Audit logging**: Emit structured logs for all skill actions (file access, shell commands, network calls, memory writes) (AST09).
- **Trust prompts**: Do not allow repository-controlled configuration to execute before explicit user trust confirmation (AST02).

## Target Audience

RolePrimary ConcernsKey AST Risks*AI Platform Developers*Secure skill runtimes, registries, installers, and CI/CD integrationAST01, AST02, AST04, AST05, AST06, AST08*AppSec / Product Security*Govern skills in enterprise deployments; review skill PRsAST03, AST04, AST05, AST07, AST09*Skill Authors*Write safe manifests, scripts, and metadata; ship signable packagesAST03, AST04, AST05, AST07*GRC / Compliance*Map skill risks to NIST AI RMF, ISO 42001, EU AI ActAST05, AST09, AST10*CISOs / Security Leadership*Understand blast radius, incident scope, and governance gapsAST02, AST05, AST06, AST09*Developers / Engineers*Safely install and use skills without introducing unreviewed riskAST01, AST02, AST07

## Project Status and Timeline

**Status**: New Project Proposal — *active development***Version**: 1.0 (2026 Edition)
**License**: Creative Commons Attribution ShareAlike 4.0 (CC-BY-SA-4.0)

### Timeline

QuarterPhaseDeliverables*Q2 2026*FoundationGitHub repo launch, OWASP project page, AST01–AST06 full write-ups, incident database*Q3 2026*CompletionAST07–AST10 write-ups, Universal Skill Format v1.0 specification, cheat sheets, v1.0 RC*Q4 2026*Launchv1.0 release, OWASP flagship project submission, RSA 2026 / OWASP Global AppSec presentations

## Leadership and Governance

### Project Lead

### Co-Leads

### Contribution Model

ChannelPurpose*GitHub Issues*Risk suggestions, new attack scenarios, mitigation proposals*GitHub PRs*Content contributions, platform-specific examples, translations

### Goals and Success Metrics

GoalMetricTarget*v1.0 Release*Complete 10 risks + full OWASP/NIST mappingsQ3 2026*OWASP Flagship*Project review and approvalQ4 2026*Conference Adoption*Presentations accepted3+ (RSA, OWASP Global AppSec)*Industry Adoption*Registries implementing Universal Skill Format2+ major registries

## Key Research and References

### Primary Research (2026)

- **Snyk ToxicSkills**(Feb 5, 2026) — First comprehensive security audit of AI agent skill ecosystem; 3,984 skills scanned across ClawHub and skills.sh.
- **Snyk: From SKILL.md to Shell Access**(Feb 3, 2026) — Threat model for agent skills; lethal trifecta framework.
- **Check Point Research: Caught in the Hook**(Feb 25, 2026) — CVE-2025-59536 (CVSS 8.7) and CVE-2026-21852 (CVSS 5.3) in Claude Code.
- **Antiy CERT: ClawHavoc Campaign Analysis**(Feb 2026) — 1,184 malicious skills;

  ```
  Trojan/OpenClaw.PolySkill  ```

  classification.
- **Oasis Security: ClawJacked**(Feb 26, 2026) — CVE-2026-28363 (CVSS 9.9); WebSocket brute-force against local OpenClaw instances.
- **SecurityScorecard**(Feb 2026) — 135,000+ OpenClaw instances publicly exposed; 53,000+ correlated with prior breach activity.
- **Snyk: 280+ Leaky Skills**(Feb 5, 2026) — API key and PII exposure across ClawHub.
- **Snyk: Why Your Skill Scanner Is Just False Security**(Feb 11, 2026) — Pattern-matching scanner limitations.
- **Air Security: The Story of Skills**(Jun 22, 2026) — Researcher-built malicious skill reached 26,000+ agents via a trusted marketplace and social media; every scanner cleared it.
- **Air Security: The Circus of Skills**(Jun 24, 2026) — 142,836 skills scanned for untrusted external instruction sources; 17,822 (12.4%, 6.7M installs) affected.
- **Air Security: SkillJacking**(Jul 2, 2026) — 925 skills resting on instantly hijackable dependencies (~134K agents); top skills.sh video-generation skill taken over via a deleted GitHub account.

### Industry Reports

- **Cisco State of AI Security 2026**— Comprehensive AI threat landscape; agentic AI proliferation and governance gap.
- **Microsoft Defender Security Research Team**(Feb 2026) — OpenClaw enterprise security advisory.
- **BlueRock Security**(2026) — 7,000+ MCP server analysis; 36.7% SSRF-vulnerable.
- **Bitdefender**(Feb 2026) — Enterprise telemetry on shadow AI / OpenClaw deployment.
- **Hudson Rock**(Feb 2026) — Vidar infostealer variants targeting OpenClaw identity files.
- **IBM X-Force 2025 Threat Intelligence Index**— AI supply chain risk baseline.

### Standards and Frameworks

- **OWASP AIVSS Project**(2025)
- **OWASP LLM Top 10**(2025)
- **OWASP Agentic AI Top 10**(Dec 2025)
- **NIST AI RMF**
- **ISO/IEC 42001**(AI Management System)
- **EU AI Act**(enforced Aug 2026)
- **NIST / CAISI Federal Register RFI on AI Agent Security**(Jan 8, 2026)

### Academic and Technical

- **“Prompt Injection Attacks on Agentic Coding Assistants”**(arXiv:2601.17548)
- **“Do Not Mention This to the User”: Detecting and Understanding Malicious Agent Skills in the Wild**(arXiv:2602.06547, USENIX Security 2026)
- **snyk-labs/toxicskills-goof**— Real malicious skill samples for scanner testing.
- **openclaw/openclaw Issue #10827**— Skill supply-chain security: provenance tracking and permission manifests proposal.

## Resources

- **GitHub**:[github.com/OWASP/www-project-agentic-skills-top-10](https://github.com/OWASP/www-project-agentic-skills-top-10)
- **OWASP Project Page**:[owasp.org/www-project-agentic-skills-top-10](https://owasp.org/www-project-agentic-skills-top-10/)
- **Full Risk Documentation**:[Visual Top 10 Overview](/www-project-agentic-skills-top-10/top10)
- **Project Proposal**:[proposal.md](/www-project-agentic-skills-top-10/proposal.html)
- **Security Assessment Checklist**:[checklist.md](/www-project-agentic-skills-top-10/checklist.html)
- **Universal Skill Format Specification**:[universal-skill-format.md](/www-project-agentic-skills-top-10/universal-skill-format.html)

## License

This work is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-sa/4.0/).

You are free to share and adapt this material for any purpose, provided you give appropriate credit, provide a link to the license, indicate if changes were made, and distribute your contributions under the same license.

## Contact

For questions, suggestions, or to get involved:

- Open an issue on GitHub

*Last updated: March 2026. This document reflects confirmed incidents, published CVEs, and research available as of that date. The threat landscape is evolving rapidly — contributions and corrections are welcome.*

## Example

Put whatever you like here: news, screenshots, features, supporters, or remove this file and don’t use tabs at all.

# Leadership & Founding Members

## Project Leadership

### Current Leaders

### Ken Huang

### Hammad Atta

### Fabio Cerullo

### Aonan Guan

### Bhavya Gupta

### Niv Hoffman

### Iftach Orr

### Akram Sheriff

## AIVSS Distinguished Review Board

The OWASP AIVSS project’s Distinguished Review Board comprises world-renowned cybersecurity leaders, former government officials, and industry pioneers who provide strategic guidance and expert oversight for the AI Vulnerability Scoring System framework. We thank them for their guidance, several of whom have also supported this project’s work.

#### Rob Joyce

*Advisor to PwC and OpenAI, Former Special Assistant to the President and Cybersecurity Coordinator*

#### Jason Clinton

*Deputy CISO, Anthropic*

#### Amy R. Steagall

*Chief Information Security Officer, Stanford University*

#### Martin Stanley

*AI Risk Management Framework Lead, NIST*

#### Apostol Vassilev

*Research Supervisor, NIST*

#### Andrew Coyne

*CISO, Banner Health, Former CISO, Mayo Clinic*

#### Kevin Rocque

*Managing Director/Executive Vice President, Global Technology Risk Officer, TD Bank*

#### Jeff Williams

*Former Global OWASP Chair, Founder and CTO, Contrast Security*

#### Michael Tran Duff

*University Chief Information Security and Data Privacy Officer, Harvard University*

#### Emil Bender Lassen

*Standards Lead, AIUC-1*

## Agentic Skills Top 10 Founding Members

Founding members of the OWASP Agentic Skills Top 10 project itself — project leads, co-leads, and additional contributors — listed alphabetically. Several also contribute to the sibling OWASP AIVSS project listed above.

#### Ken Huang

*Project Lead, Agentic Skills Top 10*

#### Hammad Atta

*Co-Lead, Agentic Skills Top 10*

#### Manish Bhatt

*Security Researcher, AWS*

#### Fabio Cerullo

*Co-Lead, Agentic Skills Top 10*

#### David Girard

*Senior Director, AI Security & AI Alliances, Trend Micro*

#### Aonan Guan

*Co-Lead, Agentic Skills Top 10*

#### Bhavya Gupta

*Co-Lead, Agentic Skills Top 10*

#### Pamela Gupta

*Founder & CEO, OutSecure / Trusted AI*

#### Idan Habler

*Staff AI/ML Security Researcher, Intuit*

#### Niv Hoffman

*CTO, Air Security*

#### Charles Iheagwara

*AI/ML Security Leader, AstraZeneca*

#### Sushmitha Janapareddy

*Director - Security Integrations, American Express*

#### Edward Lee

*Vice President, Lead AI Security, JP Morgan*

#### KJ Lian

*Senior Manager, Data & AI (Public Sector), AWS*

#### Vineeth Sai Narajala

*Application Security, AWS*

#### Iftach Orr

*Co-Lead, Agentic Skills Top 10*

#### Kanna Sekar

*Cyber Security, Google*

#### Akram Sheriff

*Co-Lead, Agentic Skills Top 10*

#### Dennis Xu

*Research VP, AI, Gartner*

## OWASP AIVSS Founding Members

The [OWASP AIVSS (Agentic AI Vulnerability Scoring System)](https://owasp.org/www-project-agentic-ai-vulnerability-scoring-system/) project is a sibling OWASP initiative focused on scoring the severity of agentic AI vulnerabilities. Its founding members are recognized here as OWASP founding members in the agentic AI security space; many of them have also contributed directly to the Agentic Skills Top 10 project’s research and review process.

#### Sunil Agrawal

*Chief Information Security Officer, Glean*

#### David Ames

*Partner, PwC*

#### Michael Bargury

*Founder and CTO, Zenity*

#### Joshua Beck

*Application Security Architect, SAS*

#### Manish Bhatt

*Security Researcher, Amazon Kuiper Security*

#### Mark Breitenbach

*Security Engineer, Dropbox*

#### Anat Bremler-Barr

*Professor of Computer Science, Tel Aviv University*

#### Siah Burke

*HIPAA Security Officer, Siah.ai*

#### David Campbell

*AI Security, Scale AI*

#### Ying-Jung Chen

*AI safety researcher, PhD, Georgia Institute of Technology*

#### Anton Chuvakin

*Security Solution Strategy, Google*

#### Jason Clinton

*CISO, Anthorphic*

#### Adam Dawson

*Staff AI Security Researcher, Dreadnode*

#### Leon Derczynski

*Principal Research Scientist, NVIDIA*

#### Walker Lee Dimon

*AI Security Researcher, MITRE*

#### Marissa Dotter

*AI Security Researcher, MITRE*

#### Dan Goldberg

*ISO Market Lead, Omnicom*

#### David Haber

*CEO, Lakera*

#### Idan Habler

*Staff AI/ML Security Researcher, Intuit*

#### Jason Haddix

*Founder, Arcanum Information Security*

#### Keith Hoodlet

*Director of AI/ML & AppSec, Trail of Bits*

#### Ken Huang

*AIVSS Project Lead, OWASP*

#### Chris Hughes

*CEO, Aquia*

#### Charles Iheagwara

*AI/ML Security Leader, AstraZeneca*

#### Krystal Jackson

*Researcher, Center for Long-Term Cybersecurity, UC Berkeley*

#### Sushmitha Janapareddy

*Director - Security Integrations, American Express*

#### Rob Joyce

*Former Cybersecurity Director of NSA, Advisor to PwC, PwC*

#### Diana Kelley

*CISO, Noma Security*

#### Prashant Kulkarni

*Lead AI Security Research Engineer, Google Cloud*

#### Mahesh Lambe

*Founder, MIT, Unify Dynamics*

#### Edward Lee

*Vice President, Lead AI Security, JP Morgan*

#### Nate Lee

*CEO, Cloudsec.ai*

#### Vishwas Manral

*CEO, Precize.ai*

#### Daniela Muhaj

*Executive-in-Residence for Research & Development, AI 2030*

#### Vineeth Sai Narajala

*Application Security, AWS*

#### Om Narayan

*AI Security Researcher, AWS*

#### Varun Pant

*Engineering and Product Leader, AI applications at the Automated Reasoning Group, AWS*

#### Advait Patel

*Senior Site Reliability Engineer (DevSecOps + Cloud + AIOps), Broadcom, IEEE*

#### Alex Polyakov

*CEO, adversa.ai*

#### Ramesh Raskar

*Professor & Director, MIT Media Lab*

#### Ron F. Del Rosario

*VP-Head of AI Security, SAP*

#### Tal Shapira

*Co-Founder & CTO, Reco AI*

#### Akram Sheriff

*Senior AI/ML Software Engineering Leader, Cisco*

#### Samantha Siau

*Security and Compliance, Anthropic*

#### Kevin Simmonds

*Partner on AI Offensive Security, PWC*

#### Martin Stanley

*NIST AI RMF Lead, Independent*

#### Omar A. Turner

*General Manager of Security, Microsoft*

#### Apostol Vassilev

*AI Research Team Supervisor, NIST*

#### Matthew Versaggi

*AI Fellow, White House Presidential Innovation Fellow*

#### David Webb

*Agency Cybersecurity Officer, Cybersecurity and Infrastructure Security Agency*

#### Dennis Xu

*Research VP, AI, Gartner*

#### Xiaochen Zhang

*Executive Director and Chief Responsible AI Officer, AI 2030*

### Recognition

We extend our gratitude to all founding members who have contributed to establishing this crucial framework for AI security assessment. Their vision and dedication have been instrumental in shaping the Agentic Skills Top 10 project.

## Get Involved

Interested in contributing to the Agentic Skills Top 10 project? We welcome new contributors and leaders. Please see our [Contribution Guidelines](CONTRIBUTING.md) for more information on how to get involved.
