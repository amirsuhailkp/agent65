---
title: A06:2021 – Unsichere oder veraltete Komponenten
source: owasp.org
url: https://owasp.org/Top10/2021/de/A06_2021-Vulnerable_and_Outdated_Components/
collector: owasp
category: web-security
tags:
- web-security
- die
- oder
- komponenten
- und
date_collected: '2026-07-25T14:26:34.027127Z'
language: unknown
---

# A06:2021 – Unsichere oder veraltete Komponenten

## Beurteilungskriterien

Zugeordnete CWEsMaximale HäufigkeitDurchschn. HäufigkeitDurchschn. Ausnutzbarkeit (gewichtet)Durchschn. Auswirkungen (gewichtet)Maximale AbdeckungDurchschnittliche AbdeckungGesamtanzahlCVEs insgesamt327.96 %8.77 %5.005.0051.78 %22.47 %30,4570

## Übersicht

Es belegte Platz 2 in der Top-10-Community-Umfrage, verfügte aber auch über genügend Daten, um es datentechnisch in die Top 10 zu schaffen.
Unsichere Komponenten sind ein bekanntes Problem, das wir nur schwer testen und bewerten können. Sie stellen die einzige Kategorie dar, in der den enthaltenen CWEs keine Common Vulnerability and Exposures (CVEs) zugeordnet sind. Daher wird eine standardmäßige Exploit-/Auswirkungsgewichtung von 5,0 verwendet. Bemerkenswerte CWEs sind *CWE-1104: Use of Unmaintained Third-Party Components* und die beiden CWEs aus den Top 10 2013 und 2017.

## Beschreibung

Die Anwendung besitzt möglicherweise Schwachstellen, wenn folgendes zutrifft:

- Fehlende Kenntnis über die Versionen aller verwendeten Komponenten der in der Anwendung (sowohl client- als auch serverseitig). Dies beinhaltet sowohl direkte als auch indirekte, verschachtelte Abhängigkeiten.
- Die verwendete Software besitzt Schwachstellen, wird nicht mehr unterstützt oder ist veraltet. Dies beinhaltet das Betriebssystem, den Web-/Applikationsserver, das Datenbankmanagementsystem (DBMS), Anwendungen, APIs und alle verwendeten Komponenten, Laufzeitumgebungen sowie Bibliotheken.
- Schwachstellenscans werden nicht regelmäßig durchgeführt und die sicherheitsrelevanten Bulletins der verwendeten Komponenten sind nicht abonniert.
- Die zugrundeliegende Plattform, die Frameworks und die Abhängigkeiten werden nicht risikobasiert und rechtzeitig repariert oder aktualisiert. Dies geschiet in der Regel in Umgebungen, in denen Patchen eine monatliche oder quartalsweise Tätigkeit ist und einer Änderungskontrolle unterliegt. Dies setzt die Organisation unnötigerweise über Tage oder Monate dem Risiko von Schwachstellen aus, für die schon Patches existieren.
- Softwareentwickler führen keine Kompatibilitäts-Tests der aktualisierten oder gepatchten Bibliotheken durch.
- Die Komponenten sind nicht sicher konfiguriert (siehe

  [A05:2021-Sicherheitsrelevante Fehlkonfiguration](../A05_2021-Security_Misconfiguration/)).

## Prävention und Gegenmaßnahmen

Es sollte ein Patch-Management-Prozess vorhanden sein:

- Entfernen Sie ungenutzte Abhängigkeiten, unnötige Funktionen, Komponenten, Dateien und Dokumentation.
- Kontinuierliche Bestandsaufnahme der Versionen sowohl der clientseitigen als auch der serverseitigen Komponenten (z. B. Frameworks, Bibliotheken) und ihrer Abhängigkeiten mithilfe von Tools wie "versions", "OWASP Dependency Check", "retire.js" usw. Überwachen Sie kontinuierlich Quellen wie Common Vulnerability and Exposures (CVE) und die National Vulnerability Database (NVD) für Schwachstellen in den Komponenten. Verwenden Sie Software-Tools zur Analyse der Softwarebestandteile, um den Prozess zu automatisieren. Abonnieren Sie E-Mail-Benachrichtigungen zu Sicherheitslücken im Zusammenhang mit den verwendeten Komponenten.
- Beziehen Sie Komponenten nur von offiziellen Quellen über sichere Links. Bevorzugen Sie signierte Pakete, um die Wahrscheinlichkeit zu verringern, dass eine modifizierte, bösartige Komponente enthalten ist (siehe

  [A08:2021-Fehlerhafte Prüfung der Software- und Datenintegrität](../A08_2021-Software_and_Data_Integrity_Failures/)).
- Überwachen Sie Bibliotheken und Komponenten, die nicht gewartet werden oder keine Sicherheitspatches für ältere Versionen erstellen. Wenn das Patchen nicht möglich ist, erwägen Sie die Bereitstellung eines virtuellen Patches zur Überwachung, Erkennung oder zum Schutz vor dem entdeckten Problem.

Jede Organisation muss einen fortlaufenden Plan für die Überwachung, Triage und Anwendung von Updates oder Konfigurationsänderungen während der gesamten Lebensdauer der Anwendung oder des Portfolios sicherstellen.

## Beispielhafte Angriffsszenarien

**Szenario Nr. 1:** Komponenten werden normalerweise mit denselben Berechtigungen wie die Anwendung selbst ausgeführt, sodass Fehler in einer Komponente schwerwiegende Auswirkungen haben können. Solche Fehler können zufällig (z. B. ein Programmierfehler) oder absichtlich (z. B. eine Backdoor in einer Komponente) sein. Einige Beispiele für entdeckte ausnutzbare Komponentenschwachstellen sind:

- CVE-2017-5638, eine Remote Code Execution Schwachstelle in Struts 2, die Angreifende ermächtigt, beliebigen Code auf dem Server auszuführen, wurde für einige erhebliche Sicherheitsvorfälle verantwortlich gemacht.
- Obwohl das Patchen von Internet of Things (IoT) Geräten oft nur sehr schwierig oder unmöglich ist, kann dies sehr wichtig sein (z. B. für biomedizinische Geräte).

Es existieren automatisierte Tools, die Angreifenden helfen, nicht gepatchte oder falsch konfigurierte Systeme zu finden. Die Shodan IoT-Suchmaschine kann Ihnen beispielsweise dabei helfen, Geräte zu finden, die immer noch für die im April 2014 gepatchte Heartbleed-Sicherheitslücke verwundbar sind.

## Referenzen

- [OWASP Application Security Verification Standard (ASVS): V1 Architecture, Design and Threat Modeling](https://github.com/OWASP/ASVS/blob/master/4.0/en/0x10-V1-Architecture.md#4-0-1)
- [OWASP Dependency Check (for Java and .NET libraries)](https://owasp.org/www-project-dependency-check)
- [OWASP Web Security Testing Guide: Map Application Architecture](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/01-Information_Gathering/10-Map_Application_Architecture)
- [OWASP Community Content: Virtual Patching Best Practices](https://owasp.org/www-community/Virtual_Patching_Best_Practices)
- [Contrast Security: The Unfortunate Reality of Insecure Libraries](https://cdn2.hubspot.net/hub/203759/file-1100864196-pdf/docs/Contrast - Insecure_Libraries_2014.pdf)
- [MITRE Common Vulnerabilities and Exposures (CVE): search by cvedetails](https://www.cvedetails.com/version-search.php)
- [National Vulnerability Database (NVD)](https://nvd.nist.gov/)
- [Retire.js for detecting known vulnerable JavaScript libraries](https://github.com/retirejs/retire.js/)
- [GitHub Advisory Database](https://github.com/advisories)
- [RubySec: Ruby Libraries Security Advisory Database and Tools](https://rubysec.com/)
- [SAFECode: Software Integrity Controls [PDF]](https://safecode.org/publication/SAFECode_Software_Integrity_Controls0610.pdf)
