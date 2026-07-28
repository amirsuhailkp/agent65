---
title: A09:2021 – Unzureichendes Logging und Sicherheitsmonitoring
source: owasp.org
url: https://owasp.org/Top10/2021/de/A09_2021-Security_Logging_and_Monitoring_Failures/
collector: owasp
category: web-security
tags:
- web-security
- und
- die
- der
- von
date_collected: '2026-07-25T14:26:37.471523Z'
language: unknown
---

# A09:2021 – Unzureichendes Logging und Sicherheitsmonitoring

## Beurteilungskriterien

Zugeordnete CWEsMaximale HäufigkeitDurchschn. HäufigkeitDurchschn. Ausnutzbarkeit (gewichtet)Durchschn. Auswirkungen (gewichtet)Maximale AbdeckungDurchschnittliche AbdeckungGesamtanzahlCVEs insgesamt419.23 %6.51 %6.874.9953.67 %39.97 %53,615242

## Übersicht

Sicherheitsprotokollierung und -überwachung wurden in der Top-10-Community-Umfrage (Platz 3) genannt, was eine leichte Verbesserung gegenüber dem zehnten Platz in der OWASP Top 10 2017 bedeutet. Das Logging und Monitoring können schwierig zu testen sein, da sie oft Interviews oder die Frage nach der Erkennung von Angriffen während eines Penetrationstests beinhalten. Es gibt nicht viele CVE/CVSS-Daten für diese Kategorie, aber das Erkennen von und Reagieren auf Angriffe ist von entscheidender Bedeutung. Allerdings kann dies für die Nachweisbarkeit, die Nachvollziehbarkeit, die Alarmierung bei Vorfällen und Forensik von großer Bedeutung sein. Diese Kategorie erstreckt sich über *CWE-778 Insufficient Logging* hinaus und umfasst auch *CWE-117 Improper Output Neutralization for Logs*, *CWE-223 Omission of Security-relevant Information* und *CWE-532 Insertion of Sensitive Information into Log File*.

## Beschreibung

Mit Blick auf die OWASP Top 10 2021 soll diese Kategorie bei der Erkennung, Eskalation und Reaktion auf laufende Angriffe unterstützen. Ohne Protokollierung und Überwachung können Angriffe nicht erkannt werden. Unzureichende Protokollierung, Erkennung, Überwachung und aktive Reaktion sind jederzeit möglich:

- Nachvollziehbare Ereignisse, wie Anmeldungen, fehlgeschlagene Anmeldungen und wertvolle Transaktionen, werden nicht protokolliert.
- Warnungen und Fehler erzeugen keine, unangemessene oder unklare Log-Einträge.
- Die Logs von Anwendungen und APIs werden nicht auf verdächtige Aktivitäten überwacht.
- Protokolle werden nur lokal gespeichert.
- Geeignete Schwellenwerte für Warnmeldungen und Eskalationsprozesse für Gegenmaßnahmen sind nicht vorhanden oder nicht wirksam.
- Penetrationstests und Scans durch DAST-Tools (Dynamic Application Security Testing) (wie OWASP ZAP) lösen keine Alarme aus.
- Die Anwendungen können Angriffe weder in Echtzeit noch nahezu in Echtzeit erkennen, eskalieren oder Alarm schlagen.

Es besteht die Gefahr von Informationslecks, falls Sie die Logging- und Alerting Ereignisse für Nutzende oder Angreifende sichtbar gemacht werden (siehe [A01:2021-Broken Access Control](../A01_2021-Broken_Access_Control/)).

## Prävention und Gegenmaßnahmen

Je nach dem Risiko der Anwendung sollten Entwickler einige oder alle der folgenden Maßnahmen ergreifen:

- Sicherstellen, dass alle Anmeldevorgänge, Zugriffskontrollen und Fehler bei der serverseitigen Eingabeüberprüfung mit ausreichendem Sitzungskontext der Nutzenden erfasst werden, um verdächtige oder böswillige Anwendende zu identifizieren und ausreichend lange gespeichert werden, um eine spätere forensische Analyse zu ermöglichen.
- Stellen Sie sicher, dass die Protokolle in einem Format gespeichert werden, das von Protokollmanagement Lösungen leicht verarbeitet werden können.
- Es sollte sichergestellt werden, dass die Protokolldaten korrekt umgewandelt werden, sodass Injection-Angriffe oder Angriffe auf Logging- oder Überwachungssysteme verhindert werden.
- Es soll sichergestellt sein, dass hochwertige Transaktionen einen Prüfpfad mit Integritätskontrollen aufweisen um Manipulationen oder Löschungen zu verhindern, z. B. durch Datenbanktabellen, die nur erweitert werden können, oder ähnliches.
- DevSecOps-Teams sollten eine effektive Überwachung und Alarmierung einrichten, sodass verdächtige Aktivitäten schnell erkannt und darauf reagiert werden kann.
- Erstellen oder übernehmen Sie einen Notfallplan für die Reaktion auf Vorfälle und für die Wiederherstellung, wie z. B. dem Leitfaden des National Institute of Standards and Technology (NIST) 800-61r2 oder neuer.

Es gibt kommerzielle und Open-Source-Frameworks zum Schutz von Anwendungen wie das OWASP ModSecurity Core Rule Set, und Open-Source-Log correlation software, wie Elasticsearch, Logstash, Kibana (ELK) Stack, die individuelle Dashboards und Warnmeldungen bereitstellen.

## Beispielhafte Angriffsszenarien

**Szenario 1:** Der Betreiber der Website eines Anbieters von Kinderkrankenversicherungen konnte das Eindringen in das System aufgrund mangelnder Überwachung und Protokollierung nicht erkennen. Eine externe Partei informierte den Krankenversicherungsanbieter, dass Angreifende auf Tausende der mehr als 3,5 Millionen sensiblen Gesundheitsdaten der Kinder zugegriffen und diese verändert hatten. Eine Überprüfung nach dem Vorfall ergab, dass die Entwickler der Website wesentliche Schwachstellen nicht behoben hatten. Da es weder eine Protokollierung noch eine Überwachung des Systems gab, bestand die Datenlücke möglicherweise bereits seit 2013, also über einen Zeitraum von mehr als sieben Jahren.

**Szenario #2:** Bei einer größeren indischen Fluggesellschaft kam es zu einer Datenpanne, die mehr als zehn Jahre lang personenbezogene Daten von Millionen von Fluggästen betraf, einschließlich Reisepass- und Kreditkartendaten. Die Datenpanne trat bei einem externen Cloud-Hosting-Anbieter auf, der die Fluggesellschaft nach einiger Zeit über die Lücke informierte.

**Szenario #3:** Bei einer großen europäischen Fluggesellschaft kam es zu einem meldepflichtigen Verstoß gegen die DSGVO. Der Verstoß wurde Berichten zufolge durch Sicherheitsschwachstellen in Zahlungsanwendungen verschuldet, die von Angreifenden ausgenutzt wurden, die mehr als 400.000 Zahlungsdatensätze von Kunden abfingen. Die Fluggesellschaft wurde daraufhin von der Datenschutzbehörde mit einer Geldstrafe von 20 Millionen Pfund belegt.

## Referenzen

- [OWASP Proactive Controls: C9: Implement Security Logging and Monitoring](https://github.com/OWASP/www-project-proactive-controls/blob/master/v3/en/c9-security-logging.md)
- [OWASP Application Security Verification Standard (ASVS): V7 Error Handling and Logging](https://github.com/OWASP/ASVS/blob/master/4.0/en/0x15-V7-Error-Logging.md#4-0-7)
- [OWASP Web Security Testing Guide: Testing for Improper Error Handling](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/08-Testing_for_Error_Handling/01-Testing_For_Improper_Error_Handling)
- [OWASP Cheat Sheet Series: Logging Vocabulary Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Vocabulary_Cheat_Sheet)
- [OWASP Cheat Sheet Series: Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet)
- [NIST Computer Security Resource Center: SP 1800-11: Data Integrity: Recovering from Ransomware and Other Destructive Events](https://csrc.nist.gov/publications/detail/sp/1800-11/final)
- [NIST Computer Security Resource Center: SP 1800-25: Data Integrity: Identifying and Protecting Assets Against Ransomware and Other Destructive Events](https://csrc.nist.gov/publications/detail/sp/1800-25/final)
- [NIST Computer Security Resource Center: SP 1800-26: Data Integrity: Recovering from Ransomware and Other Destructive Events](https://csrc.nist.gov/publications/detail/sp/1800-26/final)
