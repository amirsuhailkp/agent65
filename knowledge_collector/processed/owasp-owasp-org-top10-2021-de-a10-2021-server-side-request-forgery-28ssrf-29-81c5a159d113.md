---
title: A10:2021 – Server-Side Request Forgery SSRF
source: owasp.org
url: https://owasp.org/Top10/2021/de/A10_2021-Server-Side_Request_Forgery_(SSRF)/
collector: owasp
category: web-security
tags:
- web-security
- die
- und
- ssrf
- sie
date_collected: '2026-07-25T14:26:39.130007Z'
language: unknown
---

# A10:2021 – Server-Side Request Forgery (SSRF)

## Beurteilungskriterien

Zugeordnete CWEsMaximale HäufigkeitDurchschn. HäufigkeitDurchschn. Ausnutzbarkeit (gewichtet)Durchschn. Auswirkungen (gewichtet)Maximale AbdeckungDurchschnittliche AbdeckungGesamtanzahlCVEs insgesamt12.72 %2.72 %8.286.7267.72 %67.72 %9,503385

## Übersicht

Diese Kategorie stammt aus der Top-10-Community-Umfrage (Nr. 1). Die Daten zeigen eine relativ niedrige Häufigkeit mit einer überdurchschnittlichen Testabdeckung und überdurchschnittlichen Missbrauchs- und Auswirkungspotentialen. Da es sich bei neuen Einträgen wahrscheinlich um einzelne oder kleine Gruppen von Common Weakness Enumerations (CWEs) handelt, die für Aufmerksamkeit und Bewusstsein sorgen, besteht die Hoffnung, dass sie in einer zukünftigen Ausgabe in eine größere Kategorie aufgenommen werden können.

## Beschreibung

SSRF-Schwachstellen treten immer dann auf, wenn eine Webanwendung eine Remote-Ressource abruft, ohne die, vom Nutzenden angegebene URL zu überprüfen. Dadurch kann ein Angreifender die Anwendung dazu zwingen, eine manipulierte Anfrage an ein unerwartetes Ziel zu senden, selbst wenn sie durch eine Firewall, ein VPN oder eine andere Art von Netzwerkzugriffskontrollliste (ACL) geschützt ist.

Da moderne Webanwendungen Nutzenden komfortable Funktionen bieten, wird das Abrufen einer URL zu einem gängigen Szenario. Infolgedessen nimmt die Häufigkeit von SSRF zu. Außerdem nimmt der Schweregrad von SSRF aufgrund von der Verbreitung von Cloud-Diensten und der Komplexität der Architekturen zu.

## Prävention und Gegenmaßnahmen

Entwickler können SSRF verhindern, indem sie folgende Defense-in-Depth-Controls implementieren:

### **Auf der Netzwerk-Ebene**

- Segmentieren Sie die Remote-Ressourcenzugriffsfunktionalität in separate Netzwerke, um die Auswirkungen von SSRF zu reduzieren.
- Setzen Sie standardmäßig blockierende Firewall-Richtlinien oder Netzwerkzugriffskontrollregeln ein, um den gesamten Intranet-Verkehr zu blockieren, der nicht unbedingt erforderlich ist.

  *Hinweise:*
  ~ Legen Sie eine Zuständigkeit und einen Lebenszyklus für Firewall-Regeln auf der Grundlage von Anwendungen fest.
  ~ Protokollieren aller akzeptierten*und*blockierten Netzströme auf Firewalls (siehe[A09:2021 – Fehler beim Logging und Monitoring](../A09_2021-Security_Logging_and_Monitoring_Failures/)).

### **Auf der Anwendungsebene:**

- Bereinigung und Validierung aller vom Client gelieferten Eingabedaten
- Erzwingen Sie das URL-Schema, den Port und das Ziel mit einer Positivliste
- Senden Sie keine ungeprüften Antworten an Clients.
- Deaktivieren Sie HTTP-Umleitungen.
- Achten Sie auf die URL-Konsistenz, um Angriffe wie DNS-Rebinding und „time of check, time of use“ (TOCTOU) Race Conditions zu vermeiden

Verhindern Sie SSRF nicht durch die Verwendung einer Negativliste oder eines regulären Ausdrucks. Angreifer verfügen über Payload-Listen, Tools und Fähigkeiten zum Umgehen von Negativlisten.

### **Zusätzliche zu berücksichtigende Maßnahmen:**

- Setzen Sie keine anderen sicherheitsrelevanten Dienste auf Frontsystemen ein (z. B. OpenID). Kontrollieren Sie den lokalen Verkehr auf diesen Systemen (z. B. localhost).
- Für Frontends mit dedizierten und verwaltbaren Gruppen für Anwendende nutzen Sie Netzwerkverschlüsselung (z. B. VPNs) auf unabhängigen Systemen um sehr hohen Schutzbedarf zu berücksichtigen.

## Beispielhafte Angriffsszenarien

Angreifende können SSRF nutzen, um Systeme anzugreifen, die durch Web Application Firewalls, Firewalls oder Netzwerk-ACLs geschützt sind, und dabei Szenarien wie folgende verwenden:

**Szenario Nr. 1:** Port-Scan interner Server – Wenn die Netzwerkarchitektur nicht segmentiert ist, können Angreifende interne Netzwerke abbilden und anhand der Verbindungsergebnisse oder der verstrichenen Zeit für die Verbindung oder Ablehnung von SSRF-Nutzlast-Verbindungen feststellen, ob Ports auf internen Servern offen oder geschlossen sind.

**Szenario Nr. 2:** Preisgabe sensibler Daten – Angreifende können auf lokale Dateien oder interne Dienste zugreifen, um vertrauliche Informationen wie „file:///etc/passwd“ und „http://localhost:28017/“ zu erhalten.

**Szenario Nr. 3:** Zugriff auf Metadatenspeicher von Cloud-Diensten – Die meisten Cloud-Anbieter verfügen über Metadatenspeicher wie „http://169.254.169.254/“. Eine angreifende Person kann die Metadaten lesen, um an vertrauliche Informationen zu gelangen.

**Szenario Nr. 4:** Kompromittierung interner Dienste – Die angreifende Person kann interne Dienste missbrauchen, um weitere Angriffe wie beispielsweise Remote Code Execution (RCE) oder Denial of Service (DoS) durchzuführen.

## Referenzen

- [OWASP Cheat Sheet Series: Server Side Request Forgery Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet)
- [Portswigger Web Security Academy: Server-side request forgery (SSRF)](https://portswigger.net/web-security/ssrf)
- [Acunetix Web Security Blog: What is Server-Side Request Forgery (SSRF)?](https://www.acunetix.com/blog/articles/server-side-request-forgery-vulnerability/)
- [Wallarm: SSRF bible [PDF]](https://cheatsheetseries.owasp.org/assets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet_SSRF_Bible.pdf)
- [Blackhat USA 2017: Orange Tsai: A New Era of SSRF - Exploiting URL Parser in Trending Programming Languages! [pdf]](https://www.blackhat.com/docs/us-17/thursday/us-17-Tsai-A-New-Era-Of-SSRF-Exploiting-URL-Parser-In-Trending-Programming-Languages.pdf)
