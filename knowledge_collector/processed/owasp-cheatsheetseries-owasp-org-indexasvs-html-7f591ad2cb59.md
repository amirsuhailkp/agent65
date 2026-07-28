---
title: ASVS Index¶
source: cheatsheetseries.owasp.org
url: https://cheatsheetseries.owasp.org/IndexASVS.html
collector: owasp
category: web-security
tags:
- web-security
- cheat
- sheet
- security
- prevention
date_collected: '2026-07-26T12:36:02.907348Z'
language: unknown
---

# ASVS Index[¶](#asvs-index)

## Table of Contents[¶](#table-of-contents)

- [Objective](#objective)
- [V1: Encoding and Sanitization](#v1-encoding-and-sanitization)
- [V2: Validation and Business Logic](#v2-validation-and-business-logic)
- [V3: Web Frontend Security](#v3-web-frontend-security)
- [V4: API and Web Service](#v4-api-and-web-service)
- [V5: File Handling](#v5-file-handling)
- [V6: Authentication](#v6-authentication)
  - [V6.1 Authentication Documentation](#v61-authentication-documentation)
  - [V6.2 Password Security](#v62-password-security)
  - [V6.3 General Authentication Security](#v63-general-authentication-security)
  - [V6.4 Authentication Factor Lifecycle and Recovery](#v64-authentication-factor-lifecycle-and-recovery)
  - [V6.5 General Multi-factor authentication requirements](#v65-general-multi-factor-authentication-requirements)
  - [V6.6 Out-of-Band authentication mechanisms](#v66-out-of-band-authentication-mechanisms)
  - [V6.7 Cryptographic authentication mechanism](#v67-cryptographic-authentication-mechanism)
  - [V6.8 Authentication with an Identity Provider](#v68-authentication-with-an-identity-provider)
- [V7: Session Management](#v7-session-management)
- [V8: Authorization](#v8-authorization)
- [V9: Self-contained Tokens](#v9-self-contained-tokens)
- [V10: OAuth and OIDC](#v10-oauth-and-oidc)
- [V11: Cryptography](#v11-cryptography)
- [V12: Secure Communication](#v12-secure-communication)
- [V13: Configuration](#v13-configuration)
- [V14: Data Protection](#v14-data-protection)
- [V15: Secure Coding and Architecture](#v15-secure-coding-and-architecture)
- [V16: Security Logging and Error Handling](#v16-security-logging-and-error-handling)
- [V17: WebRTC](#v17-webrtc)

## Objective[¶](#objective)

The objective of this index is to help an OWASP [Application Security Verification Standard](https://owasp.org/www-project-application-security-verification-standard/) (ASVS) user clearly identify which cheat sheets are useful for each section during his or her usage of the ASVS.

This index is based on the version 5.0.x of the ASVS.

## V1: Encoding and Sanitization[¶](#v1-encoding-and-sanitization)

### V1.1 Encoding and Sanitization Architecture[¶](#v11-encoding-and-sanitization-architecture)

[Security Terminology Cheat Sheet](cheatsheets/Security_Terminology_Cheat_Sheet.html)

[Cross Site Scripting Prevention Cheat Sheet](cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)

### V1.2 Injection Prevention[¶](#v12-injection-prevention)

[Cross Site Scripting Prevention Cheat Sheet](cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)

[DOM based XSS Prevention Cheat Sheet](cheatsheets/DOM_based_XSS_Prevention_Cheat_Sheet.html)

[Injection Prevention Cheat Sheet](cheatsheets/Injection_Prevention_Cheat_Sheet.html)

[Query Parameterization Cheat Sheet](cheatsheets/Query_Parameterization_Cheat_Sheet.html)

[XSS Filter Evasion Cheat Sheet](cheatsheets/XSS_Filter_Evasion_Cheat_Sheet.html)

[XML External Entity Prevention Cheat Sheet](cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html)

### V1.3 Sanitization[¶](#v13-sanitization)

[Cross-Site Request Forgery Prevention Cheat Sheet](cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html)

[Cross Site Scripting Prevention Cheat Sheet](cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)

[DOM based XSS Prevention Cheat Sheet](cheatsheets/DOM_based_XSS_Prevention_Cheat_Sheet.html)

[Injection Prevention Cheat Sheet](cheatsheets/Injection_Prevention_Cheat_Sheet.html)

[Injection Prevention Cheat Sheet in Java](cheatsheets/Injection_Prevention_in_Java_Cheat_Sheet.html)

[Server Side Request Forgery Prevention Cheat Sheet](cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html)

[XML External Entity Prevention Cheat Sheet](cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html)

### V1.4 Memory, String, and Unmanaged Code[¶](#v14-memory-string-and-unmanaged-code)

None.

### V1.5 Safe Deserialization[¶](#v15-safe-deserialization)

[Server Side Request Forgery Prevention Cheat Sheet](cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html)

[XML External Entity Prevention Cheat Sheet](cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html)

## V2: Validation and Business Logic[¶](#v2-validation-and-business-logic)

### V2.1 Validation and Business Logic Documentation[¶](#v21-validation-and-business-logic-documentation)

### V2.2 Input Validation[¶](#v22-input-validation)

[Microservices Security Cheat Sheet](cheatsheets/Microservices_Security_Cheat_Sheet.html)

[Web Service Security Cheat Sheet](cheatsheets/Web_Service_Security_Cheat_Sheet.html)

### V2.3 Business Logic Security[¶](#v23-business-logic-security)

### V2.4 Anti-automation[¶](#v24-anti-automation)

## V3: Web Frontend Security[¶](#v3-web-frontend-security)

### V3.1 Web Frontend Security Documentation[¶](#v31-web-frontend-security-documentation)

[Content Security Policy Cheat Sheet](cheatsheets/Content_Security_Policy_Cheat_Sheet.html)

[Cross-Site Request Forgery Prevention Cheat Sheet](cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html)

[HTTP Strict Transport Security Cheat Sheet](cheatsheets/HTTP_Strict_Transport_Security_Cheat_Sheet.html)

### V3.2 Unintended Content Interpretation[¶](#v32-unintended-content-interpretation)

[Cross-Site Request Forgery Prevention Cheat Sheet](cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html)

[DOM Clobbering Prevention Cheat Sheet](cheatsheets/DOM_Clobbering_Prevention_Cheat_Sheet.html)

[Third Party Javascript Management Cheat Sheet](cheatsheets/Third_Party_Javascript_Management_Cheat_Sheet.html)

### V3.3 Cookie Setup[¶](#v33-cookie-setup)

[Cross-Site Request Forgery Prevention Cheat Sheet](cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html)

[Session Management Cheat Sheet](cheatsheets/Session_Management_Cheat_Sheet.html)

[Transport Layer Security Cheat Sheet](cheatsheets/Transport_Layer_Security_Cheat_Sheet.html)

### V3.4 Browser Security Mechanism Headers[¶](#v34-browser-security-mechanism-headers)

[Cross-Site Request Forgery Prevention Cheat Sheet](cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html)

[HTTP Strict Transport Security Cheat Sheet](cheatsheets/HTTP_Strict_Transport_Security_Cheat_Sheet.html)

### V3.5 Browser Origin Separation[¶](#v35-browser-origin-separation)

[Cross-Site Request Forgery Prevention Cheat Sheet](cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html)

### V3.6 External Resource Integrity[¶](#v36-external-resource-integrity)

[Third Party Javascript Management Cheat Sheet](cheatsheets/Third_Party_Javascript_Management_Cheat_Sheet.html)

### V3.7 Other Browser Security Considerations[¶](#v37-other-browser-security-considerations)

[Cross-Site Request Forgery Prevention Cheat Sheet](cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html)

[HTTP Strict Transport Security Cheat Sheet](cheatsheets/HTTP_Strict_Transport_Security_Cheat_Sheet.html)

[Third Party Javascript Management Cheat Sheet](cheatsheets/Third_Party_Javascript_Management_Cheat_Sheet.html)

[Unvalidated Redirects and Forwards Cheat Sheet](cheatsheets/Unvalidated_Redirects_and_Forwards_Cheat_Sheet.html)

## V4: API and Web Service[¶](#v4-api-and-web-service)

### V4.1 Generic Web Service Security[¶](#v41-generic-web-service-security)

[Cross-Site Request Forgery Prevention Cheat Sheet](cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html)

[Transport Layer Security Cheat Sheet](cheatsheets/Transport_Layer_Security_Cheat_Sheet.html)

[Web Service Security Cheat Sheet](cheatsheets/Web_Service_Security_Cheat_Sheet.html)

### V4.2 HTTP Message Structure Validation[¶](#v42-http-message-structure-validation)

[Web Service Security Cheat Sheet](cheatsheets/Web_Service_Security_Cheat_Sheet.html)

### V4.3 GraphQL[¶](#v43-graphql)

### V4.4 WebSocket[¶](#v44-websocket)

[Transport Layer Security Cheat Sheet](cheatsheets/Transport_Layer_Security_Cheat_Sheet.html)

## V5: File Handling[¶](#v5-file-handling)

### V5.1 File Handling Documentation[¶](#v51-file-handling-documentation)

### V5.2 File Upload and Content[¶](#v52-file-upload-and-content)

### V5.3 File Storage[¶](#v53-file-storage)

[Server Side Request Forgery Prevention Cheat Sheet](cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html)

### V5.4 File Download[¶](#v54-file-download)

## V6: Authentication[¶](#v6-authentication)

### V6.1 Authentication Documentation[¶](#v61-authentication-documentation)

[Security Terminology Cheat Sheet](cheatsheets/Security_Terminology_Cheat_Sheet.html)

[Credential Stuffing Prevention Cheat Sheet](cheatsheets/Credential_Stuffing_Prevention_Cheat_Sheet.html)

### V6.2 Password Security[¶](#v62-password-security)

### V6.3 General Authentication Security[¶](#v63-general-authentication-security)

[Credential Stuffing Prevention Cheat Sheet](cheatsheets/Credential_Stuffing_Prevention_Cheat_Sheet.html)

### V6.4 Authentication Factor Lifecycle and Recovery[¶](#v64-authentication-factor-lifecycle-and-recovery)

[Choosing and Using Security Questions Cheat Sheet](cheatsheets/Choosing_and_Using_Security_Questions_Cheat_Sheet.html)

[Multifactor Authentication Cheat Sheet](cheatsheets/Multifactor_Authentication_Cheat_Sheet.html)

### V6.5 General Multi-factor authentication requirements[¶](#v65-general-multi-factor-authentication-requirements)

[Multifactor Authentication Cheat Sheet](cheatsheets/Multifactor_Authentication_Cheat_Sheet.html)

[Transaction Authorization Cheat Sheet](cheatsheets/Transaction_Authorization_Cheat_Sheet.html)

### V6.6 Out-of-Band authentication mechanisms[¶](#v66-out-of-band-authentication-mechanisms)

[Multifactor Authentication Cheat Sheet](cheatsheets/Multifactor_Authentication_Cheat_Sheet.html)

### V6.7 Cryptographic authentication mechanism[¶](#v67-cryptographic-authentication-mechanism)

[Multifactor Authentication Cheat Sheet](cheatsheets/Multifactor_Authentication_Cheat_Sheet.html)

### V6.8 Authentication with an Identity Provider[¶](#v68-authentication-with-an-identity-provider)

## V7: Session Management[¶](#v7-session-management)

[Session Management Cheat Sheet](cheatsheets/Session_Management_Cheat_Sheet.html)

### V7.1 Session Management Documentation[¶](#v71-session-management-documentation)

[Session Management Cheat Sheet](cheatsheets/Session_Management_Cheat_Sheet.html)

### V7.2 Fundamental Session Management Security[¶](#v72-fundamental-session-management-security)

[Session Management Cheat Sheet](cheatsheets/Session_Management_Cheat_Sheet.html)

### V7.3 Session Timeout[¶](#v73-session-timeout)

[Session Management Cheat Sheet](cheatsheets/Session_Management_Cheat_Sheet.html)

### V7.4 Session Termination[¶](#v74-session-termination)

[Session Management Cheat Sheet](cheatsheets/Session_Management_Cheat_Sheet.html)

### V7.5 Defenses Against Session Abuse[¶](#v75-defenses-against-session-abuse)

[Session Management Cheat Sheet](cheatsheets/Session_Management_Cheat_Sheet.html)

### V7.6 Federated Re-authentication[¶](#v76-federated-re-authentication)

[Session Management Cheat Sheet](cheatsheets/Session_Management_Cheat_Sheet.html)

## V8: Authorization[¶](#v8-authorization)

### V8.1 Authorization Documentation[¶](#v81-authorization-documentation)

[Security Terminology Cheat Sheet](cheatsheets/Security_Terminology_Cheat_Sheet.html)

[Authorization Testing Automation](cheatsheets/Authorization_Testing_Automation_Cheat_Sheet.html)

### V8.2 General Authorization Design[¶](#v82-general-authorization-design)

[Insecure Direct Object Reference Prevention Cheat Sheet](cheatsheets/Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet.html)

[Session Management Cheat Sheet](cheatsheets/Session_Management_Cheat_Sheet.html)

### V8.3 Operation Level Authorization[¶](#v83-operation-level-authorization)

[Transaction Authorization Cheat Sheet](cheatsheets/Transaction_Authorization_Cheat_Sheet.html)

### V8.4 Other Authorization Considerations[¶](#v84-other-authorization-considerations)

[Multi-Tenant Application Security Cheat Sheet](cheatsheets/Multi_Tenant_Security_Cheat_Sheet.html)

## V9: Self-contained Tokens[¶](#v9-self-contained-tokens)

### V9.1 Token source and integrity[¶](#v91-token-source-and-integrity)

### V9.2 Token content[¶](#v92-token-content)

## V10: OAuth and OIDC[¶](#v10-oauth-and-oidc)

### V10.1 Generic OAuth and OIDC Security[¶](#v101-generic-oauth-and-oidc-security)

### V10.2 OAuth Client[¶](#v102-oauth-client)

### V10.3 OAuth Resource Server[¶](#v103-oauth-resource-server)

[Transport Layer Security Cheat Sheet](cheatsheets/Transport_Layer_Security_Cheat_Sheet.html)

### V10.4 OAuth Authorization Server[¶](#v104-oauth-authorization-server)

[Transport Layer Security Cheat Sheet](cheatsheets/Transport_Layer_Security_Cheat_Sheet.html)

[Unvalidated Redirects and Forwards Cheat Sheet](cheatsheets/Unvalidated_Redirects_and_Forwards_Cheat_Sheet.html)

### V10.5 OIDC Client[¶](#v105-oidc-client)

### V10.6 OpenID Provider[¶](#v106-openid-provider)

### V10.7 Consent Management[¶](#v107-consent-management)

[Browser Extension Security Vulnerabilities](cheatsheets/Browser_Extension_Vulnerabilities_Cheat_Sheet.html)

## V11: Cryptography[¶](#v11-cryptography)

### V11.1 Cryptographic Inventory and Documentation[¶](#v111-cryptographic-inventory-and-documentation)

[Security Terminology Cheat Sheet](cheatsheets/Security_Terminology_Cheat_Sheet.html)

[Cryptographic Storage Cheat Sheet](cheatsheets/Cryptographic_Storage_Cheat_Sheet.html)

### V11.2 Secure Cryptography Implementation[¶](#v112-secure-cryptography-implementation)

[Cryptographic Storage Cheat Sheet](cheatsheets/Cryptographic_Storage_Cheat_Sheet.html)

### V11.3 Encryption Algorithms[¶](#v113-encryption-algorithms)

[Cryptographic Storage Cheat Sheet](cheatsheets/Cryptographic_Storage_Cheat_Sheet.html)

### V11.4 Hashing and Hash-based Functions[¶](#v114-hashing-and-hash-based-functions)

### V11.5 Random Values[¶](#v115-random-values)

[Cryptographic Storage Cheat Sheet](cheatsheets/Cryptographic_Storage_Cheat_Sheet.html)

### V11.6 Public Key Cryptography[¶](#v116-public-key-cryptography)

[Transport Layer Security Cheat Sheet](cheatsheets/Transport_Layer_Security_Cheat_Sheet.html)

### V11.7 In-Use Data Cryptography[¶](#v117-in-use-data-cryptography)

[Microservices Security Cheat Sheet](cheatsheets/Microservices_Security_Cheat_Sheet.html)

[Secrets Management Cheat Sheet](cheatsheets/Secrets_Management_Cheat_Sheet.html)

## V12: Secure Communication[¶](#v12-secure-communication)

### V12.1 General TLS Security Guidance[¶](#v121-general-tls-security-guidance)

[Transport Layer Security Cheat Sheet](cheatsheets/Transport_Layer_Security_Cheat_Sheet.html)

### V12.2 HTTPS Communication with External Facing Services[¶](#v122-https-communication-with-external-facing-services)

[Transport Layer Security Cheat Sheet](cheatsheets/Transport_Layer_Security_Cheat_Sheet.html)

### V12.3 General Service to Service Communication Security[¶](#v123-general-service-to-service-communication-security)

[Transport Layer Security Cheat Sheet](cheatsheets/Transport_Layer_Security_Cheat_Sheet.html)

## V13: Configuration[¶](#v13-configuration)

### V13.1 Configuration Documentation[¶](#v131-configuration-documentation)

[Server Side Request Forgery Prevention Cheat Sheet](cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html)

### V13.2 Backend Communication Configuration[¶](#v132-backend-communication-configuration)

[Server Side Request Forgery Prevention Cheat Sheet](cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html)

### V13.3 Secret Management[¶](#v133-secret-management)

[Cryptographic Storage Cheat Sheet](cheatsheets/Cryptographic_Storage_Cheat_Sheet.html)

### V13.4 Unintended Information Leakage[¶](#v134-unintended-information-leakage)

## V14: Data Protection[¶](#v14-data-protection)

### V14.1 Data Protection Documentation[¶](#v141-data-protection-documentation)

[Cryptographic Storage Cheat Sheet](cheatsheets/Cryptographic_Storage_Cheat_Sheet.html)

[User Privacy Protection Cheat Sheet](cheatsheets/User_Privacy_Protection_Cheat_Sheet.html)

### V14.2 General Data Protection[¶](#v142-general-data-protection)

[User Privacy Protection Cheat Sheet](cheatsheets/User_Privacy_Protection_Cheat_Sheet.html)

### V14.3 Client-side Data Protection[¶](#v143-client-side-data-protection)

## V15: Secure Coding and Architecture[¶](#v15-secure-coding-and-architecture)

### V15.1: Secure Coding and Architecture Documentation[¶](#v151-secure-coding-and-architecture-documentation)

[Security Terminology Cheat Sheet](cheatsheets/Security_Terminology_Cheat_Sheet.html)

[Attack Surface Analysis Cheat Sheet](cheatsheets/Attack_Surface_Analysis_Cheat_Sheet.html)

[Dependency Graph & SBOM Best Practices Cheat Sheet](cheatsheets/Dependency_Graph_SBOM_Cheat_Sheet.html)

[Software Supply Chain Security](cheatsheets/Software_Supply_Chain_Security_Cheat_Sheet.html)

[Third Party Javascript Management Cheat Sheet](cheatsheets/Third_Party_Javascript_Management_Cheat_Sheet.html)

### V15.2: Security Architecture and Dependencies[¶](#v152-security-architecture-and-dependencies)

[Software Supply Chain Security](cheatsheets/Software_Supply_Chain_Security_Cheat_Sheet.html)

[Third Party Javascript Management Cheat Sheet](cheatsheets/Third_Party_Javascript_Management_Cheat_Sheet.html)

[Vulnerable Dependency Management Cheat Sheet](cheatsheets/Vulnerable_Dependency_Management_Cheat_Sheet.html)

### V15.3: Defensive Coding[¶](#v153-defensive-coding)

[Prototype Pollution Prevention Cheat Sheet](cheatsheets/Prototype_Pollution_Prevention_Cheat_Sheet.html)

[Unvalidated Redirects and Forwards Cheat Sheet](cheatsheets/Unvalidated_Redirects_and_Forwards_Cheat_Sheet.html)

### V15.4: Safe Concurrency[¶](#v154-safe-concurrency)

[Secure Code Review Cheat Sheet](cheatsheets/Secure_Code_Review_Cheat_Sheet.html)

[Transaction Authorization Cheat Sheet](cheatsheets/Transaction_Authorization_Cheat_Sheet.html)

## V16: Security Logging and Error Handling[¶](#v16-security-logging-and-error-handling)

### V16.1: Security Logging Documentation[¶](#v161-security-logging-documentation)

[Logging Vocabulary Cheat Sheet](cheatsheets/Logging_Vocabulary_Cheat_Sheet.html)

### V16.2: General Logging[¶](#v162-general-logging)

[Session Management Cheat Sheet](cheatsheets/Session_Management_Cheat_Sheet.html)

### V16.3: Security Events[¶](#v163-security-events)

[Logging Vocabulary Cheat Sheet](cheatsheets/Logging_Vocabulary_Cheat_Sheet.html)

### V16.4: Log Protection[¶](#v164-log-protection)

### V16.5: Error Handling[¶](#v165-error-handling)

## V17: WebRTC[¶](#v17-webrtc)

### V17.1 TURN Server[¶](#v171-turn-server)

None.

## V17.2 Media[¶](#v172-media)

[Transport Layer Security Cheat Sheet](cheatsheets/Transport_Layer_Security_Cheat_Sheet.html)

## V17.3 Signaling[¶](#v173-signaling)

None.
