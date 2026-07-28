---
title: OWASP Security Shepherd
source: owasp.org
url: https://owasp.org/www-project-security-shepherd/
collector: owasp
category: web-security
tags:
- web-security
- security
- shepherd
- owasp
- users
date_collected: '2026-07-26T12:43:46.439785Z'
language: unknown
---

# OWASP Security Shepherd

## OWASP Security Shepherd

OWASP Security Shepherd is a web and mobile application security training platform. Security Shepherd has been designed to foster and improve security awareness among a varied skill-set demographic. The aim of this project is to take AppSec novices or experienced engineers and sharpen their penetration testing skillset to security expert status.

## Description

The OWASP Security Shepherd project enables users to learn or to improve upon existing manual penetration testing skills. This is accomplished by presenting security risk concepts to users in lessons followed by challenges. A lesson provides a user with help in layman terms about a specific security risk, and helps them exploit a text book version of the issue. Challenges include poor security mitigations to vulnerabilities which have left room for users to exploit.

Utilizing the OWASP top ten as a challenge test bed, common security vulnerabilities can be explored and their impact on a system understood. The by-product of this challenge game is the acquired skill to harden a player’s own environment from OWASP top ten security risks. The modules have been crafted to provide not only a challenge for a security novice, but security professionals as well.

Shepherd’s security risks are delivered through hardened real vulnerabilities that can not be abused to compromise the application or its environment. Shepherd does not simulate security risks so that all and any attack vectors will work, ensuring a real world response.

Security Shepherd is highly configurable. System administrators can tune the project experience to present specific security risk topics or even specific Security Shepherd modules. The array of user and module configuration available allows Shepherd to be used by a single local user, by many in a competitive classroom environment or by hundreds in an online hacking competition.

## Licensing

The Security Shepherd project is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

The Security Shepherd project is distributed in the hope that it will be useful, but without any warranty; without even the implied warranty of merchantability or fitness for a particular purpose. See the GNU General Public License for more details. See http://www.gnu.org/licenses/

## Layout Options

An administrator user of Security Shepherd can change the layout in which the levels are presented to players. There are three options

## CTF Mode

When Shepherd has been deployed in the CTF mode, a user can only access one uncompleted module at a time. The first module presented to the user is the easiest in Security Shepherd, which has not been marked as closed by the administrator. The levels increase slowly in difficulty and jump from one topic to another. This layout is the recommended setting when using Security Shepherd for a competitive training scenario.

## Open Floor Mode

When Shepherd has been deployed in the Open Floor mode, a user can access any level that is marked as open by the admin. Modules are sorted into their Security Risk Categories, and the lessons are presented first. This layout is ideal for users wishing to explore security risks.

## Tournament Mode

When Shepherd has been deployed in the Tournament Mode, a user can access any level that is marked as open by the admin. Modules are sorted into difficulty bands, from least to most difficult. This layout is ideal when Shepherd is being utilised as an open application security competition

## What is Security Shepherd

Security Shepherd provides;

- Teaching tool for application security
- Web application pen testing training
- Mobile application pen testing training
- Safe playground to practice AppSec techniques
- Real security risk examples

## Why use Security Shepherd?

FeatureDetailsWide Topic CoverageShepherd includes more than seventy levels across the entire spectrum of Web and mobile application security - within a single project.Gentle Learning CurveShepherd is a perfect entry point for users completely new to security, with levels increasing in difficulty at a manageable pace.Layman Write UpsEach security concept, when first addressed in Shepherd, is presented using plain language, so it can be readily understood by beginners.Real World ExamplesThe security risks in Shepherd are real vulnerabilities that have had their exploit impact dampened to protect the application, users and environment. There are no simulated security risks which require an expected, specific attack vector in order to pass a level. Attack vectors when used on Shepherd are how they would behave in the real world.ScalabilityShepherd can be used locally by a single user or easily as a server for a high amount of users.Highly CustomisableShepherd enables admins to set what levels are available to their users and in what way they are presented (Open, CTF and Tournament Layouts)Perfect for ClassroomsShepherd gives its players user specific solution keys to prevent students from sharing keys, rather than going through the steps required to complete a level.ScoreboardSecurity Shepherd has a configurable scoreboard to encourage a competitive learning environment. Users that complete levels first, second and third get medals on their scoreboard entry and bonus points to keep things entertaining on the scoreboard.User ManagementSecurity Shepherd admins can create users, create admins, suspend, unsuspend, add bonus points or take penalty points away user accounts with the admin user management controls. Admins can also segment their students into specific class groups. Admins can view the progress a class has made to identify struggling participants. An admin can even close public registration and manually create users if they wish for a private experience.Localisation SupportSecurity Shepherd material is available in multiple languages from a single instance. Students with alternative language preferences can compete in the same Shepherd instance as others without issue.Robust ServiceShepherd has been used to run online CTFs such as the OWASP Global CTF and OWASP LATAM Tour CTF 2015, both surpassing 200 active users and running with no downtime, bar planned maintenance periods.Configurable FeedbackAn administrator can enable a feedback process, which must be completed by users before a level is marked as complete. This is used both to facilitate project improvements based on feedback submitted and for system administrators to collect “Reports of Understanding” from their students.Granular LoggingThe logs reported by Security Shepherd are highly detailed and descriptive, but not screen blinding. If a user is misbehaving, you will know.

## Topic Coverage

The Security Shepherd project covers the following web and mobile application security topics;

- SQL Injection
- Broken Authentication and Session Management
- Cross Site Scripting
- Insecure Direct Object Reference
- Security Misconfiguration
- Sensitive Data Exposure
- Missing Function Level Access Control
- Cross Site Request Forgery
- Unvalidated Redirects and Forwards
- Poor Data Validation
- Insecure Data Storage
- Unintended Data Leakage
- Poor Authentication and Authorisation
- Broken crypto
- Client Side Injection
- Lack Of Binary Protections

## FAQs

> Can I Re-Skin Shepherd and then Train People With it?

Yes! Follow [this guide](https://github.com/OWASP/SecurityShepherd/wiki/How-To-Reskin-Shepherd)!

> Where can I access Security Shepherd?

You can Download it and run it yourself or there are various public instances (eg: [CTF365](https://community.ctf365.com/t/owasp-security-shepherd/357))

> Where can I download Security Shepherd?

You can download it from the [GitHub Release Page](https://github.com/OWASP/SecurityShepherd/releases/tag/v3.0)

> How can I run Shepherd on my network safely?

Just start the docker containers, boot up the VM or install Shepherd manually. The Security Shepherd application cannot be exploited to compromise the security of its environment. Make sure you patch your VM/Machine regularly to prevent intrusion to the host machine though

> How do I setup Security Shepherd?

Use our [Github Wiki](https://github.com/OWASP/SecurityShepherd/wiki) page for the best Setup Help going!

## Project Sponsors

The OWASP Security Shepherd project would like to acknowledge and thank the generous support of our sponsors. Please be certain to visit their websites and follow them on Twitter.

## Contributors

OWASP Security Shepherd is developed by a worldwide team of volunteers. The primary contributors to date have been:

- Mark Denihan
- Sean Duggan
- Paul McCann
- John Clarke
- Lei Shao
- Natalia Lopez
- Aidan Knowles
- Jason Flood

The Security Shepherd template makes it extremely easy to add additional lessons. We are actively seeking developers to add new lessons as new web technologies emerge. If you are interested in volunteering for the project, or have a comment, question, or suggestion, please contact [[email protected]](/cdn-cgi/l/email-protection)

New levels or level ideas are wanted in the highest degree and there is development is in progress to fork the Security Shepherd platform into a CTF framework. If you wish to contribute a level or even an idea; contact Mark Denihan on [[email protected]](/cdn-cgi/l/email-protection). The aim of Security Shepherd’s future development is to create a comprehensive platform for web and mobile application pen testing training / security risk education. Check out the project GitHub and find some issues that you can help with right away.

To contribute right away, pull the source from GitHub

## Other

Both the Security Shepherd Platform and the Mobile Shepherd aspects of this project were initially created as part of BSc degrees in the Dublin Institute of Technology. Thanks to DIT for allowing those projects to be donated to the OWASP community.

## Security Shepherd Road Map

Security Shepherd wants to be as highly usable as we can achieve. Our primary objective is currently to achieve full language localisation support for the entire application. Currently we have covered the main pages users would interact with. We actively need volunteers to take part in the translation process. If you are interested in getting involved please check out our [GitHub Wiki](http://bit.ly/securityShepherdGithub) describing [How to Add a New Language to Security Shepherd](https://github.com/OWASP/SecurityShepherd/wiki/How-to-Create-a-Web-Shepherd-Level).

Our long term goals are to cover as many web and mobile application security risks as possible. If you are interested in getting involved in adding levels to Security Shepherd, please check out our [GitHub Wiki](http://bit.ly/securityShepherdGithub) describing [How to Make a Security Shepherd Level](https://github.com/OWASP/SecurityShepherd/wiki/Adding-a-new-Language-to-Shepherd). For the Latest and Greatest short term goals. Please see the [issues page](https://github.com/OWASP/SecurityShepherd/issues) in our GitHub. We use ZenHub Boards to PM.
