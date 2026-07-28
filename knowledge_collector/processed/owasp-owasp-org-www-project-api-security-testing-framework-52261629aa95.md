---
title: OWASP API Security Testing Framework
source: owasp.org
url: https://owasp.org/www-project-api-security-testing-framework/
collector: owasp
category: web-security
tags:
- web-security
- owasp
- security
- api
- jar
date_collected: '2026-07-26T12:43:57.880462Z'
language: unknown
---

# OWASP API Security Testing Framework

# OWASP API Security Testing Framework

## Description

The OWASP API Security Testing Framework (ASTF) is a specialized security testing tool designed to automatically detect vulnerabilities in APIs based on the **OWASP API Security Top 10 2023**. It discovers endpoints automatically, runs 12 security test cases covering the full Top 10 plus GraphQL and gRPC, and produces findings in JSON, HTML, SARIF, and XML formats.

**Current release: v1.0.0**

ASTF has been validated against [OWASP crAPI](https://github.com/OWASP/crAPI) — the intentionally vulnerable API — where it auto-discovered 832 endpoints and detected 11 distinct vulnerability types including JWT algorithm weaknesses, missing authentication controls, and improper inventory management.

## Key Features

- **100% OWASP API Security Top 10 2023 coverage**— all 10 categories implemented and tested
- **12 security test cases**— API1 through API10, plus dedicated GraphQL and gRPC checks
- **Auto endpoint discovery**— finds endpoints via OpenAPI/Swagger probing and common path patterns; zero config required for a first scan
- **Multiple auth modes**— Bearer token, API key, Basic auth, custom headers
- **Four output formats**— HTML (human review), JSON (processing), SARIF (GitHub Code Scanning), XML
- **CI/CD ready**— GitHub Actions workflow included; exits with code
  ```
  1
  ```

  when findings detected for pipeline gating
- **229 passing unit tests**— fully test-covered implementation
- **Proven on real targets**— validated against OWASP crAPI public demo

## Test Case Coverage

IDVulnerabilityWhat It DetectsASTF-API1-2023Broken Object Level AuthorizationBOLA/IDOR via ID manipulationASTF-API2-2023Broken AuthenticationMissing auth, JWT
```
none
```

algorithm, expired tokens, 2FA bypassASTF-API3-2023Broken Object Property Level AuthorizationSensitive fields in responses, mass assignmentASTF-API4-2023Unrestricted Resource ConsumptionMissing rate limiting headersASTF-API5-2023Broken Function Level AuthorizationAdmin endpoints accessible without privilegesASTF-API6-2023Unrestricted Access to Sensitive FlowsMissing bot protection on login/OTP/payment flowsASTF-API7-2023Server-Side Request ForgerySSRF via URL/webhook/redirect parametersASTF-API8-2023Security MisconfigurationMissing security headers, verbose errorsASTF-API9-2023Improper Inventory ManagementDeprecated versions, shadow endpoints, exposed docsASTF-API10-2023Unsafe Consumption of APIsInjection via integration endpoints, open redirectASTF-GRAPHQL-2023GraphQL SecurityIntrospection, field suggestions, depth attacks, batch abuseASTF-GRPC-2023gRPC Endpoint DetectionService detection, server reflection enabled

## Getting Started

**Requirements:** Java 21+
```
```
# Download the latest release
curl -LO https://github.com/OWASP/www-project-api-security-testing-framework/releases/latest/download/astf-v1.0.0.jar

# Run against your API
java -jar astf-v1.0.0.jar -u https://api.example.com --token "YOUR_TOKEN" -f HTML -o report.html

# Try against OWASP crAPI (zero config needed)
java -jar astf-v1.0.0.jar -u http://crapi.apisec.ai -f HTML -o crapi-report.html```
```

Or build from source:
```
```
git clone https://github.com/OWASP/www-project-api-security-testing-framework.git
cd www-project-api-security-testing-framework
mvn clean package -DskipTests
java -jar target/api-security-testing-framework-1.0-SNAPSHOT.jar -u https://api.example.com```
```

For full documentation see the [GitHub repository](https://github.com/OWASP/www-project-api-security-testing-framework).

## CI/CD Integration

Add ASTF to your GitHub Actions pipeline to scan on every pull request:
```
```
- name: Download ASTF
  run: curl -LO https://github.com/OWASP/www-project-api-security-testing-framework/releases/latest/download/astf-v1.0.0.jar

- name: Run security scan
  run: java -jar astf-v1.0.0.jar -u $ --token $ -f SARIF -o results.sarif

- name: Upload to Code Scanning
  uses: github/codeql-action/upload-sarif@v3
  with:
    sarif_file: results.sarif```
```

## Roadmap

### ✅ Phase 1 — Core Framework (Completed Q2 2025)

- Core scanning engine with virtual thread concurrency
- All 10 OWASP API Security Top 10 2023 test cases
- JSON, HTML, SARIF, XML report generators
- CLI with config file support (YAML/JSON)
- 229 unit tests

### ✅ Phase 2 — Extended Coverage (Completed Q4 2025)

- GraphQL security test case (introspection, field suggestions, depth attacks, batch abuse)
- gRPC endpoint detection stub with server reflection check
- GitHub Actions CI/CD workflow
- Comprehensive documentation (Quick Start, CLI reference, Troubleshooting)
- Validated against OWASP crAPI — 11 vulnerability types detected

### ✅ Phase 3 — Beta Release (Completed Q2 2026)

- Automated release workflow — JAR published to GitHub Releases on version tags
- ```
  v1.0.0  ```

  released with pre-built downloadable JAR
- Full OWASP project page update

### 🔜 Phase 4 — Stable Release (Planned)

- OpenAPI/Swagger spec import for precise endpoint targeting
- Plugin system for custom test cases
- Distributed scanning for large API surfaces
- Integration with vulnerability management platforms (Defect Dojo, Jira)

## Getting Involved

The API Security Testing Framework welcomes community contributions:

- **Bug reports**— use the[Bug Report template](https://github.com/OWASP/www-project-api-security-testing-framework/issues/new?template=bug_report.md)
- **Feature requests**— use the[Feature Request template](https://github.com/OWASP/www-project-api-security-testing-framework/issues/new?template=feature_request.md)
- **New test cases**— see the[Architecture docs](https://github.com/OWASP/www-project-api-security-testing-framework/blob/main/docs/ARCHITECTURE.md)for the extension guide
- **Documentation**— use the[Documentation Improvement template](https://github.com/OWASP/www-project-api-security-testing-framework/issues/new?template=documentation_improvement.md)

## Related Projects

- [OWASP API Security Project](https://owasp.org/www-project-api-security/)— The Top 10 standard this framework implements
- [OWASP crAPI](https://github.com/OWASP/crAPI)— Intentionally vulnerable API for testing
- [OWASP ZAP](https://www.zaproxy.org)— Complementary web application scanner

## Licensing

This project is licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0.html).

## Project Leaders

- [Govindarajan Lakshmikanthan](/cdn-cgi/l/email-protection#2f48405946414b4e5d4e454e4101434e445c474246444e415b474e416f40584e5c5f01405d48)— Project Leader
  - GitHub: [@GovindarajanL](https://github.com/GovindarajanL)
- GitHub:

## Example

Put whatever you like here: news, screenshots, features, supporters, or remove this file and don’t use tabs at all.
