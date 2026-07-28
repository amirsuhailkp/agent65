---
title: Wie man die OWASP Top 10 als Standard verwendet
source: owasp.org
url: https://owasp.org/Top10/2021/de/A00_2021_How_to_use_the_OWASP_Top_10_as_a_standard/
collector: owasp
category: web-security
tags:
- web-security
- die
- owasp
- top
- der
date_collected: '2026-07-25T14:26:27.942651Z'
language: unknown
---

# Wie man die OWASP Top 10 als Standard verwendet

Die OWASP Top 10 sind in erster Linie ein Sensibilisierungsdokument. Dies hat Unternehmen jedoch nicht davon abgehalten, sie seit ihrer Einführung im Jahr 2003 als De-facto-Standard für Anwendungssicherheit (AppSec) zu verwenden. Wenn Sie die OWASP Top 10 als Coding- oder Teststandard verwenden möchten, sollten Sie wissen, dass es sich um das absolute Minimum und nur um einen Anfang handelt.

Eine der Schwierigkeiten bei der Verwendung der OWASP Top 10 als Standard besteht darin, dass wir AppSec-Risiken dokumentieren und nicht unbedingt leicht testbare Probleme.
Beispielsweise liegt [A04:2021 Unsicheres Anwendungsdesign](../A04_2021-Insecure_Design/) außerhalb des Rahmens der meisten Testverfahren.
Ein weiteres Beispiel ist das Testen, ob eine wirksame Protokollierung und Überwachung implementiert und operativ ist, was nur durch Befragungen und Stichproben wirksamer Behandlungen von Incidents möglich ist.
Ein Tool zur statischen CodeAnalyse kann nach fehlender Protokollierung suchen,
es wird jedoch unmöglich sein, festzustellen, ob die Geschäftslogik oder die Zugriffskontrolle kritische Sicherheitsverstöße protokolliert. Penetrationstests werden möglicherweise nur in einer Testumgebung stattfinden, die selten in der gleichen Weise wie die Produktion überwacht ist, dabei ist es schwierig feststellen ob eine Reaktion auf die Vorfälle ausgelöst wurde.

Hier sind unsere Empfehlungen, wann es sinnvoll ist, die OWASP Top 10 zu verwenden:

AnwendungsfallOWASP Top 10 2021OWASP Application Security Verification StandardAwarenessjaAusbildungEinstiegsniveauumfassendDesign und ArchitekturgelegentlichjaCodierungsstandardals MindestanforderungjaSecurity Code Reviewals MindestanforderungjaCheckliste für Peer-Reviewsals MindestanforderungjaUnit-TestsgelegentlichjaIntegrationstestsgelegentlichjaPenetrationstestsals MindestanforderungjaWerkzeugunterstützungals MindestanforderungjaSichere Lieferkettegelegentlichja

Wir empfehlen jedem, der einen Anwendungssicherheitsstandard übernehmen möchte,
den [OWASP Application Security Verification Standard](https://owasp.org/www-project-application-security-verification-standard/) (ASVS) zu verwenden,
da er entworfen wurde, um überprüfbar und testbar zu sein und in allen Teilen eines sicheren Entwicklungslebenszyklus verwendet werden kann.

Für Tool-Anbieter ist der ASVS die einzig akzeptable Wahl. Aufgrund der Beschaffenheit mehrerer Top-10-Risiken, insbesondere A04:2021 – Unsicheres Anwendungsdesign, können Tools die OWASP Top 10 nicht umfassend erkennen, testen oder davor schützen. OWASP rät davon ab, eine vollständige Abdeckung der OWASP Top 10 zu behaupten, da dies schlichtweg unwahr ist.
