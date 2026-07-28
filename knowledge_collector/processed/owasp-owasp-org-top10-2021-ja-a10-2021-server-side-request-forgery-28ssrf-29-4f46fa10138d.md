---
title: A10:2021 - サーバーサイドリクエストフォージェリ SSRF
source: owasp.org
url: https://owasp.org/Top10/2021/ja/A10_2021-Server-Side_Request_Forgery_(SSRF)/
collector: owasp
category: web-security
tags:
- web-security
- ssrf
- url
- network
- services
date_collected: '2026-07-25T14:28:03.681073Z'
language: unknown
---

# A10:2021 - サーバーサイドリクエストフォージェリ (SSRF)

## 因子

対応する CWE 数最大発生率平均発生率加重平均（攻撃の難易度）加重平均（攻撃による影響）最大網羅率平均網羅率総発生数CVE 合計件数12.72%2.72%8.286.7267.72%67.72%9,503385

## 概要

このカテゴリはTop10コミュニティの調査（第1位）から追加されました。 調査データからわかることは、よくあるテストより広範な範囲において、問題の発生率は比較的低いものの、問題が起きた場合のエクスプロイトとインパクトは平均以上のものとなり得ます。 このSSRFのような新しい項目は、注意と認識を上げるために単一または小さな共通脆弱性タイプ一覧 (CWE) の集合であることが多く、注目を集めることで将来のバージョンにてより大きなカテゴリに集約されるよう期待されています。

## 説明

SSRFの欠陥は、Webアプリケーション上からリモートのリソースを取得する際に、ユーザーから提供されたURLを検証せずに使用することで発生します。 ファイアウォールやVPNあるいはその他の種類のネットワークアクセス制御リスト(ACL)によってアプリケーションが保護されている場合であっても、SSRFによりアプリケーションに対して意図しない宛先へ細工されたリクエストを強制的に発行させることができます。

モダンなアプリケーションではエンドユーザーに便利な機能を提供するようになり、アプリケーション側でURLを取得することは珍しい状況ではなくなりました。 そのためSSRFの発生が増加しています。 またSSRFの深刻度も、クラウドサービスやアーキテクチャの複雑性を背景として、段々と大きくなりつつあります。

## 防止方法

開発者は以下の多層防御の制御の一部ないし全てを実装することにより、SSRFを防ぐことができます。

### **ネットワーク層から**

- SSRFの影響を減らすために、リモートのリソースへアクセスする機能を分離されたネットワークに切り出します。
- 必須のイントラネット通信を除き全ての通信をブロックするよう、「デフォルト拒否」のファイアウォールポリシーまたはネットワークアクセス制御を強制します。

  *ヒント:*
  ~ アプリケーションに応じて、ファイアウォールルールの所有権とライフサイクルを明確化します。
  ~ ファイアウォールにおいて許可されたネットワークフロー、*そして*ブロックされたネットワークフローを全てログとして記録します ([A09:2021-セキュリティログとモニタリングの失敗](../A09_2021-Security_Logging_and_Monitoring_Failures/)を参照)。

### **アプリケーション層から:**

- クライアントが提供した全ての入力データをサニタイズし、検証します。
- 明確な許可リスト用いてURLスキーム、ポート、宛先を強制します。
- 生のレスポンスをクライアントに送信しないようにします。
- HTTPのリダイレクトを無効化します。
- DNSリバインディングや"time of check, time of use" (TOCTOU) 競合状態といった攻撃を防ぐために、URLの整合性に注意します。

拒否リストや正規表現を用いてのSSRF対策を実装しないでください。攻撃者は拒否リストを回避するためのペイロードのリスト、ツール、そして技術を備えています。

### **検討すべき追加の対策:**

- フロントシステムには、他のセキュリティ関連サービス（例：OpenID）をデプロイ（配備）しないでください。また、これらのシステム上のローカルトラフィック（例：localhost）も制御してください。
- ユーザーグループが限定的かつ管理可能であるフロントエンドで、特に高いレベルの保護が求められる場合は、独立したシステム上でネットワーク暗号化（例：VPN）を使用してください。

## 攻撃シナリオの例

攻撃者は以下のようなシナリオで、Webアプリケーションファイアウォールやファイアウォール、もしくはネットワークACLによって保護されたアプリケーションを攻撃することができます:

**シナリオ #1:** 内部サーバーへのポートスキャン - セグメント化されていないネットワークアーキテクチャの場合、攻撃者は内部ネットワークを標的として、SSRFペイロードの接続結果もしくは接続や拒否されるまでにかかった時間をもとに内部サーバーのポートがオープンかクローズかを調べます。

**シナリオ #2:** 機微な情報の露出 - 攻撃者は機微な情報を取得するために、
```
file:///etc/passwd</span>
```

や
```
http://localhost:28017/
```

のようなローカルファイルまたは内部サーバーにアクセスします。

**シナリオ #3:** クラウドサービスのメタデータストレージへのアクセス - 多くのクラウドプロバイダは
```
http://169.254.169.254/
```

のようなメタデータストレージを提供しています。攻撃者は機微な情報を取得するためにメタデータを読み取ります。

**シナリオ #4:** 内部サービスの乗っ取り - 攻撃者はリモートコード実行 (RCE) やサービス拒否 (DoS) のようなさらなる攻撃を行うために内部サービスを悪用します。

## 参考資料

## 対応する CWE のリスト

[CWE-918 Server-Side Request Forgery (SSRF)](https://cwe.mitre.org/data/definitions/918.html)

# A10:2021 – Server-Side Request Forgery (SSRF)

## Factors

CWEs MappedMax Incidence RateAvg Incidence RateAvg Weighted ExploitAvg Weighted ImpactMax CoverageAvg CoverageTotal OccurrencesTotal CVEs12.72%2.72%8.286.7267.72%67.72%9,503385

## Overview

This category is added from the Top 10 community survey (#1). The data shows a relatively low incidence rate with above average testing coverage and above-average Exploit and Impact potential ratings. As new entries are likely to be a single or small cluster of Common Weakness Enumerations (CWEs) for attention and awareness, the hope is that they are subject to focus and can be rolled into a larger category in a future edition.

## Description

SSRF flaws occur whenever a web application is fetching a remote resource without validating the user-supplied URL. It allows an attacker to coerce the application to send a crafted request to an unexpected destination, even when protected by a firewall, VPN, or another type of network access control list (ACL).

As modern web applications provide end-users with convenient features, fetching a URL becomes a common scenario. As a result, the incidence of SSRF is increasing. Also, the severity of SSRF is becoming higher due to cloud services and the complexity of architectures.

## How to Prevent

Developers can prevent SSRF by implementing some or all the following defense in depth controls:

### **From Network layer**

- Segment remote resource access functionality in separate networks to reduce the impact of SSRF
- Enforce “deny by default” firewall policies or network access control rules to block all but essential intranet traffic.

  *Hints:*
  ~ Establish an ownership and a lifecycle for firewall rules based on applications.
  ~ Log all accepted*and*blocked network flows on firewalls (see[A09:2021-Security Logging and Monitoring Failures](../A09_2021-Security_Logging_and_Monitoring_Failures/)).

### **From Application layer:**

- Sanitize and validate all client-supplied input data
- Enforce the URL schema, port, and destination with a positive allow list
- Do not send raw responses to clients
- Disable HTTP redirections
- Be aware of the URL consistency to avoid attacks such as DNS rebinding and “time of check, time of use” (TOCTOU) race conditions

Do not mitigate SSRF via the use of a deny list or regular expression. Attackers have payload lists, tools, and skills to bypass deny lists.

### **Additional Measures to consider:**

- Don't deploy other security relevant services on front systems (e.g. OpenID). Control local traffic on these systems (e.g. localhost)
- For frontends with dedicated and manageable user groups use network encryption (e.g. VPNs) on independent systems to consider very high protection needs

## Example Attack Scenarios

Attackers can use SSRF to attack systems protected behind web application firewalls, firewalls, or network ACLs, using scenarios such as:

**Scenario #1:** Port scan internal servers – If the network architecture
is unsegmented, attackers can map out internal networks and determine if
ports are open or closed on internal servers from connection results or
elapsed time to connect or reject SSRF payload connections.

**Scenario #2:** Sensitive data exposure – Attackers can access local
files such as or internal services to gain sensitive information such
as
```
file:///etc/passwd</span>
```

and
```
http://localhost:28017/
```

.

**Scenario #3:** Access metadata storage of cloud services – Most cloud
providers have metadata storage such as
```
http://169.254.169.254/
```

. An
attacker can read the metadata to gain sensitive information.

**Scenario #4:** Compromise internal services – The attacker can abuse
internal services to conduct further attacks such as Remote Code
Execution (RCE) or Denial of Service (DoS).
