---
title: OWASP Application Gateway
source: owasp.org
url: https://owasp.org/www-project-application-gateway/
collector: owasp
category: web-security
tags:
- web-security
- application
- owasp
- gateway
- login
date_collected: '2026-07-26T12:44:02.028240Z'
language: unknown
---

# OWASP Application Gateway

🏗️ **OWASP Application Gateway is work-in-progress. No productive version has been released yet.**

## What is the OWASP Application Gateway?

OWASP Application Gateway is an HTTP reverse proxy that sits between your web application and the client and handles Oauth2 login, session management as well as other security aspects and operational requirements (including for example correlation logging / tracing). For you, as a developer, OWASP Application Gateway removes the hassle to implement complicated oauth2 logic in the backend and frontend so you can focus totally on your applications logic. OAG is built in an extendable way, so that it is easy to customize it with your own code when required.

## Abstract

See: [Speakerdeck](https://speakerdeck.com/gianlucafrei/owasp-application-gateway-abstract)

## Functionality

- HTTPS Redirection with Proxy Awareness
- OpenID Connect Login with multiple providers
- Multiple Backend routes
- Authenticated routes
- Request Logging
- Add and remove response headers
- Secure, HTTP-only and same-site session cookies
- Forward id token to backend
- Upstream authentication with API key
- GitHub Login support
- Method whitelisting
- CSRF Protection
- Correlation logging / Tracing
- more to come…

See also the documentation [GitHub](https://the-oag-development-project.github.io/docs/)

## Contributing

All kinds of contributions are much wanted and highly appreciated! You can help us with coding, writing documentation, propose architectural improvements, test the prototype, advocate the project or any other kind of activity. Please make sure to read the [CONTRIBUTION.md](https://github.com/The-OAG-Development-Project/Application-Gateway/blob/main/CONTRIBUTING.md) before you start coding. If you have any questions or are not sure how exactly you can contribute feal free to contact any of the project leaders.
