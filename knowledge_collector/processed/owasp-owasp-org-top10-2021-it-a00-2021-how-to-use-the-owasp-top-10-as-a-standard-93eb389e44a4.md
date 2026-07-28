---
title: Come usare la OWASP Top 10 come standard
source: owasp.org
url: https://owasp.org/Top10/2021/it/A00_2021_How_to_use_the_OWASP_Top_10_as_a_standard/
collector: owasp
category: web-security
tags:
- web-security
- owasp
- top
- come
- standard
date_collected: '2026-07-25T14:27:33.003580Z'
language: unknown
---

# Come usare la OWASP Top 10 come standard

La OWASP Top 10 è principalmente un documento per diffondere consapevolezza. Tuttavia, questo non ha impedito alle organizzazioni di usarlo come standard *de facto* per l'AppSec sin dal suo inizio nel 2003. Se volete usare la OWASP Top
10 come standard di codifica o di test, sappiate che è il minimo indispensabile e
solo un punto di partenza.

Una delle difficoltà nell'usare la OWASP Top 10 come standard è che
documentiamo i rischi di sicurezza delle applicazioni, e non necessariamente problematiche facilmente testabili.
Per esempio, **A04:2021-Insecure Design** è oltre la portata della maggior parte delle forme di test. Un altro esempio è il test sul posto, in uso, ed efficace dei log e il monitoraggio degli stessi che può essere fatto solo con interviste e con la richiesta di un
campione di risposte agli incidenti di sicurezza. Uno strumento di analisi statica del codice può cercare l'assenza di istruzioni di logging, ma potrebbe essere impossibile determinare se la logica di business o il controllo degli accessi sta registrando violazioni della sicurezza. I penetration tester possono essere in grado solo di determinare che hanno invocato la procedura di incident response in un ambiente di test, ambienti che sono raramente monitorati allo stesso modo dell'ambiente di produzione.

Ecco le nostre raccomandazioni per quando è appropriato usare la OWASP Top 10:

Caso d'usoOWASP Top 10 2021OWASP Application Security Verification StandardAwarenessSiTrainingLivello baseCompletoDesign and architectureOccasionalmenteSiCoding standardMinimo indispensabileSiSecure Code reviewMinimo indispensabileSiPeer review checklistMinimo indispensabileSiUnit testingOccasionalmenteSiIntegration testingOccasionalmenteSiPenetration testingMinimo indispensabileSiTool supportMinimo indispensabileSiSecure Supply ChainOccasionalmenteSi

Incoraggiamo chiunque voglia adottare uno standard di sicurezza per le applicazioni
ad utilizzare lo standard [OWASP Application Security Verification Standard](https://owasp.org/www-project-application-security-verification-standard/)
(ASVS), poiché è progettato per essere verificabile e testato, e può essere usato in
tutte le parti del un ciclo di vita di sviluppo sicuro del software.

L'ASVS è l'unica scelta accettabile per chi produce strumenti di testing. Gli strumenti non possono rilevare, testare o proteggere in modo esaustivo contro la Top 10 di OWASP a causa della natura di molti dei rischi OWASP Top 10, ad esempio A04:2021-Insecure Design. OWASP scoraggia qualsiasi pretesa di copertura completa della OWASP Top 10, perché è semplicemente falso.
