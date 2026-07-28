---
title: A08:2021 – Fehlerhafte Prüfung der Software- und Datenintegrität
source: owasp.org
url: https://owasp.org/Top10/2021/de/A08_2021-Software_and_Data_Integrity_Failures/
collector: owasp
category: web-security
tags:
- web-security
- und
- der
- eine
- die
date_collected: '2026-07-25T14:26:36.696586Z'
language: unknown
---

# A08:2021 – Fehlerhafte Prüfung der Software- und Datenintegrität

## Beurteilungskriterien

Zugeordnete CWEsMaximale HäufigkeitDurchschn. HäufigkeitDurchschn. Ausnutzbarkeit (gewichtet)Durchschn. Auswirkungen (gewichtet)Maximale AbdeckungDurchschnittliche AbdeckungGesamtanzahlCVEs insgesamt1016.67 %2.05 %6.947.9475.04 %45.35 %47,9721,152

## Übersicht

Bei der neuen Kategorie für 2021 liegt der Schwerpunkt auf Annahmen in Bezug auf Software-Updates, relevante Daten und CI/CD-Pipelines ohne Überprüfung der Integrität. Eine der am höchsten gewichteten Auswirkungen von Common Vulnerability and Exposures/Common Vulnerability Scoring System (CVE/CVSS) Daten. Zu den erwähnenswerten Common Weakness Enumerations (CWEs) gehören:
*CWE-829: Inclusion of Functionality from Untrusted Control Sphere*,
*CWE-494: Download of Code Without Integrity Check* und
*CWE-502: Deserialization of Untrusted Data*.

## Beschreibung

Software- und Datenintegritätsfehler beziehen sich auf Code und Infrastruktur, die keine Schutzmaßnahmen gegen Integritätsverletzungen bieten. Ein Beispiel hierfür ist, wenn eine Anwendung auf Plugins, Bibliotheken oder Module aus nicht vertrauenswürdigen Quellen, Repositories und Content Delivery Networks (CDNs) angewiesen ist. Eine unsichere CI/CD-Pipeline kann das Potenzial für unbefugten Zugriff, bösartigen Code oder Systemkompromittierung bieten. Schließlich enthalten viele Anwendungen heute eine automatische Update-Funktion, bei der Updates ohne ausreichende Integritätsprüfung heruntergeladen und auf die zuvor vertrauenswürdige Anwendung angewendet werden. Angreifende könnten ihre eigenen Updates hochladen, die dann auf alle Installationen verbreitet und ausgeführt werden. Ein weiteres Beispiel besteht darin, dass Objekte oder Daten in eine Struktur kodiert oder serialisiert werden, die Angreifende sehen und ändern können, und die durch eine unsichere Deserialisierung verwundbar sind.

## Prävention und Gegenmaßnahmen

- Verwenden Sie digitale Signaturen oder ähnliche Mechanismen, um sicherzustellen, dass die Software oder Daten aus der erwarteten Quelle stammen und nicht verändert wurden.
- Stellen Sie sicher, dass Bibliotheken und Abhängigkeiten, wie z. B. npm oder Maven, vertrauenswürdige Repositories nutzen. Wenn Sie ein höheres Risikoprofil haben, sollten Sie in Erwägung ziehen, ein internes Repository zu hosten, das als vertrauenswürdig gilt und überprüft wurde.
- Stellen Sie sicher, dass ein Software-Supply-Chain-Sicherheitstool wie OWASP Dependency Check oder OWASP CycloneDX verwendet wird, um zu überprüfen, dass Komponenten keine bekannten Schwachstellen enthalten.
- Stellen Sie sicher, dass es einen Überprüfungsprozess für Code- und Konfigurationsänderungen gibt, um das Risiko zu minimieren, dass bösartiger Code oder bösartige Konfigurationen in Ihre Software-Pipeline eingeschleust werden.
- Stelle Sie sicher, dass Ihre CI/CD-Pipeline über eine angemessene Trennung, Konfiguration und Zugriffskontrolle verfügt, um die Integrität des Codes zu gewährleisten, der den Build- und Bereitstellungsprozess durchläuft.
- Stellen Sie sicher, dass unsignierte oder unverschlüsselte serialisierte Daten nicht an nicht vertrauenswürdige Clients ohne eine Form der Integritätsprüfung oder digitalen Signatur gesendet werden, um dadurch eine Manipulation oder ein erneutes Versenden der serialisierten Daten zu erkennen.

## Beispielhafte Angriffsszenarien

**Szenario Nr. 1: Update ohne Signierung:** Viele Heimrouter, Set-Top-Boxen, Geräte-Firmware und Andere verifizieren Updates nicht über signierte Firmware. Unsignierte Firmware ist ein wachsendes Ziel für Angreifende, und es wird erwartet, dass es in Zukunft noch schlimmer werden wird. Dies ist besonders besorgniserregend, da es in vielen Fällen keinen anderen Mechanismus zur Behebung gibt, als die Fehler in einer zukünftigen Version zu beheben und zu warten, bis die vorherigen Versionen veraltet sind.

**Szenario #2 SolarWinds bösartiges Update**: Nationalstaaten sind dafür bekannt, dass sie Update-Mechanismen angreifen. Ein bemerkenswerter Angriff war vor kurzem der SolarWinds-Orion-Angriff. Das Unternehmen, das die Software entwickelt, verfügte über sichere Build- und Update-Integritätsprozesse. Dennoch konnten diese unterwandert werden, und das Unternehmen verteilte über mehrere Monate hinweg ein sehr gezieltes bösartiges Update an mehr als 18.000 Organisationen, von denen etwa 100 betroffen waren. Dies ist eine der weitreichendsten und bedeutendsten Sicherheitsverletzungen dieser Art in der Geschichte.

**Szenario #3 Unsichere Deserialisierung:** Eine React-Anwendung ruft eine Reihe von Spring Boot Microservices auf. Als funktionale Programmierer versuchten sie sicherzustellen, dass ihr Code unveränderlich ist. Die Lösung, die sie gefunden haben, besteht darin, den Sitzungszustand zu serialisieren und ihn mit jeder Anfrage hin und her zu schicken. Eine angreifende Person bemerkt die "`rO0" Java-Objektsignatur (in base64) und verwendet das Java Serial Killer-Tool, um Remote-Code-Ausführung auf dem Anwendungsserver zu erlangen.

## Referenzen

- [OWASP Cheat Sheet Series: Software Supply Chain Security](https://cheatsheetseries.owasp.org/cheatsheets/Software_Supply_Chain_Security)
- [OWASP Cheat Sheet Series: OWASP Cheat Sheet: Secure build and deployment (Coming Soon)](https://cheatsheetseries.owasp.org/Glossary.html#s)
- [OWASP Cheat Sheet Series: Infrastructure as Code Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Infrastructure_as_Code_Security_Cheat_Sheet)
- [OWASP Cheat Sheet Series: Deserialization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet)
- [SAFECode Publications: Software Integrity Controls [PDF]](https://safecode.org/publication/SAFECode_Software_Integrity_Controls0610.pdf)
- [NPR News: A 'Worst Nightmare' Cyberattack: The Untold Story Of The SolarWinds Hack](https://www.npr.org/2021/04/16/985439655/a-worst-nightmare-cyberattack-the-untold-story-of-the-solarwinds-hack)
- [Bash Uploader Security Update](https://about.codecov.io/security-update)
- [Securing DevOps](https://www.manning.com/books/securing-devops)

## Liste der zugeordneten CWEs

- [CWE-345: Insufficient Verification of Data Authenticity](https://cwe.mitre.org/data/definitions/345.html)
- [CWE-353: Missing Support for Integrity Check](https://cwe.mitre.org/data/definitions/353.html)
- [CWE-426: Untrusted Search Path](https://cwe.mitre.org/data/definitions/426.html)
- [CWE-494: Download of Code Without Integrity Check](https://cwe.mitre.org/data/definitions/494.html)
- [CWE-502: Deserialization of Untrusted Data](https://cwe.mitre.org/data/definitions/502.html)
- [CWE-565: Reliance on Cookies without Validation and Integrity Checking](https://cwe.mitre.org/data/definitions/565.html)
- [CWE-784: Reliance on Cookies without Validation and Integrity Checking in a Security Decision](https://cwe.mitre.org/data/definitions/784.html)
- [CWE-829: Inclusion of Functionality from Untrusted Control Sphere](https://cwe.mitre.org/data/definitions/829.html)
- [CWE-830: Inclusion of Web Functionality from an Untrusted Source](https://cwe.mitre.org/data/definitions/830.html)
- [CWE-915: Improperly Controlled Modification of Dynamically-Determined Object Attributes](https://cwe.mitre.org/data/definitions/915.html)
