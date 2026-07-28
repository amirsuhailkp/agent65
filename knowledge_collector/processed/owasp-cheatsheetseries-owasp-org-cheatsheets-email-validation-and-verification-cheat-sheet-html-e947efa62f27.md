---
title: Email Validation and Verification in Identity Systems Cheat Sheet¶
source: cheatsheetseries.owasp.org
url: https://cheatsheetseries.owasp.org/cheatsheets/Email_Validation_and_Verification_Cheat_Sheet.html
collector: owasp
category: web-security
tags:
- web-security
- email
- verification
- recommendations
- reset
date_collected: '2026-07-26T12:36:25.588656Z'
language: unknown
---

# Email Validation and Verification in Identity Systems Cheat Sheet[¶](#email-validation-and-verification-in-identity-systems-cheat-sheet)

## Introduction[¶](#introduction)

Email addresses are widely used as primary identifiers in authentication and account recovery workflows. Improper handling of email validation, normalization, and verification can lead to account takeover, user enumeration, and identity confusion.

This cheat sheet provides guidance on securely handling email addresses within identity systems.

## Goals[¶](#goals)

- Safely treat email as an identifier
- Prevent account takeover via email-based flows
- Reduce user enumeration risk
- Define secure verification and change workflows

## Threat Model[¶](#threat-model)

Attackers may attempt to:

- Register equivalent or visually similar email addresses
- Exploit inconsistent normalization logic
- Abuse password reset functionality
- Enumerate valid accounts
- Take over accounts through email change workflows

## Email Canonicalization[¶](#email-canonicalization)

Applications must define a consistent normalization strategy before storing or comparing email addresses.

### Recommendations[¶](#recommendations)

- Normalize the domain portion to lowercase
- Avoid provider-specific transformations (e.g., Gmail dot removal) unless fully controlled
- Store both:
  - Original input (for display and communication)
  - Canonical form (for comparison according to your policy)
- Document the comparison policy explicitly and apply it consistently across registration, login, password reset, account recovery, and account linking flows

## Email Format Validation[¶](#email-format-validation)

Strict regex-based validation often rejects valid addresses or introduces inconsistencies.

### Recommendations[¶](#recommendations_1)

- Use well-tested libraries instead of custom regex
- Accept a broad range of valid formats
- Reject clearly malformed input only

## Unicode and IDN Considerations[¶](#unicode-and-idn-considerations)

Unicode introduces spoofing risks via visually similar characters.

### Recommendations[¶](#recommendations_2)

- Normalize Unicode input
- Convert internationalized domains to punycode for comparison
- Be aware of homoglyph attacks (e.g., Latin vs Cyrillic characters)
- Be especially cautious with internationalized local-parts, because normalization and comparison behavior may differ across systems

## Case Sensitivity[¶](#case-sensitivity)

- Domain part: always case-insensitive
- Local part: technically case-sensitive under SMTP, though many providers do not enforce this in practice

### Recommendation[¶](#recommendation)

- Preserve the original email address as entered by the user
- Define an explicit comparison policy for the local part based on your identity architecture and interoperability requirements
- Only fold or normalize the local part when the system fully owns that behavior and the decision will not create account-collision or mistaken-account risk

## Email Ownership Verification[¶](#email-ownership-verification)

Email ownership must be verified before enabling account use.

### Recommendations[¶](#recommendations_3)

- Use cryptographically secure, random tokens
- Ensure tokens are:
  - Single-use
  - Time-limited
- Do not activate accounts before verification is completed

## Password Reset Flows[¶](#password-reset-flows)

Password reset is a high-risk operation.

### Recommendations[¶](#recommendations_4)

- Use single-use, time-limited tokens
- Do not disclose whether an email exists in the system
- Invalidate tokens after use or expiration
- Rate limit reset requests

## Email Change Workflows[¶](#email-change-workflows)

Changing an email address is equivalent to changing identity.

### Recommendations[¶](#recommendations_5)

- Require re-authentication
- Notify the existing email address of the change
- Require confirmation of the new email address
- Consider requiring confirmation from both addresses for high-risk systems

## Anti-Enumeration Controls[¶](#anti-enumeration-controls)

Attackers should not be able to determine whether an email is registered.

### Recommendations[¶](#recommendations_6)

- Use consistent responses for login and reset flows
- Avoid timing discrepancies between valid and invalid cases
- Implement rate limiting and monitoring

## Temporary Email Abuse[¶](#temporary-email-abuse)

Disposable email services can be used to bypass controls.

### Recommendations[¶](#recommendations_7)

- Maintain a list of known disposable domains if appropriate
- Prefer risk-based controls over strict blocking
- Monitor for suspicious patterns of account creation

## Email as an Authentication Factor[¶](#email-as-an-authentication-factor)

Email should not be treated as a strong authentication factor.

### Recommendations[¶](#recommendations_8)

- Treat email as a weak factor
- Require multi-factor authentication (MFA) for sensitive operations
- Do not rely on email alone for account security

## Logging and Monitoring[¶](#logging-and-monitoring)

Monitoring email-related flows helps detect abuse.

### Recommendations[¶](#recommendations_9)

- Log verification attempts and failures
- Monitor password reset activity
- Detect abnormal patterns (e.g., high-frequency requests)
- Avoid logging full email addresses; mask or pseudonymize them where logging is necessary (e.g.,
  ```
  j***@example.com
  ```

  )
- Never log verification, reset, or authentication tokens or full verification/reset URLs
- Treat email addresses and related identifiers in logs as personal or sensitive data and restrict access accordingly
