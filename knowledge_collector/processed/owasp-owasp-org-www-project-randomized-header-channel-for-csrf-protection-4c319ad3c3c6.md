---
title: OWASP Randomized Header Channel for CSRF Protection
source: owasp.org
url: https://owasp.org/www-project-randomized-header-channel-for-csrf-protection/
collector: owasp
category: web-security
tags:
- web-security
- header
- token
- csrf
- owasp
date_collected: '2026-07-26T12:45:41.867068Z'
language: unknown
---

# OWASP Randomized Header Channel for CSRF Protection

The **Randomized Header Channel (RHC)** is a security technique designed to increase the integrity and unpredictability of token transmission in web applications. The method proposes rotating multiple valid request headers for token delivery on each request, making it significantly harder for attackers to perform interception, automation, replay, or predictive token-placement attacks.

**RHC** was originally conceptualized and documented in Spanish during the development of a real-world SaaS platform that required secure, stateless, and high-availability communication channels. The technique aligns naturally with **JWT-based authentication**, microservices, and distributed architectures where traditional CSRF protections may be insufficient or incompatible.

### Key Objectives

- Introduce unpredictability in token transportation mechanisms.
- Reduce token-targeting opportunities during request interception.
- Provide a lightweight and implementation-agnostic layer that complements existing CSRF defenses.
- Facilitate adoption through clear documentation and implementations for developers and security professionals.

### Roadmap

- Submit the proposal for community review.
- Collect feedback from OWASP leaders, contributors, and security practitioners.
- Expand documentation with architecture diagrams, entropy analysis, and practical examples.
- Publish recommended integration patterns for common frameworks.
- Maintain the project as open security documentation long-term.

## Contribute

Contributions are welcome. Please submit pull requests, issues, or implementation proposals in the GitHub repository.

# Architecture & Examples

Este archivo contiene **todos los ejemplos oficiales**, incluyendo los **4 niveles del RHC**, fragmentos HTTP, diagramas y flujos.

# 🔷 Nivel 1 — *Dispersión Aleatoria* (Dispersión Aleatoria)

El cliente utiliza una tabla con encabezados válidos definida desde el inicio y un solo token CSRF generado por el servidor.

### **Flujo**

- El servidor publica una tabla fija:
  ```
  H1, H2, H3
  ```

  .
- El cliente selecciona un header al azar.
- El token CSRF se inserta en ese header.
- El servidor valida el header y el token.

### **Ejemplo HTTP**
```
```
POST /v1/transfer
X-RHC-Header-2: 6F8dP2sQ9RmC1aZ7Xh4K
Content-Type: application/json```
```

# 🔷 Nivel 2 — *Dual Entrop* (Dual Entrop)

El cliente utiliza una tabla con encabezados válidos y tres tokens CSRF, donde en cada ciclo se elige:

- un header al azar
- un token CSRF al azar

### **Flujo**

- El servidor publica una tabla fija:
  ```
  H1, H2, H3
  ```

  .
- El cliente selecciona un header al azar.
- El cliente selecciona uno de los 3 tokens CSRF al azar.
- El token se inserta en ese header.
- El servidor valida el header y el token.

### **Ejemplo HTTP**
```
```
POST /v1/payments
X-RHC-Header-3: Zp7Qm4Ay81FsK9TdHr6W
Content-Type: application/json```
```

# 🔷 Nivel 3 — *Entropía Variable* (Entropía Variable)

El cliente utiliza encabezados válidos como en los niveles anteriores, pero los tokens CSRF tienen longitudes y codificaciones variables, lo que incrementa la entropía real.

### **Flujo**

- El servidor publica una tabla fija:
  ```
  H1, H2, H3
  ```

  .
- El cliente selecciona un header al azar.
- El cliente selecciona un token CSRF al azar (longitud variable).
- El token se inserta en ese header.
- El servidor valida el header y el token.

### **Ejemplo 1 HTTP** \*\* — \*\* *Token largo*
```
```
POST /v1/payments
X-CSRF-H3: qP4fA1wZ9kT7mB3sJ2uR8hX0VyM5nLgC
Content-Type: application/json```
```

### **Ejemplo 2 HTTP** \*\* — \*\* *Token Mediano*
```
```
POST /v1/payments
X-CSRF-H1: 73sPqr52WbKJgA4cL3sPYv
Content-Type: application/json```
```

### **Ejemplo 3 HTTP** \*\* — \*\* *Token Corto*
```
```
POST /v1/payments
X-CSRF-H2: fQ9dL7xS1mA4
Content-Type: application/json```
```

# 🔷 Nivel 4 — *Dynamic Adaptive RHC* (Canal Adaptativo Dinámico)

El **Nivel 4** es la versión más avanzada del RHC. No es solo un grupo de headers: es un **canal vivo**, dinámico y adaptativo.

Supera los niveles previos mediante:

- rotación dinámica de encabezados válidos
- señuelos activos con ruido estadístico
- filtros adaptativos según contexto
- canal que muta según condiciones externas
- dispersión y ruido útil
- protección contra correlación predictiva

Es el primer nivel **no-determinista**, imposible de resolver por análisis estático o fuerza bruta tradicional.

El servidor utiliza **filtros adaptativos** que reconocen los headers correctos e ignoran decoys.

## 🧬 Principio del Nivel 4

> *“El canal RHC ya no es un conjunto de encabezados: es un organismo.”*

## ✔ 1. Headers válidos dinámicos (N por ciclo)

De una lista total, se eligen **N headers válidos** que cambian por ciclo según:

- carga (PoC)
- tiempo
- endpoint
- intentos fallidos
- comportamiento del cliente

## ✔ 2. Headers señuelo (Decoys) con ruido útil

- Parecen legítimos
- No se distinguen externamente
- El servidor sí puede identificarlos
- Pueden rotar o mutar

## ✔ 3. Filtro adaptativo del servidor

Cambia su respuesta según:

- carga (PoC)
- IP o fingerprint
- número de fallos
- endpoint
- nivel del recurso
- hora del día

El mismo cliente puede recibir escenarios distintos.

## ✔ 4. Dynamic Channel Rotation (DCR)

La rotación puede dispararse por:

- intentos fallidos
- métricas de entropía
- ruido
- tiempo

Una rotación invalida:

- tokens
- headers válidos
- disposición interna del canal

## ✔ 5. Entropía multifactor

FactorOrigenEncabezados válidosRotados dinámicamenteTokensLongitud variableDecoysRuido estadísticoRuido útilDispersiónDistribuciónAnti-correlaciónFiltro adaptativoContextual

El atacante NO puede crear correlación estable.

## ✔ 6. Reacción autónoma (Defense Reflex)

### PoC:

- decoys fijos
- longitudes dinámicas
- headers válidos fijos
- dispersión fija

### Implementación real:

- aumentar decoys ante sospecha
- modificar longitudes de token
- reducir headers válidos
- aumentar dispersión
- posible: cerrar canal temporalmente

### **Ejemplo HTTP**
```
```
POST /v1/identity/update
X-RHC-H1: Cf9Gx2A7tPqLs91kZb3uQm4NsyW86Rhv   ← decoy
X-RHC-H4: TmQ8yLr29FvS13KpWg5aXb7cN0HqD4Mt   ← token real (ciclo actual)
X-RHC-H6: qP4fA1wZ9kT7mB3sJ2uR8hX0VyM5nLgC   ← decoy
X-RHC-H2: mD73sPq18YvHr52WbKx9Rf0tJgA4cLzE   ← decoy
X-RHC-H5: R9tK0wLh6BfP2uS3nQ7vX1cZpM4eD8Yr   ← token real (ciclo actual)
X-RHC-H7: Zk5Pq1Nf8GyA7uT4wE9bC3hL0sV6mJdR   ← decoy
X-RHC-H3: Hc8Lx4Vw1SgD9pQ2tR3mF6aYkB0uZ7Jn   ← decoy
X-RHC-H8: F2aQp8Vx3WnL7rC1bS9uH4kD0M5tJ6Gz   ← token real (ciclo actual)
X-RHC-H9: yN1rT5mP8bQ4vS2kJ6aW9gF3D0xH7LzC   ← decoy
Content-Type: application/json```
```

# 📊 Diagrams

Consulta los diagramas completos en:

- ```
  /docs/architecture.md  ```
- ```
  /docs/conceptual/marco_conceptual_rhc.md
  ```

# 📦 Additional Examples

### **PSR‑15 Middleware**

Validación automática del header + token + timestamp.

### **Node.js Microservice Adapter**

Implementación para entornos distribuidos.

### **Header Fuzzing Test Cases**

Pruebas de:

- colisiones
- predicción adversaria
- entropía efectiva
- canales paralelos
