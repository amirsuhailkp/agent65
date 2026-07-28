---
title: OWASP Smart Contract Top 10
source: owasp.org
url: https://owasp.org/www-project-smart-contract-top-10/
collector: owasp
category: web-security
tags:
- web-security
- contract
- smart
- top
- owasp
date_collected: '2026-07-26T12:45:51.724791Z'
language: unknown
---

# OWASP Smart Contract Top 10

## About the Smart Contract Top 10

The **OWASP Smart Contract Top 10 : 2026** is a standard awareness document that aims to provide Web3 developers and security teams with insights into the top 10 vulnerabilities found in smart contracts. It is a **sub‑project of the broader OWASP Smart Contract Security (OWASP SCS) initiative**.

It serves as a reference to ensure that smart contracts are secured against the most critical weaknesses exploited or discovered in recent years. The **Smart Contract Top 10** can be used alongside other OWASP SCS projects to ensure comprehensive risk coverage:

- **OWASP SC Weakness Enumeration (SCWE):**<https://scs.owasp.org/SCWE/>
- **OWASP SCS Checklist:**<https://scs.owasp.org/checklists/>
- **OWASP Top 15: Web3 Attack Vectors (Beyond Smart Contracts)**<https://scs.owasp.org/sctop10/Web3-Attack-Vectors-Top15/>
- **OWASP SC Top 10 Live Site (2026):**<https://scs.owasp.org/sctop10/>

Use the Top 10 for:

- **Awareness**: Understand the most common and critical vulnerabilities affecting smart contracts.
- **Prevention**: Implement best practices to safeguard against these known issues.
- **Standard Compliance**: A reference to ensure secure development and assessment of smart contracts.

> Note: The current
>
> *2026*Top 10 is*forward-looking*: its ordering and category definitions are derived from*security incidents and survey data collected during 2025*, and then used to forecast which risks are expected to be most significant in the upcoming year. In other words, 2025 breach and vulnerability data provides the empirical foundation, while the 2026 list reflects how those observations are projected into the near future.
>
> This ranking is intended to raise awareness among security researchers, auditors, developers, protocol owners, and the broader industry about the 10 most commonly occurring and impactful smart contract risks.

## Changes (2025-2026)

### 2026 Top 10 (Forward-Looking)

- SC01:2026 - [Access Control Vulnerabilities](/www-project-smart-contract-top-10/2026/en/src/SC01-access-control-vulnerabilities.html)
- SC02:2026 - [Business Logic Vulnerabilities](/www-project-smart-contract-top-10/2026/en/src/SC02-business-logic-vulnerabilities.html)
- SC03:2026 - [Price Oracle Manipulation](/www-project-smart-contract-top-10/2026/en/src/SC03-price-oracle-manipulation.html)
- SC04:2026 - [Flash Loan–Facilitated Attacks](/www-project-smart-contract-top-10/2026/en/src/SC04-flash-loan-facilitated-attacks.html)
- SC05:2026 - [Lack of Input Validation](/www-project-smart-contract-top-10/2026/en/src/SC05-lack-of-input-validation.html)
- SC06:2026 - [Unchecked External Calls](/www-project-smart-contract-top-10/2026/en/src/SC06-unchecked-external-calls.html)
- SC07:2026 - [Arithmetic Errors](/www-project-smart-contract-top-10/2026/en/src/SC07-arithmetic-errors.html)
- SC08:2026 - [Reentrancy Attacks](/www-project-smart-contract-top-10/2026/en/src/SC08-reentrancy-attacks.html)
- SC09:2026 - [Integer Overflow and Underflow](/www-project-smart-contract-top-10/2026/en/src/SC09-integer-overflow-underflow.html)
- SC10:2026 - [Proxy & Upgradeability Vulnerabilities](/www-project-smart-contract-top-10/2026/en/src/SC10-proxy-and-upgradeability-vulnerabilities.html)

### Overview

TitleDescriptionSC01 - Access Control VulnerabilitiesAccess control flaws allow unauthorized users or roles to invoke privileged functions or modify critical state, often leading to full protocol compromise when admin, governance, or upgrade paths are exposed.SC02 - Business Logic VulnerabilitiesDesign-level flaws in lending, AMM, reward, or governance logic that break intended economic or functional rules, enabling attackers to extract value even when low-level checks appear correct.SC03 - Price Oracle ManipulationWeak oracles and unsafe price integrations that let attackers skew reference prices, enabling under-collateralized borrowing, unfair liquidations, and mispriced swaps as part of larger exploit chains.SC04 - Flash Loan–Facilitated AttacksAttacks that use large, uncollateralized flash loans to magnify small bugs (in logic, pricing, or arithmetic) into large drains, by executing complex multi-step sequences in a single transaction.SC05 - Lack of Input ValidationMissing or weak validation of user, admin, or cross-chain inputs that allows unsafe parameters to reach core logic, corrupting state, breaking assumptions, or enabling direct fund loss.SC06 - Unchecked External CallsUnsafe interactions with external contracts or addresses where failures, reverts, or callbacks are not safely handled, often enabling reentrancy or inconsistent state.SC07 - Arithmetic ErrorsSubtle bugs in integer math, scaling, and rounding; especially in share, interest, and AMM calculations; that can be repeatedly exploited to cause precision loss, or siphon value, particularly when paired with flash loans.SC08 - Reentrancy AttacksSituations where external calls can re-enter vulnerable functions before state is fully updated, allowing repeated withdrawals or state changes from outdated views of contract state.SC09 - Integer Overflow and UnderflowDangerous arithmetic on platforms or code paths without robust overflow checks, leading to wrapped values, broken invariants, and potential drains of liquidity or mis-accounting.SC10 - Proxy & Upgradeability VulnerabilitiesMisconfigured or weakly governed proxy, initialization, and upgrade mechanisms that let attackers seize control of implementations or reinitialize critical state.

## Data Sources

### SolidityScan’s Web3HackHub:

To identify and validate the OWASP Smart Contract Top 10 vulnerabilities, we incorporated insights from multiple authoritative sources, with a notable focus on  **SolidityScan’s Web3HackHub (2025)**. This resource provides a comprehensive database of blockchain-related incidents, offering valuable data on attack vectors, financial losses, and trends.

Web3HackHub documents breaches from 2011 onward, enabling analysis of evolving attack methods, the increasing sophistication of exploits, and lessons learned from each incident.

The complete **methodology, ranking logic, and external data sources** for the 2026 Top 10 are documented on the OWASP SCS site:

- **Methodology & Data for the 2026 Top 10:**<https://scs.owasp.org/sctop10/data-sources/>

On that page you’ll find:

- How the practitioner survey is designed and how category rankings are aggregated.
- How 2025 smart‑contract incident data (SolidityScan Web3HackHub, SlowMist, BlockSec, DeFiHackLabs, etc.) is mapped into OWASP categories.
- Category‑wise loss totals, risk metrics, and the justification for the final ordering.

## Licensing

The OWASP Smart Contract Top 10 (2026) is [licensed](https://github.com/OWASP/www-project-smart-contract-top-10/blob/main/LICENSE.md) under the [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/), the Creative Commons Attribution-ShareAlike 4.0 license. Some rights reserved.

## Project Leaders

- [Jinson Varghese Behanan](/cdn-cgi/l/email-protection#355f5c5b465a5b755a425446451b5a4752)(Twitter:[@JinsonCyberSec](https://x.com/JinsonCyberSec))
- [Shashank](/cdn-cgi/l/email-protection#d2a1bab3a1bab3bcb992b1a0b7b6a1babbb7beb6a1fcb1bdbf)(Twitter:[@cyberboyIndia](https://x.com/cyberboyIndia))

## Example

Put whatever you like here: news, screenshots, features, supporters, or remove this file and don’t use tabs at all.

## Project Lead

NameAffiliationPersonal LinksJinson Varghese Behanan[Astra Security](https://www.getastra.com)[Website](https://www.jinsonvarghese.com), [Twitter](https://twitter.com/JinsonCyberSec), [LinkedIn](https://www.linkedin.com/in/JinsonVarghese/)Shashank[CredShields](https://credshields.com)[Twitter](https://x.com/cyberboyIndia), [LinkedIn](https://www.linkedin.com/in/shashank-in/)

## Contributors

Individuals that provided a significant contribution to the project:

NameAffiliationPersonal LinksMoises Ruiz Diaz[Web3 Security Latam](https://www.web3securitylatam.com)[Twitter](https://twitter.com/bunturx), [LinkedIn](https://www.linkedin.com/in/bunturx)Hansen Wong-[Twitter](https://twitter.com/hansen_wong)Pratik Lagaskar[CredShields](https://credshields.com/)[LinkedIn](https://www.linkedin.com/in/pratik-lagaskar), [Twitter](https://x.com/warlordsam077)Nehal Pillai[CredShields](https://credshields.com/)[LinkedIn](https://www.linkedin.com/in/nehal-pillai), [Twitter](https://x.com/nehal_10_0)Sobhan Shokri-[LinkedIn](https://www.linkedin.com/in/xdevman/), [Twitter](https://x.com/xdevman)whackur[DSRV](https://dsrv.com)[LinkedIn](https://www.linkedin.com/in/whackur/)Siddharth Neekher[CredShields](https://credshields.com/)[LinkedIn](http://www.linkedin.com/in/siddharth-neekher-340519117), [Twitter](https://x.com/sidartdigital)Shreya Berry[CredShields](https://credshields.com/)[LinkedIn](https://www.linkedin.com/in/shreya-berry/), [Twitter](https://x.com/ShreyaBerry2)

All discussions take place on the OWASP Smart Contract Top Ten [GitHub repository](https://github.com/OWASP/www-project-smart-contract-top-10) or [Slack Channel](https://owasp.slack.com/archives/C07MNDE6TPZ).

We welcome all community members to actively participate and help enhance this project. If you have any suggestions, feedback or want to help improve the list, we invite you to kickstart a dialogue by raising an issue or submitting a pull request.

You can read our contributing guidelines [here](https://github.com/OWASP/www-project-smart-contract-top-10/blob/main/CONTRIBUTING.md).

## About the Smart Contract Top 10

The OWASP Smart Contract Top 10 is a standard awareness document that intends to provide Web3 developers and security teams with insight into the top 10 vulnerabilities found in smart contracts.

It will serve as a reference to ensure that smart contracts are secured against the top 10 weaknesses exploited/discovered over the last couple of years.

### Top 10

- SC01:2023 - [Reentrancy Attacks](2023/en/src/SC01-reentrancy-attacks.md)
- SC02:2023 - [Integer Overflow and Underflow](2023/en/src/SC02-integer-overflow-underflow.md)
- SC03:2023 - [Timestamp Dependence](2023/en/src/SC03-timestamp-dependence.md)
- SC04:2023 - [Access Control Vulnerabilities](2023/en/src/SC04-access-control-vulnerabilities.md)
- SC05:2023 - [Front-running Attacks](2023/en/src/SC05-front-running-attacks.md)
- SC06:2023 - [Denial of Service (DoS) Attacks](2023/en/src/SC06-denial-of-service-attacks.md)
- SC07:2023 - [Logic Errors](2023/en/src/SC07-logic-errors.md)
- SC08:2023 - [Insecure Randomness](2023/en/src/SC08-insecure-randomness.md)
- SC09:2023 - [Gas Limit Vulnerabilities](2023/en/src/SC09-gas-limit-vulnerabilities.md)
- SC10:2023 - [Unchecked External Calls](2023/en/src/SC10-unchecked-external-calls.md)

### Overview

TitleDescriptionSC01 - Reentrancy AttacksA reentrancy attack exploits the vulnerability in smart contracts when a function makes an external call to another contract before updating its own state. This allows the external contract, possibly malicious, to reenter the original function and repeat certain actions, like withdrawals, using the same state. Through such attacks, an attacker can possibly drain all the funds from a contract.SC02 - Integer Overflow and UnderflowThe Ethereum Virtual Machine (EVM) defines fixed-size data types for integers, which limits the range of values they can represent. Overflow occurs when an arithmetic operation exceeds the maximum value a data type can hold, while underflow happens when an operation goes below the minimum value. For unsigned integers, underflow results in the maximum value, and for signed integers, exceeding the minimum value wraps around to the maximum positive value.SC03 - Timestamp DependenceSmart contracts often use block.timestamp for time-sensitive functions. However, miners can slightly adjust this timestamp, creating a vulnerability where they can manipulate the timing to gain an unfair advantage.SC04 - Access Control VulnerabilitiesAn access control vulnerability is a security flaw that allows unauthorized users to access or modify a contract’s data or functions. These vulnerabilities occur when the contract’s code fails to properly restrict access based on user permissions.SC05 - Front-running AttacksFront-running is an attack where a malicious actor exploits knowledge of pending transactions to gain an unfair advantage. Attackers observe the mempool and place their own transactions with higher gas fees to be processed before the target transaction, leading to potential financial losses and disruption of smart contract functionality.SC06 - Denial of Service (DoS) AttacksA Denial of Service (DoS) attack in Solidity targets vulnerabilities within smart contracts to exhaust critical resources such as gas, CPU cycles, or storage. These attacks aim to render the contract non-functional, disrupting its intended operation and potentially causing financial harm.SC07 - Logic ErrorsLogic errors, or business logic vulnerabilities, are subtle flaws found in smart contracts where the code deviates from its intended behavior. These errors can be challenging to detect as they reside within the contract’s logic, potentially leading to unintended outcomes or exploitable conditions.SC08 - Insecure RandomnessGenerating true randomness in smart contracts on blockchain networks is challenging due to their deterministic nature. Predictability or influence over a supposedly random number can allow attackers to exploit contracts for their benefit, undermining fairness and security measures.SC09 - Gas Limit VulnerabilitiesGas limits on blockchain platforms like Ethereum impose constraints on smart contract computations per transaction. Functions exceeding the block gas limit, particularly those involving loops over dynamic data structures such as arrays, risk transaction failure due to resource exhaustion, highlighting a common vulnerability in contract design.SC10 - Unchecked External CallsIn Ethereum smart contracts, failing to properly verify the outcome of external function calls can lead to unintended consequences. If the called function fails and the calling contract does not check for this, it may incorrectly proceed under the assumption of success, potentially compromising contract integrity and functionality.

## Licensing

The OWASP Smart Contract Top 10 document is licensed under the [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/), the Creative Commons
Attribution-ShareAlike 4.0 license. Some rights reserved.

## Project Leaders

- [Jinson Varghese Behanan](/cdn-cgi/l/email-protection#3e5457504d51507e51495f4d4e10514c59)(Twitter:[@JinsonCyberSec](https://x.com/JinsonCyberSec))
- [Shashank](/cdn-cgi/l/email-protection#03706b62706b626d684360716667706b6a666f67702d606c6e)(Twitter:[@cyberboyIndia](https://x.com/cyberboyIndia))

## About the Smart Contract Top 10

The OWASP Smart Contract Top 10 (2025) is a standard awareness document providing Web3 developers and security teams with insights into the top 10 vulnerabilities found in smart contracts.

It serves as a reference to ensure that smart contracts are secured against the most critical weaknesses exploited or discovered in recent years. The **Smart Contract Top 10** can be used alongside other smart contract security projects to ensure comprehensive risk coverage. Visit [scs.owasp.org](https://scs.owasp.org/) for more details on OWASP Smart Contract Security Projects.

## Changes

### Top 10

- SC01:2025 - [Access Control Vulnerabilities](2025/en/src/SC01-access-control.md)
- SC02:2025 - [Price Oracle Manipulation](2025/en/src/SC02-price-oracle-manipulation.md)
- SC03:2025 - [Logic Errors](2025/en/src/SC03-logic-errors.md)
- SC04:2025 - [Lack of Input Validation](2025/en/src/SC04-lack-of-input-validation.md)
- SC05:2025 - [Reentrancy Attacks](2025/en/src/SC05-reentrancy-attacks.md)
- SC06:2025 - [Unchecked External Calls](2025/en/src/SC06-unchecked-external-calls.md)
- SC07:2025 - [Flash Loan Attacks](2025/en/src/SC07-flash-loan-attacks.md)
- SC08:2025 - [Integer Overflow and Underflow](2025/en/src/SC08-integer-overflow-underflow.md)
- SC09:2025 - [Insecure Randomness](2025/en/src/SC09-insecure-randomness.md)
- SC10:2025 - [Denial of Service (DoS) Attacks](2025/en/src/SC10-denial-of-service.md)

### Overview

TitleDescriptionSC01 - Access Control VulnerabilitiesAccess control flaws allow unauthorized users to access or modify a contract’s data or functions. These vulnerabilities arise when the code fails to enforce proper permission checks, potentially leading to severe security breaches.SC02 - Price Oracle ManipulationPrice Oracle Manipulation exploits vulnerabilities in how smart contracts fetch external data. By tampering with or controlling oracle feeds, attackers can affect contract logic, leading to financial losses or system instability.SC03 - Logic ErrorsLogic errors, or business logic vulnerabilities, occur when a contract’s behavior deviates from its intended functionality. Examples include incorrect reward distribution, token minting issues, or flawed lending/borrowing logic.SC04 - Lack of Input ValidationInsufficient input validation can lead to vulnerabilities where an attacker may manipulate the contract by providing harmful or unexpected inputs, potentially breaking logic or causing unexpected behaviors.SC05 - Reentrancy AttacksReentrancy attacks exploit the ability to reenter a vulnerable function before its execution is complete. This can lead to repeated state changes, often resulting in drained contract funds or broken logic.SC06 - Unchecked External CallsFailing to verify the success of external function calls can result in unintended consequences. When a called contract fails, the calling contract may incorrectly proceed, risking integrity and functionality.SC07 - Flash Loan AttacksFlash loans, while useful, can be exploited to manipulate protocols by executing multiple actions in a single transaction. These attacks often result in drained liquidity, altered prices, or exploited business logic.SC08 - Integer Overflow and UnderflowArithmetic errors due to exceeding the limits of fixed-size integers can lead to serious vulnerabilities, such as incorrect calculations or token theft. Unsigned integers wrap around on underflow, while signed integers flip between extremes.SC09 - Insecure RandomnessDue to the deterministic nature of blockchain networks, generating secure randomness is challenging. Predictable or manipulable randomness can lead to exploitation in lotteries, token distributions, or other randomness-dependent functionalities.SC10 - Denial of Service (DoS) AttacksDoS attacks exploit vulnerabilities to exhaust contract resources, rendering it non-functional. Examples include excessive gas consumption in loops or function calls designed to disrupt normal contract operation.

## Data Sources

### SolidityScan’s Web3HackHub:

To identify and validate the OWASP Smart Contract Top 10 vulnerabilities, we incorporated insights from multiple authoritative sources, with a notable focus on  **SolidityScan’s Web3HackHub (2024)**. This resource provides a comprehensive database of blockchain-related incidents, offering valuable data on attack vectors, financial losses, and trends.

Web3HackHub documents breaches from 2011 onward, enabling analysis of evolving attack methods, the increasing sophistication of exploits, and lessons learned from each incident.

**Key highlights from Web3HackHub for 2024 include:**

- Total Financial Impact: $1.42 billion lost across 149 documented incidents in 2024.
- Top Attack Vectors (by frequency, total losses):

  - Access Control Vulnerabilities: $953.2M in losses.
  - Logic Errors: $63.8M in losses.
  - Reentrancy Attacks: $35.7M in losses.
  - Flash Loan Attacks: $33.8M in losses.
  - Lack of Input Validation: $14.6M in losses.
  - Price Oracle Manipulation: $8.8M in losses.
  - Unchecked External Calls: $550.7K in losses.

### Other Sources:

In addition to SolidityScan’s Web3HackHub, incorporating insights from [Peter Kacherginsky’s “Top 10 DeFi Attack Vectors - 2024”](https://x.com/_iphelix/status/1855855006219690233) provides valuable data for creating the OWASP Smart Contract Top 10 for 2025. Peter’s analysis is instrumental in understanding the evolving threat landscape and aligning the OWASP Smart Contract Top 10 with real-world observations.

By integrating data from both SolidityScan’s Web3HackHub and Kacherginsky’s “Top 10 DeFi Attack Vectors - 2024,” we were able to provide a well-rounded justification for the 2025 rankings.

After analyzing **149 security incidents from SolidityScan’s Web3HackHub (2024)**, **Peter Kacherginsky’s “Top 10 DeFi Attack Vectors - 2024”**, and the  **Immunefi Crypto Losses in 2024 Report**, which collectively document over

**$1.42 billion in financial losses across decentralized ecosystems**, the

**OWASP Smart Contract Top 10 for 2025**was created to address the most critical vulnerabilities in the blockchain and smart contract ecosystem.

## Licensing

The OWASP Smart Contract Top 10 (2025) is [licensed](https://github.com/OWASP/www-project-smart-contract-top-10/blob/8083e976d6d18013dce2d5e6e62f98e632151a09/LICENSE.md) under the [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/), the Creative Commons Attribution-ShareAlike 4.0 license. Some rights reserved.

## Project Leaders

- [Jinson Varghese Behanan](/cdn-cgi/l/email-protection#bcd6d5d2cfd3d2fcd3cbddcfcc92d3cedb)(Twitter:[@JinsonCyberSec](https://x.com/JinsonCyberSec))
- [Shashank](/cdn-cgi/l/email-protection#bfccd7deccd7ded1d4ffdccddadbccd7d6dad3dbcc91dcd0d2)(Twitter:[@cyberboyIndia](https://x.com/cyberboyIndia))
