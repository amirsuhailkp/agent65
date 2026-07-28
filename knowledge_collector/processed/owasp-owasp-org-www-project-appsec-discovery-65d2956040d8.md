---
title: OWASP Appsec Discovery
source: owasp.org
url: https://owasp.org/www-project-appsec-discovery/
collector: owasp
category: web-security
tags:
- web-security
- field
- name
- type
- file
date_collected: '2026-07-26T12:44:02.642285Z'
language: unknown
---

# OWASP Appsec Discovery

# Introduction

OWASP Appsec Discovery cli tool scan provided code projects and extract structured protobuf, graphql, swaggers, database schemas, python, go and java object DTOs, used api clients and methods, and other kinds of external contracts. It scores risk level for found object fields with provided in config static keywords ruleset and store results in own format json or sarif reports for fast integration with exist vuln management systems like Defectdojo.

Cli tool can also use local LLM model Llama 3.2 3B from Huggingface and provided prompt to score objects without pre-existing knowledge about assets in code. Small open source models work fast on common hardware and are just enouth for such classification tasks.

Appsec Discovery service continuosly fetch changes from local Gitlab via api, clone code for particular projects, scan for objects in code and score them with provided via UI rules, store result objects with projects, branches and MRs from Gitlab in local db and alert about critical changes via messenger or comments to MR in Gitlab.

Under the hood tool powered by Semgrep OSS engine and specialy crafted discovery rules and parsers that extract particular objects from semgrep report meta variables.

## Searching for sensitive fields

Install cli tool:
```
```
pip install appsec-discovery```
```

Provided rules in conf.yaml or leave it empty for default list:
```
```
score_tags:
  pii:
    high:
      - 'first_name'
      - 'last_name'
      - 'phone'
      - 'passport'
    medium:
      - 'address'
    low:
      - 'city'
  finance:
    high:
      - 'pan'
      - 'card_number'
    medium:
      - 'amount'
      - 'balance'
  auth:
    high:
      - 'password'
      - 'pincode'
      - 'codeword'
      - 'token'
    medium:
      - 'login'```
```

Run on code project folder with swaggers, protobuf and other structured contracts in code and get parsed objects and fields marked with severity and category tags:
```
```
appsec-discovery --source tests/swagger_samples

- hash: 40140abef3b5f45d447d16e7180cc231
  object_name: Route /user/login (GET)
  object_type: route
  parser: swagger
> severity: high  <<<<<<<<<<<<<<<<<<<<<<<< !!!
  tags:
> - auth  <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< !!!
  file: swagger.yaml
  line: 1
  properties:
    path:
      prop_name: path
      prop_value: /user/login
>>>>  severity: medium  <<<<<<<<<<<<<<<<<< !!!
      tags:
>>>>  - auth  <<<<<<<<<<<<<<<<<<<<<<<<<<<< !!!
    method:
      prop_name: method
      prop_value: GET
  fields:
    query.param.username:
      field_name: query.param.username
      field_type: string
      file: swagger.yaml
      line: 1
>>>>  severity: medium  <<<<<<<<<<<<<<<<<< !!!
      tags:
>>>>  - auth  <<<<<<<<<<<<<<<<<<<<<<<<<<<< !!!
    query.param.password:
      field_name: query.param.password
      field_type: string
      file: swagger.yaml
      line: 1
>>>>  severity: high    <<<<<<<<<<<<<<<<<< !!!
      tags:
>>>>  - auth  <<<<<<<<<<<<<<<<<<<<<<<<<<<< !!!
    output:
      field_name: output
      field_type: string
      file: swagger.yaml
      line: 1
      ...
- hash: 8a878eb2050c855faab96d2e52cc7cf8
  object_name: Query Queries.promoterInfo
  object_type: query
  parser: graphql
> severity: high  <<<<<<<<<<<<<<<<<<<<<<<< !!!
  tags:
> - pii  <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< !!!
  file: query.graphql
  line: 143
  properties: {}
  fields:
    input.PromoterInfoInput.link:
      field_name: input.PromoterInfoInput.link
      field_type: String
      file: query.graphql
      line: 291
    output.PromoterInfoPayload.firstName:
      field_name: output.PromoterInfoPayload.firstName
      field_type: String
      file: query.graphql
      line: 342
>>>>  severity: high  <<<<<<<<<<<<<<<<<< !!!
      tags:
>>>>  - pii  <<<<<<<<<<<<<<<<<<<<<<<<<<< !!!
    output.PromoterInfoPayload.lastName:
      field_name: output.PromoterInfoPayload.lastName
      field_type: String
      file: query.graphql
      line: 365
      severity: high
      tags:
>>>>  - pii  <<<<<<<<<<<<<<<<<<<<<<<<<<< !!!```
```

## Use local LLM model for scoring fields

Replace or combine exist static keyword ruleset with local LLM like Llama-3.2, fill conf.yaml with choosed LLM and system prompt to define what type of data you want to look after:
```
```
ai_params:
  model_id: "mradermacher/Llama-3.2-3B-Instruct-uncensored-GGUF"
  gguf_file: "Llama-3.2-3B-Instruct-uncensored.Q8_0.gguf"
  model_folder: "/app/tests/ai_samples/hf_home"
  prompt: "You are security bot, for provided objects select only field names that contain personally identifiable information (pii), finance, authentication and other sensitive data."```
```

Run scan with new settings and get objects and fields severity from local AI engine:
```
```
appsec-discovery --source tests/swagger_samples --config tests/config_samples/ai_conf_llama.yaml

...
- hash: 2e20a348a612aa28d24c1bd0498eebf0
  object_name: Swagger route /user/login (GET)
  object_type: route
  parser: swagger
> severity: medium  <<<<<<<<<<<<<<<< !!!
  tags:
> - llm  <<<<<<<<<<<<<<<<<<<<<<<<<<< !!!
  file: /swagger.yaml
  line: 83
  properties:
    path:
      prop_name: path
      prop_value: /user/login
    method:
      prop_name: method
      prop_value: get
  fields:
    ...
    Input.password:
      field_name: Input.password
      field_type: string
      file: /swagger.yaml
      line: 83
>>>>  severity: medium  <<<<<<<<<<<<<< !!!
      tags:
>>>>  - llm  <<<<<<<<<<<<<<<<<<<<<<<<< !!!
      ...```
```

At first run tool with download provided model from Huggingface into local cache dir, for next offline scans use this dir with pre downloaded models.

Play around with with various [models](https://huggingface.co/models?search=llama-3.2) from Huggingface and prompts for best results.

## Integrate into CI/CD

Run scan with sarif output format:
```
```
appsec-discovery --source tests/swagger_samples --config tests/config_samples/conf.yaml --output report.json --output-type sarif```
```

Load result reports into vuln management system like Defectdojo:

## Service mode

Clone code to local folder:
```
```
git clone https://github.com/dmarushkin/appsec-discovery
cd appsec-discovery/appsec_discovery_service```
```

Fillout .env file with your gitlab url and token, change passwords for local db and ui user, for alerts register new telegram bot or use exist one, or just leave TG args empty to only store objects:
```
```
POSTGRES_HOST=discovery_postgres
POSTGRES_DB=discovery_db
POSTGRES_USER=discovery_user
POSTGRES_PASSWORD=some_secret_str
GITLAB_PRIVATE_TOKEN=some_secret_str
GITLAB_URL=https://gitlab.examle.com
GITLAB_PROJECTS_PREFIX=backend/,frontend/,test/
[email protected]
UI_ADMIN_PASSWORD=admin
UI_JWT_KEY=some_secret_str
MAX_WORKERS=5
MR_ALERTS=1
TG_ALERT_TOKEN=test
TG_CHAT_ID=0000000000```
```

Run service localy with docker compose:
```
```
docker-compose up --build```
```

Service will continuosly fetch new projects and MRs for provided prefixes from Gitlab api, clone code and scan it for objects, score found ones and save into local postgres db for any analysis.

If sensitive fields in objects added on Merge requests service will alert via provided channel.

To ajust default rule list authorize in Rules Management UI at http://127.0.0.1/ and make some new rules or make exclude rules for false positives:

For now service does not provide any local UI for parsed and scored objects, so we recomend to use any kind of external analytic systems like Apache Superset, Grafana, Tableu etc.

For prod environments bake Docker images in your k8s env, use external db.

## Usage examples

- Appsec specialists can monitor codebase for critical changes and review them manualy, also sum scores for particular fields and get overall risk score for entire projects, and use it for prioritization of any kind of appsec rutines (triage vulns, plan security audits).
- Governance, Risk, and Compliance (GRC) specialists can use discovered data schemas for any kind of data governance (localize PII, payment and other critical data, dataflows), restricting access to and between critical services, focus on hardening environments that contain critical data.
- Monitoring or Incident Response specialists can focus attention on logs and anomalies in critical services or even particular routes in clients traffic.
- Infrastructure security specialists can use same approach to extract structured data about assets from IaC repositories like terraform or ansible (service now extracts VMs from terraform files).

# Examples

Some examples of code input and tool output for common contract types like Swagger, Protobuf and Graphql.

## Swagger

Swagger file:
```
```
openapi: 3.0.3
info:
  title: Swagger Petstore - OpenAPI 3.0
  ...
paths:
  /user/login:
    get:
      tags:
        - user
      summary: Logs user into the system
      description: ''
      operationId: loginUser
      parameters:
        - name: username
          in: query
          description: The user name for login
          required: false
          schema:
            type: string
        - name: password
          in: query
          description: The password for login in clear text
          required: false
          schema:
            type: string
      responses:
        '200':
          description: successful operation
          headers:
            X-Rate-Limit:
              description: calls per hour allowed by the user
              schema:
                type: integer
                format: int32
            X-Expires-After:
              description: date in UTC when token expires
              schema:
                type: string
                format: date-time
          content:
            application/xml:
              schema:
                type: string
            application/json:
              schema:
                type: string
        '400':
          description: Invalid username/password supplied```
```

Scanned structure:
```
```
appsec-discovery --source tests/swagger_samples

- hash: 40140abef3b5f45d447d16e7180cc231
  object_name: Route /user/login (GET)
  object_type: route
  parser: swagger
  severity: high
  tags:
  - auth
  file: swagger.yaml
  line: 1
  properties:
    path:
      prop_name: path
      prop_value: /user/login
      severity: medium
      tags:
      - auth
    method:
      prop_name: method
      prop_value: GET
  fields:
    query.param.username:
      field_name: query.param.username
      field_type: string
      file: swagger.yaml
      line: 1
      severity: medium
      tags:
      - auth
    query.param.password:
      field_name: query.param.password
      field_type: string
      file: swagger.yaml
      line: 1
      severity: high
      tags:
      - auth
    output:
      field_name: output
      field_type: string
      file: swagger.yaml
      line: 1```
```

## Protobuf

Proto file:
```
```
syntax = "proto3";

package com.surajgharat.practice.grpc.service;

service SumService {
  rpc Sum(SumInput) returns (SumOutput) {}
}

message SumInput {
  int32 n1 = 1;
  int32 n2 = 2;
}

message SumOutput { int32 result = 1; }```
```

Scanned structure:
```
```
appsec-discovery --source tests/protobuf_samples/

- hash: 9e167a92c3a4ecb34a52a148775b3dba
  object_name: Rpc /com.surajgharat.practice.grpc.service.SumService/Sum
  object_type: rpc
  parser: protobuf
  file: test2.proto
  line: 1
  properties: {}
  fields:
    input.SumInput.n1:
      field_name: SumInput.n1
      field_type: int32
      file: test2.proto
      line: 1
    input.SumInput.n2:
      field_name: SumInput.n2
      field_type: int32
      file: test2.proto
      line: 2
    output.SumOutput.result:
      field_name: SumOutput.result
      field_type: int32
      file: test2.proto
      line: 1```
```

## Graphql

Graphql file:
```
```
type MgmQueries

extend type Query {
    mgm: MgmQueries!
}

extend type MgmQueries  {
    offer(input: MgmOfferInput!): MgmOfferPayload!
    promoterInfo(input: MgmPromoterInfoInput!): MgmPromoterInfoPayload!
}

input MgmOfferInput {
    link: String!
}

input MgmPromoterInfoInput {
    link: String!
}

type MgmPromoterInfoPayload {
    firstName: String!
    lastName: String!
}

type MgmOfferPayload {
    offer: MgmOffer!
}```
```

Scanned structure:
```
```
appsec-discovery --source tests/graphql_samples/

- hash: 073e49453527d0792215a5359bf237db
  object_name: Query MgmQueries.offer
  object_type: query
  parser: graphql
  file: query.graphql
  line: 91
  properties: {}
  fields:
    input.MgmOfferInput.link:
      field_name: input.MgmOfferInput.link
      field_type: String
      file: query.graphql
      line: 241
    output.MgmOfferPayload.offer:
      field_name: output.MgmOfferPayload.offer
      field_type: MgmOffer
      file: query.graphql
      line: 413
- hash: 8a878eb2050c855faab96d2e52cc7cf8
  object_name: Query MgmQueries.promoterInfo
  object_type: query
  parser: graphql
  severity: high
  tags:
  - pii
  file: query.graphql
  line: 143
  properties: {}
  fields:
    input.MgmPromoterInfoInput.link:
      field_name: input.MgmPromoterInfoInput.link
      field_type: String
      file: query.graphql
      line: 291
    output.MgmPromoterInfoPayload.firstName:
      field_name: output.MgmPromoterInfoPayload.firstName
      field_type: String
      file: query.graphql
      line: 342
      severity: high
      tags:
      - pii
    output.MgmPromoterInfoPayload.lastName:
      field_name: output.MgmPromoterInfoPayload.lastName
      field_type: String
      file: query.graphql
      line: 365
      severity: high
      tags:
      - pii```
```
