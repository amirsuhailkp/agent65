---
title: OWASP Dragon-GPT
source: owasp.org
url: https://owasp.org/www-project-dragon-gpt/
collector: owasp
category: web-security
tags:
- web-security
- owasp
- dragon-gpt
- threat
- modeling
date_collected: '2026-07-26T12:44:10.920383Z'
language: unknown
---

# OWASP Dragon-GPT

## Description

Dragon-GPT is an AI-powered tool that automatically performs the threat modeling analysis on the diagram made using the OWASP Threat Dragon modeling software. It uses the OpenAI API, so you need to have a valid account for their tokens to use on each program call, and the JSON file generated when you save/export an OWASP Threat Dragon project (generally saved in td.vue folder).

The program itself is pretty simple, it extracts every relevant information on the JSON file, like the diagram model and components used on the modeling, and transforms it into a human-readable sentence. After that, the sentence is send via OpenAI API, and the result of the analysis is printed. By default, it uses chatgpt-3.5-turbo but you can change that via parameter to another model like the chatgpt-4.

## Changelog

- [Update on 27/10/23] Add Support to Local LLM, the Llama 2, so you don’t need an OpenAI account. The results using Llama may be inferior and slower than ChatGPT but at least it’s free.

## Example

In the example below we have a very simple architecture where a user interacts with a web client, the web client sends HTTP requests to the server and the server makes queries to an SQL database. The Dragon-GPT creates a list of sentences, describes the diagram based on the JSON file created by OWASP THreat Dragon, and uses it as input to the LLM, which can be the ChatGPT or a local LLM.

Contributing in the development and promotion of Dragon-GPT is actively encouraged! You don’t need to be a security nor developer expert in order to contribute. Some of the ways you can help:
