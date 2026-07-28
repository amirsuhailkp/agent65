---
title: A03:2021 – Injection
source: owasp.org
url: https://owasp.org/Top10/2021/de/A03_2021-Injection/
collector: owasp
category: web-security
tags:
- web-security
- die
- von
- oder
- und
date_collected: '2026-07-25T14:26:31.381650Z'
language: unknown
---

# A03:2021 – Injection

## Beurteilungskriterien

Zugeordnete CWEsMaximale HäufigkeitDurchschn. HäufigkeitDurchschn. Ausnutzbarkeit (gewichtet)Durchschn. Auswirkungen (gewichtet)Maximale AbdeckungDurchschnittliche AbdeckungGesamtanzahlCVEs insgesamt3319.09 %3.37 %7.257.1594.04 %47.90 %274,22832,078

## Übersicht

Die Injection rutscht von der ersten auf die dritte Position ab. 94 % der Anwendungen wurden auf irgendeine Form der Injection getestet, mit einer maximalen Häufigkeit von 19,09 %, einer durchschnittlichen Häufigkeit von 3,37 % und über 274.000 Vorkommnissen. Zu den wichtigsten Common Weakness Enumerations (CWEs) zählen *CWE-79: Cross-Site Scripting*, *CWE-89: SQL Injection* und *CWE-73: External Control of File Name or Path*.

## Beschreibung

Eine Anwendung ist für diesen Angriff anfällig, wenn:

- Daten, die von Nutzenden stammen, von der Anwendung nicht ausreichend validiert, gefiltert oder bereinigt werden.
- Dynamische Anfragen oder nicht-parametrisierte Aufrufe ohne ein, dem Kontext entsprechendes Escaping direkt einem Interpreter übergeben werden.
- Bösartige Daten innerhalb von ORM („Object-Relational Mapping“)-Suchparametern genutzt werden können, um vertrauliche Datensätze von Dritten zu extrahieren.
- Bösartige Daten direkt oder als Teil zusammengesetzter, dynamischer Querys verwendet werden. Die SQL-Abfragen oder Befehle beinhalten die Struktur und die schädlichen Daten in den dynamischen Querys, Befehlen oder Stored Procedures.

Zu den häufigeren Injection Arten gehören SQL, NoSQL, OS-Befehle, Object Relational Mapping (ORM), LDAP und Expression Language (EL) oder Object Graph Navigation Library (OGNL). Das Grundkonzept eines Injection-Angriffs ist für alle Interpreter gleich. Ein Quellcode-Review ist die beste Methode, um Injection-Schwachstellen in Anwendungen zu finden. Ausführliches (ggf. automatisiertes) Testen aller Parameter und Variablen, Header-, URL-, Cookies-, JSON-, SOAP- und XML-Eingaben wird dringend empfohlen. Statische (SAST, Quellcode-Ebene), dynamische (DAST, laufende Anwendung) und interaktive (IAST, Mischform aus statisch und dynamisch) Test-Werkzeuge können von Organisationen für ihre CI/CD-Pipeline genutzt werden, um neue Schwachstellen noch vor einer möglichen Auslieferung in Produktivsysteme zu identifizieren.

## Prävention und Gegenmaßnahmen

Eine konsequente Trennung von Daten, Suchanfragen und Befehlen ist für die Vermeidung von Injection-Angriffen unerlässlich:

- Die bevorzugte Methode ist die Verwendung einer sicheren API, die die Verwendung des Interpreters vollständig vermeidet, eine parametrisierte Schnittstelle bereitstellt oder in objektrelationale Mapping-Tools (ORMs) umwandelt.

  **Anmerkung:**Stored Procedures können - auch parametrisiert - immer noch SQL-Injections ermöglichen, wenn PL/SQL oder T-SQL Anfragen und Eingabedaten konkateniert oder mit EXECUTE IMMEDIATE oder exec() ausgeführt werden.
- Für die serverseitige Eingabe-Validierung empfiehlt sich die Nutzung eines Positivlisten(“Whitelist”)-Ansatzes. Dies ist i. A. kein vollständiger Schutz, da viele Anwendungen Sonderzeichen z. B. in Textfelder oder APIs für mobile Anwendungen benötigen.
- Für jede noch verbliebene dynamische Query müssen Sonderzeichen für den jeweiligen Interpreter mit der richtigen Escape-Syntax entschärft werden.

  **Anmerkung:**Ein Escaping von SQL-Bezeichnern, wie z. B. die Namen von Tabellen oder Spalten usw. ist nicht möglich. Falls Nutzende solche Bezeichner selbst eingeben können, so ist dies durchaus gefährlich. Dies ist eine übliche Schwachstelle bei Software, die Reports aus einer Datenbank erstellt.
- SQL-Querys sollten LIMIT oder andere SQL-Controls verwenden, um den möglichen Massen-Abfluss von Daten zu verhindern.

## Beispielhafte Angriffsszenarien

**Szenario Nr. 1:** Eine Anwendung nutzt ungeprüfte Eingabedaten für den Zusammenbau der folgenden  **verwundbaren** SQL-Abfrage:
```
```
String query = "SELECT \* FROM Accounts WHERE custID='" + request.getParameter("id") + "'";```
```

**Szenario Nr. 2:** Auch das blinde Vertrauen in Frameworks kann zu Querys führen, die ganz analog zu obigem Beispiel  **verwundbar** sind (z. B. Hibernate Query Language (HQL)):
```
```
Abfrage HQLQuery = session.createQuery("FROM Accounts WHERE custID='" + request.getParameter("id") + "'");```
```

In beiden Fällen können Angreifende den ‘id’-Parameter im Browser ändern und sendet: „UNION SLEEP(10);--“. Zum Beispiel:
```
```
http://example.com/app/accountView?id=' UNION SELECT SLEEP(10);--```
```

Hierdurch wird die Logik der Anfrage verändert, so dass alle Datensätze der Tabelle „accounts“ ohne Einschränkung auf einen Kunden zurückgegeben werden. Gefährlichere Attacken wären z. B. das Ändern oder Löschen von Daten oder das Aufrufen von Stored Procedures.

## Referenzen

- [OWASP Proactive Controls: C3: Secure Database Access](https://github.com/OWASP/www-project-proactive-controls/blob/master/v3/en/c3-secure-database.md)
- [OWASP Application Security Verification Standard (ASVS): V5 Validation, Sanitization and Encoding](https://github.com/OWASP/ASVS/blob/master/4.0/en/0x13-V5-Validation-Sanitization-Encoding.md#4-0-5)
- [OWASP Web Security Testing Guide: Testing for SQL Injection](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/07-Input_Validation_Testing/05-Testing_for_SQL_Injection),[Testing for Command Injection](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/07-Input_Validation_Testing/12-Testing_for_Command_Injection),[Testing for ORM Injection](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/07-Input_Validation_Testing/05.7-Testing_for_ORM_Injection)
- [OWASP Cheat Sheet Series: Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Injection_Prevention_Cheat_Sheet)
- [OWASP Cheat Sheet Series: SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet)
- [OWASP Cheat Sheet Series: Injection Prevention in Java Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Injection_Prevention_in_Java_Cheat_Sheet)
- [OWASP Cheat Sheet Series: Query Parameterization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Query_Parameterization_Cheat_Sheet)
- [OWASP Automated Threats to Web Applications: OAT-014 Vulnerability Scanning](https://owasp.org/www-project-automated-threats-to-web-applications/assets/oats/EN/OAT-014_Vulnerability_Scanning)
- [Portswigger Issue Definitions: Server-side template injection](https://portswigger.net/kb/issues/00101080_serversidetemplateinjection)

## Liste der zugeordneten CWEs

- [CWE-20: Improper Input Validation](https://cwe.mitre.org/data/definitions/20.html)
- [CWE-74: Improper Neutralization of Special Elements in Output Used by a Downstream Component ('Injection')](https://cwe.mitre.org/data/definitions/74.html)
- [CWE-75: Failure to Sanitize Special Elements into a Different Plane (Special Element Injection)](https://cwe.mitre.org/data/definitions/75.html)
- [CWE-77: Improper Neutralization of Special Elements used in a Command ('Command Injection')](https://cwe.mitre.org/data/definitions/77.html)
- [CWE-78: Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection')](https://cwe.mitre.org/data/definitions/78.html)
- [CWE-79: Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting')](https://cwe.mitre.org/data/definitions/79.html)
- [CWE-80: Improper Neutralization of Script-Related HTML Tags in a Web Page (Basic XSS)](https://cwe.mitre.org/data/definitions/80.html)
- [CWE-83: Improper Neutralization of Script in Attributes in a Web Page](https://cwe.mitre.org/data/definitions/83.html)
- [CWE-87: Improper Neutralization of Alternate XSS Syntax](https://cwe.mitre.org/data/definitions/87.html)
- [CWE-88: Improper Neutralization of Argument Delimiters in a Command ('Argument Injection')](https://cwe.mitre.org/data/definitions/88.html)
- [CWE-89: Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection')](https://cwe.mitre.org/data/definitions/89.html)
- [CWE-90: Improper Neutralization of Special Elements used in an LDAP Query ('LDAP Injection')](https://cwe.mitre.org/data/definitions/90.html)
- [CWE-91: XML Injection (aka Blind XPath Injection)](https://cwe.mitre.org/data/definitions/91.html)
- [CWE-93: Improper Neutralization of CRLF Sequences ('CRLF Injection')](https://cwe.mitre.org/data/definitions/93.html)
- [CWE-94: Improper Control of Generation of Code ('Code Injection')](https://cwe.mitre.org/data/definitions/94.html)
- [CWE-95: Improper Neutralization of Directives in Dynamically Evaluated Code ('Eval Injection')](https://cwe.mitre.org/data/definitions/95.html)
- [CWE-96: Improper Neutralization of Directives in Statically Saved Code ('Static Code Injection')](https://cwe.mitre.org/data/definitions/96.html)
- [CWE-97: Improper Neutralization of Server-Side Includes (SSI) Within a Web Page](https://cwe.mitre.org/data/definitions/97.html)
- [CWE-98: Improper Control of Filename for Include/Require Statement in PHP Program ('PHP Remote File Inclusion')](https://cwe.mitre.org/data/definitions/98.html)
- [CWE-99: Improper Control of Resource Identifiers ('Resource Injection')](https://cwe.mitre.org/data/definitions/99.html)
- [CWE-100: DEPRECATED: Technology-Specific Input Validation Problems (CWE CATEGORY)](https://cwe.mitre.org/data/definitions/100.html)
- [CWE-113: Improper Neutralization of CRLF Sequences in HTTP Headers ('HTTP Request/Response Splitting')](https://cwe.mitre.org/data/definitions/113.html)
- [CWE-116: Improper Encoding or Escaping of Output](https://cwe.mitre.org/data/definitions/116.html)
- [CWE-138: Improper Neutralization of Special Elements](https://cwe.mitre.org/data/definitions/138.html)
- [CWE-184: Incomplete List of Disallowed Inputs](https://cwe.mitre.org/data/definitions/184.html)
- [CWE-470: Use of Externally-Controlled Input to Select Classes or Code ('Unsafe Reflection')](https://cwe.mitre.org/data/definitions/470.html)
- [CWE-471: Modification of Assumed-Immutable Data (MAID)](https://cwe.mitre.org/data/definitions/471.html)
- [CWE-564: SQL Injection: Hibernate](https://cwe.mitre.org/data/definitions/564.html)
- [CWE-610: Externally Controlled Reference to a Resource in Another Sphere](https://cwe.mitre.org/data/definitions/610.html)
- [CWE-643: Improper Neutralization of Data within XPath Expressions ('XPath Injection')](https://cwe.mitre.org/data/definitions/643.html)
- [CWE-644: Improper Neutralization of HTTP Headers for Scripting Syntax](https://cwe.mitre.org/data/definitions/644.html)
- [CWE-652: Improper Neutralization of Data within XQuery Expressions ('XQuery Injection')](https://cwe.mitre.org/data/definitions/652.html)
- [CWE-917: Improper Neutralization of Special Elements used in an Expression Language Statement ('Expression Language Injection')](https://cwe.mitre.org/data/definitions/917.html)
