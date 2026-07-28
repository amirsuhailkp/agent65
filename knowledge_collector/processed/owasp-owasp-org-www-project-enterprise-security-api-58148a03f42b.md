---
title: OWASP Enterprise Security API ESAPI
source: owasp.org
url: https://owasp.org/www-project-enterprise-security-api/
collector: owasp
category: web-security
tags:
- web-security
- esapi
- security
- java
- owasp
date_collected: '2026-07-26T12:44:12.357709Z'
language: unknown
---

# OWASP Enterprise Security API (ESAPI)

## What is ESAPI?

ESAPI (The OWASP Enterprise Security API) is a free, open source, web application security control library that makes it easier for programmers to write lower-risk applications. The ESAPI libraries are designed to make it easier for programmers to retrofit security into existing applications. The ESAPI libraries also serve as a solid foundation for new development.

Allowing for language-specific differences, all OWASP ESAPI versions have the same basic design:

- **There is a set of security control interfaces.**They define for example types of parameters that are passed to types of security controls.
- **There is a reference implementation for each security control.**The logic is not organization‐specific and the logic is not application‐specific. An example: string‐based input validation. (Note that some of the reference implementations are simply “toy” examples to illustrate how to implement a specific interface [e.g., ESAPI for Java’s
  ```
  org.owasp.esapi.reference.FileBasedAuthenticator
  ```

  ] whereas others are full-fledged enterprise ready reference implementations [e.g.,
  ```
  org.owasp.esapi.reference.DefaultEncoder
  ```

  or
  ```
  org.owasp.esapi.reference.DefaultValidator
  ```

  ].)
- **There are optionally your own implementations for each security control.**There may be application logic contained in these classes which may be developed by or for your organization. An example: enterprise authentication.

## Downloads

**NOTE** - Use of links to vendor specific ESAPI presentations does not constitute an
endorsement of that vendor by either the OWASP Foundation, nor by ESAPI contributors.

### About ESAPI

- Data sheet - [PDF](https://owasp.org/www-pdf-archive/Esapi-datasheet.pdf),[Word](http://wiki.owasp.org/images/3/32/Esapi-datasheet.doc)
- Project presentation [Slide deck](https://www.denimgroup.com/media/pdfs/DenimGroup_ESAPI_SATJUG_20100603.pdf)
- Video presentations – [YouTube videos on ESAPI](https://www.youtube.com/results?search_query=OWASP+ESAPI)

### Get ESAPI

- [ESAPI for Java Downloads (binaries)](https://search.maven.org/#search%7Cga%7C1%7Cesapi)
- [ESAPI for Java (source)](https://github.com/ESAPI/esapi-java-legacy)
- **DEPRECATED**-[ESAPI for JavaScript](https://github.com/ESAPI/owasp-esapi-js)
- [ESAPI for NodeJS](https://github.com/ESAPI/node-esapi)- a minimal port of “ESAPI for JavaScript” for use with Node.js

#### Unsupported versions

The following flavors of ESAPI are no longer supported by OWASP. If you absolutely need to download one of those, it is suggested that you search the [Internet Archive Wayback Machine](https://archive.org/) or perhaps [GitHub](https://github.com/) for someone who may have mirrored it:

- ESAPI for .NET
- ESAPI for Classic ASP
- ESAPI for PHP
- ESAPI for ColdFusion & CFML (May still be supported by Adobe; also appears to be mirrored [here](https://github.com/damonmiller/esapi4cf)on GitHub.)
- ESAPI for Python

### Learn ESAPI

- ESAPI design patterns (not language-specific): [PDF](http://wiki.owasp.org/images/8/82/Esapi-design-patterns.pdf),[Word](http://wiki.owasp.org/index.php/File:Esapi-design-patterns.doc),[PPT](http://wiki.owasp.org/images/8/87/Esapi-design-patterns.ppt)
- [ESAPI Swingset](https://wiki.owasp.org/index.php/ESAPI_Swingset)– a sample application that demonstrates how to leverage ESAPI to protect a web application. (Uses ESAPI4Java 1.4.)
- [LAMP should be spelled LAMPE](https://owasp.org/www-pdf-archive/LAMP_Should_be_Spelled_LAMPE.pdf)
- [ESAPI for Java interface documentation (Javadoc)](https://www.javadoc.io/doc/org.owasp.esapi/esapi/latest/index.html)

## What I did with ESAPI

- I used ESAPI for Java with Google AppEngine. I used it for simple validation and encoding. –

  [Jeff](/cdn-cgi/l/email-protection#9df7f8fbfbb3eaf4f1f1f4fcf0eeddf2eafceeedb3f2effa)
- I used ESAPI for PHP with a custom web 2.0 corporate knowledge management application, made up of many open source and commercial applications integrated to work together. I added an organization- and application-specific “Adapter” control to wrap calls to the other ESAPI controls. –

  [Mike](/cdn-cgi/l/email-protection#14797d7f713a767b767166677f7d547b637567643a7b6673)
- I used ESAPI for Java’s “Logger” control to make it easier for a US Government customer to meet C\&A requirements. –

  [Dave](/cdn-cgi/l/email-protection#d9bdb8afbcf7aeb0bab1bcabaa99b6aeb8aaa9f7b6abbe)
- I used ESAPI for Java to build a low risk web application that was over 250,000+ lines of code in size. –

  [Jim](/cdn-cgi/l/email-protection#472d2e2a692a26292e242807283026343769283520)
- I used ESAPI for Java’s “Authenticator” to replace a spaghetti-like mechanism in a legacy financial services web application. In hindsight I should have used the application-specific “Adapter” pattern mentioned by Mike above. The organization also uses the ESAPI Encryptor as an interface to a hardware security module. –

  [Roman](/cdn-cgi/l/email-protection#70021f1d111e5e180503041114300911181f1f5e131f1d)
- I use ESAPI to be our security package for all our product, this way we can set one standard for all products. –

  [Yair](/cdn-cgi/l/email-protection#275e464e5555674b4e51425742555448490944484a)
- I use ESAPI for Java to educate developers about application security principals at several of the world’s largest organizations. –

  [Jim](/cdn-cgi/l/email-protection#9ef4f7f3b0f3fff0f7fdf1def1e9ffedeeb0f1ecf9)

## Should I use ESAPI?

[NOTE: The heretical opinions on this ESAPI tab are 100% my own and do not necessarily reflect the rest of other ESAPI contributors / creators, or the OWASP Foundation staff, leadership, community. –kevin wall]

Or, specifically, “Should I use ESAPI for Java (Legacy)?” since that’s the only one run by OWASP that still shows any semblance of life. While maintenance activities are down compared to ESAPI’s peak development years and there is no new significant functionality planned (although we did recently add support for SLF4J in the ESAPI Logger), it is not completely abandoned as rumor would have it. A few of us are still regularly working on ESAPI and haven’t given up, although we certain could use some additional volunteers to help out. But without additional active contributors, ESAPI makes slow progress in terms of bug fixing.

The first question to ask is, are you already using ESAPI in your project, and if so, do you have a lot vested in it? If so, then the answer to “Should I use ESAPI?” probably is “yes”. The second question you should ask, if I’m using it, why am I not contributing to it in some manner? But we won’t go there. ;-)

### Potential alternatives to ESAPI

If you are starting out on a new project or trying for the first time to
secure an existing project, then *before* you consider ESAPI, you
should consider these possible alternatives:

- Output encoding: [OWASP Java Encoder Project](/www-project-java-encoder)
- General HTML sanitization: [OWASP Java HTML Sanitizer](/www-project-java-html-sanitizer)
- Validation: [JSR-303/JSR-349 Bean Validation](http://beanvalidation.org/)
- Strong cryptography: [Google Tink](https://github.com/google/tink),[Keyczar](https://github.com/google/keyczar)
- Authentication / authorization: [Apache Shiro](https://shiro.apache.org/),[Authentication using Spring Security](https://duckduckgo.com/?q=using+%22spring+security%22+authentication&atb=v203-1&ia=web)
- CSRF protection: [OWASP CSRFGuard Project](/www-project-csrfguard)or[OWASP CSRFProtector Project](/www-project-csrfprotector)

if *might* make sense to use ESAPI if you plan use multiple security controls
provided by ESAPI (e.g., you plan on using an output encoder to prevent XSS,
data validation, HTML sanitization, and safe logging), then ESAPI possibly makes
more sense to use than 3 or 4 other disparate class libraries, which provide but
a single security control. That is an engineering decision your development team
will need to make.

But most (perhaps 90% or more) of the ESAPI use which I have observed was solely
limited to using ESAPI’s Encoder to remediate XSS vulnerabilities. If that is
all that you intend to do with ESAPI, steer clear and use
[OWASP Java Encoder Project](/www-project-java-encoder) instead.

A final note: If you want to use ESAPI for authentication / authorization, keep in mind that ESAPI’s reference implementation of those are “flat file based” and will not scale to enterprise levels. Those 2 reference implementations are more or less intended as 1) instructional models so show fundamental implementation ideas, and 2) provided so we could do unit testing that we otherwise would not be able to accomplishment without some reference implementation. That said, writing a RDBMS implementation or an LDAP implementation should not be rocket science.

### Is ESAPI “safe” to use?

#### A brief history

Note that none of the above recommended alternatives are meant to suggest that ESAPI is dead, but rather to acknowledge the fact that it isn’t being as well-maintained as most F500 companies would like for their enterprise software.

In the past, ESAPI had gathered the reputation that it was not well maintained,
but that’s not the whole story. There were a few of us who were actively
fixing bugs (including updating dependencies), but because no one had
instructions of how to upload a new release to Maven Central, we couldn’t make
official releases available to the public unless they were willing to get them
from our GitHub ‘develop’ branch where the fixes were being applied. Despite
me pleading for help, none arrived until 2Q-2019. Since that time, there have
been 7 *official* releases (see https://mvnrepository.com/artifact/org.owasp.esapi/esapi
for a complete list).

#### Concerns about vulnerable ESAPI dependencies are usually over-hyped

Despite that, I still see objections that the ESAPI development team is still not responsive enough to new vulnerabilities discovered in its dependencies. Let me respond to that.

- I get security alerts from both Snyk and GitHub as well as regularly using OWASP Dependency Check in our build process to stay on top of vulnerabilities in library dependencies. In addition, the ever astute ESAPI user community regularly emails the ESAPI co-leaders notices of new CVEs that might affect ESAPI.
- When I become aware of a new CVE in an ESAPI dependency, whether that it is in a direct or transitive dependency, I attempt to research it to see if it leads to an *exploitable*path to those using ESAPI. Usually that means digging through the source code of the affected dependency and looking at the commits that fixed the problem. As it turns out, vulnerabilities in ESAPI dependencies rarely to lead to exploitable paths via ESAPI, but if it does, the ESAPI team discusses it, and either upgrades or prepares a workaround. And if that is not possible, we will put usually will put out an announcement on our Google groups mailing lists and prepare a security bulletin, such as this[one](https://github.com/ESAPI/esapi-java-legacy/blob/develop/documentation/ESAPI-security-bulletin2.pdf)for CVE-2019-17571 in Log4J 1.x.
- If users of ESAPI are overly concerned, then can generally edit their Maven or Gradle, etc. configuration file to exclude the vulnerable dependency and use an updated one that has patched whatever CVE. This does not require a Ph.D. in quantum physics; any developer with a clue (or knowing how to use Stack Overflow :) ought to be able to figure this out. There may be some rare cases where this is not possible and breaks their tests, but if that is the case, it means that ESAPI generally would not be able to upgrade either. (Note because ESAPI currently has a minimal baseline dependency of Java 7, there are times when we cannot upgrade to later versions of dependencies because they require Java 8 or later. That is rare, but could happen. Of course, if your application is stuck using Java 7, then CVEs in ESAPI dependencies probably should be the least of your worries.)

#### If you are still concerned about support…

There used to be, and probably still are, companies from which you can purchase ESAPI support. I am not going to list such companies here in order to remain vendor neutral. If you are searching for, and unable to locate, one, then contact me privately via email and I will provide you with a few pointers.

### So why then are you against recommending ESAPI?

At one point when I originally created this ‘tab’ on the OWASP ESAPI ‘wiki’, my primary motivation of recommending other security alternatives to ESAPI was indeed because I felt that we could not adequately support it because I had not yet figured out how to do a release, but having now done a couple of releases to Maven Central and having written down detailed documentation, that is no longer my concern for recommending alternatives.

So if not that, then why steer people clear of ESAPI 2.x? Glad you asked. There are two primary reasons:

- ESAPI’s monolithic architecture means that your project will probably unnecessarily pull in lots of dependencies that are not actually needed, which in turn leads to more bloated application deployments. Maybe that’s not an issue everywhere, especially if your application war file is in the GB range, but I grew up in the day when Bill Gates told us that 640Kb ought to be enough RAM for anybody and I foolishly believed him. Given that the latest ESAPI jar is a tad over 450Kb, that doesn’t leave much room for its dependent jars, much less for the rest of your application. :) So, in part, its a personal crusade against software bloat.
- It is going to be a difficult path forward to ESAPI 3 for those applications using ESAPI 2.x. To decouple things and be able to package major functionality into separate ESAPI jars (for instance, there likely will be an esapi3-core jar and an esapi3-encoder jar, etc.), we likely will break some existing interfaces. We won’t do that intentionally, but the main goal will not be to preserve backward compatibility. The fact of the matter is, I don’t think any of the active ESAPI 2.x contributors wants to spend their time on mailing lists or Stack Overflow or at their companies advising application development teams on the best way of migrating from ESAPI 2.x to ESAPI 3. So the less projects that are on ESAPI 2 now, the better it will be for us when ESAPI 3 finally does arrive. It’s somewhat of a selfish reason, but application developers themselves should be selfish in the same sense about the future maintainability of their code. We certainly will not needlessly (at least as I’m a project co-lead) deviate from the ESAPI 2.x interfaces and its current semantic behavior, but at this point, I cannot promise anything. I personally think many of the current ESAPI 2 interfaces are too bloated and confusing and need to be “broken apart” because the current structure ultimately leads to confusion on the part of developers and is an impediment to learning the ESAPI SDK. Therefore we will, in fact, not be hesitant to change such things. In the end, the transition from ESAPI 2 to ESAPI 3 may be easy, but it almost certainly will NOT be seamless and could end up being a royal PITA, much like the transition from Struts 1 to Struts 2. No promises at this point.

### Closing thoughts

It is not a perfect world that we live in, but I would be remiss as an AppSec guy if I were to plug ESAPI over other good security solutions simply because of my contributions to / involvement with ESAPI. I think that ESAPI has its place and I will do my best to maintain it, but not to the exclusion of my family or day job and I don’t expect that of the other ESAPI contributors either. However, if you would like to volunteer to help, you know where to find me.

-[Kevin W. Wall](/cdn-cgi/l/email-protection#660d03100f0848114811070a0a26010b070f0a4805090b), ESAPI project co-lead
(last updated July 2020)

## Glossary

**ESAPI Terminology**

- **adapter**- There are optionally your own implementations for each security control. There may be application logic contained in these classes which may be developed by or for your organization. The logic may be organization-specific and/or application-specific. There may be proprietary information or logic contained in these classes which may be developed by or for your organization.
- **built-in singleton design pattern**- The “built-in” singleton design pattern refers to the replacement of security control reference implementations with your own implementations. ESAPI interfaces are otherwise left intact.
- **codec**- ESAPI encoder/decoder reference implementations.
- **core**- The ESAPI interfaces and reference implementations that are not intended to be replaced with enterprise-specific versions are called the ESAPI Core.
- **encoder**- Interfaces and implementation classes that perform some sort of output encoding, whether as a defense against XSS or to do base64 encoding, etc.
- **exception**- ESAPI exception reference implementations.
- **extended factory design pattern**- The “extended” factory design pattern refers to the addition of a new security control interface and corresponding implementation, which in turn calls ESAPI security control reference implementations and/or security control reference implementations that were replaced with your own implementations. The ESAPI locator class would be called in order to retrieve a singleton instance of your new security control, which in turn would call ESAPI security control reference implementations and/or security control reference implementations that were replaced with your own implementations.
- **extended singleton design pattern**- The “extended” singleton pattern refers to the replacement of security control reference implementations with your own implementations and the addition/modification/subtraction of corresponding security control interfaces.
- **ES-enable (or ESAPI-enable)**- Just as web applications and web services can be Public Key Infrastructure (PKI) enabled (PK-enabled) to perform for example certificate-based authentication, applications and services can be OWASP ESAPI-enabled (ES-enabled) to enable applications and services to protect themselves from attackers.
- **filter**- In ESAPI for Java, there is additionally an HTTP filter that can be called separately from the other controls.
- **interfaces**- There is a set of security control interfaces. There is no application logic contained in these interfaces. They define for example types of parameters that are passed to types of security controls. There is no proprietary information or logic contained in these interfaces.
- **locator**- The ESAPI security control interfaces include an “ESAPI” class that is commonly referred to as a “locator” class. The ESAPI locator class is called in order to retrieve singleton instances of individual security controls, which are then called in order to perform security checks (such as performing an access control check) or that result in security effects (such as generating an audit record).
- **safe logging**– ESAPI’s attempt to sanitize log output as a defense against Log Forging attacks.
- **reference implementation**- There is a reference implementation for each security control. There is application logic contained in these classes, i.e. contained in these interface implementations. However, the logic is not organization-specific and the logic is not application-specific. There is no proprietary information or logic contained in these reference implementation classes.
- **validator**- An interface or implementation class that does some sort of data validation, usually via an accept-list or regular expression. ESAPI validators also often handle canonicalization of input before the actual data validation is performed.
- **Web Application Firewall (WAF)**- In ESAPI for Java, there is additionally a Web Application Firewall (WAF) that can be called separately from the other controls.

## OWASP ESAPI for Java EE

### Release Info

- Current release: 2.7.0.0 - June 2, 2025 [(download)](https://mvnrepository.com/artifact/org.owasp.esapi/esapi/2.7.0.0)
- Release notes: [2.7.0.0 release notes](https://github.com/ESAPI/esapi-java-legacy/blob/develop/documentation/esapi4java-core-2.7.0.0-release-notes.txt)

### Summary

**Purpose:** This is the Java EE language version of OWASP ESAPI. The ESAPI for Java EE is the baseline ESAPI design.

- The current release of this project is suitable for production use. It now requires Java 8 or later to use.
- The ESAPI 2.x branch supports Java 5 and above, but the releases 2.2.0.0 and later require **Java 7**or later. Note that release 2.3.0.0 was be the**last**release to support Java 7. Thereafter, Java 8 will be the minimal supported JDK.
- You may view the Javadocs here https://www.javadoc.io/doc/org.owasp.esapi/esapi/latest/index.html
- The unsupported ESAPI 1.4 branch supports Java 4 and above. Complete information on latest 1.4 branch dependencies can be found here http://owasp-esapi-java.googlecode.com/svn/trunk\_doc/1.4.4/site/dependencies.html. (Google may have removed this though, so you may have to search for it on the [Internet Wayback Machine](https://archive.org/).)
- The OWASP AppSensor-ESAPI integration guide is out! See [AppSensor\_GettingStarted](https://wiki.owasp.org/index.php/AppSensor_GettingStarted)for details.

## Project Details

- **ESAPI for Java**: Work for ESAPI 3.0 is still in the early planning stages and ESAPI 2.x is in maintenance / bug-fix mode (i.e., no new features will be added). Unless you are legacy project that is already using ESAPI, you are highly encouraged to read the[“Should I Use ESAPI”](/www-project-enterprise-security-api#div-shouldiuseesapi)tab.
- **ESAPI for JavaScript**:**DEPRECATED**- No longer supported; use at your own risk. See the associated[README.md](https://github.com/ESAPI/owasp-esapi-js/blob/master/README.md)file for details.
- **ESAPI for Node**: Only one outstanding issue, but no known vulnerabile dependencies.
