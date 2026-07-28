---
title: A07:2021 – Identification and Authentication Failures
source: owasp.org
url: https://owasp.org/Top10/2021/tr/A07_2021-Identification_and_Authentication_Failures/
collector: owasp
category: web-security
tags:
- web-security
- authentication
- kullan
- lar
- session
date_collected: '2026-07-25T14:28:31.147436Z'
language: unknown
---

# A07:2021 – Identification and Authentication Failures

## Faktörler

CWEs MappedMax Incidence RateAvg Incidence RateAvg Weighted ExploitAvg Weighted ImpactMax CoverageAvg CoverageTotal OccurrencesTotal CVEs2214.84%2.55%7.406.5079.51%45.72%132,1953,897

## Genel Bakış

Önceden *Broken Authentication* olarak bilinen bu kategori, ikinci sıradan aşağı kaydı ve artık kimlik doğrulama (authentication) değil, kimlik tespiti (identification) ile ilgili hatalara dair Common Weakness Enumerations (CWEs) kümelerini de içeriyor. Dikkate değer CWE’ler arasında *CWE-297: Improper Validation of Certificate with Host Mismatch*, *CWE-287: Improper Authentication* ve *CWE-384: Session Fixation* bulunur.

## Açıklama

Kullanıcının kimliğinin doğrulanması, authentication ve session yönetimi; authentication kaynaklı saldırılara karşı korunmak için kritiktir. Aşağıdaki durumlar varsa uygulamada authentication zafiyetleri olabilir:

- Saldırganın geçerli username/password listeleriyle credential stuffing gibi otomatik saldırılar yapmasına izin veriyorsa.
- Brute force veya diğer otomatik saldırılara izin veriyorsa.
- “Password1” veya “admin/admin” gibi varsayılan, zayıf veya yaygın parolalara izin veriyorsa.
- “Bilgiye dayalı sorular” gibi güvenli hâle getirilemeyen zayıf/hatalı credential recovery ve forgot-password süreçleri kullanılıyorsa.
- Parolalar plain text, şifreli ama hatalı veya zayıf şekilde hash’lenmiş data store’larda tutuluyorsa (bkz. [A02:2021-Cryptographic Failures](../A02_2021-Cryptographic_Failures/)).
- Multi-factor authentication eksik veya etkisizse.
- Session identifier URL’de açığa çıkıyorsa.
- Başarılı login’den sonra aynı session identifier yeniden kullanılıyorsa.
- Session ID’ler doğru şekilde geçersiz kılınmıyorsa. Kullanıcı session’ları veya authentication token’ları (özellikle single sign-on (SSO) token’ları) logout sırasında veya belli bir inactivity süresinden sonra düzgün biçimde invalid edilmiyorsa.

## Nasıl Önlenir

- Mümkün olan yerlerde multi-factor authentication uygulayın; credential stuffing, brute force ve çalıntı credential tekrar kullanımına karşı koruma sağlar.
- Özellikle admin kullanıcılar için, varsayılan credential’larla ship/deploy etmeyin.
- Yeni veya değiştirilen parolaları en kötü 10.000 parola listesine karşı test etmek gibi zayıf parola kontrollerini uygulayın.
- Parola uzunluğu, karmaşıklığı ve rotasyon politikalarını NIST 800-63b’nin 5.1.1 (Memorized Secrets) bölümündeki rehberle veya diğer modern, kanıta dayalı parola politikalarıyla hizalayın.
- Kayıt, credential recovery ve API akışlarını; tüm sonuçlar için aynı mesajları kullanarak account enumeration saldırılarına karşı sertleştirin.
- Başarısız login denemelerini sınırlayın veya giderek geciktirin; ancak bir denial of service senaryosu yaratmamaya dikkat edin. Tüm başarısızlıkları log’layın ve credential stuffing, brute force veya diğer saldırılar tespit edildiğinde yöneticileri uyarın.
- Login sonrasında yüksek entropili yeni ve rastgele bir session ID üreten, server-side, güvenli ve built-in bir session manager kullanın. Session identifier URL’de olmamalı, güvenli biçimde saklanmalı ve logout, idle ve absolute timeout’lardan sonra invalid edilmelidir.

## Örnek Saldırı Senaryoları

**Senaryo #1:** Credential stuffing, bilinen parola listelerinin kullanımıyla yapılan yaygın bir saldırıdır. Bir uygulama, otomatik tehdit veya credential stuffing koruması uygulamıyorsa; bu uygulama, credential’ların geçerli olup olmadığını test etmek için bir “password oracle” olarak kullanılabilir.

**Senaryo #2:** Çoğu authentication saldırısı, parolaların tek faktör olarak kullanılmaya devam edilmesi nedeniyle gerçekleşir. Bir zamanlar en iyi uygulama sayılan parola rotasyonu ve karmaşıklık gereksinimleri, kullanıcıları zayıf parolalar kullanmaya ve yeniden kullanmaya iter. NIST 800-63’e göre bu uygulamalardan vazgeçilmesi ve multi-factor authentication’a geçilmesi tavsiye edilir.

**Senaryo #3:** Uygulama session timeout’ları doğru ayarlanmamıştır. Bir kullanıcı, public bir bilgisayardan uygulamaya erişir. “Logout”u seçmek yerine yalnızca tarayıcı sekmesini kapatır ve uzaklaşır. Bir saldırgan bir saat sonra aynı tarayıcıyı kullanır ve kullanıcı hâlâ authenticated durumdadır.

## Referanslar

- [OWASP Application Security Verification Standard: V2 authentication](https://owasp.org/www-project-application-security-verification-standard)
- [OWASP Application Security Verification Standard: V3 Session Management](https://owasp.org/www-project-application-security-verification-standard)

## Eşleştirilen CWE Listesi

[CWE-255 Credentials Management Errors](https://cwe.mitre.org/data/definitions/255.html)

[CWE-259 Use of Hard-coded Password](https://cwe.mitre.org/data/definitions/259.html)

[CWE-287 Improper Authentication](https://cwe.mitre.org/data/definitions/287.html)

[CWE-288 Authentication Bypass Using an Alternate Path or Channel](https://cwe.mitre.org/data/definitions/288.html)

[CWE-290 Authentication Bypass by Spoofing](https://cwe.mitre.org/data/definitions/290.html)

[CWE-294 Authentication Bypass by Capture-replay](https://cwe.mitre.org/data/definitions/294.html)

[CWE-295 Improper Certificate Validation](https://cwe.mitre.org/data/definitions/295.html)

[CWE-297 Improper Validation of Certificate with Host Mismatch](https://cwe.mitre.org/data/definitions/297.html)

[CWE-300 Channel Accessible by Non-Endpoint](https://cwe.mitre.org/data/definitions/300.html)

[CWE-302 Authentication Bypass by Assumed-Immutable Data](https://cwe.mitre.org/data/definitions/302.html)

[CWE-304 Missing Critical Step in Authentication](https://cwe.mitre.org/data/definitions/304.html)

[CWE-306 Missing Authentication for Critical Function](https://cwe.mitre.org/data/definitions/306.html)

[CWE-307 Improper Restriction of Excessive Authentication Attempts](https://cwe.mitre.org/data/definitions/307.html)

[CWE-346 Origin Validation Error](https://cwe.mitre.org/data/definitions/346.html)

[CWE-521 Weak Password Requirements](https://cwe.mitre.org/data/definitions/521.html)

[CWE-613 Insufficient Session Expiration](https://cwe.mitre.org/data/definitions/613.html)

[CWE-620 Unverified Password Change](https://cwe.mitre.org/data/definitions/620.html)

[CWE-640 Weak Password Recovery Mechanism for Forgotten Password](https://cwe.mitre.org/data/definitions/640.html)

[CWE-798 Use of Hard-coded Credentials](https://cwe.mitre.org/data/definitions/798.html)

[CWE-940 Improper Verification of Source of a Communication Channel](https://cwe.mitre.org/data/definitions/940.html)
