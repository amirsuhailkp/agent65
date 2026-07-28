---
title: OWASP Web Shield Library OWL
source: owasp.org
url: https://owasp.org/www-project-webshield-library/
collector: owasp
category: web-security
tags:
- web-security
- owasp
- owl
- security
- run
date_collected: '2026-07-26T12:44:51.003191Z'
language: unknown
---

# OWASP Web Shield Library ( OWL )

## OWASP Web Shield Library (OWL)

OWL is a practical, open source security library for modern JavaScript applications. It provides reusable protection utilities aligned to OWASP Top 10 categories and ships with a React adapter for fast integration.

### Use The Tabs Above

This project now uses a tabbed layout to keep the homepage focused and make content easier to navigate.

- **Overview**: Architecture, A01-A10 module map, and React adapter highlights
- **Getting Started**: Installation, commands, and first integration example
- **Contributing**: Contributor workflow, pull request guidance, and conduct/security links

### Quick Project Facts

- Maturity:
  ```
  v0.1.0
  ```

  foundation release
- Coverage: A01-A10 modules
- Stack: Framework-agnostic core + React adapter
- Quality: ESLint, Jest, CI workflows, and security gates

### Project Links

## Project Leader

- [Sreejith Nair](/cdn-cgi/l/email-protection#294a504b4c5b5a5b4c4c43405d41694e44484045074a4644)
- GitHub: [@cybersreejith](https://github.com/cybersreejith)

## OWASP Web Shield Library (OWL)

**Practical, reusable OWASP Top 10 security controls for modern JavaScript applications.**

## What OWL Delivers

OWL maps reusable security controls directly to OWASP categories so teams speak the same security language as their threat models.

CapabilityApproach🛡️ Full A01–A10 coverageOne module per OWASP category, consistent naming🧩 Framework-agnostic corePure JavaScript, no runtime framework dependency⚛️ React adapterCategory-aligned providers, hooks, and guard components✅ Secure defaultsDeny-overrides, token expiry, redaction — all on by default🧪 Test-first deliveryPositive, negative, and abuse-path test coverage🔄 CI-readyLint + test + build gate in a single
```
npm run check
```

## Core Module Map (A01–A10)

OWASP #CategoryKey ExportsA01Broken Access Control
```
RBACManager
```

,
```
ACLManager
```

,
```
PermissionChecker
```

A02Cryptographic Failures
```
CryptoManager
```

,
```
PBKDF2Adapter
```

,
```
Argon2Adapter
```

,
```
SecretPolicy
```

A03Injection
```
InputSanitizer
```

,
```
InputValidator
```

A04Insecure Design
```
ThreatModelGuard
```

,
```
DesignChecklist
```

A05Security Misconfiguration
```
SecurityConfigManager
```

,
```
HardeningReporter
```

A06Vulnerable & Outdated Components
```
DependencyRiskScanner
```

,
```
ComponentPolicy
```

A07Identification & Auth Failures
```
AuthManager
```

,
```
TokenManager
```

A08Software & Data Integrity Failures
```
CSRFTokenManager
```

,
```
HTTPClient
```

A09Security Logging & Monitoring Failures
```
SecurityLogger
```

,
```
EventEmitter
```

A10SSRF
```
SSRFGuard
```

,
```
SafeFetcher
```

## React Adapter Highlights
```
```
@owl/react-adapter
 ├── A01  ACLProvider, RBACProvider, useACL, usePermission, PermissionGate
 ├── A02  useCryptoManager
 ├── A03  useInputSanitizer, SanitizedText
 ├── A04  useThreatModelGuard
 ├── A05  useHardeningReport
 ├── A06  useDependencyRiskScanner
 ├── A07  AuthProvider, useAuth, useAuthToken, AuthGate
 ├── A08  useSecureHttpClient, withSecurityHeaders
 ├── A09  SecurityProvider, useSecurityMonitoring, SecurityAlert
 └── A10  useSafeFetcher```
```

## Project Links

ResourceLink📚 API Reference[docs/api-reference.md](https://github.com/OWASP/www-project-webshield-library/blob/main/docs/api-reference.md)📁 Source[github.com/OWASP/www-project-webshield-library](https://github.com/OWASP/www-project-webshield-library)🚀 Examples[examples/](https://github.com/OWASP/www-project-webshield-library/tree/main/examples)🐛 Issues[GitHub Issues](https://github.com/OWASP/www-project-webshield-library/issues)

## Getting Started

### Requirements

RequirementVersionNode.js
```
>= 20
```

React (adapter only)
```
>= 18
```

Package managernpm, pnpm, or yarn

### Install
```
```
# Install dependencies
npm install

# Verify the quality gate passes
npm run check```
```

### Core Usage — 5-minute example
```
```
import {
  ACLManager,
  AuthManager,
  PermissionChecker,
  RBACManager,
  TokenManager
} from "@owl/core";

// 1. Set up auth and token management
const tokenManager = new TokenManager();
tokenManager.setTokens({ accessToken: "jwt", expiresAt: Date.now() + 3_600_000 });

const authManager = new AuthManager({ tokenManager });
authManager.setSession({ userId: "u1", roles: ["admin"] });

// 2. Define role permissions
const rbac = new RBACManager();
rbac.defineRole("admin", ["read:invoice", "update:invoice"]);

// 3. Add ACL policy overrides
const acl = new ACLManager();
acl.setPolicy("invoice", "delete", "deny");

// 4. Check combined permission (deny-overrides)
const checker = new PermissionChecker({ rbacManager: rbac, aclManager: acl });
console.log(checker.check({ role: "admin", action: "read", resource: "invoice" }));
// → { allowed: true, reason: "allowed", metadata: { ... } }```
```

### React Adapter — Provider Composition
```
```
import { AuthProvider, ACLProvider, RBACProvider, AuthGate, PermissionGate }
  from "@owl/react-adapter";

export function AppShell({ authManager, aclManager, rbacManager, children }) {
  return (
    <AuthProvider authManager={authManager}>
      <ACLProvider aclManager={aclManager}>
        <RBACProvider rbacManager={rbacManager}>
          <AuthGate fallback={<div>Sign in required</div>}>
            <PermissionGate action="read" resource="reports"
              fallback={<div>Access denied</div>}>
              {children}
            </PermissionGate>
          </AuthGate>
        </RBACProvider>
      </ACLProvider>
    </AuthProvider>
  );
}```
```

### Run the Examples

**Core Node demo (no build required)**
```
```
node examples/core-node-demo/index.js```
```

**React Vite demo**
```
```
cd examples/react-adapter-demo
npm install && npm run dev```
```

**Full multi-page reference app**
```
```
cd examples/owl-enabled-app
npm install && npm run dev```
```

### Available Scripts
```
```
npm run check    # lint + test (full quality gate)
npm run test     # Jest unit tests only
npm run lint     # ESLint only
npm run build    # Build ESM + CJS outputs```
```

### CI/CD Baseline
```
```
- name: Install
  run: npm ci

- name: Quality gate
  run: npm run check

- name: Build
  run: npm run build```
```

### Further Reading

ResourceDescription[docs/api-reference.md](https://github.com/OWASP/www-project-webshield-library/blob/main/docs/api-reference.md)Complete API with copyable examples[docs/framework.md](https://github.com/OWASP/www-project-webshield-library/blob/main/docs/framework.md)Adoption patterns and bootstrap guide[docs/architecture.md](https://github.com/OWASP/www-project-webshield-library/blob/main/docs/architecture.md)Module layout and design decisions[docs/troubleshooting.md](https://github.com/OWASP/www-project-webshield-library/blob/main/docs/troubleshooting.md)Common issues and resolutions

## Contributing to OWL

### Project Leader

NameRoleContact*Sreejith Sreekandan Nair*OWL Project Leader[[email protected]](/cdn-cgi/l/email-protection#a6c5dfc4c3d4d5d4c3c3cccfd2cee6c1cbc7cfca88c5c9cb)

### Ways to Contribute

TypeHow🐛 Bug fixOpen an issue first, then a focused PR✨ New security controlDiscuss on Slack or open a feature issue first📖 Docs improvementDirect PR welcome🧪 Additional testsAlways welcome — especially failure paths🔍 Security reviewReview open PRs for security impact

### Quickstart
```
```
# 1. Fork and clone
git clone https://github.com/<you>/www-project-webshield-library.git
cd www-project-webshield-library

# 2. Install dependencies
npm install

# 3. Verify gate passes before any changes
npm run check

# 4. Create a branch
git checkout -b feature/your-change

# 5. Keep gate green throughout development
npm run check

# 6. Open a pull request against main```
```

### Pull Request Checklist

Before submitting, confirm all of the following:

- ```
  npm run check  ```

  passes (lint + tests)
- Changes align with OWASP principles and project goals
- Existing behavior is not silently broken
- Tests cover new code including **failure and abuse paths**
- PR description includes: **what**,**why**, and**how to verify**
- Docs updated if the public API or any security default changes

### Testing Requirements

OWL enforces security-first testing. All contributions to core modules or adapter hooks must include:

ScenarioRequired?Successful operation✅Invalid input or boundary conditions✅Security rejection path (deny, block, throw)✅Error code and metadata shape✅ for

```
SecurityError```

throws

```
```
npm run test
```
```

### Community

- [Join OWASP Slack](https://owasp.org/slack/invite)
- Channel:

  ```
  # project-webshield-library  ```
- [OWASP Code of Conduct](https://owasp.org/www-policy/operational/code-of-conduct)
- [CODE\_OF\_CONDUCT.md](https://github.com/OWASP/www-project-webshield-library/blob/main/CODE_OF_CONDUCT.md)

### Security Reporting

> Do not open public issues for vulnerabilities.

Follow the private reporting process in [SECURITY.md](https://github.com/OWASP/www-project-webshield-library/blob/main/SECURITY.md).
