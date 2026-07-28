---
title: Como usar o OWASP Top 10 como padrão
source: owasp.org
url: https://owasp.org/Top10/2021/pt-BR/A00_2021_How_to_use_the_OWASP_Top_10_as_a_standard/
collector: owasp
category: web-security
tags:
- web-security
- owasp
- como
- top
- padr
date_collected: '2026-07-25T14:28:07.936869Z'
language: unknown
---

# Como usar o OWASP Top 10 como padrão

O OWASP Top 10 é principalmente um documento de conscientização. No entanto, isso não impediu as organizações de usá-lo de fato como um padrão AppSec na indústria desde seu início em 2003. Se você deseja usar o OWASP Top 10 como um padrão de codificação ou teste, saiba que é apenas o mínimo e um ponto de partida.

Uma das dificuldades de usar o OWASP Top 10 como padrão é que documentamos os riscos do appsec, e não necessariamente problemas testáveis com facilidade. Por exemplo, A04:2021-Insecure Design está além do escopo da maioria das formas de teste. Outro exemplo são os testes no local, em uso, e o registro e monitoramento eficazes só podem ser feitos com entrevistas e requisições de uma amostra de respostas eficazes de incidentes. Uma ferramenta de análise estática de código pode procurar a ausência de registro, mas pode ser impossível determinar se a lógica de negócios ou o controle de acesso está registrando violações de segurança críticas. Os testadores de penetração podem apenas determinar se eles chamaram a resposta a incidentes em um ambiente de teste, que raramente é monitorado da mesma maneira que a produção.

Aqui estão nossas recomendações para quando é apropriado usar o OWASP Top 10:

Caso de UsoOWASP Top 10 2021OWASP Padrão de verificação de segurança de aplicaçõesConscientizaçãoSimTreinamentoNível de entradaCompreensivoDesign e arquiteturaOcasionalmenteSimPadrão de codificaçãoMínimoSimRevisão de Código SeguroMínimoSimLista de verificação de revisão por paresMínimoSimTeste de unidadeOcasionalmenteSimTeste de integraçãoOcasionalmenteSimTeste de penetraçãoMínimoSimSuporte de ferramentaMínimoSimCadeia de abastecimento seguraOcasionalmenteSim

Nós encorajamos qualquer pessoa que queira adotar uma segurança de aplicação padrão para usar o OWASP Application Security Verification Standard (ASVS), pois é projetado para ser verificável e testado, e pode ser usado em todas as partes de um ciclo de vida de desenvolvimento seguro.

O ASVS é a única escolha aceitável para fornecedores de ferramentas. Ferramentas não podem detectar, testar ou proteger de forma abrangente contra o OWASP Top 10 devido a a natureza de vários dos 10 principais riscos OWASP, com referência a A04: 2021-Design inseguro. OWASP desencoraja qualquer reivindicações de cobertura total do OWASP Top 10 porque simplesmente não é verdadeiro.
