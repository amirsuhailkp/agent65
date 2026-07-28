---
title: OWASP Threat Dragon
source: owasp.org
url: https://owasp.org/www-project-threat-dragon/
collector: owasp
category: web-security
tags:
- web-security
- threat
- dragon
- version
- modeling
date_collected: '2026-07-26T12:43:55.177473Z'
language: unknown
---

# OWASP Threat Dragon

## What is Threat Dragon?

OWASP Threat Dragon is a modeling tool used to create threat model diagrams as part of a secure development lifecycle. It can be used to record possible threats and decide on their mitigations, as well as giving a visual indication of the threat model components and threat surfaces. Threat Dragon runs either as a web application or as a desktop application.

Threat Dragon supports STRIDE / [LINDDUN](https://linddun.org/) / CIA / DIE / [PLOT4ai](https://plot4.ai/),
provides modeling diagrams and implements a rule engine to auto-generate threats and their mitigations.

This project has [OWASP Production status](https://owasp.org/www-project-threat-dragon/) and follows the values and principles
of the [threat modeling manifesto](https://www.threatmodelingmanifesto.org/).

### Resources

Use the [version 2](https://www.threatdragon.com/docs/) documentation to get started,
along with the recording of Mike Goodwin giving a [lightning demo](https://youtu.be/n6JGcZGFq5o)
during the OWASP Open Security Summit in June 2020.
The [version 1.x](https://threatdragon.github.io/) are available if you are using legacy versions of Threat Dragon.

An [introduction](https://www.youtube.com/watch?v=hUOAoc6QGJo) to Threat Dragon is provided by
the [OWASP Spotlight](https://www.youtube.com/playlist?list=PLUKo5k_oSrfOTl27gUmk2o-NBKvkTGw0T) series,
and the [Threat Modeling Gamification](https://www.youtube.com/watch?v=u2tmLrwv-nc) seminar by Vlad Styran
shows how using Threat Dragon can make threat modeling fun.

There are a couple of OWASP community pages that give overviews on Threat Modeling and how to get started:
[Threat Modeling](https://owasp.org/www-community/Threat_Modeling)
and [Threat Modeling Process](https://owasp.org/www-community/Threat_Modeling_Process).

### Contact

The easiest way to get in contact with the Threat Dragon community is
by emailing the [OWASP google group](/cdn-cgi/l/email-protection#c8bca0baada9bce5acbaa9afa7a6e5b8baa7a2adabbc88a7bfa9bbb8e6a7baaf).
The OWASP Slack channel [#project-threat-dragon](https://owasp.slack.com/messages/CURE8PQ68) is a good source of information,
although you may [need to subscribe](https://owasp.org/slack/invite) first.

### Related OWASP projects

- [pytm (Pythonic Threat Modeling)](https://owasp.org/www-project-pytm/)
- [Threat Modeling Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html)
- [Threat Modeling Project](https://owasp.org/www-project-threat-modeling/)
- [Threat Model Library](https://github.com/OWASP/www-project-threat-model-library)

Threat Dragon: *making threat modeling less threatening*

## FAQs

- [Why do the earlier releases come from Mike Goodwin’s repo, not the OWASP repo?](https://github.com/OWASP/threat-dragon/wiki/FAQs#why-do-the-earlier-releases-come-from-mike-goodwins-repo-not-the-owasp-repo)
- [Why do I get ‘Apple cannot check it for malicious software’ errors after installing on MacOS?](https://github.com/OWASP/threat-dragon/wiki/FAQs#why-do-i-get-developer-can-not-be-verified-errors-after-installing-on-macos)
- [Why do I get ‘Permissions failure opening Mac desktop app’ when installing from the zip file?](https://github.com/OWASP/threat-dragon/wiki/FAQs#why-do-i-get-permissions-failure-opening-mac-desktop-app-when-installing-from-the-zip-file)
- [Why do I get ‘developer can not be verified’ errors after installing on MacOS?](https://github.com/OWASP/threat-dragon/wiki/FAQs#why-do-i-get-developer-can-not-be-verified-errors-after-installing-on-macos)
- [Is there a command line interface for Threat Dragon Desktop?](https://github.com/OWASP/threat-dragon/wiki/FAQs#is-there-a-command-line-interface-for-threat-dragon-desktop)
- [When is Threat Dragon’s birthday? And does Threat Dragon have a theme tune?](https://github.com/OWASP/threat-dragon/wiki/FAQs#when-is-threat-dragons-birthday-and-does-threat-dragon-have-a-theme-tune)

Threat Dragon: *making threat modeling less threatening*

## Initiatives

We appreciate greatly all our contributors: without their open-source contributions Threat Dragon would be long-gone.

There are some individuals and teams that have come forward to make an ‘above and beyond’ difference to Threat Dragon, and here they are:

### Threat model templates

With the support of [Gallagher Security](https://security.gallagher.com/en),
Ajith Penmatsa ([Ajith-Penmatsa-GGL](https://github.com/Ajith-Penmatsa-GGL))
created a new feature which allows reusable threat-model templates.
This is the first step towards providing a set of reusable threats and mitigations,
which will provide the sharing of effort and ideas within the global Threat Dragon community.

### Integration with EoP Games

A team from the Universidad Católica del Uruguay ([UCU](https://www.ucu.edu.uy/)) took part in a Coding Challenge
to provide integration between Cornucopia and Threat Dragon.
In addition they made it extensible so that other EoP-type cards can be integrated into Threat Dragon.

We are very grateful and look forward to more contributions to the open-source community:

- Anthony Pereira ([Clarensedor](https://github.com/Clarensedor))
- Belén Bulla ([bbulla](https://github.com/bbulla))
- Belén de Oliveira Madeira ([beldomadeira](https://github.com/beldomadeira))
- Chris Bentancor ([ChrisBentancor](https://github.com/ChrisBentancor))
- Diego Gamarra ([gamarradiego](https://github.com/gamarradiego))
- Emanuel Fraga ([FragaEmanuel](https://github.com/FragaEmanuel))
- Gaspar Lamas ([gasparlamas](https://github.com/gasparlamas))
- Guillermo Guerrico ([GuilleGuerrico098](https://github.com/GuilleGuerrico098))
- Javier Moreno ([javiermorenov1203](https://github.com/javiermorenov1203))

and many thanks to Gerardo Canedo ([gerardocanedoUCU](https://github.com/gerardocanedoUCU)) for making this happen.

### Google Summer of Code 2024

Mohamed El-Bohy ([mohamedselbohy](https://github.com/mohamedselbohy)) devoted his summer of 2024
to completing the Threat Dragon functionality.
When Threat Dragon moved from version 1.x to version 2.x it was not feature complete,
and Mohamed implemented these final features for Threat Dragon.

### Migration to Vue and antv/x6

Leo Reading ([lreading](https://github.com/lreading)) travelled the long road of migrating Threat Dragon
from AngularJS + JointJS to Vue + antv/x6.
This ensured that Threat Dragon made it to version 2.x,
otherwise Threat Dragon would be swamped with unsupported dependencies.

Threat Dragon: *making threat modeling less threatening*

## Strategic Roadmap

Threat Dragon maintains a strategic roadmap in a public
[GitHub Discussion](https://github.com/OWASP/threat-dragon/discussions/1480).
Please join us in defining the direction for Threat Dragon!

## Release Log

Threat Dragon creates [GitHub Releases](https://github.com/OWASP/threat-dragon/releases/)
for each release. Each release contains the artifacts and the change log.

The latest release is always available
[on GitHub](https://github.com/OWASP/threat-dragon/releases/latest)

### Versioning & Release Cadence

Threat Dragon adheres to [semantic versioning](https://semver.org/) for all releases.
In practice, this means:

- Patch versions include bug/security fixes, with no breaking changes
- Minor versions include new features or functionality, with no breaking changes
- Major versions include breaking changes, major upgrades, etc.

There is no official release cadence at this time. Threat Dragon maintainers create new releases for new features and bugfixes when appropriate.

## Major Version Releases

### Version 3.0: future initiatives

Version 3 is not well defined at this time. The following features may be included in this future release.

- TM-BOM / [Threat model file format](https://owasp.org/www-project-threat-dragon/#div-tmf)

### Version 2.0: Modernization

Version 2.0 of Threat Dragon was largely done to exist technical debt and improve the overall maturity of Threat Dragon. Some highlights from this major version:

- Migration from angular to Vue
- Upgraded the diagram library
- [Met OpenSSF Best Practices](https://www.bestpractices.dev/en/projects/9266/passing#analysis)
- Combined frontend with desktop application
- Updated threat model schema
- Implemented end to end testing
- DAST scanning via Zap
- Public [demo instance](https://www.threatdragon.com/)

### Version 1.0: Initial Release

Mike Goodwin’s initial roadmap for the project is
[archived here](https://github.com/OWASP/www-project-threat-dragon/wiki/Original-Roadmap).
The original roadmap had various milestones, most of which were achieved by late 2020.

**Milestone 4**: Dev lifecycle integration

- Some CLI interface available mid 2020

**Milestone 3**: Release 1.0

- production version released February 2020
- version 1.3.1 released October 2020

**Milestone 2**: Beta release: Threat/mitigation rule engine

- achieved May 2017 with version 0.1.26

**Milestone 1**: Alpha release - Basic threat modelling experience

- achieved October 2015

Threat Dragon: *making threat modeling less threatening*

## Threat model file format

Threat Dragon version 1.x and Threat Dragon version 2.x use closely related but incompatible JSON file formats. In addition both these file formats are arranged around diagram elements used by the graph editing engines: JointJS for version 1.x and AntV/X6 for version2.x. The data model use in the Threat Dragon file format would be better centred round threat model information rather than the data used for the graph editing.

Both Threat Dragon file formats are incompatible with other open source Threat Modeling files such as pytm, Threagile and Open Threat Model.

The intention is to change the model file format in Threat Dragon version 3.x onwards. The goal will be to define a file format that is flexible enough to easily convert from the existing:

- OWASP Threat Dragon versions 1.x and 2.x
- [OWASP pytm](https://owasp.org/www-project-pytm/)pythonic threat modeling
- [Threagile](https://threagile.io)open-source toolkit for agile threat modeling
- [Open Threat Model](https://github.com/iriusrisk/OpenThreatModel)(OTM) file format

There is an [open discussion](https://github.com/OWASP/threat-dragon/discussions/1152) for suggestions and debate on this subject.

### Threat Model Bill of Materials (TM-BOM)

It is very likely that the model file format used from version 3.x
will follow the Threat Model Bill of Materials (TM-BOM) schema.
This is similar in philosophy to a Software Bill of Materials (SBOM)
and is overseen by the [CycloneDX](https://owasp.org/www-project-cyclonedx/) organization.

The proof of concept [TM-BOM schema](https://github.com/OWASP/www-project-threat-model-library/blob/main/threat-model.schema.json) is provided
by the OWASP [Threat Model Library](https://github.com/OWASP/www-project-threat-model-library) project.
An [overview of TM-BOM](https://www.threatdragon.com/docs/development/schema.html) is available in the Threat Dragon documentation.
