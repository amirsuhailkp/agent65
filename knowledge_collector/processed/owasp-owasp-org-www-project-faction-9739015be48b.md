---
title: OWASP Faction
source: owasp.org
url: https://owasp.org/www-project-faction/
collector: owasp
category: web-security
tags:
- web-security
- faction
- vulnerability
- assessment
- get
date_collected: '2026-07-26T12:44:13.447114Z'
language: unknown
---

# OWASP Faction

# OWASP FACTION PenTesting Report Generation and Collaboration Framework

## Current Road Map

- Open sourced the base application on GitHub in December 2023
- Adding API and plugin features - March 2024
- Streamlined remediation workflows - August 2024
- Update backend and code refactor - October 2025
- Adding 4 more plugins and integrations - December 2025
- Adding MCP Server - May 2026
- Faction 2.0 - Summer 2026
  - Complete overhaul of the UI
  - Improved editing workflow
  - Much needed improvement to vulnerability management
  - App Owner Dashboards and Vulnerability Tracking

## Introduction

FACTION is your entire assessment workflow in a box. With FACTION you can:

- Automate pentesting and security assessment reports
- Peer review and track changes for reports
- Create customized DOCX templates for different assessment types and retests
- Real-time collaboration with assessors via the web app and [Burp Suite Extensions](https://github.com/factionsecurity/Faction-Burp)
- Customizable vulnerability templates with over 75 prepopulated
- Easily manage assessment teams and track progress across your organization
- Track vulnerability remediation efforts with custom SLA warnings and alerts
- Full REST API to integrate with other tools

Other Features:

- LDAP Integration
- OAUTH2.0 Integration
- SMTP integration
- Extendable with Custom Plugins similar to Burp Extender
- Custom Report Variables
- MCP Server

**Want to see it in action?** -> [Faction YouTube Channel](https://www.youtube.com/@factionsecurity/videos)

## Quick Setup

**Requirements**

- Java JDK 11
- Maven (for building the project)
- (Optional for VM). MongoDB requires a CPU with AVX support. You may run into this issue if using [Oracle Virtual](https://www.mongodb.com/community/forums/t/could-not-start-mongodb-5-0-running-oracle-linux-on-virtualbox/120524/10)Box or[Kubernetes](https://stackoverflow.com/questions/70818543/mongo-db-deployment-not-working-in-kubernetes-because-processor-doesnt-have-avx)

Run the following commands to build the WAR file and deploy it to the Docker container.
```
```
git clone [email protected]:factionsecurity/faction.git
cd faction
docker-compose up --build```
```

Once the containers are up, you can navigate to http://127.0.0.1:8080 to access your FACTION instance. On the first boot, it will ask you to create an admin account.

## Import the Vulnerability Templates

- Navigate to Templates -> Default Vulnerabilities
- Click *Update from Faction*.

## Customize Reports

You can find out more information about creating your own custom report templates here:
[Custom Security Report Templates - Faction Security](https://docs.factionsecurity.com/Custom%20Security%20Report%20Templates/)

## Burp Suite Extension

Faction is in the Burp BApp Store, but you can also get it from our GitHub:
[Burp Suite Extensions](https://github.com/factionsecurity/Faction-Burp)

## Manuals and Tutorials

## Screenshots

**Vulnerability Templates**

**Assessment Scheduling**

**Peer Review and Track Changes**

**Remediation/Retest Queue**

**Schedule Retests**

**Assessor Retest Interface**

**Vulnerability Status Tracking**

## Faction App Store

Faction 1.2 introduces the App Store! The Faction App Store makes it easier for developers to extend Faction. Faction Extensions can be used to trigger custom code when certain events happen in your workflow, like sending all vulnerabilities to Jira when an assessment is complete, or updating a tracking system when retests pass or fail. More information can be found on the [documentation site](https://docs.factionsecurity.com).

### ⭐️ Jira Integration and AppStore Dashboard

Note: you can reorder extensions so that updates from one can affect updates to the next.

### ⭐️ Extensions for Custom Graphics

Extensions also allow custom bar charts in your reports:

Generated report with graphics:

# AppStore API

Faction supports server-side extensions, similar in concept to BurpSuite extensions. An extension is a Java JAR that implements one or more Faction Extender interfaces, packaged with a small set of resource files, and uploaded through the Faction App Store UI. Faction invokes the extension when specific events fire — for example, an assessment being finalized, a report being generated, or a retest being completed.

Typical use cases: pushing vulnerabilities into an external tracker (Jira, ServiceNow), querying an external CMDB during assessment scheduling, or injecting custom HTML (charts, tables) into generated reports.

Available since Faction 1.2. Example project: <https://github.com/factionsecurity/Faction-Jira-Extension>

## Extension Hooks

An extension class extends
```
BaseExtension
```

and implements one of the following interfaces.

InterfaceTriggers onReceivesReturns
```
com.faction.extender.ApplicationInventory
```

Assessment schedulingApplication ID or name
```
InventoryResult[]
```

from an external source (replaces local DB lookup)
```
com.faction.extender.AssessmentManager
```

Assessment create / update / delete / finalize, peer review created / complete / accepted
```
Assessment
```

,
```
List<Vulnerability>
```

,
```
Operation
```
```
AssessmentManagerResult
```

with updated assessment and vulns (or
```
null
```

for no local update)
```
com.faction.extender.ReportManager
```

Report create or regenerate
```
Assessment
```

,
```
List<Vulnerability>
```

, current
```
reportText
```

Modified report text (HTML or raw);
```
null
```

leaves the report unchanged
```
com.faction.extender.VulnerabilityManager
```

Vulnerability create / update / delete
```
Assessment
```

,
```
Vulnerability
```

,
```
Operation
```

Updated
```
Vulnerability
```

(or
```
null
```

for no local update)
```
com.faction.extender.VerificationManager
```

Retest pass / fail / cancel / assigned
```
User
```

,
```
Vulnerability
```

, comment, start date, end date,
```
Operation
```

void

The
```
Operation
```

enum lets a single hook differentiate between events — for example, only acting on
```
Operation.Finalize
```

inside
```
AssessmentManager
```

.

## Project Layout

Extensions are built as Maven projects. Add the Faction Extender dependency to
```
pom.xml
```

:
```
```
<dependency>
    <groupId>com.factionsecurity</groupId>
    <artifactId>faction-extender</artifactId>
    <version>2.5</version>
</dependency>```
```

Use
```
maven-assembly-plugin
```

with
```
jar-with-dependencies
```

so the JAR includes all transitive dependencies. The manifest must include
```
Title
```

,
```
Version
```

,
```
Author
```

, and
```
URL
```

entries — these are surfaced in the App Store UI.

Required resource files:
```
```
src/main/resources/META-INF/
├── resources/
│   ├── config.json        # User-configurable settings
│   ├── description.md     # Help text shown in App Store
│   └── logo.png           # Icon shown in App Store
└── services/
    └── com.faction.extender.<InterfaceName>   # Service descriptor```
```

### ``` config.json ```

Defines the settings the user can edit in the App Store UI. Each entry produces an input field. Values defined here are defaults; users can overwrite them after install.
```
```
{
  "Jira Host":    { "type": "text",     "value": "https://yourhost.com" },
  "Jira API Key": { "type": "password", "value": "your api key" },
  "Jira Email":   { "type": "text",     "value": "[email protected]" }
}```
```
```
type
```

must be
```
text
```

or
```
password
```

.
```
password
```

fields are masked in the UI and are not returned to the UI after save.

### ``` description.md ```

Markdown describing what the extension does, why a user would install it, and how to configure it. Rendered in the App Store detail view.

### ``` logo.png ```

PNG icon shown in the App Store listing.

### ``` services/ ``` descriptor file

The filename **must** be the fully-qualified interface name your extension implements — one of:

- ```
  com.faction.extender.ApplicationInventory  ```
- ```
  com.faction.extender.AssessmentManager
  ```
- ```
  com.faction.extender.ReportManager  ```
- ```
  com.faction.extender.VerificationManager
  ```
- ```
  com.faction.extender.VulnerabilityManager  ```

The file contents are the fully-qualified class name of your implementation, e.g.

```
org.faction.JiraPlugin```

. Without this file, Faction cannot load the extension.

An extension that hooks multiple events includes one service descriptor file per interface implemented.

## Minimal Example

A Jira extension that pushes vulnerabilities to Jira only when an assessment is finalized, and writes the returned issue IDs back to Faction as tracking IDs:

```
```
package org.faction;

public class JiraPlugin extends BaseExtension implements com.faction.extender.AssessmentManager {

    @Override
    public AssessmentManagerResult assessmentChange(Assessment assessment,
                                                    List<Vulnerability> vulns,
                                                    Operation opcode) {
        String project = "KAN"; // Jira project key

        if (opcode == Operation.Finalize) {
            for (Vulnerability vuln : vulns) {
                String issueId = sendVulnerabilityToJira(vuln, project);
                if (issueId != null) {
                    vuln.setTracking(issueId); // Sync Jira ID back to Faction
                }
            }
        }

        AssessmentManagerResult result = new AssessmentManagerResult();
        result.setAssessment(assessment);
        result.setVulnerabilities(vulns);
        return result; // Returning null would skip the Faction-side update
    }
}
```
```

Full reference implementation: <https://github.com/factionsecurity/Faction-Jira-Extension>

## Build and Install

Build the JAR:

```
```
mvn clean compile assembly:single
```
```

This produces

```
target/<artifact>-<version>-jar-with-dependencies.jar```

.

In Faction, go to **Admin → App Store → Install Extension** and upload the JAR. The extension installs in a disabled state. Click the extension in the list, fill in the settings defined by

```
config.json```

, and enable it. The hook will fire on its registered events from that point on.

## Reference

- [App Store Extension API](https://docs.factionsecurity.com/APIS/App%20Store%20Extension%20API/)— hook interface reference.
- [JIRA App Integration Example](https://docs.factionsecurity.com/APIS/JIRA%20App%20Integration%20Example/)— full walkthrough.
- [Faction-Jira-Extension](https://github.com/factionsecurity/Faction-Jira-Extension)— example project source.
- [Faction-Vulnerability-Bar-Chart](https://github.com/factionsecurity/Faction-Vulnerability-Bar-Chart)— example

  ```
  ReportManager  ```

  extension that injects HTML bar charts into reports.

# MCP Server

The Faction MCP server is a Model Context Protocol (MCP) server that exposes a Faction instance — assessments, vulnerabilities, retests, vulnerability templates, and audit logs — to any MCP-compatible AI client (Claude Code, Claude Desktop, OpenCode, GitHub Copilot CLI, LM Studio, and others).

It lets an AI agent read from and write to Faction directly, so workflows like running a CLI tool, parsing its output, creating a finding, and generating a report can be automated end-to-end without copying data between tools by hand.

Source repository: <https://github.com/factionsecurity/faction-mcp> (MIT licensed)

## What you can do with it

- Drive Faction from an AI client: pull your assessment queue, open vulnerabilities, retests, and audit log entries.
- Create and update vulnerabilities programmatically, including from default templates.
- Generate or download assessment reports (PDF/DOCX) and have the client open them directly.
- Generate executive summaries from stripped-down vulnerability data optimized for LLM context windows.
- Wire CLI security tools (nmap, nuclei, custom scripts, etc.) into reproducible workflows by combining the MCP server with agent skill files.
- Use any AI provider, including local LLMs (LM Studio, Ollama-style runners), so assessment data does not have to leave your environment.

## Requirements

- A running Faction instance.
- A Faction API key — generated from your user profile page in Faction.
- Docker, Docker Compose, Podman, or Podman Compose on the host that will run the MCP server.
- An MCP-compatible client (Claude Code, Claude Desktop, OpenCode, Copilot CLI, LM Studio, etc.).

## Installation

There are two supported installation paths.

### Option 1: Docker Desktop MCP Catalog

Install directly from the Docker Desktop MCP Catalog and enter

```
FACTION_API_KEY```

and

```
FACTION_BASE_URL```

when prompted. This is the lowest-friction option if you already use Docker Desktop.

### Option 2: Docker Compose (Docker or Podman)

Works anywhere Docker Compose or Podman Compose is available.

**1. Clone the repository and create the environment file**

```
```
git clone https://github.com/factionsecurity/faction-mcp.git
cd faction-mcp
cp .env.example .env
```
```

**2. Edit .env with your Faction details**

```
```
FACTION_API_KEY=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
FACTION_BASE_URL=https://faction.yourcompany.com
```
```

To rotate credentials later, edit

```
.env```

— no rebuild is required.

**3. Build the image**

```
```
docker compose build
# or
podman-compose build
```
```

**4. Configure your MCP client**

Add the server to your client’s MCP config. Use the absolute path to your cloned

```
docker-compose.yml```

.

Claude Code / Claude Desktop (

```
~/.claude/settings.json```

or

```
claude_desktop_config.json```

):

```
```
{
  "mcpServers": {
    "faction": {
      "command": "docker",
      "args": [
        "compose",
        "-f", "/absolute/path/to/faction-mcp/docker-compose.yml",
        "run", "--rm", "-T", "faction-mcp"
      ]
    }
  }
}
```
```

OpenCode:

```
```
{
  "mcp": {
    "faction": {
      "type": "local",
      "command": [
        "docker", "compose",
        "-f", "/absolute/path/to/faction-mcp/docker-compose.yml",
        "run", "--rm", "-T", "faction-mcp"
      ],
      "enabled": true
    }
  }
}
```
```

Podman users substitute

```
podman-compose```

for

```
docker compose```

. The

```
-T```

flag disables pseudo-TTY allocation so stdio passes cleanly between the client and the server.

After restarting the client, run its MCP listing command (

```
/mcps```

in OpenCode, equivalent elsewhere) to confirm

```
faction```

is connected.

### Shared reports / images directory

The compose files mount one host directory into the container at

```
/app/reports```

. By default this is

```
/tmp```

. It is used for two things:

- **Report downloads.**

  ```
  get_assessment_report  ```

  and

  ```
  generate_assessment_report  ```

  write the PDF/DOCX here and return the host path so the client can open the file.
- **Image uploads.**

  ```
  upload_assessment_image  ```

  reads from this directory. The agent is instructed to copy or save images into it first, then pass the host path. The server translates

  ```
  /tmp/foo.png  ```

  →

  ```
  /app/reports/foo.png  ```

  internally.

Routing image bytes through disk avoids round-tripping large base64 strings through tool arguments, where token-stream drift can corrupt the payload.

To use a different host folder, set

```
FACTION_REPORTS_HOST_DIR```

to an absolute path in

```
.env```

:

```
```
FACTION_REPORTS_HOST_DIR=/Users/me/faction-reports
```
```

## Available Tools

The server exposes the following tool surface to the AI client.

### Assessments

ToolDescription

```
get_assessment_queue```

Active queue for the authenticated user (in-progress / upcoming / past-due). Use for “my recent assessments”.

```
get_completed_assessments```

Completed assessments in a date range with full detail.

```
get_completed_assessments_condensed```

Same as above with large text blocks stripped. Preferred for stats and historical summaries.

```
get_assessment```

Full details for a specific assessment by ID.

```
update_assessment```

Update assessment notes, executive summary, distribution list, custom fields.

```
get_assessment_vulnerabilities```

Full vulnerability data for an assessment (large; includes HTML and screenshots).

```
get_vulnerability_summary_data```

Stripped vulnerability data optimized for executive summary generation.

```
get_assessment_report```

Download the existing PDF/DOCX report to the configured reports directory.

```
generate_assessment_report```

Kick off a fresh report build and poll for completion.

```
check_report_status```

Standalone poll used to resume waiting when generation outlasts the initial wait.

### Vulnerabilities

ToolDescription

```
get_vulnerabilities```

All vulnerabilities opened in a date range with full detail.

```
get_vulnerabilities_condensed```

Same with large text blocks stripped.

```
create_vulnerability```

Add a vulnerability to an assessment. Interactively prompts for missing fields and offers matching templates.

```
update_vulnerability```

Update fields on an existing vulnerability.

```
add_templated_vulnerability```

Add a vulnerability from a default template.

```
get_vulnerability```

Get a vulnerability by ID.

```
get_vulnerability_by_tracking```

Get a vulnerability by tracking ID (e.g. Jira ticket).

```
set_vulnerability_tracking```

Assign a tracking ID.

```
set_vulnerability_status```

Set remediation status (dev/prod closed dates).

```
get_risk_levels```

Configured risk level definitions; unmapped slots filtered out.

```
get_categories```

/

```
get_category```

/

```
create_category```

Manage vulnerability categories (create requires manager role).

### Vulnerability Templates

ToolDescription

```
get_vulnerability_templates```

All default vulnerability templates.

```
search_vulnerability_templates```

Search templates by name (partial match).

```
get_vulnerability_template```

Get a template by ID.

```
create_vulnerability_templates```

Create or update default templates.

### Retests / Verifications

ToolDescription

```
get_verification_queue```

Retest queue for the authenticated user.

```
get_all_verifications```

All verifications, optionally filtered by date range.

```
get_user_verifications```

Verifications for a specific user.

```
complete_verification```

Mark a retest as passed or failed.

```
schedule_retest```

Schedule a retest for a vulnerability.

### Audit Logs

ToolDescription

```
get_audit_log```

System audit log for a date range (admin role required).

```
get_assessment_audit_log```

Audit entries for all assessments in a date range.

```
get_assessment_audit_log_by_id```

Audit entries for a specific assessment.

```
get_user_audit_log```

Audit entries for a specific user.

## Key Workflows

### Creating a vulnerability

```
create_vulnerability```

,

```
update_vulnerability```

, and

```
add_templated_vulnerability```

accept severity, impact, and likelihood as risk-level **names** (

```
"Critical"```

,

```
"High"```

,

```
"P1"```

, etc.). The server resolves the name to the correct numeric ID for your Faction instance via

```
get_risk_levels```

, so the LLM never needs to know the IDs and skills do not break when IDs differ between instances.

When required information is missing,

```
create_vulnerability```

walks the user through an interactive workflow via MCP elicitation (supported by Claude Code, Claude Desktop, and other elicitation-capable clients):

- **Title and severity**— if either is missing, the user is prompted. Risk levels are presented as a dropdown of the names actually configured on the instance.
- **Template offer**— if no description, recommendation, or template ID is supplied, the server searches default templates by title and offers matches. Selecting one auto-populates description and recommendation.
- **Mirror severity**— if severity is set but impact/likelihood are not, the server asks whether to mirror severity to both, or to set them explicitly.

If the client does not support elicitation, the tool returns an error listing the missing fields so the agent can ask the user in plain text.

### Generating executive summaries

Use

```
get_vulnerability_summary_data```

rather than

```
get_assessment_vulnerabilities```

. It returns text-only, stripped vulnerability data optimized for LLM processing. After the AI drafts the summary HTML, it calls

```
update_assessment```

to write it back to Faction.

### Generating and downloading reports

Three tools cover report handling:

- ```
  generate_assessment_report
  ```

  — starts a fresh report build (use
  ```
  retest=true
  ```

  for finalized assessments) and polls up to
  ```
  max_wait_seconds
  ```

  (default 60).
- ```
  check_report_status  ```

  — standalone poll when the initial wait expires. Pass

  ```
  last_known_gentime  ```

  from the generate response.
- ```
  get_assessment_report
  ```

  — downloads the existing report. The file is written to the configured reports directory and the absolute host path is returned as
  ```
  file_path
  ```

  .

A typical run: ask the agent to generate a new report for an assessment ID; the server fires generation, waits, and reports completion; the agent then calls
```
get_assessment_report
```

and surfaces the file path.

## Automating CLI Tools with Agent Skills

The MCP server gives the agent access to Faction. To turn ad-hoc agent runs into reproducible workflows, pair it with agent skill files (
```
SKILL.md
```

/
```
AGENTS.md
```

) that describe a fixed procedure: which command to run, how to parse the output, what severity to use, what fields to populate in Faction.

A typical skill for an nmap-driven information finding might:

- Require explicit user authorization that the target is in scope.
- Run a fast top-ports scan (
  ```
  nmap -Pn --top-ports 100 <target>
  ```

  ).
- Run a vulnerability scan against only the discovered open ports (
  ```
  nmap -sV --script=vuln -p <ports> <target>
  ```

  ).
- Parse the output into a list of ports, services, versions, and identified CVEs.
- Call
  ```
  create_vulnerability
  ```

  with a fixed naming convention, the configured lowest severity tier (e.g.
  ```
  "Recommended"
  ```

  ), and a markdown details field containing two tables (commands run, and ports/weaknesses).

Because the skill pins the procedure — command flags, severity, description structure, table format — the resulting findings are consistent across assessments and across whoever (or whatever agent) runs the skill. The same pattern applies to any CLI tool that produces parseable output.

A worked nmap skill example is published with the Faction blog post linked below.

## Reference

- Repository and README: <https://github.com/factionsecurity/faction-mcp>
- Walkthrough with full nmap skill example: [Automate Your Pentesting Workflow: Connecting Faction to AI Agents via MCP](https://medium.com/@we-are-faction/automate-your-pentesting-workflow-connecting-faction-to-ai-agents-via-mcp-c985c8c79e2d)
- Faction core project: <https://github.com/factionsecurity/faction>
- Background on agent skills: <https://agents.md/>
