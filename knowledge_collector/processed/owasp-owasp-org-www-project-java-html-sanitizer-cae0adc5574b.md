---
title: OWASP Java HTML Sanitizer
source: owasp.org
url: https://owasp.org/www-project-java-html-sanitizer/
collector: owasp
category: web-security
tags:
- web-security
- html
- owasp
- sanitizer
- java
date_collected: '2026-07-26T12:44:18.524360Z'
language: unknown
---

# OWASP Java HTML Sanitizer

## What is this?

The OWASP HTML Sanitizer Projects provides Java based HTML sanitization of untrusted HTML!

## About

The OWASP HTML Sanitizer is a fast and easy to configure HTML Sanitizer written in Java which lets you include HTML authored by third-parties in your web application while protecting against XSS. The existing dependencies are on guava and JSR 305. The other jars are only needed by the test suite. The JSR 305 dependency is a compile-only dependency, only needed for annotations. This code was written with security best practices in mind, has an extensive test suite, and has undergone adversarial security review. A great place to get started using the OWASP Java HTML Sanitizer is here: <https://github.com/OWASP/java-html-sanitizer/blob/master/docs/getting_started.md>.

## Benefits

- Very easy to use. It allows for simple programmatic POSITIVE policy configuration (see below). No XML config.
- Actively maintained by Mike Samuel from Google’s AppSec team!
- Passing 95+% of AntiSamy’s unit tests plus many more.
- This is code from the Caja project that was donated by Google. It is rather high performance and low memory utilization.
- Java 1.5+
- Provides 4X the speed of [AntiSamy](https://owasp.org/www-project-antisamy/)sanitization in DOM mode and 2X the speed of AntiSamy in SAX mode.

## Questions

- **How was this project tested?**This code was written with security best practices in mind, has an extensive test suite, and has undergone[adversarial security review](https://github.com/OWASP/java-html-sanitizer/blob/master/docs/attack_review_ground_rules.md).
- **How is this project deployed?**This project is best deployed through[Maven](https://github.com/OWASP/java-html-sanitizer/blob/master/docs/getting_started.md)

## Licensing

The OWASP HTML Sanitizer is free to use and is dual licensed under the [Apache 2 License](http://www.apache.org/licenses/LICENSE-2.0) and the [New BSD License](http://opensource.org/licenses/BSD-3-Clause)..

## Example

Put whatever you like here: news, screenshots, features, supporters, or remove this file and don’t use tabs at all.

## How to Use

The project is available at [OWASP HTML Sanitizer : Maven Central](https://search.maven.org/#search%7Cga%7C1%7Cowasp%20html%20sanitizer)

## Creating a HTML Policy

### 1. Use prepackaged policies

You can view basic prepackaged policies for links, tables, integers, images at:
<https://github.com/OWASP/java-html-sanitizer/blob/master/src/main/java/org/owasp/html/Sanitizers.java>.
```
```
`PolicyFactory policy = Sanitizers.FORMATTING.and(Sanitizers.LINKS);`
`String safeHTML = policy.sanitize(untrustedHTML);````
```

### 2. Configure own policy

Check the tests on how to configure your own policy at:
<https://github.com/OWASP/java-html-sanitizer/blob/master/src/test/java/org/owasp/html/HtmlPolicyBuilderTest.java>
```
```
`PolicyFactory policy = new HtmlPolicyBuilder()`
`   .allowElements("a")`
`   .allowUrlProtocols("https")`
`   .allowAttributes("href").onElements("a")`
`   .requireRelNofollowOnLinks()`
`   .build();`
`String safeHTML = policy.sanitize(untrustedHTML);````
```

### 3. Define custom policies

You can write custom policies :
```
```
`PolicyFactory policy = new HtmlPolicyBuilder()`
`   .allowElements("p")`
`   .allowElements(`
`       new ElementPolicy() {`
`         public String apply(String elementName, List`<String>` attrs) {`
`           attrs.add("class");`
`           attrs.add("header-" + elementName);`
`           return "div";`
    `         }`
`       }, "h1", "h2", "h3", "h4", "h5", "h6"))`
`   .build();`
`String safeHTML = policy.sanitize(untrustedHTML);````
```

Please note that the elements “a”, “font”, “img”, “input” and “span” need to be explicitly whitelisted using the `allowWithoutAttributes()` method if you want them to be allowed through the filter when these elements do not include any attributes.

### 4. Use ebay / slashdot policies

You can also use the default “[ebay](https://github.com/OWASP/java-html-sanitizer/blob/master/src/main/java/org/owasp/html/examples/EbayPolicyExample.java)” and “slashdot” policies.

The [Slashdot policy](https://github.com/OWASP/java-html-sanitizer/blob/master/src/main/java/org/owasp/html/examples/SlashdotPolicyExample.java) allows the following tags (“a”, “p”, “div”, “i”, “b”, “em”, “blockquote”, “tt”, “strong”n “br”, “ul”, “ol”, “li”) and only certain attributes.
This policy also allows for the custom slashdot tags,”quote” and “ecode”.

### CSS Sanitization

CSS sanitization is challenging.

We disallow position:sticky and position:fixed so that client code can use a position:relative;overflow:hidden to contain self-styling sanitized snippets. Embedders of sanitized content do have to consistently do that and make sure that contributed content is clearly demarcated.

Most CSS attacks require a payload to specify selectors which the sanitizer should not allow. Unproxied images do allow tracking and, by positioning below the fold, can track whether a user scrolls down. Embedders do need to use URL rewriting if they allow background styling and use sensible Referrer-Policy and related headers.

That said, even if care is taken, CSS has a large attack surface, so not using it puts you in a safer place.

### Inline/Embedded Images

Inline images use the data URI scheme to embed images directly within web pages. The following describes how to allow inline images in an HTML Sanitizer policy.

1) Add the “data” protocol do your whitelist. Se example [how to add “data” protocol.](https://www.javadoc.io/doc/com.googlecode.owasp-java-html-sanitizer/owasp-java-html-sanitizer/20160628.1/org/owasp/html/HtmlPolicyBuilder.html#allowUrlProtocols-java.lang.String...-)
```
```
`.allowUrlProtocols("data")````
```

2) You can then allow an attribute with an extra check thus
```
```
`.allowAttributes("src")`
`.matching(...)`
`.onElements("img")````
```

3) There are a number of things you can do in the matching part such as allow the following instead of just allowing data.

4) Since allowUrlProtocols(“data”) allows data URLs anywhere data URLs are allowed, you might want to also add a matcher to any other URL attributes that reject anything with a colon that does not start with http: or https: or mailto:
```
```
`.allowAttributes("href")`
`.matching(...)`
`.onElements("a")````
```

## News and Events

- [18 Oct 2021] v20211018.2 Released - addresses issue with <select> elements
- [10 Sep 2020] Migrate OWASP wiki page
- [20 Feb 2018] Update 20180219.1 - addresses iOS/MacOS “text bomb”
- [28 June 2016] v20160628.1 Released
- [14 Apr 2016] v20160413.1 Released
- [1 May 2015] Move to GitHub
- [2 July 2014] v239 Released
- [3 Mar 2014] v226 Released
- [5 Feb 2014] New Wiki
- [4 Sept 2013] v209 Released

## Roadmap

- Maintaining a fully featured HTML sanitizer is a lot of work. We intend to continue to handle community questions and bug reports in a very timely manner.
- There are no plans for major new features other than supporting incoming requests for advanced sanitization such as additional HTML5 support.
