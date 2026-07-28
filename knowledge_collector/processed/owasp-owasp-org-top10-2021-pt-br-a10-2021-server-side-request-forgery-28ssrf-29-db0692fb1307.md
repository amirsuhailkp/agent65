---
title: A10:2021 – Falsificação de Solicitação do Lado do Servidor SSRF
source: owasp.org
url: https://owasp.org/Top10/2021/pt-BR/A10_2021-Server-Side_Request_Forgery_(SSRF)/
collector: owasp
category: web-security
tags:
- web-security
- para
- ssrf
- uma
- como
date_collected: '2026-07-25T14:28:18.725330Z'
language: unknown
---

# A10:2021 – Falsificação de Solicitação do Lado do Servidor (SSRF)

## Fatores

CWEs MapeadasTaxa de Incidência MáximaTaxa Média de IncidênciaExploração Média PonderadaImpacto Médio PonderadoCobertura MáximaMédia de CoberturaTotal de OcorrênciasTotal de CVEs12.72%2.72%8.286.7267.72%67.72%9,503385

## Visão Geral

Esta categoria foi adicionada a partir de uma pesquisa com a comunidade levando o primeiro lugar no Top 10. Os dados mostram uma taxa de incidência relativamente baixa com cobertura de teste acima da média e classificações de potencial de exploração e impacto acima da média. Como acontece com novas entradas, provavelmente seja um único ou pequeno grupo de CWEs para atenção e conscientização, a esperança é que eles estejam sujeitos ao foco de estudo da comunidade e possamos incluir em uma categoria maior em uma edição futura.

## Descrição

As falhas de SSRF ocorrem sempre que um aplicativo da web busca um recurso remoto sem validar a URL fornecida pelo usuário. Ele permite que um invasor force o aplicativo a enviar uma solicitação criada para um destino inesperado, mesmo quando protegido por um firewall, VPN ou outro tipo de lista de controle de acesso à rede (ACL).

Como os aplicativos da web modernos fornecem aos usuários finais recursos convenientes, buscar uma URL se torna um cenário comum. Como resultado, a incidência de SSRF está aumentando. Além disso, a gravidade do SSRF está se tornando mais alta devido aos serviços em nuvem e à complexidade crescente das arquiteturas.

## Como Previnir

Os desenvolvedores podem evitar o SSRF implementando alguns ou todos os seguintes controles de defesa em profundidade:

### **Para a Camada de Rede**

- Segmente a funcionalidade de acesso a recursos remotos em redes separadas para reduzir o impacto de SSRF;
- Imponha políticas de firewall para “negar por padrão” ou regras de controle de acesso à rede para bloquear todo o tráfego da intranet, exceto o essencial.
- *Dicas:*~ Estabeleça uma propriedade e um ciclo de vida para regras de firewall baseadas em aplicativos. ~ Registrar todos os fluxos de rede aceitos*e*bloqueados em firewalls. (veja[A09:2021-Monitoramento de Falhas e Registros de Segurança](../A09_2021-Security_Logging_and_Monitoring_Failures/)).

### **Para a Camada de Aplicação:**

- Higienize e valide todos os dados de entrada fornecidos pelo cliente;
- Aplique o esquema de URL, porta e destino com uma lista de permissões positiva;
- Não envie a resposta crua ao cliente
- Desabilite redirecionamentos de HTTP;
- Tenha cuidado com a consistência URL contra ataques que mirem a resolução de nomes através do DNS e CWE-367.

Não reduza o SSRF por meio do uso de uma lista de negação ou expressão regular. Os invasores têm listas gigantes de possíveis entradas, ferramentas e habilidades para contornar as listas de negação.

### **Medidas Adicionais a Considerar:**

- Não implemente outros serviços de segurança relevantes em sistemas frontais (por exemplo, OpenID). Controle o tráfego local nesses sistemas (por exemplo, localhost)
- Para *frontends*com grupos de usuários dedicados e gerenciáveis, use criptografia de rede (por exemplo, VPNs) em sistemas independentes para as necessidades de proteção muito altas.

## Cenário de exemplo de um ataque

Os invasores podem usar SSRF para atacar sistemas protegidos por firewalls de aplicativos da web, firewalls ou ACLs de rede, usando cenários como:

**Cenário #1:** Varredura de portas em servidores internos - se a arquitetura de rede não for segmentada, os invasores podem mapear as redes internas e determinar se as portas estão abertas ou fechadas em servidores internos a partir dos resultados da conexão ou do tempo decorrido para conectar ou rejeitar as conexões de carga SSRF.

**Cenário #2:** Exposição de dados confidenciais - os invasores podem acessar arquivos locais, como ou serviços internos, para obter informações confidenciais, como
```
file:///etc/passwd
```

e
```
http://localhost:28017/
```

.

**Cenário #3:** Acesse o armazenamento de metadados de serviços em nuvem - a maioria dos provedores de nuvem possui armazenamento de metadados, como
```
http://169.254.169.254/
```

. Um invasor pode ler os metadados para obter informações confidenciais.

**Cenário #4:** Comprometimento dos serviços internos - O invasor pode abusar dos serviços internos para conduzir outros ataques, como Execução Remota de Código/Remote Code Execution (RCE) ou Negação de Serviço/Denial of Service (DoS).
