---
title: A05:2021 – Sicherheitsrelevante Fehlkonfiguration
source: owasp.org
url: https://owasp.org/Top10/2021/de/A05_2021-Security_Misconfiguration/
collector: owasp
category: web-security
tags:
- web-security
- die
- und
- oder
- der
date_collected: '2026-07-25T14:26:32.949384Z'
language: unknown
---

# A05:2021 – Sicherheitsrelevante Fehlkonfiguration

## Beurteilungskriterien

Zugeordnete CWEsMaximale HäufigkeitDurchschn. HäufigkeitDurchschn. Ausnutzbarkeit (gewichtet)Durchschn. Auswirkungen (gewichtet)Maximale AbdeckungDurchschnittliche AbdeckungGesamtanzahlCVEs insgesamt2019.84 %4.51 %8.126.5689.58 %44.84 %208,387789

## Übersicht

Die Kategorie rückt auf von Platz 6 in der vorherigen Ausgabe:
90 % der Anwendungen wurden auf irgendeine Form von Fehlkonfiguration getestet, mit einer durchschnittlichen Inzidenzrate von 4 % und über 208.000 Vorkommen einer Common Weakness Enumeration (CWE) in dieser Risikokategorie. Angesichts der zunehmenden Verlagerung hin zu hoch konfigurierbarer Software ist es nicht verwunderlich, dass diese Kategorie aufsteigt. Bemerkenswerte enthaltene CWEs sind *CWE-16 Configuration* und *CWE-611 Unproper Restriction of XML External Entity Reference*.

## Beschreibung

Die Anwendung besitzt möglicherweise Schwachstellen, wenn folgendes zutrifft:

- Mangelhafte Sicherheitshärtung des Anwendungsstacks oder ungeeignet konfigurierte Berechtigungen auf Cloud-Diensten.
- Nicht benötigte Features sind aktiviert oder installiert (z. B. unnötige Ports, Dienste, Seiten, Accounts oder Rechte).
- Standardkonten und -passwörter sind aktiviert bzw. unverändert.
- Die Fehlerbehandlung gibt Stack-Traces oder andere interne technische Fehlermeldungen an Anwendende preis.
- Für aktualisierte Systeme sind die neuesten Sicherheitsfeatures deaktiviert oder nicht sicher konfiguriert.
- Die Sicherheitseinstellungen in den Anwendungsservern und -frameworks (z. B. Struts, Spring, ASP.NET), Bibliotheken, Datenbanken etc. sind nicht auf sichere Werte gesetzt.
- Der Server sendet keine Sicherheits-Header oder -Direktiven, bzw. diese sind nicht sicher konfiguriert.
- Die Software ist veraltet oder verwundbar (siehe

  [A06:2021-Unsichere oder veraltete Komponenten](../A06_2021-Vulnerable_and_Outdated_Components/)).

Ohne einen abgestimmten und reproduzierbaren Prozess zur sicheren Konfiguration sind Systeme einem höheren Risiko ausgesetzt!

## Prävention und Gegenmaßnahmen

Es sollten sichere Installationsprozesse implementiert werden, darunter:

- Ein wiederholbarer Härtungsprozess ermöglicht die schnelle und einfache Bereitstellung zusätzlicher Umgebungen, die entsprechend abgesichert sind. Entwicklungs-, Qualitätssicherungs- und Produktionsumgebungen sollten alle identisch konfiguriert sein, wobei in jeder Umgebung unterschiedliche Anmeldeinformationen verwendet werden sollten. Dieser Prozess sollte automatisiert werden, um den Aufwand für die Einrichtung einer neuen sicheren Umgebung zu minimieren.
- Eine minimale Plattform ohne unnötige Funktionen, Komponenten, Dokumentation und Beispiele: Entfernen Sie Funktionen und Frameworks die Sie nicht verwenden oder installieren Sie diese erst gar nicht.
- Überprüfen und Aktualisieren der Konfigurationen, die für alle Sicherheitshinweise, Updates und Patches im Rahmen des Patch-Verwaltungsprozesses geeignet sind (siehe

  [A06:2021-Unsichere oder veraltete Komponenten](../A06_2021-Vulnerable_and_Outdated_Components/)). Überprüfen Sie die Cloud-Speicherberechtigungen (z. B. S3-Bucket-Berechtigungen).
- Eine segmentierte Anwendungsarchitektur sorgt durch Segmentierung, Containerisierung oder Cloud-Sicherheitsgruppen (ACLs) für eine effektive und sichere Trennung zwischen Komponenten oder Mandanten.
- Senden von Sicherheitsanweisungen an Clients, z. B. Sicherheits-Header.
- Ein automatisierter Prozess zur Überprüfung der Wirksamkeit der Konfigurationen und Einstellungen in allen Umgebungen.

## Beispielhafte Angriffsszenarien

**Szenario Nr. 1:** Der Anwendungsserver wird mit Beispielanwendungen geliefert, die nicht vom Produktionsserver entfernt wurden. Diese Beispielanwendungen weisen bekannte Sicherheitslücken auf, die Angreifende nutzen, um den Server zu gefährden. Angenommen, eine dieser Anwendungen ist die Admin-Konsole und die Standardkonten wurden nicht geändert. In diesem Fall meldet sich die angreifende Person mit Standardkennwörtern an und übernimmt die Kontrolle.

**Szenario Nr. 2:** Die Directory Listings wurden auf dem Server nicht deaktiviert. Angreifende entdecken, dass Verzeichnisse einfach aufgelistet werden können. Die angreifende Person findet die kompilierten Java-Klassen und lädt sie herunter, dekompiliert sie und betreibt Reverse Engineering, um den Code anzuzeigen. Dies ermöglicht das Findet eines schwerwiegenden Fehlers in der Zugriffskontrolle in der Anwendung.

**Szenario Nr. 3:** Die Konfiguration des Anwendungsservers ermöglicht die Rückgabe detaillierter Fehlermeldungen an Anwendende, z. B. Stack-Traces. Dadurch werden möglicherweise vertrauliche Informationen oder zugrunde liegende Fehler wie Komponentenversionen offengelegt, die bekanntermaßen anfällig sind.

**Szenario Nr. 4:** Ein Cloud-Dienstanbieter (CSP) enthält Standardfreigaben, die aus dem Internet für andere Cloud-Nutzende erreichbar sind und ermöglicht dadurch Zugriff auf sensitive Daten in der Cloud.

## Referenzen

- [OWASP Web Security Testing Guide: Configuration and Deployment Management Testing](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/02-Configuration_and_Deployment_Management_Testing/index)
- [OWASP Web Security Testing Guide: Testing for Error Handling](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/08-Testing_for_Error_Handling/index)
- [OWASP Application Security Verification Standard (ASVS): V14 Configuration](https://github.com/OWASP/ASVS/blob/master/4.0/en/0x22-V14-Config.md#4-0-14)
- [NIST Computer Security Resource Center: SP 800-123: Guide to General Server Security](https://csrc.nist.gov/publications/detail/sp/800-123/final)
- [CIS Security Configuration Guides/Benchmarks](https://www.cisecurity.org/cis-benchmarks/)
- [AWS S3 Bucket Discovery](https://blog.websecurify.com/2017/10/aws-s3-bucket-discovery)

## Liste der zugeordneten CWEs

- [CWE-2: 7PK - Environment (CWE CATEGORY)](https://cwe.mitre.org/data/definitions/2.html)
- [CWE-11: ASP.NET Misconfiguration: Creating Debug Binary](https://cwe.mitre.org/data/definitions/11.html)
- [CWE-13: ASP.NET Misconfiguration: Password in Configuration File](https://cwe.mitre.org/data/definitions/13.html)
- [CWE-15: External Control of System or Configuration Setting](https://cwe.mitre.org/data/definitions/15.html)
- [CWE-16: Configuration (CWE CATEGORY)](https://cwe.mitre.org/data/definitions/16.html)
- [CWE-260: Password in Configuration File](https://cwe.mitre.org/data/definitions/260.html)
- [CWE-315: Cleartext Storage of Sensitive Information in a Cookie](https://cwe.mitre.org/data/definitions/315.html)
- [CWE-520: .NET Misconfiguration: Use of Impersonation](https://cwe.mitre.org/data/definitions/520.html)
- [CWE-526: Cleartext Storage of Sensitive Information in an Environment Variable](https://cwe.mitre.org/data/definitions/526.html)
- [CWE-537: Java Runtime Error Message Containing Sensitive Information](https://cwe.mitre.org/data/definitions/537.html)
- [CWE-611: Improper Restriction of XML External Entity Reference](https://cwe.mitre.org/data/definitions/611.html)
- [CWE-614: Sensitive Cookie in HTTPS Session Without 'Secure' Attribute](https://cwe.mitre.org/data/definitions/614.html)
- [CWE-756: Missing Custom Error Page](https://cwe.mitre.org/data/definitions/756.html)
- [CWE-776: Improper Restriction of Recursive Entity References in DTDs ('XML Entity Expansion')](https://cwe.mitre.org/data/definitions/776.html)
- [CWE-942: Permissive Cross-domain Policy with Untrusted Domains](https://cwe.mitre.org/data/definitions/942.html)
- [CWE-1004: Sensitive Cookie Without 'HttpOnly' Flag](https://cwe.mitre.org/data/definitions/1004.html)
- [CWE-1032: OWASP Top Ten 2017 Category A6 - Security Misconfiguration (CWE CATEGORY)](https://cwe.mitre.org/data/definitions/1032.html)
- [CWE-1174: ASP.NET Misconfiguration: Improper Model Validation](https://cwe.mitre.org/data/definitions/1174.html)
