---
title: OWASP ScrapPy
source: owasp.org
url: https://owasp.org/www-project-scrappy/
collector: owasp
category: web-security
tags:
- web-security
- scrappy
- owasp
- pdfs
- analysis
date_collected: '2026-07-26T12:44:36.632988Z'
language: unknown
---

# OWASP ScrapPy

<img width=40% height=40% src="https://user-images.githubusercontent.com/72598486/200046477-94c17a93-2dc8-418b-96eb-2b554227dce2.png">

# ScrapPY: PDF Scraping Made Easy

ScrapPY is a Python utility for scraping manuals, documents, and other sensitive PDFs to generate targeted wordlists that can be utilized by offensive security tools to perform brute force, forced browsing, and dictionary attacks. ScrapPY performs word frequency, entropy, and metadata analysis, and can run in full output modes to craft custom wordlists for targeted attacks. The tool dives deep to discover keywords and phrases leading to potential passwords or hidden directories, outputting to a text file that is readable by tools such as Hydra, Dirb, and Nmap. Expedite initial access, vulnerability discovery, and lateral movement with ScrapPY!

## Future Development:

- Allow for custom output file naming and increased verbosity
- Integrate different modes of operation including word frequency analysis
- Allow for metadata analysis
- Search for high-entropy data
- Search for path-like data
- Implement image OCR to enumerate data from images in PDFs
- Allow for processing of multiple PDFs
