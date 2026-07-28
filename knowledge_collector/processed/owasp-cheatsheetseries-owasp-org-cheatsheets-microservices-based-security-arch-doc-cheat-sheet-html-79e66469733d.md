---
title: Microservices based Security Arch Doc Cheat Sheet¶
source: cheatsheetseries.owasp.org
url: https://cheatsheetseries.owasp.org/cheatsheets/Microservices_based_Security_Arch_Doc_Cheat_Sheet.html
collector: owasp
category: web-security
tags:
- web-security
- identify
- data
- name
- describe
date_collected: '2026-07-26T12:36:41.352577Z'
language: unknown
---

# Microservices based Security Arch Doc Cheat Sheet[¶](#microservices-based-security-arch-doc-cheat-sheet)

## Introduction[¶](#introduction)

The microservice architecture is being increasingly used for designing and implementing application systems in both cloud-based and on-premise infrastructures. There are many security challenges need to be addressed in the application design and implementation phases. In order to address some security challenges it is necessity to collect security-specific information on application architecture. The goal of this article is to provide a concrete proposal of approach to collect microservice-based architecture information to securing application.

## Context[¶](#context)

During securing applications based on microservices architecture, security architects/engineers usually face with the following questions (mostly referenced in the [OWASP Application Security Verification Standard Project](https://github.com/OWASP/ASVS) under the section [V1 "Architecture, Design and Threat Modeling Requirements"](https://github.com/OWASP/ASVS/blob/master/4.0/en/0x10-V1-Architecture.md#v1-architecture-design-and-threat-modeling-requirements)):

- Threat modeling and enforcement of the principle of least privilege:
  - What scopes or API keys does microservice minimally need to access other microservice APIs?
  - What grants does microservice minimally need to access database or message queue?
- Data leakage analysis:
  - What storages or message queues do contain sensitive data?
  - Does microservice read/write date from/to specific database or message queue?
  - What microservices are invoked by dedicated microservice? What data is passed between microservices?
- Attack surface analysis:
  - What microservices endpoints need to be tested during security testing?

In most cases, existing application architecture documentation is not suitable to answer those questions. Next sections propose what architecture security-specific information can be collected to answer the questions above.

## Objective[¶](#objective)

The objectives of the cheat sheet are to explain what architecture security-specific information can be collected to answer the questions above and provide concrete proposal of approach to collect microservice-based architecture information to securing application.

## Proposition[¶](#proposition)

### Collect information on the building blocks[¶](#collect-information-on-the-building-blocks)

#### Identify and describe application-functionality services[¶](#identify-and-describe-application-functionality-services)

Application-functionality services implement one or several business process or functionality (e.g., storing customer details, storing and displaying product catalog). Collect information on the parameters listed below related to each application-functionality service.

Parameter nameDescriptionService name (ID)Unique service name or IDShort descriptionShort description of business process or functionality implemented by the microserviceLink to source code repositorySpecify a link to service source code repositoryDevelopment TeamSpecify development team which develops the microserviceAPI definitionIf microservice exposes external interface specify a link to the interface description (e.g., OpenAPI specification). It is advisable to define used security scheme, e.g. define scopes or API keys needed to invoke dedicated endpoint (e.g., [see](https://swagger.io/docs/specification/authentication/)).The microservice architecture descriptionSpecify a link to the microservice architecture diagram, description (if available)Link to runbookSpecify a link to the microservice runbook

#### Identify and describe infrastructure services[¶](#identify-and-describe-infrastructure-services)

Infrastructure services including remote services may implement authentication, authorization, service registration and discovery, security monitoring, logging etc. Collect information on the parameters listed below related to each infrastructure service.

Parameter nameDescriptionService name (ID)Unique service name or IDShort descriptionShort description of functionality implemented by the service (e.g., authentication, authorization, service registration and discovery, logging, security monitoring, API gateway).Link to source code repositorySpecify a link to service source code repository (if applicable)Link to the service documentationSpecify a link to the service documentation that includes service API definition, operational guidance/runbook, etc.

#### Identify and describe data storages[¶](#identify-and-describe-data-storages)

Collect information on the parameters listed below related to each data storage.

Parameter nameDescriptionStorage name (ID)Unique storage name or IDSoftware typeSpecify software that implements the data storage (e.g., PostgreSQL, Redis, Apache Cassandra).

#### Identify and describe message queues[¶](#identify-and-describe-message-queues)

Messaging systems (e.g., RabbitMQ or Apache Kafka) are used to implement asynchronous microservices communication mechanism. Collect information on the parameters listed below related to each message queue.

Parameter nameDescriptionMessage queue (ID)Unique message queue name or IDSoftware typeSpecify software that implements the message queue (e.g., RabbitMQ, Apache Kafka).

#### Identify and describe data assets[¶](#identify-and-describe-data-assets)

Identify and describe data assets that processed by system microservices/services. It is advisable firstly to identify assets, which are valuable from a security perspective (e.g., "User information", "Payment"). Collect information on the parameters listed below related to each asset.

Parameter nameDescriptionAsset name (ID)Unique asset name or IDProtection levelSpecify asset protection level (e.g., PII, confidential)Additional infoAdd clarifying information

### Collect information on relations between building blocks[¶](#collect-information-on-relations-between-building-blocks)

#### Identify "service-to-storage" relations[¶](#identify-service-to-storage-relations)

Collect information on the parameters listed below related to each "service-to-storage" relation.

Parameter nameDescriptionService name (ID)Specify service name (ID) defined aboveStorage name (ID)Specify storage name (ID) defined aboveAccess typeSpecify access type, e.g. "Read" or "Read/Write"

#### Identify "service-to-service" synchronous communications[¶](#identify-service-to-service-synchronous-communications)

Collect information on the parameters listed below related to each "service-to-service" synchronous communication.

Parameter nameDescriptionCaller service name (ID)Specify caller service name (ID) defined aboveCalled service name (ID)Specify called service name (ID) defined aboveProtocol/framework usedSpecify protocol/framework used for communication, e.g. HTTP (REST, SOAP), Apache Thrift, gRPCShort descriptionShortly describe the purpose of communication (requests for query of information or request/commands for a state-changing business function) and data passed between services (if possible, in therms of assets defined above)

#### Identify "service-to-service" asynchronous communications[¶](#identify-service-to-service-asynchronous-communications)

Collect information on the parameters listed below related to each "service-to-service" asynchronous communication.

Parameter nameDescriptionPublisher service name (ID)Specify publisher service name (ID) defined aboveSubscriber service name (ID)Specify subscriber service name (ID) defined aboveMessage queue (ID)Specify message queue (ID) defined aboveShort descriptionShortly describe the purpose of communication (receiving of information or commands for a state-changing business function) and data passed between services (if possible, in therms of assets defined above)

#### Identify "asset-to-storage" relations[¶](#identify-asset-to-storage-relations)

Collect information on the parameters listed below related to each "asset-to-storage" relation.

Parameter nameDescriptionAsset name (ID)Asset name (ID) defined aboveStorage name (ID)Specify storage name (ID) defined aboveStorage typeSpecify storage type for the asset, e.g. "golden source" or "cache"

### Create a graphical presentation of application architecture[¶](#create-a-graphical-presentation-of-application-architecture)

It is advisable to create graphical presentation of application architecture (building blocks and relations defined above) in form of services call graph or data flow diagram. In order to do that one can use special software tools (e.g. Enterprise Architect) or [DOT language](https://en.wikipedia.org/wiki/DOT_%28graph_description_language%29). See example of using DOT language [here](https://gist.github.com/vladgolubev/80c5523336ddec3859c0e90d9a070882).

### Use collected information in secure software development practices[¶](#use-collected-information-in-secure-software-development-practices)

Collected information may be useful for doing application security practices, e.g. during defining security requirements, threat modeling or security testing. Sections below contains examples of activities related to securing application architecture (as well as its mapping to OWASP projects) and tips for their implementation using information collected above.

#### Attack surface analysis[¶](#attack-surface-analysis)

##### Implementation tips[¶](#implementation-tips)

To enumerate microservices endpoints that need to be tested during security testing and analyzed during threat modeling analyze data collected under the following sections:

- Identify and describe application-functionality services (parameter "API definition")
- Identify and describe infrastructure services (parameter "Link to the service documentation")

##### Mapping to OWASP projects[¶](#mapping-to-owasp-projects)

- [OWASP ASVS, V1 "Architecture, Design and Threat Modeling Requirements", #1.1.2](https://github.com/OWASP/ASVS/blob/master/4.0/en/0x10-V1-Architecture.md#v1-architecture-design-and-threat-modeling-requirements)
- [OWASP Attack Surface Analysis Cheat Sheet](https://github.com/OWASP/CheatSheetSeries/blob/master/cheatsheets/Attack_Surface_Analysis_Cheat_Sheet.md)

#### Data leakage analysis[¶](#data-leakage-analysis)

##### Implementation tips[¶](#implementation-tips_1)

To analyze possible data leakage analyze data collected under the following sections:

- Identify and describe data assets
- Identify "service-to-storage" relations
- Identify "service-to-service" synchronous communications
- Identify "service-to-service" asynchronous communications
- Identify "asset-to-storage" relations

##### Mapping to OWASP projects[¶](#mapping-to-owasp-projects_1)

- [OWASP ASVS, V1 "Architecture, Design and Threat Modeling Requirements", #1.1.2](https://github.com/OWASP/ASVS/blob/master/4.0/en/0x10-V1-Architecture.md#v1-architecture-design-and-threat-modeling-requirements)
- [OWASP Top 10-2017 A3-Sensitive Data Exposure](https://owasp.org/www-project-top-ten/OWASP_Top_Ten_2017/Top_10-2017_A3-Sensitive_Data_Exposure)

#### Application's trust boundaries, components, and significant data flows justification[¶](#applications-trust-boundaries-components-and-significant-data-flows-justification)

##### Implementation tips[¶](#implementation-tips_2)

To verify documentation and justification of all the application's trust boundaries, components, and significant data flows analyze data collected under the following sections:

- Identify and describe application-functionality services
- Identify and describe infrastructure services
- Identify and describe data storages
- Identify and describe message queues
- Identify "service-to-storage" relations
- Identify "service-to-service" synchronous communications
- Identify "service-to-service" asynchronous communications

##### Mapping to OWASP projects[¶](#mapping-to-owasp-projects_2)

#### Analysis of the application's high-level architecture[¶](#analysis-of-the-applications-high-level-architecture)

##### Implementation tips[¶](#implementation-tips_3)

To verify definition and security analysis of the application's high-level architecture and all connected remote services analyze data collected under the following sections:

- Identify and describe application-functionality services
- Identify and describe infrastructure services
- Identify and describe data storages
- Identify and describe message queues

##### Mapping to OWASP projects[¶](#mapping-to-owasp-projects_3)

#### Implementation of centralized security controls verification[¶](#implementation-of-centralized-security-controls-verification)

##### Implementation tips[¶](#implementation-tips_4)

To verify implementation of centralized, simple (economy of design), vetted, secure, and reusable security controls to avoid duplicate, missing, ineffective, or insecure controls analyze data collected under the section "Identify and describe infrastructure services".

##### Mapping to OWASP projects[¶](#mapping-to-owasp-projects_4)

#### Enforcement of the principle of least privilege[¶](#enforcement-of-the-principle-of-least-privilege)

##### Implementation tips[¶](#implementation-tips_5)

To define minimally needed microservice permissions analyze data collected under the following sections:

- Identify and describe application-functionality services (parameter "API definition")
- Identify "service-to-storage" relations
- Identify "service-to-service" synchronous communications
- Identify "service-to-service" asynchronous communications

##### Mapping to OWASP projects[¶](#mapping-to-owasp-projects_5)

#### Sensitive data identification and classification[¶](#sensitive-data-identification-and-classification)

##### Implementation tips[¶](#implementation-tips_6)

To verify that all sensitive data is identified and classified into protection levels analyze data collected under the following sections:

- Identify and describe data assets
- Identify "asset-to-storage" relations

##### Mapping to OWASP projects[¶](#mapping-to-owasp-projects_6)

#### Application components business/security functions verification[¶](#application-components-businesssecurity-functions-verification)

##### Implementation tips[¶](#implementation-tips_7)

To verify the definition and documentation of all application components in terms of the business or security functions they provide analyze data collected under the following sections (parameter "Short description"):

- Identify and describe application-functionality services
- Identify and describe infrastructure services
