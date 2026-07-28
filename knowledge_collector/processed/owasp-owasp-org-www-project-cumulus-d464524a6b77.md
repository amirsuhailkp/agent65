---
title: OWASP Cumulus
source: owasp.org
url: https://owasp.org/www-project-cumulus/
collector: owasp
category: web-security
tags:
- web-security
- cumulus
- card
- game
- threat
date_collected: '2026-07-26T12:45:16.596117Z'
language: unknown
---

# OWASP Cumulus

# *Threat modeling the clouds*

Cumulus is the easy way to bring security into cloud and devOps teams.

As a variant of the card game Elevation of Privilege it follows the idea to threat model a system via gamification. This lightweight and low-barrier approach helps you find threats to your devOps or cloud project and teaches the developers a security oriented mindset.

Find the latest release [here](https://github.com/OWASP/cumulus/releases/latest).

## Threat Modeling

The idea of threat modeling via serious games goes back to the card game [Elevation of Privilege](https://shostack.org/games/elevation-of-privilege) by [Adam Shostack](https://github.com/adamshostack).
The basic idea is to bring the developers on a table and get them start discussing the security of their system.
For this, a card game serves as a guide through a catalogue of threats.
It is designed to be low-barrier and naturally embeddable within agile development processes.

While the original game approaches security in general and another variant, Cornucopia by the OWASP Foundation, targets (web) application security in particular, we had the feeling that the specific needs of devOps team working in cloud environments have been missing. Cumulus seeks to fill this gap and provides a custom card deck with threats to cloud systems.

Threats are classified into the categories (which are also the suits in this game):

CategoryAccess & SecretsThreats related to IAM and secrets managementDeliveryBuild and ship software, and its supply chainRecoveryBackup and restoreMonitoringLogs, alerts and traceabilityResourcesThreats on resources and their configuration

This game does explicitly **not** try to replace Elevation of Privilege or Cornucopia.
It should rather be seen as part of a triplet of threat modeling card decks, reflecting different aspects of modern software development projects.

## Acknowledgements

Cumulus was started at and it heavily supported by [TNG Technology Consulting](https://www.tngtech.com/en/index.html).

The original and wonderful idea of conducting threat modeling via serious games goes back to [Adam Shostack](https://github.com/adamshostack), working for Microsoft at that time.
He invented the game [Elevation of Privilege](https://shostack.org/games/elevation-of-privilege) which is the blue print for Cumulus.

Another great game following Elevation of Privilege’s approach to threat modeling is [Cornucopia](https://owasp.org/www-project-cornucopia/) developed by the [OWASP Foundation](https://owasp.org/).

Both card games are great tools to help development teams increase the security of the system they are building.

However, we felt the need for a threat modeling card game targeting devOps/cloud projects in particular. Out of this idea, Cumulus arose.

## Versioning

The card deck follows [semantic versioning](https://semver.org/).
Version changes mean:

- *patch version*: Non-semantic changes: layout, typos, minor re-wordings, …
- *minor version*: Semantic changes: rephrasings, additional cards…
- *major version*: Substantial semantic changes: new categories, …

## Licensing

The card game (including the threat formulations and the released PDF) files are distributed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
When distributing this game, mentioning [TNG Technology Consulting](https://www.tngtech.com/en/index.html) is highly appreciated.

## Rules of the game

Cumulus ist trick-taking card game, similar to spades.

The objective is to collect as many points as possible, either by taking a trick or by finding threats. At the end of the game the winner is the player with the most points.

In preparation of the game a system model, e.g. an architectural overview, is generated. Ideally, this is in the form of a data flow diagram, but in the end every overview which is understood by the players is fine. Additionally, the players agree on a starting suit, i.e. a threat category.

After distributing the cards amongst the players, the game starts. The first dealer is the player holding the lowest card in the starting suit. The dealer plays a card in the starting suit. Each of the other players has to follow the suit during that round. If that is not possible, the player can choose any card on hand. The winner of the round takes the trick and is the one who played the highest value card in the round’s suit or the highest trump card.

Trumps are cards from the suit **access & secrets**.

The winner then receives a point, starts a new round and chooses the new suit. Each time a new card is played, all players are asked to think about whether that particular threat, mentioned on the current card, applies to their system in some form. If a threat is found (and the team agrees that this is a topic to look at), it is written down and the finder receives an extra point.

As Cumulus shares the same rules as Elevation of Privilege and Cornucopia, you can find alternative explanations of the rules [here](https://owasp.org/www-project-cornucopia/) or [here, chapter 2](http://download.microsoft.com/download/F/A/E/FAE1434F-6D22-4581-9804-8B60C04354E4/EoP_Whitepaper.pdf)

Also, Cornucopia has a wonderful explanation of the rules as a [Video on YouTube](https://www.youtube.com/watch?app=desktop&v=XXTPXozIHow&ab_channel=OWASPFoundation).

## Online Version

We also maintain an online version of Cumulus, which you can easily host yourselves. It can be found at

<https://github.com/tng/elevation-of-privilege>

Alternatively, Cumulus can be played at [copi.owasp.org](https://copi.owasp.org), see [the release notes](https://github.com/OWASP/cornucopia/releases/tag/v2.4.0).

## Printed Cards

Printed versions of the cards are available at [Agile Stationary](https://agilestationery.com/collections/threat-modeling).

If you want to print them yourselves, the [download](https://github.com/OWASP/cumulus/releases/latest) also contains printer-friendly versions.

## Cumulus in Media

- 2025-11-27: Cumulus was presented at the German OWASP Day 2025 in Düsseldorf. [Recording (en)](https://media.ccc.de/v/god2025-56482-owasp-cumulus-threat-model)
- 2025-06-26: [Blogpost about Cumulus](https://dev.to/owasp/no-need-to-fear-the-clouds-play-owasp-cumulus-d6g)written by[Johan Sydseter](https://github.com/sydseter)from OWASP Cornucopia.
- 2025-05-29: Cumulus was presented at the OWASP Global AppSec Conference in Barcelona: [Slides](assets/pdf/20250529_OWASPGlobalAppSec_Cumulus.pdf)
- 2025-05-20: [Threat Modeling Connect Spieleabend](https://lu.ma/njsexjws):[Slides](assets/pdf/20250520_TMC-DACH.pdf)*(in German)*
- 2025-03-25: Interview about Cumulus in the [Medical Device Cybersecurity Podcast](https://youtu.be/aMpIgmX9WZQ).
- 2023-12-14: The c’t magazine features an article about DevOps security and Cumulus:
  - [IT-Sicherheit: Eine Security-Einführung für DevOps-Teams](https://heise.de/-9573277)(German, behind paywall)
- 2023-04-06: Cumulus appears in [Adam Shostack’s blog](https://shostack.org/blog/cumulus-threat-model-thursday/)

## Contribute

Contributions to Cumulus are very much appreciated. In the end, this card deck is intended to be a community project. It should change and evolve in the same pace as cloud technologies and their particular security requirements change.

### Review and discuss

Feedback, reviews and other opinions are very welcome. This card game is only as helpful as its threats are relevant. Let’s work together to constantly improve the cards!

The best way is to simply create an [issue](https://github.com/OWASP/cumulus/issues) to start a discussion.
But you can also reach out to the project leads.

### Contribute to the cards

Changes to the threat formulations are welcome as pull requests to [cards.tex](https://github.com/OWASP/cumulus/blob/main/cards.tex).

### Contribute to documentation

When writing the threats we tried to condense each security issue into a single sentence. Although a sufficiently general (but maybe also vague) formulation can foster discussions, it can also hinder beginners to understand the threats. We would love to provide further explanations and examples to the cards.

Help (in the form of formulating explanations or giving real-world examples) are very much appreciated. Just contact the project leads.
