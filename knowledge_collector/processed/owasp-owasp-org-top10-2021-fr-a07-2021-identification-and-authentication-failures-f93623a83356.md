---
title: A07:2021 – Identification et authentification de mauvaise qualité
source: owasp.org
url: https://owasp.org/Top10/2021/fr/A07_2021-Identification_and_Authentication_Failures/
collector: owasp
category: web-security
tags:
- web-security
- les
- des
- passe
- mots
date_collected: '2026-07-25T14:27:08.690213Z'
language: unknown
---

# A07:2021 – Identification et authentification de mauvaise qualité

## Facteurs

CWEs associéesTaux d'incidence maxTaux d'incidence moyenExploitation pondérée moyenneImpact pondéré moyenCouverture maxCouverture moyenneNombre total d'occurrencesNombre total de CVEs2214,84 %2,55 %7,406,5079,51 %45,72 %132,1953 897

## Aperçu

Précédemment connue sous le nom de *Authentification de mauvaise qualité*, cette catégorie a glissé de la deuxième position et comprend maintenant les Common Weakness Enumerations (CWEs) liées aux échecs d'identification. Les CWEs les plus importantes sont *CWE-297 : Improper Validation of Certificate with Host Mismatch*, *CWE-287 : Improper Authentication*, et *CWE-384 : Session Fixation*.

## Description

La confirmation de l'identité, de l'authentification et de la session de l'utilisateur sont essentielles pour se protéger des attaques liées à l'authentification. Il peut y avoir des faiblesses d'authentification si l'application :

- autorise les attaques automatisées telles que le bourrage des informations d'identification, où l'attaquant dispose d'une liste de noms d'utilisateurs valides et mots de passe ;
- permet la force brute ou d'autres attaques automatisées ;
- autorise les mots de passe par défaut, faibles ou bien connus, tels que "Password1" ou "admin / admin" ;
- utilise des processus de récupération des informations d'identification faibles ou inefficaces et des processus de mot de passe oublié, tels que « Questions secrètes », qui ne peuvent être sécurisées ;
- utilise des mots de passe en texte brut, chiffrés ou faiblement hachés (voir [A02:2021 – Défaillances cryptographiques](../A02_2021-Cryptographic_Failures/)) ;
- absence ou utilisation inefficace de l’authentification multifacteur ;
- exposition des identifiants de session dans l'URL ;
- réutilisation de l'identifiant de session après une connexion réussie ;
- n'invalide pas correctement les identifiants de session. Les sessions utilisateurs ou les jetons d'authentification (en particulier les jetons SSO) ne sont pas correctement invalidés lors de la déconnexion ou après une période d'inactivité.

## Comment s'en prémunir

- lorsque cela est possible, implémentez l'authentification multifacteur pour éviter les attaques automatisées, le bourrage des informations d'identification, la force brute et la réutilisation des informations d'identification volées ;
- ne pas livrer ou déployer avec des informations d'identification par défaut, en particulier pour les utilisateurs avec privilèges ;
- intégrer des tests de mots de passes faibles, à la création ou au changement. Comparer ce mot de passe avec la liste des 10000 mots de passe les plus faibles ;
- respecter la longueur, la complexité et la rotation des mots de passe par rapport aux directives du *National Institute of Standards and Technology*(NIST) 800-63 B à la section 5.1.1 ou autres directives modernes ;
- assurez-vous que l'inscription, la récupération des informations d'identification et les chemins d'accès aux API sont durcis contre les attaques d'énumération de compte en utilisant le même message pour tous les résultats ;
- limitez ou retardez de plus en plus les tentatives de connexion échouées, mais veillez à ne pas créer un scénario de déni de service. Enregistrer tous les échecs et alerter les administrateurs lors du bourrage des informations d'identification, de brute force ou d'autres attaques détectées ;
- utilisez un gestionnaire de session intégré et sécurisé côté serveur qui génère un nouvel identifiant de session aléatoire avec une entropie élevée après la connexion. Les identifiants de session ne doivent pas se trouver dans l'URL, ils doivent être stockés de manière sécurisée et être invalidés après la déconnexion, une inactivité et une certaine durée.

## Exemple de scénarios d'attaque

**Scénario 1** : La réutilisation de mots de passe, l’utilisation de mots de passe connus, est une attaque classique. Supposons une application qui n’implémente pas une protection automatisée contre le bourrage d'informations ou l'utilisation des mots de passe connus. Dans ce cas, l'application peut être utilisée comme un oracle pour déterminer si les mots de passe sont valides.

**Scénario 2** : La plupart des attaques d’authentification se produisent en raison de l’utilisation de mots de passe comme facteur unique. Un temps considérées comme de bonnes pratiques, les exigences de rotation et de complexité des mots de passe sont considérées comme encourageant les utilisateurs à utiliser et réutiliser des mots de passe faibles. Il est maintenant recommandé d’arrêter ces pratiques selon les directives NIST 800-63 et d’utiliser du multifacteur.

**Scénario 3** : Les timeouts de session d’application ne sont pas paramétrés correctement. Un utilisateur utilise un ordinateur public pour accéder à une application. À la place de se déconnecter correctement, l’utilisateur ferme le navigateur et quitte l’ordinateur. Un attaquant utilise ensuite le même navigateur quelque temps après et l’utilisateur est toujours authentifié.

## Références

- [OWASP Application Security Verification Standard: V2 authentication](https://owasp.org/www-project-application-security-verification-standard)
- [OWASP Application Security Verification Standard: V3 Session Management](https://owasp.org/www-project-application-security-verification-standard)
- NIST 800-63b: 5.1.1 Memorized Secrets

## Liste des CWEs associées

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
