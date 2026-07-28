---
title: A10:2021 – A10 Falsification de requête côté serveur SSRF
source: owasp.org
url: https://owasp.org/Top10/2021/fr/A10_2021-Server-Side_Request_Forgery_(SSRF)/
collector: owasp
category: web-security
tags:
- web-security
- les
- des
- une
- pour
date_collected: '2026-07-25T14:27:11.453439Z'
language: unknown
---

# A10:2021 – A10 Falsification de requête côté serveur (SSRF)

## Facteurs

CWEs associéesTaux d'incidence maxTaux d'incidence moyenExploitation pondérée moyenneImpact pondéré moyenCouverture maxCouverture moyenneNombre total d'occurrencesNombre total de CVEs12,72 %2,72 %8,286,7267,72 %67,72 %9 503385

## Aperçu

Cette catégorie est ajoutée à partir de l'enquête communautaire Top 10 (n°1). Les données montrent un taux d'incidence relativement faible avec une couverture de test supérieure à la moyenne et des évaluations du potentiel d'exploitation et d'impact supérieures à la moyenne. Comme les nouvelles entrées sont susceptibles d'être une seule ou un petit groupe de *Common Weakness Enumerations* (CWE) pour l'attention et la sensibilisation, l'espoir est qu'elles fassent l'objet d'une attention particulière et qu'elles puissent être intégrées dans une catégorie plus importante dans une prochaine édition.

## Description

Une faille SSRF se produit lorsqu'une application web récupère une ressource distante sans valider l'URL fournie par l'utilisateur. Elle permet à un attaquant de contraindre l'application à envoyer une requête élaborée à une destination inattendue, même si elle est protégée par un pare-feu, un VPN ou un autre type de liste de contrôle d'accès au réseau (ACL).

Comme les applications Web modernes offrent aux utilisateurs finaux des fonctions pratiques, la récupération d'une URL devient un scénario courant. Par conséquent, l'incidence d'une SSRF augmente. De même, la gravité de ce phénomène augmente en raison des services en nuage et de la complexité des architectures.

## Comment s'en prémunir

Les développeurs peuvent prévenir ce type de vulnérabilité en mettant en œuvre tout ou partie des contrôles de défense en profondeur suivants :

### **Couche réseau :**

- segmenter la fonctionnalité d'accès aux ressources à distance dans des réseaux distincts pour réduire l'impact d'une SSRF ;
- appliquer des politiques de pare-feu ou des règles de contrôle d'accès au réseau "refusant par défaut" afin de bloquer tout le trafic intranet sauf celui qui est essentiel.
  *Conseils:*
  - Établir une propriété et un cycle de vie pour les règles du pare-feu en fonction des applications.
  - Consigner tous les flux réseau acceptés *et*bloqués sur les pare-feu (voir[A09:2021-Carence des systèmes de contrôle et de journalisation](../A09_2021-Security_Logging_and_Monitoring_Failures/)).
- Établir une propriété et un cycle de vie pour les règles du pare-feu en fonction des applications.

### **Couche applicative :**

- assainir et valider toutes les données d'entrée fournies par le client ;
- imposer le schéma d'URL, le port et la destination avec une liste positive d'autorisation ;
- ne pas envoyer de réponses brutes aux clients ;
- désactiver les redirections HTTP ;
- veiller à la cohérence des URL pour éviter les attaques telles que le rebinding DNS et les situations de concurrence de type "time of check, time of use" (TOCTOU).

N'atténuez pas les SSRF par l'utilisation d'une liste de refus ou d'une expression régulière. Les attaquants disposent de dictionnaires, d'outils et de compétences pour contourner les listes de refus.

### **Mesures complémentaires :**

- ne pas déployer d'autres services liés à la sécurité sur les systèmes frontaux (par exemple, OpenID). Contrôlez le trafic local sur ces systèmes (par exemple, localhost) ;
- pour les frontaux avec des groupes d'utilisateurs dédiés et gérables, utilisez le chiffrement du réseau (par exemple, les VPN) sur des systèmes indépendants pour prendre en compte les besoins de protection très élevés.

## Exemple de scénarios d'attaque

Les attaquants peuvent utiliser SSRF pour attaquer des systèmes protégés derrière des pare-feu d'applications web, des pare-feu ou des ACL de réseau, en utilisant des scénarios tels que :

**Scénario n°1 :** Analyse des ports des serveurs internes - Si l'architecture du réseau n'est pas segmentée, les attaquants peuvent cartographier les réseaux internes et déterminer si les ports sont ouverts ou fermés sur les serveurs internes à partir des résultats de connexion ou du temps écoulé pour connecter ou les connexions rejetées avec une charge utile de type SSRF.

**Scénario n°2 :** Exposition de données sensibles - Les attaquants peuvent accéder aux fichiers locaux ou aux services internes pour obtenir des informations sensibles telles que
```
file:///etc/passwd
```

et
```
http://localhost:28017/
```

.

**Scénario n°3 :** Accéder au stockage des métadonnées des services en nuage - La plupart des fournisseurs d'informatique en nuage ont un stockage de métadonnées tel que
```
http://169.254.169.254/
```

. Un attaquant peut lire les métadonnées pour obtenir des informations sensibles.

**Scénario n°4 :** Compromettre les services internes - L'attaquant peut abuser des services internes pour mener d'autres attaques telles que l'exécution de code à distance (RCE) ou le déni de service (DoS).
