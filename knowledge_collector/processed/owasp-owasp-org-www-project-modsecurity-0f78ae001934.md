---
title: OWASP ModSecurity
source: owasp.org
url: https://owasp.org/www-project-modsecurity/
collector: owasp
category: web-security
tags:
- web-security
- modsecurity
- owasp
- request
- waf
date_collected: '2026-07-26T12:43:51.996212Z'
language: unknown
---

# OWASP ModSecurity

ModSecurity is the standard open-source web application firewall (WAF) engine. Originally designed as a module for the Apache HTTP Server, it has evolved to provide HTTP request and response filtering capabilities across a number of different platforms including Apache HTTP Server, Microsoft IIS and Nginx. It is free software released under the Apache license 2.0 and remains the most widespread open source web application firewall engine used by businesses, government organizations, internet service providers and commercial WAF vendors alike.

The OWASP ModSecurity project provides the WAF engine. The engine is usually coupled with [OWASP CRS](https://coreruleset.org), the dominant WAF rule set, that brings protection against HTTP attacks.

### Road Map

The project, started in 2002, is being [transferred from Trustwave](https://www.trustwave.com/en-us/resources/blogs/spiderlabs-blog/trustwave-transfers-modsecurity-custodianship-to-the-open-worldwide-application-security-project/)[to OWASP](https://owasp.org/blog/2024/01/09/ModSecurity.html) in February 2024.

This will bring new life to ModSecurity and foster the creation of a development community around it.

It is one of the tasks of the new OWASP ModSecurity project to define a new road map.

### Communication

The website at [www.modsecurity.org](https://www.modsecurity.org) is in the hands of Trustwave. They plan to hand over the domain and the website in Summer 2024.

Until that happens, this page here will serve as intermediary website of the project.

Communication currently happens on the [#project-modsecurity](https://owasp.slack.com/archives/C069PCXSW12) channel on the OWASP Slack (the channel is public and you can get an invitation to the Slack [here](https://owasp.org/slack/invite)).

# CVEs

This page lists the official CVEs published since OWASP took over ModSecurity from Trustave on Jan 25, 2024, and started it anew as OWASP ModSecurity.

## CVE 2024-1019, 2024-01-30

### ModSecurity v3 WAF bypass (severity HIGH)

### Advisory

ModSecurity / libModSecurity 3.0.0 to 3.0.11 is affected by a WAF bypass for path-based payloads submitted via specially crafted request URLs. ModSecurity v3 decodes percent-encoded characters present in request URLs before it separates the URL path component from the optional query string component. This results in an impedance mismatch versus RFC compliant back-end applications. The vulnerability hides an attack payload in the path component of the URL from WAF rules inspecting it. A back-end may be vulnerable if it uses the path component of request URLs to construct queries. Integrators and users are advised to upgrade to 3.0.12. The ModSecurity v2 release line is not affected by this vulnerability.

### Components affected with numbers

ModSecurity / libModSecurity v3.0.0 - v3.0.11

### Fixed version

ModSecurity / libModSecurity v3.0.12

ModSecurity v2.9.x is not affected by this vulnerability.

### Download

- Source code (tagged release): <https://github.com/owasp-modsecurity/modsecurity/releases/tag/v3.0.12>
- Source code repository: <https://github.com/owasp-modsecurity/ModSecurity>
- Pre-Compiled Packages: <https://modsecurity.digitalwave.hu/>

Please notice that Trustwave Spiderlabs used to sign releases with the personal key of Martin Vierula (
```
F126692E9BA86B3958E73ED2F2FC4E45883BCBA4
```

).

The new OWASP ModSecurity project has created a new key and is now signing releases starting 3.0.12 with the key
```
0B2BA1924065B44691202A2AD286E022149F0F6E
```

issued to [[email protected]](/cdn-cgi/l/email-protection).

The key is present on most key servers. Here is how you can retrieve it:
```
```
$ gpg --keyserver keyserver.ubuntu.com --recv-key 0B2BA1924065B44691202A2AD286E022149F0F6E```
```

### CVSS 3.1

- **Score : 8.6 HIGH**
- Attack Complexity: low,
- Attack Vector: network,
- Availability Impact: none,
- Confidentiality Impact: none,
- Integrity Impact: high,
- Privileges Required: none,
- scope: changed,
- userInteraction: none,

It can be argued wether the Integrity Impact should be lowered to “medium” instead of “high”. After discussing this with our CNA NCSC Switzerland, we concluded to put it on “high”. If set to “medium”, the score drops to a “medium” level.

### CWE and CAPEC

- CWE-20: Improper Input Validation
- CAPEC-152: Inject Unexpected Items

In both taxonomies, CWE and CAPEC, we assigned very broad categories. None of the more detailed categories were really spot on.

### Official CVE listing

<https://nvd.nist.gov/vuln/detail/CVE-2024-1019>

### Longer description

The [OWASP CRS](https://coreruleset.org) team has discovered an unexpected behavior that can lead to a bypass in the [ModSecurity](https://owasp.org/www-project-modsecurity/) v3 release line (also known as libModSecurity).

For a given HTTP request, ModSecurity3 performs URL decoding on the request URL. For example, the percent-encoded character sequence “%3F” is decoded into a question mark character, “?”. ModSecurity later separates the URL path component from the optional query component, allowing for subsequent rule-based inspection of the path in isolation. ModSecurity performs this separation at the first question mark character encountered in the decoded URL as “?” denotes the start of the query component. Crucially, ModSecurity3 performs the URL decoding step before the URL path separation step.

It is thus possible for an attacker to craft a request URL that contains a percent-encoded question mark character (“
```
%3F
```

”) to trick ModSecurity into separating the URL into a path component at a position of the attacker’s choosing. This allows an attacker to place a payload in the path of a request URL following a “
```
%3F
```

” character sequence in order to bypass the scrutiny of all rules intended to inspect the URL path component. This is further facilitated by the fact, that the part after the “
```
%3F
```

” is not appearing as part of the
```
QUERY_STRING
```

variable.

The ModSecurity variables
```
REQUEST_FILENAME
```

and
```
REQUEST_BASENAME
```

are affected as these variables are intended to hold the URL path, in full or in part, for inspection. ModSecurity rules that inspect or make use of these variables are affected and may be rendered ineffective against exploits of this vulnerability. This includes a significant number of rules in OWASP CRS.

### The fix: Following the correct order of operations

Referring to the relevant RFC governing the use of URIs ([RFC 3986](https://datatracker.ietf.org/doc/html/rfc3986)) reveals that this is a known hazard. The RFC [explicitly states](https://datatracker.ietf.org/doc/html/rfc3986#section-2.4) that a URI must be separated into its component parts before performing URL decoding in order to avoid mistaking an encoded character for a component delimiter.

The fix was to modify the ModSecurity3 function that processes a request URI. The URL is now separated into its components before URL decoding is performed, removing the possibility of ModSecurity3 mistakenly using an incorrect delimiter character.

### Example bypass

Consider sending an HTTP request with the following URL, which includes an SQL injection payload in the path:
```
```
example.com/admin/id/1%3F+OR+1=1--```
```

ModSecurity would perform URL decoding, which gives:
```
```
example.com/admin/id/1?+OR+1=1--```
```

The appearance of a newly decoded question mark character tricks ModSecurity3 into believing that a query component is now present. ModSecurity3 now separates the URL path component from what it believes is a query component and sets the path-related variables like so:
```
```
REQUEST_FILENAME: /admin/id/1
REQUEST_BASENAME: 1```
```

The SQLi payload is no longer present, despite being a valid part of the URL path. The payload will bypass the detection of rules that rely on inspecting ModSecurity3’s URL path variables. Unfortunately, the payload is also not visible as part of the
```
QUERY_STRING
```

variable.

As demonstrated, this is a serious issue and ModSecurity v3 users are strongly encouraged to update to the fixed release (v3.0.12) as soon as is practical.

### Workaround

While upgrading to receive the fix is strongly encouraged, if upgrading the ModSecurity engine is impossible for some reason then a workaround can be implemented.

ModSecurity3’s
```
REQUEST_URI_RAW
```

variable contains the full URI and is unaffected by the URL decoding step. Comparing it to the path-related variables from the previous example, the raw URI variable looks like so:
```
```
REQUEST_URI_RAW: /admin/id/1%3F+OR+1=1--
REQUEST_FILENAME: /admin/id/1
REQUEST_BASENAME: 1```
```

As such, it is possible to use the
```
REQUEST_URI_RAW
```

variable to derive all other required variables correctly, including performing any required URL decoding. Note that the raw URI variable also includes the query component, if present, and so can be cumbersome and difficult to use.

Implementing such a workaround is likely to generate many new false positives with existing rules. For ModSecurity3 users, performing an engine update to receive the fix is likely to be a much more preferable and simpler solution.

### Exploitability

As with every WAF bypass, it takes an additional vulnerability in the back-end application for a successful attack. If the backend application uses path components as query parameters as is likely the case for an application with a layout as in the example presented under “Example Bypass”, then the application may be affected. This can be the case for SQL queries (SQL injection), but also an exploit via a Remote Command Execution (RCE) is possible in a similar constellation.

Again, the back-end must neglect input validation in order for this exploit to work out, but the additional security usually gained from a well-configured WAF is gone with this bypass.

### Timeline

*The timeline comes with a twist. Trustwave transferred the ModSecurity project to OWASP during the window between report and release of the fix. This means that the reporting organization became the new steward of the open source software in question before a fix was released by Trustwave. More to the point: OWASP CRS reported the problem and OWASP recruited the new OWASP ModSecurity team out of the OWASP CRS team.*

- 2023-11-13 : OWASP CRS submits report to Trustwave Spiderlabs, includes SQLi proof of concept
- 2023-11-14 : Trustwave Spiderlabs acknowledges report, promises investigation
- 2023-11-28 : OWASP CRS asks for update
- 2023-11-29 : Trustwave Spiderlabs rejects report, describes it as anomaly without security impact and links to [previous report](https://github.com/owasp-modsecurity/ModSecurity/issues/2705)
- 2023-12-01 : OWASP CRS reiterates previously shared SQLi proof of concept
- 2023-12-01 : Trustwave Spiderlabs acknowledges security impact
- 2023-12-04 : OWASP CRS shares XSS proof of concept
- 2023-12-07 : Trustwave Spiderlabs promises security release early in the new year
- 2024-01-02 : OWASP CRS asks for update
- 2024-01-03 : Trustwave Spiderlabs announces preview patch by Jan 12, release in the week of Jan 22
- 2024-01-12 : Trustwave Spiderlabs shares preview patch with primary contact from OWASP CRS
- 2024-01-22 : OWASP CRS confirms preview patch fixes vulnerability
- 2024-01-24 : Trustwave Spiderlabs announces transfer of ModSecurity project to OWASP for 2024-01-25
- 2024-01-25 : Trustwave Spiderlabs transfers ModSecurity repository to OWASP
- 2024-01-25 : OWASP creates OWASP ModSecurity, assigns OWASP ModSecurity production level, primary contact from OWASP CRS becomes OWASP ModSecurity co-lead
- 2024-01-26 : OWASP ModSecurity leaders decide to release on 2023-01-30
- 2024-01-27 : OWASP ModSecurity creates GPG to sign upcoming release
- 2024-01-29 : NCSC-CH assigns CVE 2024-1019, advisory text and release notes are being prepared, planned release procedure is discussed with Trustwave Spiderlabs
- 2024-01-30 : OWASP ModSecurity Release 3.0.12

### Reporters

- Andrea Menin [@AndreaTheMiddle](https://twitter.com/AndreaTheMiddle)<https://github.com/theMiddleBlue>
- Matteo Pace [@M4tteoP](https://twitter.com/M4tteoP)<https://github.com/M4tteoP>
- Max Leske <https://github.com/theseion>
- Ervin Hegedüs [@Airween](https://twitter.com/airween)<https://github.com/airween>(primary contact)

### Acknowledgements

The OWASP ModSecurity team thanks the wider OWASP CRS team for their patience. Unfortunately, this fix took far longer than it should. We also thank Trustwave Spiderlabs, namely Martin Vierula, for the patch for this issue and the support with the release process. Harold Blankenship from OWASP Headquarters overlooked the transfer of ModSecurity and helped with the timely setup of a new OWASP project and GitHub organization. The OWASP project committee around Björn Kimminich fast tracked OWASP ModSecurity to production level. And finally NCSC-CH that supported us with the CVE process substantially. More than anything, Open Source Software is a team effort. Thank you all.

### Links

- [Blog Post](https://blog.sicuranext.com/modsecurity-path-confusion-bugs-bypass/)explaining the situation where ModSecurity v2 installations may be affected by a similar problem.

## Endorsements of the New OWASP ModSecurity Project

The fresh start for ModSecurity with a new team and under the roof of the OWASP foundation was welcomed by many, many important people in the security community.

Here are a few statements that endorse the new project and the plans.

### Jim Manico, Author, Speaker, Advocate

### Ivan Ristić, Original Author of ModSecurity

### Ryan Barnett, Former ModSecurity Leader

### Felipe ‘Zimmerle’ Costa, Former ModSecurity Head Developer

### Chaim Sanders, Former Leader of OWASP ModSecurity Core Rule Set

## A Message From the New OWASP ModSecurity Leadership Team

*2024-01-26*

OWASP HQ has approved the intermediate leadership team for OWASP ModSecurity. We say intermediate, because the plan is to bring the community together in the 2nd quarter of 2024 and create a new leadership team. This can be the same people or a new crew, but it’s going to be a team where the community has a say.

But during the setup phase of the new OWASP ModSecurity project, there is no time for long discussions, though. Better get moving fast.

So here is the team of three OWASP ModSecurity Co-Leads for the time being:

**Ervin Hegedüs** from Digitalwave in Hungary is a C/C++ developer and long
standing contributor to OWASP CRS. He knows the ModSecurity2 and the
libModSecurity3 code base and he contributed several pull requests to the
project. He is also providing ModSecurity packages on
https://modsecurity.digitalwave.hu/, a very popular service and he is official
maintainer for ModSecurity and CRS on Debian and Ubuntu.

Digitalwave.hu is a small service provider in Hungary. They are planning to invest into ModSecurity given the new situation of the project. Expect more news in coming weeks.

For the near future, Ervin will primarily focus on coordinating the libModSecurity3 development and the development of the related connectors.

**Marc Stern** from Approach-Cyber in Belgium is a long term ModSecurity
contributor with literally dozens of open pull requests on GitHub.
Interestingly, he is not active in the CRS community, so he contributes with a
perspective of somebody using a custom rule set that is embedded in a complex
management framework complementing the CRS capabilities. We think this
non-CRS perspective is an important counter weight.

Approach-Cyber is a mid-sized security service provider from Belgium with offices in Belgium and - lately - Switzerland. Approach-Cyber has a very strong ModSecurity offering and custom extension development starting as early as 2003. They apparently see ModSecurity as strategic for their offering with the board backing Marc’s investment into the code base.

Approach plans to contribute code that improves the software in the following areas:

- Stability
- Consistency
- Performance
- Orthogonality
- Genericity

So clearly for a quality improvement of the code base.

For the near future, Marc will primarily focus on coordinating the ModSecurity2 development.

**Christian Folini** from netnea.com in Switzerland is a long term ModSecurity
user and OWASP CRS co-leader with a lot of experience with community building
and project governance. He contributed very little to the ModSecurity code
base, but he wrote the 2nd edition of the quasi official ModSecurity Handbook
with original author Ivan Ristić. Christian is a well known teacher on the
subject and a long standing figure in the ModSecurity / CRS community as well
as the OWASP community, that he joined 15+ years ago.

Netnea.com is a small Swiss consulting company focusing on network monitoring and application security.

For the near future, Christian will primarily focus on project coordination, communication, documentation and administration. Christian plans to give up his leadership position at said community meeting Spring 2024.

As you can see, we bring a lot of experience and credibility to the table. We know what we are doing and we welcome this frest start for ModSecurity with open arms.

We tried to balance CRS with non-CRS interests and we tried to bring in a non-OWASP person (-> Marc) into the team as well. We are all working for small and mid-sized companies, definitely not big tech or startups with a need for fast money. So we do this, because it’s the right thing to do.

Let’s get going!

Ervin, Marc and Christian

## News From the OWASP ModSecurity Project

The following is a lose collection of news and status reports since OWASP took over the project in Jan 2024.

### Status 2024-02-23

- We had more discussions about code, bug reports and improvements. Given we are seeking to build a new development company, this is a very good sign and deserves the top priority.
- With 3 open source SecLang implementations (ModSec v2, ModSec v3, Coraza), there is a growing need to coordinate the behavior, namely with implementation differences and new features. OWASP ModSecurity has proposed a SecLang round table and invited several stakeholders (Coraza and several rules projects) to discuss a pending problem. This meeting will happen in the coming weeks.
- Original author of ModSecurity, Ivan Ristić, presented at the OWASP London 20 years anniversary event about 22 years of ModSecurity. [Link to video](https://www.youtube.com/watch?v=SbAVBQODDR0&t=3592s)

### Status 2024-02-16

- We had to roll back several commits on v2. This brought us to the conclusion we need CI/CD in place before we merge anything.
- So Ervin has set up a minimal CI/CD environment and development picked up again.
- We have established minimal review process that involves either Marc or Ervin signing off any pull request before merging for the time being.
- Technical discussions with more participants have started on Slack and on Github. Apparently a good sign.
- Christian did a presentation around OWASP ModSecurity, history, status, plans and an OWASP perspective for OWASP Netherlands. Recording will be published soon.
- OWASP CRS has released CRS 4. This includes a plugin functionality but more importantly for ModSecurity, it no longer depends on PCRE.

### Status 2024-02-04

- The first release under new management: 3.0.12. Given Trustwave handed over the repo with the fix for CVE-2024-1019 scheduled but not released, we had to get going very fast.
- The day after the release, a blog post went up that explains a different behavior in v2 and v3. It is in an area close to the CVE we fixed. We’ll have to sort this out.
- ModSecurity development has started again and Marc has merged a few PRs that have been open for quite some time. One of them addressed longstanding problem with t:cmdLine (PR 3051).
- More talks with commercial integrators.

### Status 2024-01-26

- Trustwave has transferred the ModSecurity repo to https://github.com/owasp-modsecurity/ModSecurity.
- The OWASP.org page at https://owasp.org/www-project-modsecurity/ has been launched.
- OWASP has confirmed the new intermediary leadership team: Ervin Hegedüs, Marc Stern and Christian Folini. A portrait of them is on the owasp.org page of the project.
- The OWASP project committee has promoted OWASP ModSecurity to production level. While this is only an administrative status, there is symbolic value in the promotion.
- Trustwave has handed over the Twitter (X) account to OWASP. Ervin and Christian are delegates on the account.
- Trustwave did not release the previously announced security fix for ModSecurity3. Instead, they have asked OWASP ModSecurity execute the release with their assistance. We are now aiming for Jan 29 / 30. (this came a bit out of the blue for us)
- Contact with an additional ModSecurity integrator established.

### Status 2024-01-19

- Trustwave has shared the patch for the upcoming ModSecurity3 security release with Ervin. He tested it and it looks good. Expect a release on Monday.
- We got two additional endorsements. More are promised and I might ping again.
- There is a vendor who runs ModSec3 with Apache. My contact is currently out skiing but he promised to call me after his return.
- Contact with OWASP project committee established.
- Ivan Ristić shared the trademark identifier for ModSecurity with us. The trademark is currently with Trustwave and OWASP will make sure it’s transferred too.
- We’re still waiting to get the github repo to setup an initial OWASP project page via https://github.com/owasp/project-modsecurity (does not exist yet). We’re getting there, I’m sure.
- We have started to collect a list of ModSecurity vendors and integrators. Two people volunteered to do more research. If you are also able to contribute, then please get in touch.

### Status 2024-01-12

- Talked to 7 people / industry leaders about an endorsement of OWASP ModSecurity
  - Ofer Shezaf promised to write an endorsement on LinkedIn
  - Ryan Barnett tells me to use his twitter statement
- Addressed community via existing communication channels:
  - Trustwave Spiderlabs Blog
  - OWASP Blog
  - ModSecurity Mailinglists
  - Various social media accounts on Twitter / X as well as LinkedIn
  - Christian Folini’s ModSecurity / CRS newsletter sent to 1950 addresses
  - The only thing missing is a tweet by the @ModSecurity twitter account
- Lined up a first podcast appearance, but it will be February or March
- Contact with OWASP project committee initiated (we know the process to become a flagship project now), but no real feedback so far
- We’re making progress with forming a temporary leader team for the project (The idea is to run with a self-appointed leader team during the incubation phase and then let the community form a production leader team in Spring)
- #project-modsecurity channel on Slack established
- Apparently development has not really started, but ModSec3 is planned to get a security release on Jan 22 (bookmark that date, it has at least a medium severity) and Trustwave has asked OWASP to cooperate on that release.
