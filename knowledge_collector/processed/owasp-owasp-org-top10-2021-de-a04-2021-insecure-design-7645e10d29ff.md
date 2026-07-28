---
title: A04:2021 – Unsicheres Anwendungsdesign
source: owasp.org
url: https://owasp.org/Top10/2021/de/A04_2021-Insecure_Design/
collector: owasp
category: web-security
tags:
- web-security
- und
- sie
- die
- der
date_collected: '2026-07-25T14:26:32.190831Z'
language: unknown
---

# A04:2021 – Unsicheres Anwendungsdesign

## Beurteilungskriterien

Zugeordnete CWEsMaximale HäufigkeitDurchschn. HäufigkeitDurchschn. Ausnutzbarkeit (gewichtet)Durchschn. Auswirkungen (gewichtet)Maximale AbdeckungDurchschnittliche AbdeckungGesamtanzahlCVEs insgesamt4024.19 %3.00 %6.466.7877.25 %42.51 %262,4072,691

## Übersicht

Eine der neuen Kategorie für 2021 konzentriert sich auf Risiken im Zusammenhang mit Design- und Architekturfehlern und fordert einen stärkeren Einsatz von Bedrohungsmodellierung, sicheren Design Pattern und Referenzarchitekturen. Als Community sollten wir uns nicht nur auf den "Shift-Left"-Ansatz während der Entwicklung fokussieren, sondern auch auf die vorangehenden Aktivitäten, die für die Prinzipien von „Secure by Design“ wesentlich sind. Bemerkenswerte Common Weakness Enumerations (CWEs) sind *CWE-209: Generation of Error Message Containing Sensitive Information*, *CWE-256: Unprotected Storage of Credentials*, *CWE-501: Trust Boundary Violation*, and *CWE-522: Insufficiently Protected Credentials*.

## Beschreibung

Unsicheres Design ist eine umfassende Kategorie, die verschiedene Schwachstellen umfasst und als „fehlendes oder ineffektives Design von Schutzmechanismen“ beschrieben wird.Unsicheres Anwendungsdesign ist nicht die Ursache für alle anderen Top-10-Risikokategorien. Es gibt einen Unterschied zwischen unsicherem Design und unsicherer Implementierung. Designfehler und Implementierungsfehler unterscheiden sich aus gutem Grund, da sie unterschiedliche Ursachen und Mitigationen erfordern. Ein sicheres Design kann immer noch Implementierungsfehler enthalten, die zu ausnutzbaren Schwachstellen führen. Ein unsicheres Design lässt sich nicht durch eine perfekte Implementierung beheben, da die notwendigen Sicherheitskontrollen von vornherein nicht zur Abwehr bestimmter Angriffe vorgesehen waren. Ein Faktor, der zu einem unsicheren Design beiträgt, ist das Fehlen eines Geschäftsrisikoprofils, das der entwickelten Software oder dem System zugrunde liegt, was dazu führt, dass das erforderliche Maß an Sicherheitsdesign nicht bestimmt wird.

### Anforderungs- und Ressourcenmanagement

Legen Sie zusammen mit den Geschäftseinheiten die fachlichen Anforderungen an die Anwendung fest, einschließlich des Schutzbedarfs hinsichtlich Vertraulichkeit, Integrität, Verfügbarkeit und Authentizität aller Datenbestände, sowie die vorgesehene Geschäftslogik. Berücksichtigen Sie, wie exponiert Ihre Anwendung sein wird und ob Sie (zusätzlich zur Zugangskontrolle) eine Mandantentrennung benötigt. Stellen Sie die technischen Anforderungen zusammen, einschließlich funktionaler und nicht funktionaler Sicherheitsanforderungen. Planen Sie das Budget für alle Design-, Entwicklungs-, Test- und Betriebsaktivitäten, unter Berücksichtigung der Sicherheit.

### Sicheres Design

Sicheres Design ist sowohl eine Denkweise als auch eine Vorgehensweise, die kontinuierlich Bedrohungen analysiert und sicherstellt, dass der Code robust entwickelt und getestet wird, um bekannte Angriffsmethoden zu verhindern. Die Bedrohungsmodellierung sollte in *Backlog Refinement* Terminen oder vergleichbaren Aktivitäten integriert werden. Dabei sollten Änderungen im Datenfluss, in der Zugriffskontrolle und anderen Sicherheitsmaßnahmen überprüft werden. Identifizieren Sie während der Entwicklung der User Story die richtigen Ablauf- und Fehlerzustände und stellen Sie sicher, dass sie gut verstanden sind und die Verantwortlichen und sonstigen Beteiligten dazu übereinstimmen. Analysieren Sie Annahmen und Bedingungen für erwartete sowie fehlgeschlagene Prozesse, um sicherzustellen, dass diese weiterhin angemessen und die erwünschten sind. Bestimmen Sie, wie Annahmen überprüft und Bedingungen erzwingt werden können, die für das korrekte Verhalten erforderlich sind. Stellen Sie sicher, dass die Ergebnisse in der User Story dokumentiert sind. Lernen Sie aus Fehlern und bieten Sie positive Anreize, um kontinuierliche Verbesserungen voranzutreiben. Sicheres Design ist weder ein Add-on noch ein Tool, das Sie einer Software hinzufügen können.

### Sicherer Entwicklungslebenszyklus

Sichere Software erfordert einen sicheren Entwicklungslebenszyklus, den Einsatz von sicheren Entwurfsmustern, eine bewährte Methodik, sichere Komponentenbibliotheken, geeignete Tools und Bedrohungsmodellierung. Wenden Sie sich zu Beginn eines Softwareprojekts während der gesamten Projektlaufzeit und Wartung Ihrer Software an Ihre Sicherheitsspezialisten. Erwägen Sie die Nutzung des [OWASP Software Assurance Maturity Model (SAMM)](https://owaspsamm.org), um Ihre Bemühungen zur sicheren Softwareentwicklung zu strukturieren.

## Prävention und Gegenmaßnahmen

- Entwickeln und nutzen Sie einen sicheren Entwicklungslebenszyklus mit Unterstützung durch AppSec-Experten bei der Bewertung und Gestaltung von Sicherheits- und Datenschutzkontrollen.
- Erstellen und verwenden Sie eine Bibliothek mit sicheren Entwurfsmustern und bewährten, erprobten Komponenten.
- Verwenden Sie Bedrohungsmodellierung für kritische Bereiche wie Authentifizierung, Zugriffskontrolle, Geschäftslogik und wichtige Abläufe.
- Integrieren Sie Sicherheitsvorgaben und -kontrollen in den User Stories.
- Implementieren Sie Plausibilitätsprüfungen auf allen Ebenen Ihrer Anwendung, vom Frontend bis zum Backend.
- Schreiben Sie Unit- und Integrationstests, um zu validieren, dass alle kritischen Abläufe resistent gegen das Bedrohungsmodell sind. Stellen Sie Anwendungs-

  *und*Missbrauchsfälle für jede Ebene Ihrer Anwendung zusammen.
- Trennen Sie die Ebenen basierend auf Gefährdungs- und Schutzbedarf auf System- und Netzwerkebene.
- Stellen Sie sicher, dass die Trennung der Mandanten konsequent auf allen Ebenen erfolgt.
- Begrenzen Sie den Ressourcenverbrauch pro Nutzerin/Nutzer oder Dienst

## Beispielhafte Angriffsszenarien

**Szenario Nr. 1:** Ein Workflow zur Wiederherstellung von Anmeldeinformationen kann „Fragen und Antworten“ enthalten, was jedoch gemäß NIST 800-63b, dem OWASP ASVS und den OWASP Top 10 nicht zulässig ist. Fragen und Antworten können nicht als vertrauenswürdiger Identitätsnachweis betrachtet werden. Mehr als eine Person kann die Antworten kennen, weshalb sie verboten sind. Dieser Code sollte entfernt und durch ein sichereres Design ersetzt werden.

**Szenario Nr. 2:** Eine Kinokette bietet Gruppenbuchungsrabatte an und verlangt erst bei mehr als fünfzehn Besuchern eine Anzahlung. Angreifende könnten dieses System ausnutzen, indem sie versuchen, mit wenigen Anfragen sechshundert Sitzplätze in allen Kinos gleichzeitig zu reservieren, was zu erheblichen Einnahmeverlusten führen könnte.

**Szenario Nr. 3:** Die E-Commerce-Website einer Einzelhandelskette ist nicht vor Bots geschützt, die von Scalpern betrieben werden, die High-End-Grafikkarten kaufen, um sie auf Auktionsplattformen weiterzuverkaufen. Dies sorgt für schreckliche Publicity bei den Grafikkartenherstellern und Besitzern von Einzelhandelsketten und sorgt für anhaltende Frustration bei Enthusiasten, die diese Karten nicht erwerben können. Sorgfältiges Anti-Bot-Design sowie Automatismen, die z. B. Käufe ablehnen, die innerhalb weniger Sekunden nach Verfügbarkeit getätigt werden, können helfen, unechte Käufe zu identifizieren und solche Transaktionen zu verhindern.

## Referenzen

- [OWASP Cheat Sheet Series: Secure Product Design Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secure_Product_Design_Cheat_Sheet)
- [OWASP Software Assurance Maturity Model: OWASP SAMM Security Architecture](https://owaspsamm.org/design/security-architecture)
- [OWASP Software Assurance Maturity Model: OWASP SAMM Threat Assessment](https://owaspsamm.org/design/threat-assessment)
- [NIST Publications: Guidelines on Minimum Standards for Developer Verification of Software](https://www.nist.gov/publications/guidelines-minimum-standards-developer-verification-software)
- [The Threat Modeling Manifesto](https://threatmodelingmanifesto.org)
- [Awesome Threat Modeling](https://github.com/hysnsec/awesome-threat-modelling)

## Liste der zugeordneten CWEs

- [CWE-73: External Control of File Name or Path](https://cwe.mitre.org/data/definitions/73.html)
- [CWE-183: Permissive List of Allowed Inputs](https://cwe.mitre.org/data/definitions/183.html)
- [CWE-209: Generation of Error Message Containing Sensitive Information](https://cwe.mitre.org/data/definitions/209.html)
- [CWE-213: Exposure of Sensitive Information Due to Incompatible Policies](https://cwe.mitre.org/data/definitions/213.html)
- [CWE-235: Improper Handling of Extra Parameters](https://cwe.mitre.org/data/definitions/235.html)
- [CWE-256: Plaintext Storage of a Password](https://cwe.mitre.org/data/definitions/256.html)
- [CWE-257: Storing Passwords in a Recoverable Format](https://cwe.mitre.org/data/definitions/257.html)
- [CWE-266: Incorrect Privilege Assignment](https://cwe.mitre.org/data/definitions/266.html)
- [CWE-269: Improper Privilege Management](https://cwe.mitre.org/data/definitions/269.html)
- [CWE-280: Improper Handling of Insufficient Permissions or Privileges](https://cwe.mitre.org/data/definitions/280.html)
- [CWE-311: Missing Encryption of Sensitive Data](https://cwe.mitre.org/data/definitions/311.html)
- [CWE-312: Cleartext Storage of Sensitive Information](https://cwe.mitre.org/data/definitions/312.html)
- [CWE-313: Cleartext Storage in a File or on Disk](https://cwe.mitre.org/data/definitions/313.html)
- [CWE-316: Cleartext Storage of Sensitive Information in Memory](https://cwe.mitre.org/data/definitions/316.html)
- [CWE-419: Unprotected Primary Channel](https://cwe.mitre.org/data/definitions/419.html)
- [CWE-430: Deployment of Wrong Handler](https://cwe.mitre.org/data/definitions/430.html)
- [CWE-434: Unrestricted Upload of File with Dangerous Type](https://cwe.mitre.org/data/definitions/434.html)
- [CWE-444: Inconsistent Interpretation of HTTP Requests ('HTTP Request/Response Smuggling')](https://cwe.mitre.org/data/definitions/444.html)
- [CWE-451: User Interface (UI) Misrepresentation of Critical Information](https://cwe.mitre.org/data/definitions/451.html)
- [CWE-472: External Control of Assumed-Immutable Web Parameter](https://cwe.mitre.org/data/definitions/472.html)
- [CWE-501: Trust Boundary Violation](https://cwe.mitre.org/data/definitions/501.html)
- [CWE-522: Insufficiently Protected Credentials](https://cwe.mitre.org/data/definitions/522.html)
- [CWE-525: Use of Web Browser Cache Containing Sensitive Information](https://cwe.mitre.org/data/definitions/525.html)
- [CWE-539: Use of Persistent Cookies Containing Sensitive Information](https://cwe.mitre.org/data/definitions/539.html)
- [CWE-579: J2EE Bad Practices: Non-serializable Object Stored in Session](https://cwe.mitre.org/data/definitions/579.html)
- [CWE-598: Use of GET Request Method With Sensitive Query Strings](https://cwe.mitre.org/data/definitions/598.html)
- [CWE-602: Client-Side Enforcement of Server-Side Security](https://cwe.mitre.org/data/definitions/602.html)
- [CWE-642: External Control of Critical State Data](https://cwe.mitre.org/data/definitions/642.html)
- [CWE-646: Reliance on File Name or Extension of Externally-Supplied File](https://cwe.mitre.org/data/definitions/646.html)
- [CWE-650: Trusting HTTP Permission Methods on the Server Side](https://cwe.mitre.org/data/definitions/650.html)
- [CWE-653: Improper Isolation or Compartmentalization](https://cwe.mitre.org/data/definitions/653.html)
- [CWE-656: Reliance on Security Through Obscurity](https://cwe.mitre.org/data/definitions/656.html)
- [CWE-657: Violation of Secure Design Principles](https://cwe.mitre.org/data/definitions/657.html)
- [CWE-799: Improper Control of Interaction Frequency](https://cwe.mitre.org/data/definitions/799.html)
- [CWE-807: Reliance on Untrusted Inputs in a Security Decision](https://cwe.mitre.org/data/definitions/807.html)
- [CWE-840: Business Logic Errors (CWE CATEGORY)](https://cwe.mitre.org/data/definitions/840.html)
- [CWE-841: Improper Enforcement of Behavioral Workflow](https://cwe.mitre.org/data/definitions/841.html)
- [CWE-927: Use of Implicit Intent for Sensitive Communication](https://cwe.mitre.org/data/definitions/927.html)
- [CWE-1021: Improper Restriction of Rendered UI Layers or Frames](https://cwe.mitre.org/data/definitions/1021.html)
- [CWE-1173: Improper Use of Validation Framework](https://cwe.mitre.org/data/definitions/1173.html)
