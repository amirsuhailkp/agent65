---
title: A07:2021 – Fehlerhafte Authentifizierung
source: owasp.org
url: https://owasp.org/Top10/2021/de/A07_2021-Identification_and_Authentication_Failures/
collector: owasp
category: web-security
tags:
- web-security
- die
- und
- authentication
- oder
date_collected: '2026-07-25T14:26:34.935349Z'
language: unknown
---

# A07:2021 – Fehlerhafte Authentifizierung

## Beurteilungskriterien

Zugeordnete CWEsMaximale HäufigkeitDurchschn. HäufigkeitDurchschn. Ausnutzbarkeit (gewichtet)Durchschn. Auswirkungen (gewichtet)Maximale AbdeckungDurchschnittliche AbdeckungGesamtanzahlCVEs insgesamt2214.84 %2.55 %7.406.5079.51 %45.72 %132,1953,897

## Übersicht

Diese Kategorie, die früher als *Broken Authentication* bekannt war, rutschte von der zweiten Position nach unten und umfasst nun Common Weakness Enumerations (CWEs) im Zusammenhang mit Identifikationsfehlern. Die bedeutendsten CWEs sind

## Beschreibung

Die Überprüfung der Identität des Nutzenden, die Authentifizierung und die Sitzungsverwaltung sind entscheidend für den Schutz vor authentifizierungsbezogenen Angriffen. Schwachstellen bei der Authentifizierung können auftreten, falls die Anwendung:

- automatisierte Angriffe wie Credential Stuffing zulässt, bei dem Angreifende über eine Liste gültiger Usernamen und Passwörter verfügen.
- Brute-Force- oder andere automatisierte Angriffe ermöglicht.
- Standard-, schwache oder gängige Passwörter zulässt, wie z. B. "Passwort1" oder "admin/admin".
- schwache oder ineffektive Verfahren zur Wiederherstellung von Anmeldeinformationen und Verfahren für vergessene Passwörtern, wie z. B. „wissensbasierte Antworten“, die nicht sicher gemacht werden können, verwendet werden.
- Klartext-, verschlüsselte oder schwach gehashte Kennwortdatenspeicher (siehe

  [A02:2021-Cryptographic Failures](../A02_2021-Cryptographic_Failures/)) verwendet.
- Fehlende oder unwirksame Multi-Faktor-Authentifizierung.
- Die Session-ID wird in der URL angezeigt.
- Session-IDs nach erfolgreichem Login wieder verwendet werden.
- Session-IDs werden nicht korrekt ungültig gemacht. Sitzungen von Benutzenden (user sessions) oder Authentifizierungs-Tokens (hauptsächlich Single Sign-On (SSO) Tokens) werden beim Abmelden oder bei Inaktivität nicht ordnungsgemäß invalidiert.

## Prävention und Gegenmaßnahmen

- Wenn möglich, sollte eine Multi-Faktor-Authentifizierung implementiert werden, um automatisiertes Credential Stuffing, Brute Force-Angriffe und die Wiederverwendung gestohlener Zugangsdaten zu verhindern.
- Liefern Sie die Anwendung nicht mit Standard Login-Daten aus, insbesondere nicht für Administrator-Konten.
- Implementieren Sie Prüfungen auf schwache Passwörter, wie z. B. durch den Vergleich von neuen oder geänderten Passwörtern mit der Liste der 10.000 schlechtesten Passwörter.
- Angleichung der Passwortlänge, -komplexität und -rotation an die Richtlinien des National Institute of Standards and Technology (NIST) 800-63b in Abschnitt 5.1.1 "Memorized Secrets" oder andere modernen, bewährten Passwortrichtlinien.
- Sicherstellen, dass die Registrierung, die Wiederherstellung von Zugangsdaten und die API-Pfade gegen Angriffe zur Ermittlung von Konten gehärtet sind, indem für alle Resultate die gleiche Nachricht ausgegeben wird.
- Begrenzen oder bremsen Sie fehlgeschlagene Anmeldeversuche immer weiter aus, aber achten Sie darauf, dass hierbei kein Denial-of-Service-Szenario entsteht. Loggen Sie alle Fehlversuche und alarmieren Sie die Administratoren, wenn Credential Stuffing, Brute Force oder andere Angriffe erkannt werden.
- Verwenden Sie einen serverseitigen, sicheren, integrierten Sitzungsmanager, der für jede Sitzung eine neue zufällige Sitzungs-ID mit hoher Entropie erzeugt. Die Sitzungs-ID sollte nicht in der URL enthalten sein, sicher gespeichert werden und nach Abmeldung, Inaktivität und Absoluten Timeouts entwertet werden.

## Beispielhafte Angriffsszenarien

**Szenario Nr. 1:** Credential Stuffing, die Verwendung von Listen mit bekannten Kennwörtern, ist ein gängiger Angriff. Angenommen, eine Anwendung verfügt keinen automatischen Schutz vor Bedrohungen oder Credential Stuffing. In diesem Fall kann die Anwendung als Passwort-Orakel verwendet werden, um festzustellen, ob die Anmeldeinformationen gültig sind.

**Szenario #2:** Die meisten Authentifizierungsangriffe erfolgen aufgrund der andauernden Verwendung von Kennwörtern als einzigem Zugangsmerkmal. Die früher als Best Practices geltenden Anforderungen an den Wechsel und die Komplexität von Passwörtern verleiten die Nutzende zur Verwendung und Wiederverwendung schwacher Passwörter. Organisationen wird empfohlen, diese Praktiken gemäß NIST 800-63 einzustellen und eine Mehrfaktor-Authentifizierung zu verwenden.

**Szenario #3:** Die Session-Timeouts von Anwendungen sind nicht korrekt gesetzt. Eine Nutzerin/Nutzer verwendet einen öffentlichen Computer, um auf eine Anwendung zuzugreifen. Anstatt sich abzumelden, schließt die nutzende Person einfach die Browser-Registerkarte und geht weg. Angreifende verwenden denselben Browser eine Stunde später, und die Nutzerin/Nutzer ist noch immer authentifiziert.

## Referenzen

- [OWASP Proactive Controls: C6: Implement Digital Identity](https://github.com/OWASP/www-project-proactive-controls/blob/master/v3/en/c6-digital-identity.md)
- [OWASP Application Security Verification Standard (ASVS): V2 Authentication](https://github.com/OWASP/ASVS/blob/master/4.0/en/0x11-V2-Authentication.md#4-0-2)
- [OWASP Application Security Verification Standard (ASVS): V3 Session Management](https://github.com/OWASP/ASVS/blob/master/4.0/en/0x12-V3-Session-management.md#4-0-3)
- [OWASP Web Security Testing Guide: Identity Management Testing](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/03-Identity_Management_Testing/index),[Authentication Testing](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/04-Authentication_Testing/index)
- [OWASP Cheat Sheet Series: Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet)
- [OWASP Cheat Sheet Series: Credential Stuffing Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Credential_Stuffing_Prevention_Cheat_Sheet)
- [OWASP Cheat Sheet Series: Forgot Password Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet)
- [OWASP Cheat Sheet Series: Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet)
- [OWASP Automated Threats to Web Applications](https://owasp.org/www-project-automated-threats-to-web-applications/)
- [NIST SP 800-63b: Digital Identity Guidelines: Authentication and Lifecycle Management: 5.1.1 Memorized Secrets](https://pages.nist.gov/800-63-3/sp800-63b.html#memsecret)

## Liste der zugeordneten CWEs

- [CWE-255: Credentials Management Errors (CWE CATEGORY)](https://cwe.mitre.org/data/definitions/255.html)
- [CWE-259: Use of Hard-coded Password](https://cwe.mitre.org/data/definitions/259.html)
- [CWE-287: Improper Authentication](https://cwe.mitre.org/data/definitions/287.html)
- [CWE-288: Authentication Bypass Using an Alternate Path or Channel](https://cwe.mitre.org/data/definitions/288.html)
- [CWE-290: Authentication Bypass by Spoofing](https://cwe.mitre.org/data/definitions/290.html)
- [CWE-294: Authentication Bypass by Capture-replay](https://cwe.mitre.org/data/definitions/294.html)
- [CWE-295: Improper Certificate Validation](https://cwe.mitre.org/data/definitions/295.html)
- [CWE-297: Improper Validation of Certificate with Host Mismatch](https://cwe.mitre.org/data/definitions/297.html)
- [CWE-300: Channel Accessible by Non-Endpoint](https://cwe.mitre.org/data/definitions/300.html)
- [CWE-302: Authentication Bypass by Assumed-Immutable Data](https://cwe.mitre.org/data/definitions/302.html)
- [CWE-304: Missing Critical Step in Authentication](https://cwe.mitre.org/data/definitions/304.html)
- [CWE-306: Missing Authentication for Critical Function](https://cwe.mitre.org/data/definitions/306.html)
- [CWE-307: Improper Restriction of Excessive Authentication Attempts](https://cwe.mitre.org/data/definitions/307.html)
- [CWE-346: Origin Validation Error](https://cwe.mitre.org/data/definitions/346.html)
- [CWE-384: Session Fixation](https://cwe.mitre.org/data/definitions/384.html)
- [CWE-521: Weak Password Requirements](https://cwe.mitre.org/data/definitions/521.html)
- [CWE-613: Insufficient Session Expiration](https://cwe.mitre.org/data/definitions/613.html)
- [CWE-620: Unverified Password Change](https://cwe.mitre.org/data/definitions/620.html)
- [CWE-640: Weak Password Recovery Mechanism for Forgotten Password](https://cwe.mitre.org/data/definitions/640.html)
- [CWE-798: Use of Hard-coded Credentials](https://cwe.mitre.org/data/definitions/798.html)
- [CWE-940: Improper Verification of Source of a Communication Channel](https://cwe.mitre.org/data/definitions/940.html)
- [CWE-1216: Lockout Mechanism Errors (CWE CATEGORY)](https://cwe.mitre.org/data/definitions/1216.html)
