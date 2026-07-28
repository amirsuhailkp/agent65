---
title: OWASP Raider
source: owasp.org
url: https://owasp.org/www-project-raider/
collector: owasp
category: web-security
tags:
- web-security
- raider
- http
- owasp
- process
date_collected: '2026-07-26T12:44:32.584393Z'
language: unknown
---

# OWASP Raider

# What is Raider

This is a framework initially designed to test and automate the authentication process for web applications, and by now it has evolved and can be used for all kinds of stateful HTTP processes. It abstracts the client-server information exchange as a finite state machine. Each step comprises one request with inputs, one response with outputs, arbitrary actions to do on the response, and conditional links to other stages. Thus, a graph-like structure is created.

Raider’s configuration is inspired by Emacs. Hylang is used, which is LISP on top of Python. LISP is used because of its “Code is Data, Data is Code” property. With the magic of LISP macros generating configuration automatically becomes easy. Flexibility is in its DNA, meaning it can be infinitely extended with actual code. You can use it for example to create, store, reproduce, and share proof-of-concepts easily for HTTP attacks. With Raider you can also search through your Projects, filter by hyfile, Flows, FlowGraphs, etc… Then you run either just one step, or a chain of steps, so you can automate and run tests on any HTTP process.

# Graph-like architecture

Raider defines a DSL to describe the information flow between the client and the server for HTTP processes. Each step of the process is described by a Flow, which contains the Request with inputs, Response with outputs, and arbitrary actions including links to other Flows:

Chaining several Flows together can be used to simulate any stateful HTTP process. FlowGraphs indicate the starting point. They can be placed on any Flow. A FlowGraphs runs all Flows in the link until Success/Failure is returned or if there are no more links.
