---
title: A05:2021 – Configuração Incorreta de Segurança
source: owasp.org
url: https://owasp.org/Top10/2021/pt-BR/A05_2021-Security_Misconfiguration/
collector: owasp
category: web-security
tags:
- web-security
- seguran
- para
- configura
- que
date_collected: '2026-07-25T14:28:13.913169Z'
language: unknown
---

# A05:2021 – Configuração Incorreta de Segurança

## Fatores

CWEs MapeadosTaxa de Incidência MáximaTaxa de Incidência MédiaExploração Média PonderadaImpacto Médio PonderadoCobertura MáximaCobertura MédiaTotal de ocorrênciasTotal de CVEs2019.84%4.51%8.126.5689.58%44.84%208,387789

## Visão Geral

Saindo da #6 posição na edição anterior, 90% das aplicações foram testados
para alguma forma de configuração incorreta, com uma taxa de incidência
média de 4% e mais de 208 mil ocorrências de *Common Weakness Enumeration* (CWE)
nesta categoria de risco. Com mais mudanças em software altamente configurável,
não é surpreendente ver essa categoria subir. CWEs notáveis incluídos são
*CWE-16 Configuração* e *CWE-611 Restrição Imprópria de Referência de Entidade Externa XML*.

## Descrição

A aplicação pode ser vulnerável se for:

- Falta de proteção de segurança apropriada em qualquer parte da

  *stack*das aplicações ou permissões configuradas incorretamente em serviços em nuvem.
- Recursos desnecessários são ativados ou instalados (por exemplo, portas, serviços, páginas, contas ou privilégios desnecessários).
- As contas padrão e suas senhas ainda estão ativadas e inalteradas.
- O tratamento de erros revela

  *stack traces*ou outras mensagens de erro excessivamente informativas aos usuários.
- Para sistemas atualizados, os recursos de segurança mais recentes estão desabilitados ou não estão configurados com segurança.
- As configurações de segurança nos servidores das aplicações, nos

  *frameworks*(por exemplo, Struts, Spring, ASP.NET), bibliotecas, bancos de dados, etc., não estão definidas para proteger os valores.
- O servidor não envia cabeçalhos ou diretivas de segurança, ou eles não estão configurados para proteger os valores.
- O software está desatualizado ou vulnerável (consulte

  [A06: 2021-Componentes Vulneráveis e Desatualizados](../A06_2021-Vulnerable_and_Outdated_Components/)).

Sem um processo de configuração de segurança de aplicações que seja integrado e repetível, os sistemas correm um risco maior.

## Como Prevenir

Devem ser implementados processos de instalação segura, incluindo:

- Um processo de proteção repetível torna mais rápido e fácil implantar outro ambiente que esteja devidamente bloqueado. Os ambientes de desenvolvimento, controle de qualidade e produção devem ser todos configurados de forma idêntica, com credenciais diferentes usadas em cada ambiente. Este processo deve ser automatizado para minimizar o esforço necessário para configurar um novo ambiente seguro.
- Uma plataforma mínima sem recursos, componentes, documentação e outros desnecessários. Remova ou não instale recursos e estruturas não utilizados.
- Uma tarefa para revisar e atualizar as configurações apropriadas para todas as notas de segurança, atualizações e patches como parte do processo de gerenciamento de patch (consulte

  [A06: 2021-Componentes Vulneráveis e Desatualizados](../A06_2021-Vulnerable_and_Outdated_Components/)). Revise as permissões de armazenamento em nuvem (por exemplo,*S3 bucket permissions*).
- Uma arquitetura de aplicação segmentada fornece separação eficaz e segura entre componentes ou

  *tenants*, com segmentação, conteinerização ou grupos de segurança em nuvem (ACLs).
- Envio de diretivas de segurança para clientes, por exemplo,

  *Security Headers*.
- Um processo automatizado para verificar a eficácia das configurações em todos os ambientes.

## Exemplos de Cenários de Ataque

**Cenário #1:** O servidor da aplicação é fornecido com os sistemas de amostra
não removidos do servidor de produção. Esses aplicativos de amostra têm
falhas de segurança conhecidas que os invasores usam para comprometer o
servidor. Suponha que um desses aplicativos seja o console de administração
e as contas padrão não tenham sido alteradas. Nesse caso, o invasor
efetua login com as senhas padrão e assume o controle.

**Cenário #2:** A listagem do diretório não está desabilitada no servidor.
Um invasor descobre que pode simplesmente listar diretórios. O invasor
encontra e baixa as classes Java compiladas, que ele descompila e
faz engenharia reversa para visualizar o código. O invasor então
encontra uma falha grave de controle de acesso no aplicativo.

**Cenário #3:** A configuração do servidor de aplicações permite que os
detalhes das mensagens de erro, por exemplo, *stack trace*, sejam retornadas
aos usuários. Isso potencialmente expõe informações confidenciais ou falhas
subjacentes, como versões de componentes que são conhecidas por serem vulneráveis.

**Cenário #4:** Um provedor de serviços de nuvem tem permissões de
compartilhamento padrão abertas para a Internet por outros usuários de
*Content Security Policy header (CSP)*. Isso permite que dados confidenciais
armazenados no armazenamento em nuvem sejam acessados.

## Referências

- Application Security Verification Standard V19 Configuration

## Lista dos CWEs Mapeados

[CWE-11 ASP.NET Misconfiguration: Creating Debug Binary](https://cwe.mitre.org/data/definitions/11.html)

[CWE-13 ASP.NET Misconfiguration: Password in Configuration File](https://cwe.mitre.org/data/definitions/13.html)

[CWE-15 External Control of System or Configuration Setting](https://cwe.mitre.org/data/definitions/15.html)

[CWE-260 Password in Configuration File](https://cwe.mitre.org/data/definitions/260.html)

[CWE-315 Cleartext Storage of Sensitive Information in a Cookie](https://cwe.mitre.org/data/definitions/315.html)

[CWE-520 .NET Misconfiguration: Use of Impersonation](https://cwe.mitre.org/data/definitions/520.html)

[CWE-526 Exposure of Sensitive Information Through Environmental Variables](https://cwe.mitre.org/data/definitions/526.html)

[CWE-537 Java Runtime Error Message Containing Sensitive Information](https://cwe.mitre.org/data/definitions/537.html)

[CWE-541 Inclusion of Sensitive Information in an Include File](https://cwe.mitre.org/data/definitions/541.html)

[CWE-547 Use of Hard-coded, Security-relevant Constants](https://cwe.mitre.org/data/definitions/547.html)

[CWE-611 Improper Restriction of XML External Entity Reference](https://cwe.mitre.org/data/definitions/611.html)

[CWE-614 Sensitive Cookie in HTTPS Session Without 'Secure' Attribute](https://cwe.mitre.org/data/definitions/614.html)

[CWE-756 Missing Custom Error Page](https://cwe.mitre.org/data/definitions/756.html)

[CWE-776 Improper Restriction of Recursive Entity References in DTDs ('XML Entity Expansion')](https://cwe.mitre.org/data/definitions/776.html)

[CWE-942 Permissive Cross-domain Policy with Untrusted Domains](https://cwe.mitre.org/data/definitions/942.html)

[CWE-1004 Sensitive Cookie Without 'HttpOnly' Flag](https://cwe.mitre.org/data/definitions/1004.html)

[CWE-1032 OWASP Top Ten 2017 Category A6 - Security Misconfiguration](https://cwe.mitre.org/data/definitions/1032.html)

[CWE-1174 ASP.NET Misconfiguration: Improper Model Validation](https://cwe.mitre.org/data/definitions/1174.html)
