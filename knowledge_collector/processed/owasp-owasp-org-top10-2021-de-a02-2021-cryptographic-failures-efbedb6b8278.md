---
title: A02:2021 – Fehlerhafter Einsatz von Kryptographie
source: owasp.org
url: https://owasp.org/Top10/2021/de/A02_2021-Cryptographic_Failures/
collector: owasp
category: web-security
tags:
- web-security
- werden
- die
- sie
- der
date_collected: '2026-07-25T14:26:30.181182Z'
language: unknown
---

# A02:2021 – Fehlerhafter Einsatz von Kryptographie

## Beurteilungskriterien

Zugeordnete CWEsMaximale HäufigkeitDurchschn. HäufigkeitDurchschn. Ausnutzbarkeit (gewichtet)Durchschn. Auswirkungen (gewichtet)Maximale AbdeckungDurchschnittliche AbdeckungGesamtanzahlCVEs insgesamt2946.44 %4.49 %7.296.8179.33 %34.85 %233,7883,075

## Übersicht

Dieses Thema ist um eine Position auf Platz 2 vorgerückt und war früher bekannt als *Verlust der Vertraulichkeit sensibler Daten*, bei dem es sich eher um ein allgemeines Symptom als um eine Grundursache handelt. Nun liegt der Schwerpunkt mehr auf Fehlern im Zusammenhang mit Kryptografie oder dass diese nicht zur Anwendung kommt, was häufig zur Offenlegung sensibler Daten führt. Bemerkenswerte Common Weakness Enumerations (CWEs) sind *CWE-259: Use of Hard-coded Password*, *CWE-327: Broken or Risky Crypto Algorithm* und *CWE-331 Insufficient Entropy*.

## Beschreibung

Zunächst gilt es, den Schutzbedarf der Daten während der Übermittlung und der Speicherung zu ermitteln. Beispielsweise erfordern Passwörter, Kreditkartennummern, Gesundheitsakten, persönliche Informationen und Geschäftsgeheimnisse zusätzlichen Schutz, vor allem dann, wenn diese Daten unter Datenschutzgesetze, z. B. die Datenschutz-Grundverordnung (DSGVO) der EU, oder andere Vorschriften fallen, beispielsweise dem Payment Card Industry Data Security Standard (PCI-DSS).

Folgendes ist zu klären:

- Werden Daten im Klartext übermittelt? Das betrifft Protokolle wie HTTP, SMTP, und FTP unter Umständen auch bei Verwendung von TLS-Upgrades wie STARTTLS. Das Internet ist hier besonders gefährlich. Überprüfen Sie auch internen Datenverkehr, z. B. zwischen Load Balancer, Webservern oder Back-End-Systemen.
- Werden alte oder schwache kryptografische Algorithmen oder Protokolle verwendet, z. B. per Default-Einstellung oder in älterem Code?
- Werden vordefinierte kryptografische Schlüssel verwendet, schwache Schlüssel generiert oder Schlüssel wiederverwendet? Fehlt eine Schlüsselverwaltung oder Schlüsselrotation? Werden kryptografische Schlüssel in Quellcode-Repositories eingecheckt?
- Wird Verschlüsselung nicht verbindlich erzwungen, z. B. fehlen bei Web Anwendungen Vorgaben für den Browser in den entsprechenden HTTP-Headern?
- Werden empfangene Serverzertifikate und die Zertifikatskette korrekt validiert?
- Werden Initialisierungsvektoren ignoriert, wiederverwendet oder nicht ausreichend sicher für den kryptografischen Betriebsmodus generiert? Ist ein unsicherer Betriebsmodus wie ECB im Einsatz? Wird ein Betriebsmodus verwendet, der nur verschlüsselt, obwohl ein AEAD Betriebsmodus angebracht wäre, der auch die Integrität schützt?
- Werden Passwörter direkt als kryptografische Schlüssel verwendet ohne eine Schlüsselableitung mittels Key Derivation Function?
- Werden Zufallszahlen für kryptografische Zwecke genutzt, die nicht auf kryptografische Anforderungen ausgelegt sind? Selbst wenn die richtige Funktion genutzt wird, muss diese eventuell vom Entwickler korrekt initialisiert werden. Wurde eine integrierte starke Initialisierung eventuell durch einen Entwickler mit einem schwachen Wert überschrieben, dem es an ausreichender Entropie und Nichtvorhersehbarkeit mangelt?
- Werden Hash-Funktionen mit bekannten Schwächen wie MD5 oder SHA1 verwendet oder werden nicht-kryptografische Hash-Funktionen verwendet, wenn kryptografische Hash-Funktionen benötigt werden?
- Werden veraltete kryptografische Padding Methoden verwendet, z. B. PKCS#1 v1.5?
- Sind kryptografische Fehlermeldungen oder Seitenkanäle ausnutzbar, beispielsweise in Form von Padding-Oracle-Angriffen?

Siehe [ASVS V6 Stored Cryptography](https://github.com/OWASP/ASVS/blob/master/4.0/en/0x14-V6-Cryptography.md#4-0-6), [V8 Data Protection](https://github.com/OWASP/ASVS/blob/master/4.0/en/0x16-V8-Data-Protection.md#4-0-8), [V9 Communication](https://github.com/OWASP/ASVS/blob/master/4.0/en/0x17-V9-Communications.md#4-0-9)

## Prävention und Gegenmaßnahmen

Gehen Sie als Minimum wie folgt vor und konsultieren Sie die Referenzen:

- Klassifizieren Sie die Daten, die von einer Anwendung verarbeitet, gespeichert oder übermittelt werden nach ihrem Schutzbedarf. Berücksichtigen Sie dabei auch Datenschutzgesetze, regulatorische und Geschäfts-Anforderungen.
- Speichern Sie sensible Daten nicht unnötig. Löschen Sie sensible Daten auf sichere Weise sobald wie möglich oder verwenden Sie Techniken wie PCI-DSS-konformes Speichern von Ersatzwerten (tokenization) oder gar gekürzten (truncation) Werten. Daten, die es nicht mehr gibt, können auch nicht gestohlen werden.
- Stellen Sie sicher, dass alle vertraulichen Daten bei Speicherung verschlüsselt werden.
- Stellen Sie sicher, dass aktuelle, starke, standardisierte Algorithmen, Protokolle und Schlüssel, z. B. gemäß BSI TR-02102, verwendet werden. Etablieren Sie wirksames Schlüsselmanagement für kryptografische Schlüssel.
- Verschlüsseln Sie alle Daten während der Übertragung mit sicheren Protokollen wie TLS. Priorisieren Sie dabei durch serverseitig Cipher-Suiten, die Forward Secrecy (FS) bieten, und sichere Parameter. Erzwingen Sie die Verschlüsselung wenn möglich, z. B. durch Einführung von HTTP Strict Transport Security (HSTS).
- Deaktivieren Sie das Caching für den Empfang vertraulicher Daten.
- Wenden Sie die Sicherheitsmaßnahmen gemäß dem Schutzbedarf der Datenklassifizierung an.
- Verwenden Sie keine veralteten Protokolle wie FTP und SMTP für den Transport sensibler Daten.
- Verwenden Sie spezielle Hash-Funktionen für das Hashen von Passwörtern, bei denen für jedes Passwort ein Salt-Wert (salted hash) zum Einsatz kommt und durch Parametrisierung der Rechenaufwand adaptiv gesteuert werden kann (work-factor). Beispiele sind: Argon2, scrypt, bcrypt oder PBKDF2.
- Initialisierungsvektoren müssen passend zum kryptografischen Betriebsmodus gewählt werden. In vielen Fällen bedeutet dies, dass ein CSPRNG (kryptografisch sicherer Pseudozufallszahlengenerator) für die Generierung des Initialisierungsvektors verwendet wird. Für Modi, die eine Nonce erfordern, benötigt der Initialisierungsvektor nicht notwendigerweise einen CSPRNG. In allen Fällen darf der gleiche Initialisierungsvektor niemals zweimal für den gleichen Schlüssel verwendet werden.
- Verwenden Sie immer eine authentifizierte Verschlüsselung statt nur einer Verschlüsselung.
- Schlüssel sollten kryptografisch zufällig generiert und als Byte-Arrays im Speicher gehalten werden. Wenn ein Passwort zur Verschlüsselung verwendet werden soll, muss über eine Funktion zur Schlüsselableitung ein Schlüssel generiert werden.
- Stellen Sie sicher, dass an den notwendigen Stellen kryptografisch sichere, unvorhersagbare Zufallszahlen verwendet werden, und dass der Pseudozufallszahlengenerator nicht auf vorhersehbare Weise oder nur mit geringer Entropie initialisiert wurde. Bei den meisten modernen APIs muss der Entwickler die Initialisierung des Pseudozufallszahlengenerators (CSPRNG) nicht manuell durchführen.
- Vermeiden Sie veraltete kryptografische Funktionen und Padding-Verfahren wie MD5, SHA1, PKCS Nummer 1 v1.5.
- Lassen Sie die Wirksamkeit der Einstellungen unabhängig überprüfen.

## Beispielhafte Angriffsszenarien

**Szenario Nr. 1:**: Eine Anwendung verschlüsselt Kreditkartendaten automatisch bei der Speicherung in einer Datenbank. Das bedeutet aber auch, dass durch SQL-Injection erlangte Kreditkartendaten in diesem Fall automatisch entschlüsselt werden.

**Szenario Nr. 2:**: Eine Webseite benutzt kein TLS,
erzwingt dies nicht auf allen Seiten oder lässt schwache Verschlüsselung zu.
Die angreifende Person liest die Kommunikation mit (z. B. in einem offenen WLAN), ersetzt HTTPS- durch HTTP-Verbindungen, hört diese ab und stiehlt das Sitzungscookie.
Durch Wiedereinspielen dieses Cookies übernimmt die angreifende Person die (authentifizierte) Sitzung des Nutzers und erlangt Zugriff auf dessen private Daten.
Anstatt dessen kann die angreifende Person auch die übertragenen Daten ändern, z. B. den Empfänger einer Überweisung.

**Szenario Nr. 3:**: Die Passwortdatenbank benutzt einfache Hashwerte oder Hashes ohne Salt zur Speicherung der Passwörter. Eine Schwachstelle in der Downloadfunktion erlaubt Angreifenden den Zugriff auf die Passwortdatei. Zu Hashes ohne Salt kann über vorausberechnete Rainbow-Tabellen der Klartext gefunden werden. Hashes, die über einfache oder schnelle Funktionen berechnet wurden, können effizient mit Grafikkarten gebrochen werden.

## Referenzen

- [OWASP Proactive Controls: C8: Protect Data Everywhere](https://github.com/OWASP/www-project-proactive-controls/blob/master/v3/en/c8-protect-data-everywhere.md)
- [OWASP Application Security Verification Standard (ASVS): V6 Stored Cryptography](https://github.com/OWASP/ASVS/blob/master/4.0/en/0x14-V6-Cryptography.md#4-0-6),[V8 Data Protection](https://github.com/OWASP/ASVS/blob/master/4.0/en/0x16-V8-Data-Protection.md#4-0-8),[V9 Communication](https://github.com/OWASP/ASVS/blob/master/4.0/en/0x17-V9-Communications.md#4-0-9)
- [OWASP Cheat Sheet Series: Transport Layer Protection Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Protection_Cheat_Sheet)
- [OWASP Cheat Sheet Series: User Privacy Protection Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/User_Privacy_Protection_Cheat_Sheet)
- [OWASP Cheat Sheet Series: Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet)
- [OWASP Cheat Sheet Series: Cryptographic Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet)
- [OWASP Cheat Sheet Series: HTTP Strict Transport Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Strict_Transport_Security_Cheat_Sheet)
- [OWASP Web Security Testing Guide: Testing for Weak Cryptography](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/09-Testing_for_Weak_Cryptography/index)

## Liste der zugeordneten CWEs

- [CWE-261: Weak Encoding for Password](https://cwe.mitre.org/data/definitions/261.html)
- [CWE-296: Improper Following of a Certificate's Chain of Trust](https://cwe.mitre.org/data/definitions/296.html)
- [CWE-310: Cryptographic Issues (CWE CATEGORY)](https://cwe.mitre.org/data/definitions/310.html)
- [CWE-319: Cleartext Transmission of Sensitive Information](https://cwe.mitre.org/data/definitions/319.html)
- [CWE-321: Use of Hard-coded Cryptographic Key](https://cwe.mitre.org/data/definitions/321.html)
- [CWE-322: Key Exchange without Entity Authentication](https://cwe.mitre.org/data/definitions/322.html)
- [CWE-323: Reusing a Nonce, Key Pair in Encryption](https://cwe.mitre.org/data/definitions/323.html)
- [CWE-324: Use of a Key Past its Expiration Date](https://cwe.mitre.org/data/definitions/324.html)
- [CWE-325: Missing Cryptographic Step](https://cwe.mitre.org/data/definitions/325.html)
- [CWE-326: Inadequate Encryption Strength](https://cwe.mitre.org/data/definitions/326.html)
- [CWE-327: Use of a Broken or Risky Cryptographic Algorithm](https://cwe.mitre.org/data/definitions/327.html)
- [CWE-328: Use of Weak Hash](https://cwe.mitre.org/data/definitions/328.html)
- [CWE-329: Generation of Predictable IV with CBC Mode](https://cwe.mitre.org/data/definitions/329.html)
- [CWE-330: Use of Insufficiently Random Values](https://cwe.mitre.org/data/definitions/330.html)
- [CWE-331: Insufficient Entropy](https://cwe.mitre.org/data/definitions/331.html)
- [CWE-335: Incorrect Usage of Seeds in Pseudo-Random Number Generator (PRNG)](https://cwe.mitre.org/data/definitions/335.html)
- [CWE-336: Same Seed in Pseudo-Random Number Generator (PRNG)](https://cwe.mitre.org/data/definitions/336.html)
- [CWE-337: Predictable Seed in Pseudo-Random Number Generator (PRNG)](https://cwe.mitre.org/data/definitions/337.html)
- [CWE-338: Use of Cryptographically Weak Pseudo-Random Number Generator (PRNG)](https://cwe.mitre.org/data/definitions/338.html)
- [CWE-340: Generation of Predictable Numbers or Identifiers](https://cwe.mitre.org/data/definitions/340.html)
- [CWE-347: Improper Verification of Cryptographic Signature](https://cwe.mitre.org/data/definitions/347.html)
- [CWE-523: Unprotected Transport of Credentials](https://cwe.mitre.org/data/definitions/523.html)
- [CWE-720: OWASP Top Ten 2007 Category A9 - Insecure Communications (CWE CATEGORY)](https://cwe.mitre.org/data/definitions/720.html)
- [CWE-757: Selection of Less-Secure Algorithm During Negotiation ('Algorithm Downgrade')](https://cwe.mitre.org/data/definitions/757.html)
- [CWE-759: Use of a One-Way Hash without a Salt](https://cwe.mitre.org/data/definitions/759.html)
- [CWE-760: Use of a One-Way Hash with a Predictable Salt](https://cwe.mitre.org/data/definitions/760.html)
- [CWE-780: Use of RSA Algorithm without OAEP](https://cwe.mitre.org/data/definitions/780.html)
- [CWE-818: OWASP Top Ten 2010 Category A9 - Insufficient Transport Layer Protection (CWE CATEGORY)](https://cwe.mitre.org/data/definitions/818.html)
- [CWE-916: Use of Password Hash With Insufficient Computational Effort](https://cwe.mitre.org/data/definitions/916.html)
