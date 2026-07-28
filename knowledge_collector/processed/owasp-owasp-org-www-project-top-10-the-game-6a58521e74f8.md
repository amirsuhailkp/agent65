---
title: OWASP Top 10 The Game
source: owasp.org
url: https://owasp.org/www-project-top-10-the-game/
collector: owasp
category: web-security
tags:
- web-security
- game
- top
- owasp
- how
date_collected: '2026-07-26T12:44:44.322270Z'
language: unknown
---

# OWASP Top 10 The Game

Cybersecurity education and training often suffer from being too theoretical, complex, or disconnected from real-world scenarios. Traditional learning methods fail to engage professionals effectively, leading to knowledge gaps in critical OWASP vulnerabilities ([Top 10](https://owasp.org/Top10/), [API Security Top 10](https://owasp.org/API-Security/editions/2023/en/0x00-header/), [Mobile Top 10](https://owasp.org/www-project-mobile-top-10/), [IoT Top 10](https://ot.owasp.org/), [AI Top 10](https://owasp.org/www-project-machine-learning-security-top-10/), [LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/), etc.) that remain the most exploited attack vectors year after year.

## Introduction

OWASP Top 10 The Game is a gamified and interactive learning experience that transforms cybersecurity training to make it more engaging, practical, and collaborative. It focuses on the most critical real-world vulnerabilities described by OWASP, turning learning into a fun activity that fosters teamwork and builds a strong security culture, all in an accessible, free-to-play format.

To start using OWASP Top 10 The Game or find out more about the game please visit this site [Top10TheGame.org](https://top10thegame.org/en)

## How to Contribute

Thank you for your interest in contributing to OWASP Top 10 The Game! We are excited to receive help from the community and appreciate every contribution, from fixing a typo to implementing a new feature, gameplay mechanics, new characters, etc. The game is designed to build new boards together with the community. These can be general-purpose, or very specific to an infrastructure deployment, how a tool helps to mitigate threats in a specific scenario, etc. Click on the “How to Contribute” tab to see the complete guide for contributing to the project.

## Licensing

OWASP Top 10 The Game is free to use. It is licensed under the Creative Commons Attribution-ShareAlike 4.0 license, so you can distribute, remix, adapt, and build upon the material in any medium or format, so long as attribution is given to the creator. The license allows for commercial use. If you remix, adapt, or build upon the material, you must license the modified material under identical terms. CC BY-SA includes the following elements:

BY: credit must be given to the creator.
SA: Adaptations must be shared under the same terms.

© OWASP Foundation

## How to Play

Please visit [OAWSP Top 10 The Game - Rules](https://top10thegame.org/en/#how-to-play)

## How to Contribute

We are finalizing our contribution guidelines and will publish a comprehensive “How to Contribute” guide here shortly. It will cover how to report issues, propose improvements, submit PRs, and especially how to create and publish new game boards so the community can learn from and build on your work. Stay tuned!

# Road Map

##### Pedro Miguel Díaz Peña

This is an OWASP Top 10 The Game road map.

## Important Dates

### Public Release

Initial public release of OWASP Top 10 The Game.

## Objectives

### Adoption in the security community

Achieve widespread use of the game by the security community as a learning tool for the OWASP Top 10 lists.

### Active community of board creators

Foster an active community of game board creators, engaging cybersecurity experts, security tool builders, and industry companies.

## Milestones

### How to Contribute Guide

Create, publish, and maintain the contribution guide for the project.

#### DOING How to add new game boards MUST

Document the steps and required assets to add new game boards.

#### TODO Repository contribution guide SHOULD

Define how to contribute to the game's repository: local setup, coding standards, branching model, commit conventions, PR workflow, and how to add new features or modify existing code.

#### TODO Guide for custom images and characters SHOULD

Provide guidance on using custom images and characters so security teams can personalize the game for their contexts without breaking consistency.

### Digital Game Features

Provide digital features so the game can be played beyond physical format.

#### DOING Virtual Table MUST

Provide a digitized game table including the game board, OWASP tokens, and the trust board, so that only the physical cards are needed to play.

#### DOING Categorized map selector MUST

Implement a map selector categorized by typology, complexity, security area, and other relevant filters to help players quickly find the most suitable game board.

#### TODO Private map selector MUST

Allow teams to create and select private game boards that can be played without uploading anything to the project's repository.

#### TODO Peer-to-peer game rooms SHOULD

Create peer-to-peer rooms so groups can play completely digitally using their phones when meeting physically, without requiring a central server.

### New Design

Commission professional graphic design for cards and overall game visuals.

#### TODO Redesign player cards SHOULD

Update layout, iconography, and readability of player cards.

#### DOING Deck case design SHOULD

Design a protective deck case for storing and transporting cards.

## Project Supporters

### Top Supporters

*In order to be recognized as a “Top Supporter” a company
must have donated $1000 in the last 12 months.*

### All Corporate Supporters

*In order to be recognized as a “Corporate Supporters” a company
must have donated $100 in the last 12 months.*

### All Individual Supporters

*In order to be recognized as a “Individual Supporters” an individual
must have donated $25 in the last 12 months.*

# OWASP Top 10 The Game Repo - Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.1] - 2025-10-01

### Added

- Top10TheGame Home, Characters, Components, Rules & Team Building extension
- Download Print&Play:
  - Base cards and components
  - Game boards
  - Team Building extension cards

# OWASP Project Repo - Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.1] - 2025-10-01

### Added

- Top10TheGame-header.png image to project assets
- Project logo (logo.png) and CC license images (by.png, sa.png)
- 404 error page images in
  ```
  assets/images/web/
  ```
- New tabs:
  ```
  tab_howtocontribute.md
  ```

  ,
  ```
  tab_howtoplay.md
  ```

  ,
  ```
  tab_roadmap.md
  ```

  ,
  ```
  tab_supporters.md
  ```
- Roadmap data file
  ```
  roadmap.yml
  ```

  and Roadmap tab content/visual timeline
- Roadmap milestones and deliverables:
  - M1 How to Contribute Guide
    - How to add new game boards (DOING, MUST)
    - Repository contribution guide (TODO, SHOULD)
    - Guide for custom images and characters (TODO, SHOULD)
  - M2 Digital Game Features
    - Virtual Table (DOING, MUST)
    - Categorized map selector (DOING, MUST)
    - Private map selector (TODO, MUST)
    - Peer-to-peer game rooms (TODO, SHOULD)
  - M3 New Design
    - Redesign player cards (TODO, SHOULD)
    - Deck case design (DOING, SHOULD)
- M1 How to Contribute Guide

### Changed

- ```
  index.md  ```

  : clearer instruction to select the “How to Contribute” tab (plain text, no MD link)
- ```
  tab_howtocontribute.md
  ```

  : placeholder replaced with pending-guidelines notice
- ```
  tab_supporters.md  ```

  : updated logo placeholder; copy tweaks
- Supporters text: “an individual” for Individual Supporters criteria
- Roadmap M2 title to “Digital Game Features” with description to support non-physical play
- Roadmap tab order updated (order: 3)
- Roadmap visual status bars standardized (gray for TODO, blue for DOING)

### Fixed

- Replaced localhost contribution link with proper reference
- Typo and spacing fixes in supporters and roadmap descriptions

### Removed

- ```
  assets/images/README.md
  ```
- ```
  tab_example.md  ```
