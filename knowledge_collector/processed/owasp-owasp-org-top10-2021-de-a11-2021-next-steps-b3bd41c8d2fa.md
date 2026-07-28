---
title: A11:2021 – Nächste Schritte
source: owasp.org
url: https://owasp.org/Top10/2021/de/A11_2021-Next_Steps/
collector: owasp
category: web-security
tags:
- web-security
- die
- und
- der
- oder
date_collected: '2026-07-25T14:26:40.131172Z'
language: unknown
---

# A11:2021 – Nächste Schritte

Die OWASP Top 10 sind von Natur aus auf die zehn bedeutendsten Risiken beschränkt.
Jede OWASP Top 10 hat Risiken, die an der Schwelle zur Aufnahme in die Top 10 stehen, die aber letztendlich doch nicht in die Liste aufgenommen wurden.
Ganz gleich, wie wir die Daten zu interpretieren oder zu verändern versuchten, die anderen Risiken waren weitaus häufiger und schwerwiegender.

Für Unternehmen, die auf ein ausgereiftes Programm zur Anwendungssicherheit hinarbeiten, oder für Sicherheitsberatungsunternehmen und Tool-Anbieter, die ihre Angebote erweitern möchten, lohnen sich die folgenden vier Probleme, die es zu identifizieren und zu beheben gilt.

## Probleme mit der Codequalität

Zugeordnete CWEsMaximale HäufigkeitDurchschn. HäufigkeitDurchschn. Ausnutzbarkeit (gewichtet)Durchschn. Auswirkungen (gewichtet)Maximale AbdeckungDurchschnittliche AbdeckungGesamtanzahlCVEs insgesamt3849.46 %2.22 %7.16.760.85 %23.42 %1017367564

- **Beschreibung.** Zu den Problemen der Codequalität gehören bekannte Sicherheitsmängel oder -muster, die Wiederverwendung von Variablen für mehrere Zwecke, die Offenlegung vertraulicher Informationen in der Debugging-Ausgabe, Off-by-One-Fehler, TOCTOU-Race-Conditions (Time of Check/Time of Use), Konvertierungsfehler bei der Verwendung von vorzeichenlosen oder vorzeichenbehafteten Daten, die Verarbeitung nach dem Freigeben von Daten und vieles mehr. Das Besondere an diesem Abschnitt ist, dass sie in der Regel durch strenge Compiler-Flags, statische Code-Analyse-Tools und Linter-IDE-Plugins identifiziert werden können. Moderne Sprachen haben viele dieser Probleme durch ihr Design eliminiert, wie z. B. Rusts Konzept des Speicherbesitzes und der -ausleihe, Rusts Threading-Design und die strikte Typisierung und Grenzwertprüfung in Go.
- **Prävention und Gegenmaßnahmen**. Aktivieren und verwenden Sie die statische Code- Analyse Ihres Editors und Ihrer Sprache. Erwägen Sie die Verwendung eines Tools zur statischen Codeanalyse. Überlegen Sie, ob es möglich ist, eine Sprache oder ein Framework zu verwenden oder dorthin zu migrieren, welches Fehlerklassen eliminiert, wie z. B. in Rust oder Go.
- **Beispielhafte Angriffsszenarien**. Ein Angreifer könnte vertrauliche Informationen erhalten oder verändern, indem er eine Race Condition ausnutzt, die eine statisch freigegebene Variable in mehreren Threads verwendet.
- **Referenzen**
- [OWASP Code Review Guide: OWASP Code Review Guide [PDF]](https://owasp.org/www-project-code-review-guide/assets/OWASP_Code_Review_Guide_v2.pdf)
- [Google Engineering Practices Documentation: Code Review Guide](https://google.github.io/eng-practices/review/)

## Denial of Service

Zugeordnete CWEsMaximale HäufigkeitDurchschn. HäufigkeitDurchschn. Ausnutzbarkeit (gewichtet)Durchschn. Auswirkungen (gewichtet)Maximale AbdeckungDurchschnittliche AbdeckungGesamtanzahlCVEs insgesamt817.54 %4.89 %8.35.979.58 %33.26 %66985973

- **Beschreibung**. Mit den nötigen Ressourcen ist ein Denial-of-Service immer möglich.
  Design- und Programmierpraktiken haben jedoch einen erheblichen Einfluss auf das Ausmaß des Denial-of-Service.
  Mit ausreichenden Ressourcen ist eine Denial of Service immer möglich. Allerdings haben Design und Programmierpraktiken einen erheblichen Einfluss auf das Ausmaß des Denial of Service. Angenommen, jede Person mit einem Link kann auf eine große Datei zugreifen, oder auf jeder Seite findet eine rechenintensive Transaktion statt. In diesem Fall ist die Denial-of-Service-Attacke mit weniger Aufwand zu bewerkstelligen.
- **Prävention und Gegenmaßnahmen**. Testen Sie die Effizienz des Codes auf CPU-, E/A- und Speichernutzung, überarbeiten, optimieren oder cachen Sie aufwendige Operationen. Erwägen Sie Zugriffskontrollen für größere Objekte, um sicherzustellen, dass nur autorisierte Personen auf große Dateien oder Objekte zugreifen können, oder stellen Sie sie über ein Edge-Caching-Netzwerk bereit.
- **Beispielhafte Angriffsszenarien**. Ein Angreifer könnte feststellen, dass ein Vorgang 5-10 Sekunden benötigt, um ihn abzuschließen. Wenn vier Threads gleichzeitig laufen, scheint der Server nicht mehr zu reagieren. Der Angreifer nutzt 1000 Threads und nimmt das gesamte System offline.
- **Referenzen**

## Speicherverwaltungsfehler

Zugeordnete CWEsMaximale HäufigkeitDurchschn. HäufigkeitDurchschn. Ausnutzbarkeit (gewichtet)Durchschn. Auswirkungen (gewichtet)Maximale AbdeckungDurchschnittliche AbdeckungGesamtanzahlCVEs insgesamt147.03 %1.16 %6.78.156.06 %31.74 %2657616184

- **Beschreibung**. Webanwendungen werden in der Regel in Managed Memory-Sprachen geschrieben, wie zum Beispiel Java, .NET oder node.js (JavaScript oder TypeScript). Allerdings sind diese Sprachen in Systemsprachen geschrieben, die Probleme mit der Speicherverwaltung haben, z. B. Puffer- oder Heap-Überläufe, Use after free, Integer-Überläufe und mehr. Im Laufe der Jahre gab es viele Sandbox-„Ausbrüche“, die zeigen, dass nur weil die Webanwendungssprache nominell „ speicher- sicher“ ist, die Grundlagen es nicht sind.
- **Prävention und Gegenmaßnahmen**. Viele moderne APIs sind heute in speichersicheren Sprachen wie Rust oder Go geschrieben. Im Fall von Rust ist die Speichersicherheit ein entscheidendes Merkmal der Sprache. Bei vorhandenem Code kann die Verwendung von strengen Compiler-Flags, starker Typisierung, statischer Codeanalyse und Fuzzing-Tests bei der Identifizierung von Speicherlecks, Speicher- und Array-Überläufen und vielem mehr hilfreich sein.
- **Beispielhafte Angriffsszenarien**. Puffer- und Heap-Überläufe sind seit Jahren ein beliebtes Ziel von Angreifern. Der Angreifer sendet dabei Daten an ein Programm, welches diese in einem zu kleinen Stack-Puffer speichert. Dies hat zur Folge, dass Informationen auf dem Call Stack überschrieben werden, darunter auch der Rückgabezeiger der Funktion. Die Daten legen den Wert des Rückgabezeigers fest, so dass bei der Rückkehr der Funktion die Kontrolle an den in den Daten des Angreifers enthaltenen Schadcode übergeben wird.
- **Referenzen**
