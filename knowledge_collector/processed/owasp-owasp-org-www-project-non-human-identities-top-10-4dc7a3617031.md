---
title: OWASP Non-Human Identities Top 10
source: owasp.org
url: https://owasp.org/www-project-non-human-identities-top-10/
collector: owasp
category: web-security
tags:
- web-security
- non-human
- identities
- top
- nhis
date_collected: '2026-07-26T12:45:34.576636Z'
language: unknown
---

# OWASP Non-Human Identities Top 10

We're thrilled to introduce the [OWASP Non-Human Identities Top 10 for 2025](./2025/)!

This comprehensive list highlights the most critical challenges in integrating Non-Human Identities (NHIs) into the development lifecycle, ranked based on exploitability, prevalence, detectability, and impact.

## What is Non-Human Identities top 10?

The Non-human identity (NHI) top 10 is a comprehensive list of the most pressing security risks and vulnerabilities that non-human identities present to organizations.

Production software environments are composed of a large number of applications which need to be identified, resulting in “non-human identities” or NHI. Application identities are often associated with secrets, which are used as credentials similarly to the way humans authenticate into computer systems. Application secrets may be used to authenticate into other applications within the trust domain. They may also be used to authenticate into 3rd party SaaS applications.

While long-term application secrets behave similarly to human passwords, short term secrets may be generated on the fly by the run-time environment, based on application attestation, where the environment identifies the application and provisions it with credentials.

This project is aimed at helping security professionals thoroughly understand their non-human identity attack surface, so they can better protect and manage it. The project spans across thoroughly explaining the risks and their potential exploits, as well as providing actionable prevention practices and incident response playbooks.

## NHI Top 10 - 2025 - A sneak peek

Improper offboarding refers to the inadequate deactivation or removal of non-human identities (NHIs) such as service accounts and access keys when they are no longer needed.
Unmonitored and deprecated services may remain vulnerable, and their associated NHIs can be exploited by attackers to gain unauthorized access to sensitive systems and data.
[Read More »](/www-project-non-human-identities-top-10/2025/1-improper-offboarding/)

Secret Leakage refers to the leakage of sensitive NHIs such as API keys, tokens, encryption keys, and certificates to unsanctioned data stores throughout the software development lifecycle
When secrets are leaked —for instance, hard-coded into source code, stored in plain text configuration files, or sent over public chat applications —they become susceptible to exposure.
[Read More »](/www-project-non-human-identities-top-10/2025/2-secret-leakage/)

Third-party non-human identities (NHIs) are extensively integrated into the development workflow, both through the use of integrated development environments (IDEs) and their extensions and also through the use of 3rd party SaaS.
If a third-party extension is compromised—whether through a security vulnerability or a malicious update—it can be exploited to steal these credentials or misuse the granted permissions.
[Read More »](/www-project-non-human-identities-top-10/2025/2-secret-leakage/)

Developers frequently integrate internal and external (third-party) services into their applications. These services require access to resources within these systems, necessitating authentication credentials.
However, some authentication methods are deprecated, vulnerable to known attacks, or considered weak due to outdated security practices. Utilizing insecure or obsolete authentication mechanisms can expose organizations to significant risks.
[Read More »](/www-project-non-human-identities-top-10/2025/4-insecure-authentication/)

During application development and maintenance, developers or administrators may assign NHIs with significantly more privileges than required for their function.
When an over-privileged NHI is compromised — whether through vulnerabilities in the application, malware, or other security breaches — attackers can exploit the excessive permissions.
[Read More »](/www-project-non-human-identities-top-10/2025/5-overprivileged-nhi/)

Continuous Integration and Continuous Deployment (CI/CD) applications enable developers to automate the process of building, testing, and deploying code to production environments.
These integrations often require authentication with cloud services, typically achieved using static credentials or OpenID Connect (OIDC).
Static credentials can be inadvertently exposed through code repositories, logs, or configuration files. If compromised, these credentials can provide attackers with persistent and potentially privileged access to production environments.
While OIDC offers a more secure alternative, if the identity tokens are not properly validated or there are no strict conditions on token claims unauthorized users might exploit these weaknesses to gain access.
[Read More »](/www-project-non-human-identities-top-10/2025/6-insecure-cloud-deployment-configurations/)

Long-lived Secrets refers to the use of sensitive NHIs such as API keys, tokens, encryption keys, and certificates with expiration dates that are too far in the future or that don’t expire at all.
If a breached secret is long-lived, it provides attackers with access to sensitive services without any time constraints.
[Read More »](/www-project-non-human-identities-top-10/2025/7-long-lived-secrets/)

Environment isolation is a fundamental security practice in cloud application deployment, where separate environments are used for development, testing, staging, and production.
NHIs are often utilized during the deployment process and throughout an application’s lifecycle. However, reusing the same NHIs across multiple environments—especially between testing and production—can introduce significant security vulnerabilities.
[Read More »](/www-project-non-human-identities-top-10/2025/8-environment-isolation/)

Reusing the same NHI across different applications, services, or components — even if they are deployed together — introduces significant security risks. If an NHI is compromised in one area, an attacker can exploit it to gain unauthorized access to other parts of the system that use the same credentials.
[Read More »](/www-project-non-human-identities-top-10/2025/9-nhi-reuse/)

During application development and maintenance, developers or administrators may misuse NHIs for manual tasks that should be performed using individual human identities with appropriate privileges. This practice introduces significant security risks such as elevated privileges for NHIs, lack of auditing and accountability due to indistinguishable activity between humans and automation.
[Read More »](/www-project-non-human-identities-top-10/2025/10-human-use-of-nhi/)

## How to contribute

Involvement in the development and promotion of OWASP Non-Human Identities Top 10 is actively encouraged! You do not have to be a security expert in order to contribute.

Here are some ways you can help:

- We are looking for organizations and individuals that will provide vulnerability prevalence data
- Translate the top 10 to non-English languages
- Review, critique and suggest improvements to the Top 10 list
- Star the [GitHub Project](https://github.com/OWASP/www-project-non-human-identities-top-10)
- Contribute real world examples to categories in the Top 10 list
- Add your Success Story - [tell us](/cdn-cgi/l/email-protection#bdcfd2d3d493d1d4ded5c9d0dcd3fdd2cadccecd93d2cfda)and the world how you’re using the Top 10 list
- Feel free to also add a note for the next periodic “OWASP Non-Human Identities Top 10” meeting [here](https://docs.google.com/document/d/1lJE0AwgWc4PHUX5Y0-s3TPhi6Lh8_dqWgsiEeJopkKY/edit?pli=1#heading=h.29vste2an1z).

Individuals and organizations that provide a significant contribution to the project will be listed on the Contributors page.

## How to reach out:

- Give us feedback / suggestions / report bugs on [GitHub](https://github.com/OWASP/www-project-non-human-identities-top-10)
- Join our [email group](https://groups.google.com/g/owasp-non-human-identities)
- Contact the [project leads](/cdn-cgi/l/email-protection#5a2835343374363339322e373b341a352d3b292a7435283d)
- Talk to us on [Slack](https://owasp.slack.com/archives/C02C6RU6G10)(#non-human-identities-top-10)

## Got an idea?

Got any ideas on how to make this project better? These guidelines will help with how to get involved:

- Join the conversation on [email](https://groups.google.com/g/owasp-non-human-identities)or[Slack](https://owasp.slack.com/archives/C02C6RU6G10)to find collaborators or see if others have a similar interest.
- Search the project’s [GitHub issues](https://github.com/OWASP/www-project-non-human-identities-top-10/issues)for related proposals. Found one? Join it!
- If you haven’t found a relevant issue, create one! Clearly specify why your proposal is important and which changes are proposed. Advertise your proposal to others to find collaborators.

## Getting Started with your first Pull Request

A Pull Request (PR) can be created by [following these steps](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork).

Remember to:

- Fork the repository.
- Create an initial draft implementing your proposal and submit it for review as a PR. Don’t let perfect be the enemy of good.
- Advertise your proposal to others and ask for reviews.
- Once your PR is merged, continue to submit PRs to fine-tune and improve on previous versions.
- Congrats and thank you!

## Contributors

Individuals that provided a significant contribution to the project:

NameAffiliationContactRoni LichtmanTorch Security[Twitter](https://x.com/roni_lichtman_)[LinkedIn](https://www.linkedin.com/in/roni-lichtman/)Tal SkvererAstrix Security[LinkedIn](https://www.linkedin.com/in/reverser/)Or Cohen-[LinkedIn](https://www.linkedin.com/in/or-cohen-51a32b131/)Idan Basre-[LinkedIn](https://www.linkedin.com/in/idan-basre/)Amir Benvenisti-[LinkedIn](https://www.linkedin.com/in/amir-benvenisti/)Dor DaliCyolo[LinkedIn](https://www.linkedin.com/in/dordali/)Jack SchofieldSnyk[LinkedIn](https://www.linkedin.com/in/jackschofield85/)Tomer YahalomAstrix Security[LinkedIn](https://www.linkedin.com/in/tomer-yahalom-4622b0178/)Idan GourAstrix Security[LinkedIn](https://www.linkedin.com/in/idangour/)Danielle GuettaJazz[LinkedIn](https://www.linkedin.com/in/danielle-guetta-94108310/)Bar KaduriOrca Security[LinkedIn](https://www.linkedin.com/in/bar-kaduri)Yonatan YosefOrca Security[LinkedIn](https://www.linkedin.com/in/yonatan-yosef-93a028188/)Adam OchayonOasis Security[LinkedIn](https://www.linkedin.com/in/adamochayon/)Yaron ShefferIntuit[LinkedIn](https://www.linkedin.com/in/yaronf/)Ben KimCremit[LinkedIn](https://www.linkedin.com/in/ben-dh-kim/)

## Sponsors

The OWASP Non-Human Identities Top 10 project is sponsored by [Astrix](https://astrix.security/)
