---
title: A09:2021 – Fallas en el Registro y Monitoreo
source: owasp.org
url: https://owasp.org/Top10/2021/es/A09_2021-Security_Logging_and_Monitoring_Failures/
collector: owasp
category: web-security
tags:
- web-security
- registros
- para
- los
- que
date_collected: '2026-07-25T14:26:54.402660Z'
language: unknown
---

# A09:2021 – Fallas en el Registro y Monitoreo

## Factores

CWEs mapeadasTasa de incidencia máxTasa de incidencia promExplotabilidad ponderada promImpacto ponderado promCobertura máxCobertura promIncidencias totalesTotal CVEs419.23%6.51%6.874.9953.67%39.97%53,615242

## Resumen

Monitoreo y registro de seguridad provienen de la encuesta de la comunidad (tercer lugar), subió levemente desde la décima posición en el Top 10 2017. El registro y monitoreo pueden ser desafiantes para ser testeados, implicando entrevistas o preguntar si los ataques fueron detectados durante las pruebas de penetración. No hay muchos datos de CVE/CVSS para esta categoría, pero detectar y responder a las brechas es crítico. Aún así, puede tener un gran impacto para la auditabilidad, visibilidad, alertas de incidentes y análisis forense. Esta categoría se expande más allá de *CWE-117 Neutralización de salida incorrecta para registros*, *CWE-223 Omisión de información relevante para la seguridad*, y *CWE-532 Inserción de información sensible en archivo de registro*.

## Descripción

Volviendo al OWASP Top 10 2021, la intención es apoyar la detección, escalamiento y respuesta ante brechas activas. Sin registros y monitoreo, las brechas no pueden ser detectadas. Registros, detecciones, monitoreo y respuesta activas insuficientes pueden ocurrir en cualquier momento:

- Eventos auditables, tales como los inicios de sesión, fallas en el inicio de sesión y transacciones de alto valor no son registradas.
- Advertencias y errores generan registros poco claros, inadecuados y en algunos casos ni se generan.
- Registros en aplicaciones y API no son monitoreados para detectar actividades sospechosas.
- Los registros son únicamente almacenados en forma local.
- Los umbrales de alerta y procesos de escalamiento no están correctamente implementados o no son efectivos.
- Las pruebas de penetración y los escaneos utilizando herramientas de pruebas dinámicas de seguridad en aplicaciones (como ser OWASP ZAP) no generan alertas.
- Las aplicaciones no logran detectar, escalar, o alertar sobre ataques activos en tiempo real ni cercanos al tiempo real.

Se es vulnerable a la fuga de información haciendo registros y eventos de alertas que sean visibles para un usuario o un atacante (consulte [A01: 2021-Pérdida de Control de Acceso](../A01_2021-Broken_Access_Control/)).

## Cómo se previene

Los desarrolladores deberían implementar algunos o todos los siguientes controles, dependiendo del riesgo de la aplicación:

- Asegúrese de que todos los errores de inicio de sesión, de control de acceso y de validación de entradas de datos del lado del servidor se pueden registrar con suficiente contexto como para identificar cuentas sospechosas o maliciosas y mantenerlo durante el tiempo suficiente para permitir un posterior análisis forense.
- Asegúrese de que los registros se generen en un formato fácil de procesar por las herramientas de gestión de registros.
- Asegúrese de que los datos de registros son correctamente codificados para prevenir inyecciones o ataques en el sistema de monitoreo o registros.
- Asegúrese de que las transacciones de alto valor poseen una traza de auditoria con controles de integridad para evitar la modificación o el borrado, tales como permitir únicamente la inserción en las tablas de base de datos o similares.
- Los equipos de DevSecOps debe establecer alertas y monitoreo efectivo tal que se detecte actividades sospechosas y responderlas rápidamente.
- Establezca o adopte un plan de respuesta y recuperación, tal como NIST 800-61r2 o posterior.

Existen frameworks de protección de aplicaciones comerciales y de código abierto, tales como el conjunto de reglas de ModSecurity de OWASP y el conjunto de programas de correlación de registros de código abierto como ser ELK (Elasticsearch, Logstash, Kibana) con paneles personalizados y alertas.

## Ejemplos de escenarios de ataque

**Escenario #1:** El sitio web de un prestador de salud que provee un plan para niños no pudo detectar una brecha debido a la falta de monitoreo y registro. Alguien externo informó al prestador que un atacante había accedido y modificados registros médicos sensibles de más de 3,5 millones de niños. Una revisión post incidente detectó que los desarrolladores del sitio web no habían encontrado vulnerabilidades significativas. Como no hubo ni registro ni monitores del sistema, la brecha de datos pudo haber estado en proceso desde el 2013, por un período de más de 7 años.

**Escenario #2:** Una gran aerolínea India tuvo una brecha de seguridad que involucró a la pérdida de datos personales de millones de pasajeros por más de 10 años, incluyendo pasaportes y tarjetas de crédito. La brecha se produjo por un proveedor de servicios de almacenamiento en la nube, quien notificó a la aerolínea después de un tiempo.

**Escenario #3:** Una gran aerolínea Europea sufrió un incumplimiento de la GRPD que debe reportar. La causa de la brecha se debió a que un atacante explotó una vulnerabilidad en una aplicación de pago, obteniendo más de 400,000 registros de pagos de usuarios. La aerolínea fue multada con 20 millones de libras como resultado del regulador de privacidad.

## Referencias

- [OWASP Application Security Verification Standard: V8 Logging and Monitoring](https://owasp.org/www-project-application-security-verification-standard)
- [Data Integrity: Recovering from Ransomware and Other Destructive Events](https://csrc.nist.gov/publications/detail/sp/1800-11/final)
- [Data Integrity: Identifying and Protecting Assets Against Ransomware and Other Destructive Events](https://csrc.nist.gov/publications/detail/sp/1800-25/final)
- [Data Integrity: Detecting and Responding to Ransomware and Other Destructive Events](https://csrc.nist.gov/publications/detail/sp/1800-26/final)

## Lista de CWEs mapeadas

[CWE-117 Improper Output Neutralization for Logs](https://cwe.mitre.org/data/definitions/117.html)

[CWE-223 Omission of Security-relevant Information](https://cwe.mitre.org/data/definitions/223.html)
