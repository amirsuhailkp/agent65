---
title: OWASP Top 10 Drone Security Risks
source: owasp.org
url: https://owasp.org/www-project-top-10-drone-security-risks/
collector: owasp
category: web-security
tags:
- web-security
- drone
- security
- risk
- data
date_collected: '2026-07-26T12:45:59.071112Z'
language: unknown
---

# OWASP Top 10 Drone Security Risks

Creating an “OWASP Drone Top 10 Security Risks” list involves adapting the known security vulnerabilities from the mobile and web application domain to the specific context of drones. Drones, or unmanned aerial vehicles (UAVs), introduce unique challenges due to their physical mobility, the diversity of their applications, and their often complex interaction with hardware and software systems. Here’s a tailored list that mirrors the structure and intent behind the original OWASP Mobile Top 10, focusing on the unique aspects of drone technology:

- Insecure Communication Risk: Transmission of data over unsecured channels, allowing interception or modification of sensitive information (e.g., video feeds, control commands). Mitigation: Implement end-to-end encryption for data transmission, use secure protocols like TLS.
- Weak Authentication/Authorization Risk: Inadequate authentication allows unauthorized access to drone controls or sensitive data. Mitigation: Strong, multi-factor authentication and role-based access control systems.
- Insecure Firmware/Software Risk: Vulnerabilities in the drone’s firmware or software can be exploited to gain unauthorized access or control. Mitigation: Regular updates, secure development practices, and vulnerability scanning.
- Inadequate Personal Data Protection Risk: Drones collecting personal data without proper safeguards or consent. Mitigation: Implement data protection measures, respect privacy norms, and ensure compliance with relevant regulations (e.g., GDPR).
- Lack of Secure Update Mechanism Risk: An insecure update process could introduce malware or unauthorized modifications. Mitigation: Signed firmware/software updates, secure update protocols, and integrity verification.
- Insecure Third-party Components Risk: Use of vulnerable third-party components (e.g., libraries, modules) can compromise drone security. Mitigation: Careful vetting of third-party components, keeping them up-to-date, and monitoring for disclosed vulnerabilities.
- Insufficient Network Security Risk: Vulnerabilities in the drone’s network services (Wi-Fi, Bluetooth) can lead to unauthorized access. Mitigation: Strong network encryption, secure network configuration, and disabling unnecessary services.
- Physical Security Weaknesses Risk: Physical tampering with the drone or its components to gain unauthorized access or control. Mitigation: Tamper detection and prevention mechanisms, secure hardware design, and access controls.
- Insecure Data Storage Risk: Sensitive data stored on the drone (e.g., location history, captured images) is not adequately protected. Mitigation: Encryption of stored data, secure data storage practices, and options for remote wipe if necessary.
- Lack of Logging and Monitoring Risk: Insufficient logging and monitoring can hinder the detection of security breaches or unauthorized activities. Mitigation: Implement comprehensive logging and real-time monitoring systems, with alerts for suspicious activities.

### Road Map

Intro April 2024 Initial version December 2024.

## Example

Put whatever you like here: news, screenshots, features, supporters, or remove this file and don’t use tabs at all.
