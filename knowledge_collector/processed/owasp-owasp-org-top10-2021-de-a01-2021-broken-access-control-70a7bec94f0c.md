---
title: A01:2021 – Mangelhafte Zugriffskontrolle
source: owasp.org
url: https://owasp.org/Top10/2021/de/A01_2021-Broken_Access_Control/
collector: owasp
category: web-security
tags:
- web-security
- oder
- der
- die
- und
date_collected: '2026-07-25T14:25:16.623668Z'
language: unknown
---

# A01:2021 – Mangelhafte Zugriffskontrolle

## Beurteilungskriterien

Zugeordnete CWEsMaximale HäufigkeitDurchschn. HäufigkeitDurchschn. Ausnutzbarkeit (gewichtet)Durchschn. Auswirkungen (gewichtet)Maximale AbdeckungDurchschnittliche AbdeckungGesamtanzahlCVEs insgesamt3455.97 %3.81 %6.925.9394.55 %47.72 %318,48719,013

## Übersicht

94 % der Anwendungen wurden auf irgendeine Form fehlerhafter Zugriffskontrolle getestet.
Vom fünften Platz aufgestiegen, weist die fehlerhafte Zugriffskontrolle mit einer durchschnittlichen Inzidenzrate von 3,81 % und mit über 318.000 die meisten Vorkommnisse im vorliegenden Datensatz auf.
Bemerkenswerte Common Weakness Enumerations (CWEs) sind *CWE-200: Exposure of Sensitive Information to an Unauthorized Actor*, *CWE-201: Insertion of Sensitive Information Into Sent Data* und *CWE-352: Cross-Site Request Forgery*.

## Beschreibung

Die Zugriffskontrolle erzwingt Richtlinien, sodass Nutzende nicht außerhalb ihrer vorgesehenen Berechtigungen handeln können. Fehler führen in der Regel zur unbefugten Offenlegung, Änderung oder Zerstörung aller Daten oder zur Ausführung einer Geschäftsfunktion außerhalb der Verfügungen der anwendenden Person. Zu den häufigsten Schwachstellen bei der Zugriffskontrolle gehören:

- Verstoß gegen die Prinzipien der geringsten Rechte oder der standardmäßigen Verweigerung, bei dem der Zugriff nur für bestimmte Fähigkeiten, Rollen oder Nutzende gewährt werden sollte, aber für jedermann verfügbar ist.
- Umgehen von Zugriffskontrollprüfungen durch Ändern der URL (Parametermanipulation oder erzwungenes Durchsuchen), des internen Anwendungsstatus oder der HTML-Seite oder durch Verwendung eines Angriffstools zur Änderung von API-Anfragen.
- Ermöglichen, das Konto einer anderen Person anzuzeigen oder zu bearbeiten, indem dessen eindeutige Kennung angegeben wird (unsichere direkte Objektreferenzen).
- Zugriff auf die API mit fehlenden Zugriffskontrollen für POST, PUT und DELETE.
- Erhöhung der Privilegien. Als Nutzerin/Nutzer fungieren, ohne angemeldet zu sein oder als Administrator fungieren, wenn man als Standard-Nutzerin/Nutzer angemeldet ist.
- Manipulation von Metadaten, wie z. B. das Abfangen oder Manipulieren eines JSON Web Token (JWT)-Zugriffskontrolltokens oder die Manipulation eines Cookies oder eines versteckten Felds, um Berechtigungen zu erhöhen oder die Ungültigerklärung von JWTs zu missbrauchen.
- CORS-Fehlkonfiguration ermöglicht API-Zugriff von nicht autorisierten/nicht vertrauenswürdigen Quellen.
- Erzwingen des Zugriffs auf authentifizierte Seiten als nicht authentifizierte Person oder zu privilegierten Seiten als Standard-Nutzerin/Nutzer.

## Prävention und Gegenmaßnahmen

Die Zugriffskontrolle ist nur wirksam bei vertrauenswürdigem serverseitigem Code oder serverlosen APIs, bei denen Angreifende die Zugriffskontrollprüfung oder Metadaten nicht ändern können.

- Verweigern Sie standardmäßig den Zugriff, mit Ausnahme öffentlicher Ressourcen.
- Implementieren Sie Zugriffskontrollmechanismen einmalig und verwenden Sie diese in der gesamten Anwendung wieder, einschließlich der Minimierung der Nutzung von Cross-Origin Resource Sharing (CORS).
- Modellzugriffskontrollen sollten die Datensatzeigentümerschaft erzwingen, anstatt zu akzeptieren, dass Nutzerinnen/Nutzer Datensätze erstellen, lesen, aktualisieren oder löschen können.
- Durch Domänenmodelle sollten eindeutige Geschäftslimitanforderungen für Anwendungen durchgesetzt werden.
- Deaktivieren Sie die Verzeichnisliste des Webservers und stellen Sie sicher, dass Dateimetadaten (z. B. .git) und Sicherungsdateien nicht in Web-Roots vorhanden sind.
- Protokollieren Sie Fehler bei der Zugriffskontrolle und benachrichtigen Sie Administratoren bei Bedarf (z. B. wiederholte Fehler).
- Setzen Sie Ratenbegrenzung für API- und Controller-Zugriff, um den Schaden durch automatisierte Angriffstools zu minimieren.
- Statusbehaftete Sitzungskennungen sollten nach dem Abmelden auf dem Server ungültig gemacht werden. Zustandslose JWT-Token sollten eher kurzlebig sein, damit das Zeitfenster für Angreifende minimiert wird. Für langlebigere JWTs wird dringend empfohlen, die OAuth-Standards zu befolgen, um den Zugriff zu widerrufen.

Entwickler und QA-Mitarbeiter sollten funktionale Zugriffskontrolleinheiten und Integrationstests durchführen.

## Beispielhafte Angriffsszenarien

**Szenario Nr. 1:** Die Anwendung verwendet nicht überprüfte Daten in einem SQL-Aufruf, der auf Kontoinformationen zugreift:
```
```
pstmt.setString(1, request.getParameter("acct"));
ResultSet results = pstmt.executeQuery( );```
```

Angreifende ändern einfach den „acct“-Parameter des Browsers, um die gewünschte Kontonummer zu senden. Bei nicht korrekter Überprüfung kann die angreifende Person auf das Konto einer beliebigen Nutzerin/Nutzers zugreifen.
```
```
https://example.com/app/accountInfo?acct=notmyacct```
```

**Szenario Nr. 2:** Eine angreifende Person erzwingt einfach die Suche nach Ziel-URLs. Für den Zugriff auf die Admin-Seite sind Admin-Rechte erforderlich.
```
```
https://example.com/app/getappInfo
https://example.com/app/admin_getappInfo```
```

Wenn eine nicht authentifizierte Benutzerin/Benutzer auf eine der Seiten zugreifen kann, liegt ein Fehler vor. Wenn ein Benutzerin/Benutzer ohne Administrationsrechte auf die Admin-Seite zugreifen kann, handelt es sich um einen Fehler.

## Referenzen

- [OWASP Proactive Controls: C7: Enforce Access Controls](https://github.com/OWASP/www-project-proactive-controls/blob/master/v3/en/c7-enforce-access-controls.md)
- [OWASP Application Security Verification Standard (ASVS): V4 Access Control](https://github.com/OWASP/ASVS/blob/master/4.0/en/0x12-V4-Access-Control.md#4-0-4)
- [OWASP Web Security Testing Guide: Authorization Testing](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/05-Authorization_Testing/index)
- [OWASP Cheat Sheet Series: Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet)
- [Portswigger Research: Exploiting CORS misconfigurations for Bitcoins and bounties](https://portswigger.net/research/exploiting-cors-misconfigurations-for-bitcoins-and-bounties)
- [OAuth 2.0: Revoking Access](https://www.oauth.com/oauth2-servers/listing-authorizations/revoking-access/)

## Liste der zugeordneten CWEs

- [CWE-22: Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal')](https://cwe.mitre.org/data/definitions/22.html)
- [CWE-23: Relative Path Traversal](https://cwe.mitre.org/data/definitions/23.html)
- [CWE-35: Path Traversal: '.../...//'](https://cwe.mitre.org/data/definitions/35.html)
- [CWE-59: Improper Link Resolution Before File Access ('Link Following')](https://cwe.mitre.org/data/definitions/59.html)
- [CWE-200: Exposure of Sensitive Information to an Unauthorized Actor](https://cwe.mitre.org/data/definitions/200.html)
- [CWE-201: Insertion of Sensitive Information Into Sent Data](https://cwe.mitre.org/data/definitions/201.html)
- [CWE-219: Storage of File with Sensitive Data Under Web Root](https://cwe.mitre.org/data/definitions/219.html)
- [CWE-264: Permissions, Privileges, and Access Controls (CWE CATEGORY)](https://cwe.mitre.org/data/definitions/264.html)
- [CWE-275: Permission Issues (CWE CATEGORY)](https://cwe.mitre.org/data/definitions/275.html)
- [CWE-276: Incorrect Default Permissions](https://cwe.mitre.org/data/definitions/276.html)
- [CWE-284: Improper Access Control](https://cwe.mitre.org/data/definitions/284.html)
- [CWE-285: Improper Authorization](https://cwe.mitre.org/data/definitions/285.html)
- [CWE-352: Cross-Site Request Forgery (CSRF)](https://cwe.mitre.org/data/definitions/352.html)
- [CWE-359: Exposure of Private Personal Information to an Unauthorized Actor](https://cwe.mitre.org/data/definitions/359.html)
- [CWE-377: Insecure Temporary File](https://cwe.mitre.org/data/definitions/377.html)
- [CWE-402: Transmission of Private Resources into a New Sphere ('Resource Leak')](https://cwe.mitre.org/data/definitions/402.html)
- [CWE-425: Direct Request ('Forced Browsing')](https://cwe.mitre.org/data/definitions/425.html)
- [CWE-441: Unintended Proxy or Intermediary ('Confused Deputy')](https://cwe.mitre.org/data/definitions/441.html)
- [CWE-497: Exposure of Sensitive System Information to an Unauthorized Control Sphere](https://cwe.mitre.org/data/definitions/497.html)
- [CWE-538: Insertion of Sensitive Information into Externally-Accessible File or Directory](https://cwe.mitre.org/data/definitions/538.html)
- [CWE-540: Inclusion of Sensitive Information in Source Code](https://cwe.mitre.org/data/definitions/540.html)
- [CWE-548: Exposure of Information Through Directory Listing](https://cwe.mitre.org/data/definitions/548.html)
- [CWE-552: Files or Directories Accessible to External Parties](https://cwe.mitre.org/data/definitions/552.html)
- [CWE-566: Authorization Bypass Through User-Controlled SQL Primary Key](https://cwe.mitre.org/data/definitions/566.html)
- [CWE-601: URL Redirection to Untrusted Site ('Open Redirect')](https://cwe.mitre.org/data/definitions/601.html)
- [CWE-639: Authorization Bypass Through User-Controlled Key](https://cwe.mitre.org/data/definitions/639.html)
- [CWE-651: Exposure of WSDL File Containing Sensitive Information](https://cwe.mitre.org/data/definitions/651.html)
- [CWE-668: Exposure of Resource to Wrong Sphere](https://cwe.mitre.org/data/definitions/668.html)
- [CWE-706: Use of Incorrectly-Resolved Name or Reference](https://cwe.mitre.org/data/definitions/706.html)
- [CWE-862: Missing Authorization](https://cwe.mitre.org/data/definitions/862.html)
- [CWE-863: Incorrect Authorization](https://cwe.mitre.org/data/definitions/863.html)
- [CWE-913: Improper Control of Dynamically-Managed Code Resources](https://cwe.mitre.org/data/definitions/913.html)
- [CWE-922: Insecure Storage of Sensitive Information](https://cwe.mitre.org/data/definitions/922.html)
- [CWE-1275: Sensitive Cookie with Improper SameSite Attribute](https://cwe.mitre.org/data/definitions/1275.html)
