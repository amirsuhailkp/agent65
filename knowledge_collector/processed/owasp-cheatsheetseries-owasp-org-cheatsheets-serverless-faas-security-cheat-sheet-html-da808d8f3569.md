---
title: Serverless / FaaS Security Cheat Sheet¶
source: cheatsheetseries.owasp.org
url: https://cheatsheetseries.owasp.org/cheatsheets/Serverless_FaaS_Security_Cheat_Sheet.html
collector: owasp
category: web-security
tags:
- web-security
- event
- functions
- serverless
- faas
date_collected: '2026-07-26T12:36:58.665828Z'
language: unknown
---

# Serverless / FaaS Security Cheat Sheet[¶](#serverless-faas-security-cheat-sheet)

## Introduction[¶](#introduction)

Serverless computing (Functions as a Service — FaaS) platforms such as AWS Lambda, Azure Functions, and Google Cloud Functions simplify application development and scaling. However, the execution model (short-lived, event-driven functions running in managed environments) introduces unique security risks compared to traditional architectures.

This cheat sheet provides best practices to secure serverless applications and minimize attack surfaces.

## Key Risks[¶](#key-risks)

- Over-permissioned functions (broad IAM roles,
  ```
  *
  ```

  policies).
- Unvalidated event inputs (API Gateway, S3, Pub/Sub, IoT).
- Cold start data leakage (persistent state, side-channel timing).
- Function chaining abuse (compromised function invoking others).
- Shared environment risks (multi-tenant leakage,
  ```
  /tmp
  ```

  reuse).
- Hardcoded secrets in code or platform config.
- Excessive network access.

## Best Practices[¶](#best-practices)

### 1. Principle of Least Privilege[¶](#1-principle-of-least-privilege)

- Assign minimal IAM permissions to each function.
- Use role-per-function (avoid shared high-privilege roles).
- Scope database/API keys to the smallest set of actions needed.

**Bad IAM Policy (too broad):**
```
```
{
  "Effect": "Allow",
  "Action": "*",
  "Resource": "*"
}```
```

**Good IAM Policy (scoped):**
```
```
{
  "Effect": "Allow",
  "Action": ["dynamodb:GetItem", "dynamodb:PutItem"],
  "Resource": "arn:aws:dynamodb:us-east-1:123456789012:table/Orders"
}```
```

### 2. Environment Isolation[¶](#2-environment-isolation)

- Disable default network access unless required (e.g. outbound internet access).
- Place functions in private subnets with controlled egress.
- Isolate sensitive functions (e.g. payment, auth) from general-purpose ones.
- Separate production vs. staging environments with strict boundaries.

**AWS Lambda VPC Config (restrictive):**
```
```
VpcConfig:
  SubnetIds:
    - subnet-123456
  SecurityGroupIds:
    - sg-restrict-outbound```
```

### 3. Secure Function Invocation[¶](#3-secure-function-invocation)

- Enforce authentication and authorization on all triggers (API Gateway, Pub/Sub, S3, IoT).
- Validate function-to-function calls with signed tokens or workload identities.
- Apply rate limiting and throttling to mitigate DoS and abuse.

**API Gateway Authorizer Example (JWT validation):**
```
```
{
  "Type": "JWT",
  "IdentitySource": "$request.header.Authorization",
  "Issuer": "https://secure-idp.example.com/",
  "Audience": "my-api-client"
}```
```

### 4. Event Data Validation[¶](#4-event-data-validation)

- Treat all event payloads as untrusted input.
- Apply strong input validation & sanitization (length, type, format).
- Protect against common injection attacks (SQLi, XSS, JSON injection, deserialization).
- Strip unnecessary fields and metadata before processing.

Example: Python input validation for Lambda
```
```
import json
import re

def lambda_handler(event, context):
    body = json.loads(event["body"])
    email = body.get("email", "")

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return {"statusCode": 400, "body": "Invalid email"}

    # process safely
    return {"statusCode": 200, "body": "OK"}```
```

### 5. Cold Start & Execution Context Security[¶](#5-cold-start-execution-context-security)

- Do not assume function runtime context is clean between invocations.
- Avoid storing secrets or temporary sensitive data in global/static variables.
- Protect against side-channel leaks (timing differences, leftover files in /tmp).
- For sensitive workloads, enforce single-use execution environments if the platform supports it.

**Bad:**
```
```
# Secret stays in global variable across invocations
SECRET_KEY = "hardcoded-secret"```
```

**Good:**
```
```
import os
from my_secrets_lib import get_secret

def lambda_handler(event, context):
    secret = get_secret("db-password")  # fetch fresh each time
    ...```
```

### 6. Secrets Management[¶](#6-secrets-management)

- Fetch secrets at runtime from a vault or caching extension — not from platform-level function configuration (e.g. Lambda Environment Variables).
- Use ephemeral credentials (STS, workload identity federation).
- Rotate secrets automatically.

**AWS Lambda Secret Fetch (Python via Parameters and Secrets Extension):**

**Note:** Ensure that the AWS Lambda Parameters and Secrets Extension is added and enabled for your function (for example, as a Lambda layer). Otherwise,
```
http://localhost:2773
```

will not be available and requests to it will fail.
```
```
import os
import json
import urllib.request
import urllib.parse

def get_secret(secret_name):
    """
    Retrieves a secret using the AWS Lambda Extension local endpoint.
    This method is faster and more cost-effective due to local caching.
    """
    # The extension provides a local HTTP endpoint on port 2773
    encoded_name = urllib.parse.quote_plus(secret_name)

    secrets_extension_endpoint = (
        f"http://localhost:2773/secretsmanager/get?secretId={encoded_name}"
    )

    # Authenticate using the identity token provided by the Lambda environment.
    # Fail fast if the token is missing to avoid confusing 4xx errors.
    session_token = os.environ.get("AWS_SESSION_TOKEN")
    if not session_token:
        raise RuntimeError(
            "Missing AWS_SESSION_TOKEN required for "
            "Parameters and Secrets Extension authentication."
        )

    headers = {
        "X-Aws-Parameters-Secrets-Token": session_token
    }

    request = urllib.request.Request(
        secrets_extension_endpoint,
        headers=headers,
        method="GET"
    )

    with urllib.request.urlopen(request, timeout=3) as response:
        if response.status != 200:
            raise Exception(
                f"Error retrieving secret: {response.read().decode('utf-8')}"
            )

        response_json = json.loads(response.read())
        secret_string = response_json["SecretString"]

        return json.loads(secret_string)```
```

### 7. Monitoring & Logging[¶](#7-monitoring-logging)

- Use centralized logging (CloudWatch, Azure Monitor, GCP Logging).
- Mask secrets and PII.

Example: Redacting fields
```
```
import logging

def log_event(event):
    safe_event = {k: ("***" if "password" in k else v) for k,v in event.items()}
    logging.info(safe_event)```
```

### 8. Supply Chain Security[¶](#8-supply-chain-security)

- Scan dependencies (
  ```
  npm audit
  ```

  ,
  ```
  pip-audit
  ```

  ,
  ```
  safety
  ```

  ).
- Use minimal deployment packages.
- Sign packages with checksums.

**AWS Lambda Layer Hash Validation:**
```
```
shasum -a 256 layer.zip```
```

## Do’s and Don’ts[¶](#dos-and-donts)

**Do**:

- Enforce least privilege per function.
- Validate all event inputs.
- Fetch secrets from vaults, not platform config.
- Restrict network egress.
- Monitor invocations and logs.

**Don’t**:

- Hardcode secrets in code or configs.
- Assume clean runtime between invocations.
- Give
  ```
  *
  ```

  IAM permissions.
- Leave sensitive data in
  ```
  /tmp
  ```

  or globals.
- Trust event sources blindly.
