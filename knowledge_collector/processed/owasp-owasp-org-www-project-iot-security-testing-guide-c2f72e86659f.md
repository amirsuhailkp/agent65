---
title: OWASP IoT Security Testing Guide
source: owasp.org
url: https://owasp.org/www-project-iot-security-testing-guide/
collector: owasp
category: web-security
tags:
- web-security
- iot
- security
- guide
- project
date_collected: '2026-07-26T12:45:31.412306Z'
language: unknown
---

# OWASP IoT Security Testing Guide

The OWASP IoT Security Testing Guide (ISTG) provides a comprehensive methodology for penetration tests in the IoT field, offering flexibility to adapt innovations, and developments in the IoT market while still ensuring comparability of test results. This guide provides an understanding of communication between manufacturers and operators of IoT devices, facilitated by establishing a common terminology. Its methodology, underlying models, and the catalog of test cases present tools that can be used separately and in conjunction with each other.

## Contributions

Please check the [OWASP Contributing Guidelines](https://owasp.org/www-project-iot-security-testing-guide/CONTRIBUTING.md) as well as the [ISTG Project Contributing Guide](https://owasp.org/www-project-iot-security-testing-guide/#div-contributing) to find more information about how to contribute to this project. Your support is highly welcome!

## Latest Version

You can find the latest version of this guide [here](https://owasp.org/owasp-istg/) or in the [GitHub Repository](https://github.com/OWASP/owasp-istg).

## Related Work

The concepts, models and test steps presented in the OWASP IoT Security Testing Guide are based on the master’s thesis **“Development of a Methodology for Penetration Tests of Devices in the Field of the Internet of Things”** by Luca Pascal Rotsch.

Test cases were derived from the following public sources:

- OWASP **“Web Security Testing Guide”**
- OWASP **“Firmware Security Testing Methodology”**
- OWASP **“Mobile Security Testing Guide”**
- by Aditya Gupta**“IoT Pentesting Guide”**
- by Aaron Guzman and Aditya Gupta**“IoT Penetration Testing Cookbook”**
- by Aditya Gupta**“The IoT Hacker’s Handbook”**
- by Fotios Chantzis, Ioannis Stais, Paulino Calderon, Evangelos Deirmentzoglou, and Beau Woods**“Practical IoT Hacking”**
- further sources are referenced in the respective test cases

**We also like to thank our collaborators and supporters (see Project Collaborators and Acknowledgements)!**

## Project Collaborators and Acknowledgements

We would like to take this opportunity to acknowledge the contributions of our collaborators and supporters who volunteered their time and expertise to this project. Thank you for your support and commitment to IoT security! This guide would not have been possible without you.

- Antje Winkler
- Clemens Keil
- Denny Vogt (Pyxon73)
- Manfred Heinz (zaphoxx aka CptSpiff)
- Martin Weißbach
- Patrick “HomeSen” Walker
- Sebastian Döring

## Contributing to the ISTG Project

*First of all,*[⭐ Please Give us a Star in GitHub](https://github.com/OWASP/owasp-istg)!

Thank you for your support and dedication to IoT security. The ISTG project is an open source effort and we welcome all kinds of contributions and feedback. To contribute, please head over to our [GitHub Repository](https://github.com/OWASP/owasp-istg). Here, you can review the project’s documentation, code, and share your valuable feedback. Your expertise and insights will play a crucial role in improving the guide’s quality and relevance. Whether you are an experienced IoT security tester or someone passionate about ensuring the security of connected devices, your contributions are highly welcome. Join us in this collaborative effort to strengthen IoT security testing practices and make a positive impact on the industry!

## 💬 Participate in Discussions

Our [GitHub Discussions](https://github.com/OWASP/owasp-istg/discussions) are the first place to go to ask questions, give feedback, and propose new ideas. If your proposal qualifies for the ISTG, we’ll convert it into an “Issue” (the discussion might take a while).

**Help us improve & join our community:**

- 🐞 Report an error (typos, grammar) or fix it on a Pull Request.
- 💬 [Give feedback](https://github.com/OWASP/owasp-istg/discussions/categories/general).
- 🙏 [Ask Questions](https://github.com/OWASP/owasp-istg/discussions/categories/q-a).

## 🎯 Create Issues

Before creating a PR, first create an [Issue](https://github.com/OWASP/owasp-istg/issues) to be discussed for missing requirements, content or errors.

- To avoid multiple people duplicating effort on the same issue, project leaders will assign it to only a few that will own it.
- Explain what you think is missing in the issue, including references (if available) and suggest where it could be added.

## 📝 Open a Pull Request

You can contribute with content or corrections by opening a Pull Request (PR). You can create a PR by following [these steps](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork).
Remember that:

- The target branch should be
  ```
  master
  ```

  .
- If your PR closes and issue, write [“Closes](https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue).
  ```
  #<issue-id>
  ```

  ”

Your PR will be reviewed soon (refer to this page to learn more about [reviews](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/about-pull-request-reviews)).

- Your PR may be merged after review.

> Learn more:
>
> [“(GitHub Docs) Reviewing proposed changes in a pull request”](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/reviewing-proposed-changes-in-a-pull-request).

## 📝Contribute with content:

- 💡 [Propose ideas or suggest improvements](https://github.com/OWASP/owasp-istg/discussions/categories/ideas). If it qualifies we’ll promote it to an Issue.
- 📄 Create a Pull Request for concrete fixes (e.g. grammar/typos) or content already approved by the core team.

## 🚫 What not to do

Although we greatly appreciate any and all contributions to the project, there are a few things that you should take into consideration:

- **No advertisement**: The OWASP IoT Security Project cannot be used as a platform for advertisement of commercial tools, companies or individuals. Technical content such as the implementation of certain techniques or tests should be written with free and open-source tools in mind. Commercial tools are typically not accepted, but might be referenced in some specific cases.
- **No unnecessary self-promotion of tools or blog posts**: If you have a relation with one of the URLs or tools you are referencing, please state so in the PR so that we can verify that the reference is in line with the rest of the guide.

If you have any doubts, please contact us.

## ✅ Become a Reviewer

You can [Review Pull Requests (PRs)](https://github.com/OWASP/owasp-istg/pulls) and also gain contributions. If you are a fluent speaker in different languages, feel free to give feedback on any of the submitted PRs.

After your PR or issue has been submitted, we will review it as quickly as possible which typically only takes a few days. If you think we have forgotten about it, feel free to give us a nudge after 7 days have passed.

## 🔎 Proof-reading

If you do proof-reading, these are the things we’re looking for:

- Content [cohesion & coherence](https://writing.chalmers.se/chalmers-writing-guide/writing-a-text/coherence-cohesion/)
  - is there a good linkage of ideas?
  - does the paragraph make sense?
  - does it make sense with the next one? think that hundreds of people have written in here, often without considering the surroundings of the text they were including).
- Reducing the content to a minimum (people tend to be very verbose/wordy) and in such a document we need clear and short/concise statements
- Optimize for *scannability*(maybe instead of a big paragraph it would be better to have a bullet point list).
- Any passive voice sentences? Convert to active voice.
- Does each paragraph focus on a single topic?
- Are key points stated at the start of each section?
- Are commas, parentheses, colons, em-dashes, and semicolons used properly?

Refer to Google Technical Writing trainings for more info:

## 🌐 Translating the ISTG

Translating the ISTG in a new language is another great way to contribute. This helps the project to reach to more people around the world.

Before starting a translation please consider the following:

- **PLEASE**contact us on Slack or via email.
- We need your commitment. After the first translation is done, we will ask for your help to translate any new changes, so your translation can remain up to date.
- We need a second translator who can verify that the English version of the ISTG has been translated properly.
