---
title: A01:2021 – Contrôles d'accès défaillants
source: owasp.org
url: https://owasp.org/Top10/2021/fr/A01_2021-Broken_Access_Control/
collector: owasp
category: web-security
tags:
- web-security
- les
- acc
- des
- contr
date_collected: '2026-07-25T14:25:18.397783Z'
language: unknown
---

# A01:2021 – Contrôles d'accès défaillants

## Facteurs

CWEs associéesTaux d'incidence maxTaux d'incidence moyenExploitation pondérée moyenneImpact pondéré moyenCouverture maxCouverture moyenneNombre total d'occurrencesNombre total de CVEs3455,97 %3,81 %6,925,9394,55 %47,72 %318 48719 013

## Aperçu

Précédemment à la cinquième place, 94 % des applications ont été testées pour une forme de contrôle d'accès défaillant avec un taux d'incidence moyen de 3,81 %. Cette catégorie a le plus d'occurrences dans l'ensemble de données contribué avec plus de 318 000. Les *Common Weakness Enumerations* (CWE) notables incluses sont *CWE-200: Exposure of Sensitive Information to an Unauthorized Actor*, *CWE-201: Insertion of Sensitive Information Into Sent Data* et *CWE-352: Cross-Site Request Forgery* .

## Description

Le contrôle d'accès applique une stratégie telle que les utilisateurs ne peuvent pas agir en dehors de leurs autorisations prévues. Les défaillances entraînent généralement la divulgation, la modification ou la destruction d'informations non autorisées de toutes les données ou l'exécution d'une fonctionnalité métier en dehors des limites de l'utilisateur. Les vulnérabilités courantes du contrôle d'accès incluent :

- Violation du principe du moindre privilège ou de refus par défaut, où l'accès ne doit être accordé que pour des capacités, des rôles ou des utilisateurs particuliers, mais est accessible à tous.
- Contourner les contrôles d'accès en modifiant l'URL (falsification de paramètres ou navigation forcée), l'état interne de l'application ou la page HTML, ou en utilisant un outil d'attaque modifiant les requêtes API.
- Autoriser l'affichage ou la modification du compte de quelqu'un d'autre, en fournissant son identifiant unique (références directes d'objet non sécurisées).
- Accès à l'API avec des contrôles d'accès manquants pour POST, PUT et DELETE.
- Élévation de privilège. Agir en tant qu'utilisateur sans être connecté ou agir en tant qu'administrateur lorsqu'il est connecté en tant qu'utilisateur.
- Manipulation de métadonnées, comme le rejeu ou la falsification de JSON Web Token (JWT), de cookies ou de champs cachés, afin d'élever les privilèges ou abuser de l'invalidation JWT.
- La mauvaise configuration de CORS permettant l'accès à l'API à partir d'origines non autorisées/non approuvées.
- Forcer la navigation vers des pages authentifiées en tant qu'utilisateur non authentifié ou vers des pages privilégiées en tant qu'utilisateur standard.

## Comment s'en prémunir

Le contrôle d'accès n'est efficace que dans le code de confiance côté serveur ou des API serverless, où l'attaquant ne peut pas modifier la vérification du contrôle d'accès ou les métadonnées.

- À l'exception des ressources publiques, tout doit être bloqué par défaut.
- Centraliser l'implémentation des mécanismes de contrôle d'accès et les réutiliser dans l'ensemble de l'application. Cela comprend de minimiser l'utilisation de CORS.
- Le modèle de contrôle d'accès doit imposer l'appartenance des enregistrements, plutôt que de permettre à l'utilisateur de créer, lire, modifier ou supprimer n'importe quel enregistrement.
- Les exigences métier spécifiques de l'application doivent être appliquées par domaines.
- Désactiver le listing de dossier sur le serveur web, et vérifier que les fichiers de métadonnées (ex : .git) et de sauvegardes ne se trouvent pas dans l'arborescence web.
- Tracer les échecs de contrôles d'accès, alerter les administrateurs quand c'est approprié (ex : échecs répétés).
- Limiter la fréquence d'accès aux API et aux contrôleurs d'accès, afin de minimiser les dégâts que causeraient des outils d'attaques automatisés.
- Les identifiants de session avec état doivent être invalidés côté serveur après une déconnexion. Les JWT, sans état, doivent être à durée de vie relativement courte pour que la fenêtre d'opportunité d'un attaquant soit minimisée. Pour les JWT avec une durée de vie plus longue, il est fortement recommandé de suivre le standard OAuth de révocation d'accès.

Les développeurs et les testeurs qualité doivent procéder à des tests unitaires et d'intégration sur les fonctionnalités de contrôle d'accès.

## Exemple de scénarios d'attaque

**Scenario 1 :** L'application utilise des données non vérifiées dans une requête SQL qui accède à des informations d'un compte :
```
```
 pstmt.setString(1, request.getParameter("acct"));
 ResultSet results = pstmt.executeQuery( );```
```

En modifiant simplement le paramètre 'acct' dans le navigateur, un attaquant peut envoyer le numéro de compte qu'il veut. Si ce numéro n'est pas vérifié, l'attaquant peut accéder à n'importe quel compte utilisateur.
```
```
 https://example.com/app/accountInfo?acct=notmyacct```
```

**Scenario 2 :** Un attaquant force le navigateur à visiter des URL arbitraires. Il faut imposer des droits pour accéder à une page d'administration.
```
```
 https://example.com/app/getappInfo
 https://example.com/app/admin_getappInfo```
```

Si un utilisateur non-authentifié peut accéder à l'une des pages, c'est une faille. Si un non-administrateur peut accéder à une page d'administration, c'est une faille.

## Références

## Liste des CWEs associées

[CWE-22 Improper Limitation of a Pathname to a Restricted Directory
('Path Traversal')](https://cwe.mitre.org/data/definitions/22.html)

[CWE-23 Relative Path Traversal](https://cwe.mitre.org/data/definitions/23.html)

[CWE-35 Path Traversal: '.../...//'](https://cwe.mitre.org/data/definitions/35.html)

[CWE-59 Improper Link Resolution Before File Access ('Link Following')](https://cwe.mitre.org/data/definitions/59.html)

[CWE-200 Exposure of Sensitive Information to an Unauthorized Actor](https://cwe.mitre.org/data/definitions/200.html)

[CWE-201 Exposure of Sensitive Information Through Sent Data](https://cwe.mitre.org/data/definitions/201.html)

[CWE-219 Storage of File with Sensitive Data Under Web Root](https://cwe.mitre.org/data/definitions/219.html)

[CWE-264 Permissions, Privileges, and Access Controls (should no longer be used)](https://cwe.mitre.org/data/definitions/264.html)

[CWE-276 Incorrect Default Permissions](https://cwe.mitre.org/data/definitions/276.html)

[CWE-284 Improper Access Control](https://cwe.mitre.org/data/definitions/284.html)

[CWE-285 Improper Authorization](https://cwe.mitre.org/data/definitions/285.html)

[CWE-352 Cross-Site Request Forgery (CSRF)](https://cwe.mitre.org/data/definitions/352.html)

[CWE-359 Exposure of Private Personal Information to an Unauthorized Actor](https://cwe.mitre.org/data/definitions/359.html)

[CWE-377 Insecure Temporary File](https://cwe.mitre.org/data/definitions/377.html)

[CWE-402 Transmission of Private Resources into a New Sphere ('Resource Leak')](https://cwe.mitre.org/data/definitions/402.html)

[CWE-425 Direct Request ('Forced Browsing')](https://cwe.mitre.org/data/definitions/425.html)

[CWE-441 Unintended Proxy or Intermediary ('Confused Deputy')](https://cwe.mitre.org/data/definitions/441.html)

[CWE-497 Exposure of Sensitive System Information to an Unauthorized Control Sphere](https://cwe.mitre.org/data/definitions/497.html)

[CWE-538 Insertion of Sensitive Information into Externally-Accessible File or Directory](https://cwe.mitre.org/data/definitions/538.html)

[CWE-540 Inclusion of Sensitive Information in Source Code](https://cwe.mitre.org/data/definitions/540.html)

[CWE-548 Exposure of Information Through Directory Listing](https://cwe.mitre.org/data/definitions/548.html)

[CWE-552 Files or Directories Accessible to External Parties](https://cwe.mitre.org/data/definitions/552.html)

[CWE-566 Authorization Bypass Through User-Controlled SQL Primary Key](https://cwe.mitre.org/data/definitions/566.html)

[CWE-601 URL Redirection to Untrusted Site ('Open Redirect')](https://cwe.mitre.org/data/definitions/601.html)

[CWE-639 Authorization Bypass Through User-Controlled Key](https://cwe.mitre.org/data/definitions/639.html)

[CWE-651 Exposure of WSDL File Containing Sensitive Information](https://cwe.mitre.org/data/definitions/651.html)

[CWE-668 Exposure of Resource to Wrong Sphere](https://cwe.mitre.org/data/definitions/668.html)

[CWE-706 Use of Incorrectly-Resolved Name or Reference](https://cwe.mitre.org/data/definitions/706.html)

[CWE-863 Incorrect Authorization](https://cwe.mitre.org/data/definitions/863.html)

[CWE-913 Improper Control of Dynamically-Managed Code Resources](https://cwe.mitre.org/data/definitions/913.html)
