---
title: A11:2021 – Étapes suivantes
source: owasp.org
url: https://owasp.org/Top10/2021/fr/A11_2021-Next_Steps/
collector: owasp
category: web-security
tags:
- web-security
- les
- des
- moire
- dans
date_collected: '2026-07-25T14:27:12.179224Z'
language: unknown
---

# A11:2021 – Étapes suivantes

De par sa conception, le Top 10 de l'OWASP est limité aux dix risques les plus importants. Dans chaque Top 10 de l'OWASP, des risques "au seuil" ont été longuement examinés en vue de leur inclusion, mais n'ont finalement pas été retenus. Quelle que soit la façon dont nous avons essayé d'interpréter ou de déformer les données, les autres risques étaient plus répandus et avaient plus d'impact.

Qu'il s'agisse d'organisations travaillant à la mise en place d'un programme de sécurité des applications mature, de consultants en sécurité ou de fournisseurs d'outils souhaitant étendre la couverture de leurs offres, les quatre problèmes suivants valent la peine d'être identifiés et corrigés.

## Problèmes de qualité du code

CWEs associéesTaux d'incidence maxTaux d'incidence moyenExploitation pondérée moyenneImpact pondéré moyenCouverture maxCouverture moyenneNombre total d'occurrencesNombre total de CVEs3849,46 %2,22 %7,16,760,85 %23,42 %101 7367 564

- **Description**. Les problèmes de qualité du code comprennent les défauts ou les schémas de sécurité connus, la réutilisation de variables à des fins multiples, l'exposition d'informations sensibles dans les résultats de débogage, les erreurs "off-by-one", les situations de concurrence "time of check/time of use" (TOCTOU), les erreurs de conversion non signées ou signées, l'utilisation après libération, etc. La caractéristique de cette section est qu'elles peuvent généralement être identifiées à l'aide d'options de compilateur, d'outils d'analyse de code statique et de plugins IDE de linter. Les langages modernes ont, de par leur conception, éliminé bon nombre de ces problèmes, comme le concept de propriété et d'emprunt de la mémoire de Rust, la conception du threading de Rust et le typage strict et la vérification des limites de Go.
- **Comment s'en prémunir**. Activez et utilisez les options d'analyse de code statique de votre éditeur et de votre langage. Envisagez d'utiliser un outil d'analyse statique du code. Envisagez la possibilité d'utiliser ou de migrer vers un langage ou un framework qui élimine des classes de bogues, comme Rust ou Go.
- **Exemple de scénarios d'attaque**. Un attaquant peut obtenir ou mettre à jour des informations sensibles en exploitant une situation de concurrence utilisant une variable statiquement partagée entre plusieurs threads.
- **Références**

## Déni de service

CWEs associéesTaux d'incidence maxTaux d'incidence moyenExploitation pondérée moyenneImpact pondéré moyenCouverture maxCouverture moyenneNombre total d'occurrencesNombre total de CVEs817,54 %4,89 %8,35,979,58 %33,26 %66 985973

- **Description**. Le déni de service est toujours possible si les ressources sont suffisantes. Cependant, les pratiques de conception et de développement ont une incidence importante sur l'ampleur du déni de service. Supposons que toute personne disposant d'un lien puisse accéder à un fichier volumineux, ou qu'une transaction coûteuse en termes de calcul se produise sur chaque page. Dans ce cas, le déni de service nécessite moins d'efforts pour être mené.
- **Comment s'en prémunir**. Testez les performances du code en termes d'utilisation du processeur, des E/S et de la mémoire, ré-architecturez, optimisez ou mettez en cache les opérations coûteuses. Envisagez des contrôles d'accès pour les objets de grande taille afin de vous assurer que seules les personnes autorisées peuvent accéder aux fichiers ou objets volumineux ou les servir par un réseau de mise en cache en périphérie.
- **Exemple de scénarios d'attaque**. Un attaquant peut déterminer qu'une opération prend 5 à 10 secondes pour se terminer. Lorsqu'il exécute quatre threads simultanés, le serveur semble ne plus répondre. L'attaquant utilise 1000 threads et met l'ensemble du système hors ligne.
- **Références**

## Erreurs de gestion de la mémoire

CWEs associéesTaux d'incidence maxTaux d'incidence moyenExploitation pondérée moyenneImpact pondéré moyenCouverture maxCouverture moyenneNombre total d'occurrencesNombre total de CVEs147,03 %1,16 %6,78,156,06 %31,74 %26 57616 184

- **Description**. Les applications Web ont tendance à être écrites dans des langages avec une gestion automatique de la mémoire, tels que Java, .NET ou node.js (JavaScript ou TypeScript). Cependant, ces langages sont écrits dans des langages systèmes qui présentent des problèmes de gestion de la mémoire, tels que les débordements de tampon ou de tas, l'utilisation après libération, les débordements d'entiers, etc. De nombreuses évasions de sandbox ont eu lieu au fil des années, ce qui prouve que même si le langage d'application Web est théoriquement "sûr" au niveau de l'allocation mémoire, les fondations ne le sont pas.
- **Comment s'en prémunir**. De nombreuses API modernes sont désormais écrites dans des langages avec une gestion de la mémoire sécurisée tels que Rust ou Go. Dans le cas de Rust, la sécurité de la mémoire est une caractéristique cruciale du langage. Pour le code existant, l'utilisation de paramètres de compilation stricts, le typage fort, l'analyse de code statique et le fuzzing peuvent être bénéfiques pour identifier les fuites de mémoire, les dépassements de mémoire et de tableau, etc.
- **Exemples de scénarios d'attaque**. Les débordements de tampon et de tas ont été un pilier des attaquants au fil des années. L'attaquant envoie des données à un programme, qui les stocke dans un tampon de pile sous-dimensionné. Le résultat est que les informations de la pile d'appel sont écrasées, y compris le pointeur de retour de la fonction. Les données définissent la valeur du pointeur de retour de sorte que, lors du retour de fonction, elle transfère le contrôle au code malveillant contenu dans les données de l'attaquant.
- **Références**
