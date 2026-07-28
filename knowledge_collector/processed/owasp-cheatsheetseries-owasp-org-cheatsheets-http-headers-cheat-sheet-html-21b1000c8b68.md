---
title: HTTP Security Response Headers Cheat Sheet¶
source: cheatsheetseries.owasp.org
url: https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html
collector: owasp
category: web-security
tags:
- web-security
- header
- http
- security
- response
date_collected: '2026-07-26T12:36:29.097957Z'
language: unknown
---

# HTTP Security Response Headers Cheat Sheet[¶](#http-security-response-headers-cheat-sheet)

## Introduction[¶](#introduction)

HTTP Headers are a great booster for web security with easy implementation. Proper HTTP response headers can help prevent security vulnerabilities like Cross-Site Scripting, Clickjacking, Information disclosure and more.

In this cheat sheet, we will review all security-related HTTP headers, recommended configurations, and reference other sources for complicated headers.

## Security Headers[¶](#security-headers)

### X-Frame-Options[¶](#x-frame-options)

The
```
X-Frame-Options
```

HTTP response header can be used to indicate whether or not a browser should be allowed to render a page in a
```
<frame>
```

,
```
<iframe>
```

,
```
<embed>
```

or
```
<object>
```

. Sites can use this to avoid [clickjacking](https://owasp.org/www-community/attacks/Clickjacking) attacks, by ensuring that their content is not embedded into other sites.

Content Security Policy (CSP) frame-ancestors directive obsoletes X-Frame-Options for supporting browsers ([source](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options)).

X-Frame-Options header is only useful when the HTTP response where it is included has something to interact with (e.g. links, buttons). If the HTTP response is a redirect or an API returning JSON data, X-Frame-Options does not provide any security.

#### Recommendation[¶](#recommendation)

Use Content Security Policy (CSP) frame-ancestors directive if possible.

Do not allow displaying of the page in a frame.

> ```
> X-Frame-Options: DENY
> ```

### X-XSS-Protection[¶](#x-xss-protection)

The HTTP
```
X-XSS-Protection
```

response header is a feature of Internet Explorer, Chrome, and Safari that stops pages from loading when they detect reflected cross-site scripting (XSS) attacks.

WARNING: Even though this header can protect users of older web browsers that don't yet support CSP, in some cases, this header can create XSS vulnerabilities in otherwise safe websites [source](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-XSS-Protection).

#### Recommendation[¶](#recommendation_1)

Use a Content Security Policy (CSP) that disables the use of inline JavaScript.

Do not set this header or explicitly turn it off.

> ```
> X-XSS-Protection: 0
> ```

Please see [Mozilla X-XSS-Protection](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-XSS-Protection) for details.

### X-Content-Type-Options[¶](#x-content-type-options)

The
```
X-Content-Type-Options
```

response HTTP header is used by the server to indicate to the browsers that the MIME types advertised in the Content-Type headers should be followed and not guessed.

This header is used to block browsers' [MIME type sniffing](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types#mime_sniffing), which can transform non-executable MIME types into executable MIME types ([MIME Confusion Attacks](https://blog.mozilla.org/security/2016/08/26/mitigating-mime-confusion-attacks-in-firefox/)).

#### Recommendation[¶](#recommendation_2)

Set the Content-Type header correctly throughout the site.

> ```
> X-Content-Type-Options: nosniff
> ```

### Referrer-Policy[¶](#referrer-policy)

The
```
Referrer-Policy
```

HTTP header controls how much referrer information (sent via the Referer header) should be included with requests.

#### Recommendation[¶](#recommendation_3)

Referrer policy has been supported by browsers since 2014. Today, the default behavior in modern browsers is to no longer send all referrer information (origin, path, and query string) to the same site but to only send the origin to other sites. However, since not all users may be using the latest browsers we suggest forcing this behavior by sending this header on all responses.

> ```
> Referrer-Policy: strict-origin-when-cross-origin
> ```

- *NOTE:*For more information on configuring this header please see[Mozilla Referrer-Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy).

### Content-Type[¶](#content-type)

The
```
Content-Type
```

representation header is used to indicate the original media type of the resource (before any content encoding is applied for sending). If not set correctly, the resource (e.g. an image) may be interpreted as HTML, making XSS vulnerabilities possible.

Although it is recommended to always set the
```
Content-Type
```

header correctly, it would constitute a vulnerability only if the content is intended to be rendered by the client and the resource is untrusted (provided or modified by a user).

#### Recommendation[¶](#recommendation_4)

> ```
> Content-Type: text/html; charset=UTF-8
> ```

- *NOTE:*the
  ```
  charset
  ```

  attribute is necessary to prevent XSS in**HTML**pages
- *NOTE*: the
  ```
  Content-Type
  ```

  can be any of the possible[MIME types](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types)

### Cache-Control[¶](#cache-control)

The
```
Cache-Control
```

header defines how responses are cached by browsers and intermediate caches.

#### Recommendation[¶](#recommendation_5)

- Use
  ```
  no-store
  ```

  for sensitive data to prevent any form of caching.
- Use
  ```
  private
  ```

  to allow caching only in non-shared (user-specific) caches and to prevent storage in shared caches (note that private caches may still persist the response).
- Avoid relying on default caching behavior for sensitive or protected content.
- Be aware that
  ```
  no-cache
  ```

  does not prevent caching; it allows caches to store responses. It requires revalidation with the origin server before reuse.

These directives help reduce the risk of sensitive data being stored or exposed through caching, but use
```
no-store
```

when storage of sensitive data must be strictly prevented.

#### References[¶](#references)

### Set-Cookie[¶](#set-cookie)

The
```
Set-Cookie
```

HTTP response header is used to send a cookie from the server to the user agent, so the user agent can send it back to the server later. To send multiple cookies, multiple Set-Cookie headers should be sent in the same response.

This is not a security header per se, but its security attributes are crucial.

#### Recommendation[¶](#recommendation_6)

- Please read [Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html#cookies)for a detailed explanation on cookie configuration options.

### Strict-Transport-Security (HSTS)[¶](#strict-transport-security-hsts)

The HTTP
```
Strict-Transport-Security
```

response header (often abbreviated as HSTS) instructs browsers to only access the website using HTTPS, even if a user attempts to connect over HTTP.

#### Recommendation[¶](#recommendation_7)

> ```
> Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
> ```

- *NOTE*: Read carefully how this header works before using it. If the HSTS header is misconfigured or if there is a problem with the SSL/TLS certificate being used, legitimate users might be unable to access the website. For example, if the HSTS header is set to a very long duration and the SSL/TLS certificate expires or is revoked, legitimate users might be unable to access the website until the HSTS header duration has expired.

Please check out [HTTP Strict Transport Security Cheat Sheet](HTTP_Strict_Transport_Security_Cheat_Sheet.html) for more information.

### Expect-CT ❌[¶](#expect-ct)

The
```
Expect-CT
```

header lets sites opt-in to reporting of Certificate Transparency (CT) requirements. Given that mainstream clients now require CT qualification, the only remaining value is reporting such occurrences to the nominated report-uri value in the header. The header is now less about enforcement and more about detection/reporting.

#### Recommendation[¶](#recommendation_8)

Do not use it. Mozilla [recommends](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Expect-CT) avoiding it, and removing it from existing code if possible.

### Content-Security-Policy (CSP)[¶](#content-security-policy-csp)

Content Security Policy (CSP) is a security feature that is used to specify the origin of content that is allowed to be loaded on a website or in a web application. It is an added layer of security that helps to detect and mitigate certain types of attacks, including Cross-Site Scripting (XSS) and data injection attacks. These attacks are used for everything from data theft to site defacement to distribution of malware.

- *NOTE*: This header is relevant to be applied in pages which can load and interpret scripts and code, but might be meaningless in the response of a REST API that returns content that is not going to be rendered.

#### Recommendation[¶](#recommendation_9)

Content Security Policy is complex to configure and maintain. For an explanation on customization options, please read [Content Security Policy Cheat Sheet](Content_Security_Policy_Cheat_Sheet.html)

### Access-Control-Allow-Origin[¶](#access-control-allow-origin)

If you don't use this header, your site is protected by default by the Same Origin Policy (SOP). What this header does is relax this control in specified circumstances.

The
```
Access-Control-Allow-Origin
```

is a CORS (cross-origin resource sharing) header. This header indicates whether the response it is related to can be shared with requesting code from the given origin. In other words, if siteA requests a resource from siteB, siteB should indicate in its
```
Access-Control-Allow-Origin
```

header that siteA is allowed to fetch that resource, if not, the access is blocked due to Same Origin Policy (SOP).

#### Recommendation[¶](#recommendation_10)

If you use it, set specific [origins](https://developer.mozilla.org/en-US/docs/Glossary/Origin) instead of
```
*
```

. Check out [Access-Control-Allow-Origin](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Allow-Origin) for details.

> ```
> Access-Control-Allow-Origin: https://yoursite.com
> ```

- *NOTE*: The use of '\*' might be necessary depending on your needs. For example, for a public API that should be accessible from any origin, it might be necessary to allow '\*'.

### Cross-Origin-Opener-Policy (COOP)[¶](#cross-origin-opener-policy-coop)

The HTTP
```
Cross-Origin-Opener-Policy
```

(COOP) response header allows you to ensure a top-level document does not share a browsing context group with cross-origin documents.

This header works together with Cross-Origin-Embedder-Policy (COEP) and Cross-Origin-Resource-Policy (CORP) explained below.

This mechanism protects against attacks like Spectre which can cross the security boundary established by Same Origin Policy (SOP) for resources in the same browsing context group.

As these headers are very related to browsers, it may not make sense to be applied to REST APIs or clients that are not browsers.

#### Recommendation[¶](#recommendation_11)

Isolates the browsing context exclusively to same-origin documents.

> ```
> Cross-Origin-Opener-Policy: same-origin
> ```

### Cross-Origin-Embedder-Policy (COEP)[¶](#cross-origin-embedder-policy-coep)

The HTTP
```
Cross-Origin-Embedder-Policy
```

(COEP) response header prevents a document from loading any cross-origin resources that don't explicitly grant the document permission (using [CORP](#cross-origin-resource-policy-corp) or CORS).

- *NOTE*: Enabling this will block cross-origin resources not configured correctly from loading.

#### Recommendation[¶](#recommendation_12)

A document can only load resources from the same origin, or resources explicitly marked as loadable from another origin.

> ```
> Cross-Origin-Embedder-Policy: require-corp
> ```

- *NOTE*: you can bypass it for specific resources by adding the
  ```
  crossorigin
  ```

  attribute:
- ```
  <img src="https://thirdparty.com/img.png" crossorigin>  ```

### Cross-Origin-Resource-Policy (CORP)[¶](#cross-origin-resource-policy-corp)

The

```
Cross-Origin-Resource-Policy```

(CORP) header allows you to control the set of origins that are empowered to include a resource. It is a robust defense against attacks like [Spectre](https://meltdownattack.com/), as it allows browsers to block a given response before it enters an attacker's process.

#### Recommendation[¶](#recommendation_13)

Limit current resource loading to the site and sub-domains only.

> ```
> Cross-Origin-Resource-Policy: same-site
> ```

### Permissions-Policy (formerly Feature-Policy)[¶](#permissions-policy-formerly-feature-policy)

Permissions-Policy allows you to control which origins can use which browser features, both in the top-level page and in embedded frames. For every feature controlled by Feature Policy, the feature is only enabled in the current document or frame if its origin matches the allowed list of origins. This means that you can configure your site to never allow the camera or microphone to be activated. This prevents that an injection, for example an XSS, enables the camera, the microphone, or other browser feature.

More information: [Permissions-Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Permissions-Policy)

#### Recommendation[¶](#recommendation_14)

Set it and disable all the features that your site does not need or allow them only to the authorized domains:

> ```
> Permissions-Policy: geolocation=(), camera=(), microphone=()
> ```

- *NOTE*: This example is disabling geolocation, camera, and microphone for all domains.

### FLoC (Federated Learning of Cohorts)[¶](#floc-federated-learning-of-cohorts)

FLoC is a method proposed by Google in 2021 to deliver interest-based advertisements to groups of users ("cohorts"). The [Electronic Frontier Foundation](https://www.eff.org/deeplinks/2021/03/googles-floc-terrible-idea), [Mozilla](https://blog.mozilla.org/en/privacy-security/privacy-analysis-of-floc/), and others believe FLoC does not do enough to protect users' privacy.

#### Recommendation[¶](#recommendation_15)

A site can declare that it does not want to be included in the user's list of sites for cohort calculation by sending this HTTP header.

> Permissions-Policy: interest-cohort=()

### Server[¶](#server)

The

```
Server```

header describes the software used by the origin server that handled the request — that is, the server that generated the response.

This is not a security header, but how it is used is relevant for security.

#### Recommendation[¶](#recommendation_16)

Remove this header or set non-informative values.

> ```
> Server: webserver
> ```

- *NOTE*: Remember that attackers have other means of fingerprinting the server technology.

### X-Powered-By[¶](#x-powered-by)

The

```
X-Powered-By```

header describes the technologies used by the webserver. This information exposes the server to attackers. Using the information in this header, attackers can find vulnerabilities easier.

#### Recommendation[¶](#recommendation_17)

Remove all

```
X-Powered-By```

headers.

- *NOTE*: Remember that attackers have other means of fingerprinting your tech stack.

### X-AspNet-Version[¶](#x-aspnet-version)

Provides information about the .NET version.

#### Recommendation[¶](#recommendation_18)

Disable sending this header. Add the following line in your

```
web.config```

in the

```
<system.web>```

section to remove it.

```
```
<httpRuntime enableVersionHeader="false" />
```
```

- *NOTE*: Remember that attackers have other means of fingerprinting your tech stack.

### X-AspNetMvc-Version[¶](#x-aspnetmvc-version)

Provides information about the .NET version.

#### Recommendation[¶](#recommendation_19)

Disable sending this header. To remove the

```
X-AspNetMvc-Version```

header, add the below line in

```
Global.asax```

file.

```
```
MvcHandler.DisableMvcResponseHeader = true;
```
```

- *NOTE*: Remember that attackers have other means of fingerprinting your tech stack.

### X-Robots-Tag[¶](#x-robots-tag)

The HTTP

```
X-Robots-Tag```

response header controls how search engines and other automated crawlers index and display resources such as PDFs, images, and other non-HTML content.
It functions similarly to the

```
<meta name="robots">```

tag, but is applied via the HTTP response header, allowing greater flexibility (e.g., for non-HTML files or server-wide rules).

```
```
X-Robots-Tag: noindex, nofollow
```
```

- **Note:**Only compliant crawlers respect these directives, and they must still make an HTTP request to read the headers before deciding how to handle the content.

#### Recommendation[¶](#recommendation_20)

Use the

```
X-Robots-Tag```

header to control crawler behavior:

- For **private or sensitive content**you don’t want indexed:

> ```
> X-Robots-Tag: noindex, nofollow
> ```
>
> This prevents compliant search engines from indexing the resource or following links on it.

- For **public content**you want indexed and discoverable (e.g., documentation, datasets):

> ```
> X-Robots-Tag: index, follow
> ```
>
> This allows search engines to index the resource and follow its links.

You can also use other directives such as

```
noarchive```

,

```
nosnippet```

, or

```
noimageindex```

depending on your needs.
Server configuration can apply this header selectively — for example, only on specific file types (like PDFs or images).

### X-DNS-Prefetch-Control[¶](#x-dns-prefetch-control)

The

```
X-DNS-Prefetch-Control```

HTTP response header controls DNS prefetching, a feature by which browsers proactively perform domain name resolution on both links that the user may choose to follow as well as URLs for items referenced by the document, including images, CSS, JavaScript, and so forth.

#### Recommendation[¶](#recommendation_21)

The default behavior of browsers is to perform DNS caching which is good for most websites.
If you do not control links on your website, you might want to set

```
off```

as a value to disable DNS prefetch to avoid leaking information to those domains.

> ```
> X-DNS-Prefetch-Control: off
> ```

- *NOTE*: Do not rely on this functionality for anything production sensitive: it is not standard or fully supported and implementation may vary among browsers.

### Public-Key-Pins (HPKP) ❌[¶](#public-key-pins-hpkp)

The HTTP

```
Public-Key-Pins```

response header was used to associate a specific cryptographic public key with a web server to mitigate MITM attacks with forged certificates. It was removed from Chromium in 2018 and is unsupported by all modern browsers.

#### Recommendation[¶](#recommendation_22)

Do not use. Remove any

```
Public-Key-Pins```

or

```
Public-Key-Pins-Report-Only```

headers from production. Rely on Certificate Transparency (CT) and CAA DNS records, which provide superior compromise detection without the operational brittleness of pinning.

### Secure File Download Headers[¶](#secure-file-download-headers)

When serving user-provided files, proper HTTP headers should be used to prevent unintended execution in the browser.

- Use

  ```
  Content-Disposition: attachment  ```

  to force download instead of inline rendering.
- Use

  ```
  Content-Type: application/octet-stream  ```

  for unknown or binary files.
- Ensure

  ```
  X-Content-Type-Options: nosniff  ```

  is set to prevent MIME type sniffing.

These headers help reduce risks such as Cross-Site Scripting (XSS) and unintended file execution.

## Adding HTTP Headers in Different Technologies[¶](#adding-http-headers-in-different-technologies)

### PHP[¶](#php)

The sample code below sets the

```
X-Frame-Options```

header in PHP.

```
```
header("X-Frame-Options: DENY");
```
```

### Apache[¶](#apache)

Below is an

```
.htaccess```

sample configuration which sets the

```
X-Frame-Options```

header in Apache.

As described in the [Apache documentation](https://httpd.apache.org/docs/2.4/mod/mod_headers.html#header),

```
Header set```

(default

```
onsuccess```

) and

```
Header always set```

operate on separate internal header tables.

In some cases, both header tables may be used, which can result in duplicate headers if the same header is configured in both contexts.

If a header needs to be removed entirely, it should be unset in both contexts (

```
onsuccess```

and

```
always```

).

To avoid duplication and ensure the header is sent on all responses, unset it first and then use

```
always set```

:

```
```
<IfModule mod_headers.c>
  Header unset X-Frame-Options
  Header always set X-Frame-Options "DENY"
</IfModule>
```
```

### IIS[¶](#iis)

Add configurations below to your

```
Web.config```

in IIS to send the

```
X-Frame-Options```

header.

```
```
<system.webServer>
...
 <httpProtocol>
   <customHeaders>
     <add name="X-Frame-Options" value="DENY" />
   </customHeaders>
 </httpProtocol>
...
</system.webServer>
```
```

### HAProxy[¶](#haproxy)

Add the line below to your front-end, listen, or backend configurations to send the

```
X-Frame-Options```

header.

```
```
http-response set-header X-Frame-Options DENY
```
```

### Nginx[¶](#nginx)

Below is a sample configuration, it sets the

```
X-Frame-Options```

header in Nginx. Note that without the

```
always```

option, the header will only be sent for certain status codes, as described in [the nginx documentation](https://nginx.org/en/docs/http/ngx_http_headers_module.html#add_header).

```
```
add_header "X-Frame-Options" "DENY" always;
```
```

### Express[¶](#express)

You can use [helmet](https://www.npmjs.com/package/helmet) to setup HTTP headers in Express. The code below is a sample for adding the

```
X-Frame-Options```

header.

```
```
const helmet = require('helmet');
const app = express();
// Sets "X-Frame-Options: SAMEORIGIN"
app.use(
 helmet.frameguard({
   action: "sameorigin",
 })
);
```
```

## Testing Proper Implementation of Security Headers[¶](#testing-proper-implementation-of-security-headers)

### Mozilla Observatory[¶](#mozilla-observatory)

The [Mozilla Observatory](https://observatory.mozilla.org/) is an online tool which helps you to check your website's header status.

### SmartScanner[¶](#smartscanner)

[SmartScanner](https://www.thesmartscanner.com/) has a dedicated [test profile](https://www.thesmartscanner.com/docs/configuring-security-tests) for testing security of HTTP headers.
Online tools usually test the homepage of the given address. But SmartScanner scans the whole website. So, you can make sure all of your web pages have the right HTTP Headers in place.

## References[¶](#references_1)

- [MDN Web Docs: Content-Disposition](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Disposition)
- [MDN Web Docs: Content-Type](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Type)
- [MDN Web Docs: X-Content-Type-Options](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Content-Type-Options)
- [MDN Web Docs: X-Frame-Options](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options)
- [MDN Web Docs: X-XSS-Protection](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-XSS-Protection)
- [MDN Web Docs: Strict-Transport-Security](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security)
- [MDN Web Docs: Expect-CT](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Expect-CT)
- [MDN Web Docs: Set-Cookie](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie)
- [MDN Web Docs: Cross-Origin-Opener-Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cross-Origin-Opener-Policy)
- [MDN Web Docs: Cross-Origin-Resource-Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cross-Origin-Resource-Policy)
- [MDN Web Docs: Cross-Origin-Embedder-Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cross-Origin-Embedder-Policy)
- [MDN Web Docs: Server](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Server)
- [HSTS Preload List](https://hstspreload.org/)
- [Content Security Policy Reference](https://content-security-policy.com/)
- [Resource Policy Reference](https://resourcepolicy.fyi/)
- [OWASP Secure Headers Project](https://owasp.org/www-project-secure-headers/)
