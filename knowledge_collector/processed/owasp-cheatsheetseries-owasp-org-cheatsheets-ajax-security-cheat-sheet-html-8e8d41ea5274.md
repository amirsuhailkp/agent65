---
title: AJAX Security Cheat Sheet¶
source: cheatsheetseries.owasp.org
url: https://cheatsheetseries.owasp.org/cheatsheets/AJAX_Security_Cheat_Sheet.html
collector: owasp
category: web-security
tags:
- web-security
- use
- security
- user
- json
date_collected: '2026-07-26T12:36:07.175062Z'
language: unknown
---

# AJAX Security Cheat Sheet[¶](#ajax-security-cheat-sheet)

## Introduction[¶](#introduction)

This document will provide a starting point for AJAX security and will hopefully be updated and expanded reasonably often to provide more detailed information about specific frameworks and technologies.

**Before applying any specific control, developers must adopt a fundamental security mindset:**
All data should be considered untrusted unless explicitly validated and safely handled.
This applies to:

- Client-side input
- API response
- Third-party integrations
- Internal services and microservices
- Cached responses
- Browser storage (localStorage, sessionStorage)
- Hidden form fields

### Client-Side (JavaScript)[¶](#client-side-javascript)

#### Use ``` innerHTML ``` with extreme caution[¶](#use-innerhtml-with-extreme-caution)

Manipulating the Document Object Model (DOM) is common in web applications, especially in monolithic server-side rendering (e.g., PHP, ASP.NET) and AJAX-driven applications. While
```
innerHTML
```

seems like a convenient way to inject HTML content, it poses significant security risks on untrusted-data, particularly cross-site scripting (XSS).

##### What is ``` innerHTML ``` ?[¶](#what-is-innerhtml)

The
```
innerHTML
```

property sets or gets the HTML content of an element, including tags, which the browser parses and renders as part of the DOM. For example, setting
```
innerHTML = "<p>Hello</p>"
```

creates a paragraph element.

##### Why does ``` innerHTML ``` require extreme caution?[¶](#why-does-innerhtml-require-extreme-caution)

Using
```
innerHTML
```

with untrusted data (e.g., from API responses in AJAX) can allow malicious JavaScript to execute in the user’s browser, leading to XSS vulnerabilities. Potential risks include:

- Stealing user session cookies.
- Defacing the website.
- Redirecting users to malicious sites.
- Performing unauthorized actions (e.g., API calls on behalf of the user).
- Keylogging user inputs.

###### Vulnerable Example[¶](#vulnerable-example)
```
```
    // DANGER! The server may have returned a payload that executes scripts, for example: <img src=abc onerror=alert('xss!')>.```
```

##### When is ``` innerHTML ``` acceptable?[¶](#when-is-innerhtml-acceptable)

The fundamental security rule is to never use innerHTML with untrusted data. However, in limited cases, such as legacy monolithic applications with no viable alternatives, innerHTML may be used cautiously:

- **Static, Hardcoded HTML**: For small, fixed HTML snippets that are part of your application’s source code and contain no user input:
```
```
```
```

- **Sanitized HTML**: For user-generated HTML (e.g., in rich text editors), sanitize with a library like[DOMPurify](DOM_Clobbering_Prevention_Cheat_Sheet.html#1-html-sanitization)before using innerHTML:
```
```
import DOMPurify from 'dompurify';
const userInput = '<img src=abc onerror=alert("xss")>';```
```

##### Alternatives[¶](#alternatives)

- Use Templating Engines (with auto-escaping) for reusable, structured HTML snippets.
- Use Modern Frameworks (React, Vue, Angular, Svelte) for complex applications. They standardize DOM manipulation, provide reactivity, and inherently handle sanitization for dynamic data. However, developers must avoid unsafe APIs (e.g.,
  ```
  dangerouslySetInnerHTML
  ```

  in React,
  ```
  [innerHTML]
  ```

  in Angular) to prevent XSS vulnerabilities.

#### Use of ``` textContent ``` or ``` innerText ``` for DOM updates (for text-only content)[¶](#use-of-textcontent-or-innertext-for-dom-updates-for-text-only-content)

In AJAX and monolithic server-side rendering applications (e.g., PHP, ASP.NET), dynamic Document Object Model (DOM) updates are common for rendering text-only content from APIs or user inputs.

##### What is ``` textContent ``` ?[¶](#what-is-textcontent)

The
```
textContent
```

property sets or gets the plain text content of an element. It treats inserted HTML tags as literal text and does not parse them. It is ideal for most text-only updates, such as displaying user comments, etc.
```
```
const userInput = '';```
```

##### What is ``` innerText ``` ?[¶](#what-is-innertext)

The
```
innerText
```

property sets or gets the visible text content of an element, respecting CSS styling (e.g., ignoring text in
```
display: none
```

elements). It also reflects rendered text formatting, such as line breaks or spacing.
```
```
const userInput = 'OWASP';```
```

##### When to Use ``` textContent ``` vs. ``` innerText ``` [¶](#when-to-use-textcontent-vs-innertext)

- **Use**: Use textContent in monolithic applications to safely insert plain text content returned from APIs.
  ```
  textContent
  ```
- **Use**: Only when CSS visibility or rendered text formatting (e.g. ignoring text in
  ```
  innerText
  ```
  ```
  display: none
  ```

  elements) is required.

> Note:
>
> ```
> textContent
> ```
>
> is slightly faster and more predictable; use it unless you need to respect rendered text formatting (
>
> ```
> innerText
> ```
>
> ).

##### Note[¶](#note)

- While
  ```
  textContent
  ```

  and
  ```
  innerText
  ```

  are safe for inserting plain text into the DOM, they do not protect against XSS in other contexts such as HTML attributes, JavaScript event handlers, or URLs. Always validate and sanitize untrusted input.
- Modern Frameworks like React, Vue, Angular, or Svelte automatically update text-only content so there is no need to manually use
  ```
  textContent
  ```

  or
  ```
  innerText
  ```

  .

#### Don't use ``` eval() ``` , ``` new Function() ``` or other code evaluation tools[¶](#dont-use-eval-new-function-or-other-code-evaluation-tools)
```
eval()
```

function is dangerous, never use it. Needing to use eval() usually indicates a problem in your design.

> Note: Using
>
> ```
> eval()
> ```
>
> or
>
> ```
> new Function()
> ```
>
> opens doors to remote code execution and XSS. Avoid it entirely.

#### Encode Data Before Use in an Output Context[¶](#encode-data-before-use-in-an-output-context)

When using data to build HTML, script, CSS, XML, JSON, etc., make sure you take into account how that data must be presented in a literal sense to keep its logical meaning.

Data should be properly encoded before being used in this manner to prevent injection style issues, and to make sure the logical meaning is preserved.

[Check out the OWASP Java Encoder Project.](https://owasp.org/www-project-java-encoder/)

#### Don't rely on client logic for security[¶](#dont-rely-on-client-logic-for-security)

Don't forget that the user controls the client-side logic. A number of browser plugins are available to set breakpoints, skip code, change values, etc. Never rely on client logic for security.

#### Don't rely on client business logic[¶](#dont-rely-on-client-business-logic)

As with security logic, make sure any important business rules are duplicated on the server side so a user cannot bypass them, which could lead to unexpected or costly behavior.

#### Avoid writing serialization code[¶](#avoid-writing-serialization-code)

This is hard and even a small mistake can cause large security issues. There are already a lot of frameworks to provide this functionality.

Refer to the [JSON page](https://www.json.org/) for more info.

#### Avoid building XML or JSON dynamically[¶](#avoid-building-xml-or-json-dynamically)

Just like building HTML or SQL you may cause XML injection bugs, so stay away from this or at least use an encoding library or safe JSON or XML library to make attributes and element data safe.

#### Never transmit secrets to the client[¶](#never-transmit-secrets-to-the-client)

Anything sent to the client can be read or modified by the user, so keep all that secret stuff on the server please.

#### Don't perform encryption in client-side code[¶](#dont-perform-encryption-in-client-side-code)

Use TLS/SSL and encrypt on the server!

#### Don't perform security impacting logic on client-side[¶](#dont-perform-security-impacting-logic-on-client-side)

This principle serves as a fail-safe—if a security decision is ambiguous, perform it on the server.

### Server-Side[¶](#server-side)

#### Use CSRF Protection[¶](#use-csrf-protection)

Take a look at the [Cross-Site Request Forgery (CSRF) Prevention](Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html) cheat sheet.

#### Protect against JSON hijacking for older browsers[¶](#protect-against-json-hijacking-for-older-browsers)

##### Review AngularJS JSON hijacking defense mechanism[¶](#review-angularjs-json-hijacking-defense-mechanism)

See the [JSON Vulnerability Protection](https://docs.angularjs.org/api/ng/service/$http#json-vulnerability-protection) section of the AngularJS documentation.

##### Always return JSON with an object on the outside[¶](#always-return-json-with-an-object-on-the-outside)

Always have the outside primitive be an object for JSON strings:

**Exploitable:**
```
```
[{"object": "inside an array"}]```
```

**Not exploitable:**
```
```
{"object": "not inside an array"}```
```

**Also not exploitable:**
```
```
{"result": [{"object": "inside an array"}]}```
```

#### Avoid writing serialization code server-side[¶](#avoid-writing-serialization-code-server-side)

Remember reference vs. value types; use a reviewed library.

#### Services can be called directly by users[¶](#services-can-be-called-directly-by-users)

Even though you only expect your AJAX client-side code to call those services, a malicious user can also call them directly.

Validate inputs and treat them as if they are under user control.

#### Avoid building XML or JSON by hand, use the framework[¶](#avoid-building-xml-or-json-by-hand-use-the-framework)

Use the framework to serialize data; building payloads by hand can introduce security issues.

#### Use JSON and XML schema for web services[¶](#use-json-and-xml-schema-for-web-services)

Use a third-party library to validate web service inputs.
