---
title: Dependency Graph & SBOM Best Practices Cheat Sheet¶
source: cheatsheetseries.owasp.org
url: https://cheatsheetseries.owasp.org/cheatsheets/Dependency_Graph_SBOM_Cheat_Sheet.html
collector: owasp
category: web-security
tags:
- web-security
- sbom
- dependency
- graph
- artifact
date_collected: '2026-07-26T12:36:21.873416Z'
language: unknown
---

# Dependency Graph & SBOM Best Practices Cheat Sheet[¶](#dependency-graph-sbom-best-practices-cheat-sheet)

## Introduction[¶](#introduction)

Modern software relies on hundreds of third-party components. A Software Bill of Materials (SBOM) provides a machine-readable inventory of those components, while a dependency graph shows how they relate. Together, they enable accurate vulnerability management, compliance checks, and faster incident response.

### TL;DR — Quick checklist[¶](#tldr-quick-checklist)

- Generate SBOMs **during build**(not ad-hoc) to capture exact resolved dependencies and metadata.
- Use standard formats (SPDX or CycloneDX) and publish at least one machine-readable SBOM per release.
- Sign SBOMs and artifacts (cosign / sigstore / in-toto) to bind SBOMs to the built artifact.
- Version and store SBOMs in a trusted artifact store or SBOM management system (e.g., Dependency-Track).
- Automate vulnerability enrichment & triage (Grype, OSS Index, Snyk, commercial feeds) and integrate with ticketing/incident flows.
- Maintain a policy that defines required SBOM elements, retention, and sharing rules.

## Definitions (short)[¶](#definitions-short)

- **SBOM**— Software Bill of Materials; machine-readable list of components, versions, checksums, and metadata.
- **Component**— A package, library, container image layer, binary, or module included in the product.
- **Dependency graph**— Directed graph of components showing dependency relationships.
- **Provenance / Attestation**— Evidence that the SBOM was produced by the claimed build process and is bound to the artifact.
- **VEX (Vulnerability Exploitability eXchange)**— A machine-readable document that states whether a known vulnerability actually affects a given product/component, and under what conditions.

## Minimum SBOM elements you should capture (practical)[¶](#minimum-sbom-elements-you-should-capture-practical)

At a minimum capture:

- Component name and version (canonicalized)
- Unique package identifiers (purl / package URL) where available
- Package type/ecosystem (npm, maven, pypi, deb, rpm, apk, OS image)
- Checksum(s) (SHA256 preferred) of the package or artifact
- Component supplier / origin (URL or VCS) where known
- License information (if available)
- Timestamps (generation time) and build identifiers (CI run ID)
- Relationship edges: direct vs transitive dependency
- SBOM generator metadata (tool, version, command)

## SBOM Formats & Generations[¶](#sbom-formats-generations)

- Generate SBOMs during build (after dependency resolution, before packaging) to capture exact versions and metadata.
- Use standard formats:
  - CycloneDX — lightweight, widely supported in SCA and Dependency-Track.
  - SPDX — rich, common in compliance/legal workflows.
- Other useful points of generation:
  - Local/dev for early validation (best-effort).
  - Container images: build-time + image scan to catch injected content.
  - Runtime/deployed: telemetry to validate what executes in production.

## Tooling & automation — pragmatic recommendations[¶](#tooling-automation-pragmatic-recommendations)

**Generate**: Syft, CycloneDX CLI, SPDX tools, or ecosystem exporters. Run in build container/agent.

**Sign / Attest**: Cosign, Sigstore, in-toto — bind SBOM ↔ artifact to prevent tampering.

**Scan / Enrich**: Grype, OSS Index, Snyk, Dependabot — map CVEs to SBOM components.

**Store & Analyze**: Dependency-Track, SBOM managers, or registries with SBOM support.

**Example commands (generation):**

- Syft to CycloneDX JSON:
```
```
syft packages dir:. -o cyclonedx-json > sbom-cyclonedx.json```
```

- Syft to SPDX JSON:
```
```
syft packages dir:. -o spdx-json > sbom-spdx.json```
```

- CycloneDX CLI (from a built artifact):
```
```
cyclonedx-bom -o bom.xml --input-pkg target/my-app.jar```
```

(Place generator commands in your build scripts or CI job and fail the build if SBOM generation fails.)

## Bind SBOM to artifacts (signing & provenance)[¶](#bind-sbom-to-artifacts-signing-provenance)

**Why:** Unsigned SBOMs can be forged; signing/attestation proves they come from the same trusted build.

**How:**

- Generate artifact + SBOM in the same CI job.
- Use Cosign/Sigstore to sign both; optionally add in-toto/SLSA provenance.
- Push artifact, SBOM, and signatures/attestations to your registry.

**Practical flow:**

build → generate SBOM → compute digests → sign/attest → publish.

## Ingesting & managing SBOMs at scale[¶](#ingesting-managing-sboms-at-scale)

Centralize in an SBOM manager (e.g., Dependency-Track) or registry with SBOM support.

Version & retain SBOMs like code for audit/incident response.

Normalize/deduplicate package IDs (purl) across suppliers.

Enrich with vulnerability, license, and policy data for automated triage.

## Vulnerability triage & remediation workflow[¶](#vulnerability-triage-remediation-workflow)

- **Map CVE → SBOM component(s)**to see direct vs transitive exposure.
- **Use VEX**where available to understand exploitability — suppliers or tooling may provide VEX documents that indicate whether a CVE is relevant, non-exploitable, or has available mitigations.
- **Prioritize**direct dependencies and high-severity runtime libraries.
- **Patch or Mitigate**: patch if possible; otherwise upgrade, isolate, or apply runtime controls.
- **Track**issues in your system with SBOM + VEX evidence (component, version, digest, exploitability status)
- **Verify**by regenerating SBOM to confirm the vulnerable component is gone.

## Handling transitive dependencies and supply chain depth[¶](#handling-transitive-dependencies-and-supply-chain-depth)

- **Visualize**with dependency graphs to show why a vulnerable transitive package is included.
- **Prefer explicit direct upgrades**where possible (bump direct dependency to a version that pulls a fixed transitive release).
- **Consider mitigation patterns**: dependency replacement, patching (if legal and feasible), or runtime limitations.
- **Long-lived third-party binaries**: include policy to monitor and re-evaluate older dependencies that receive no updates.

## SBOM quality — common pitfalls & how to avoid them[¶](#sbom-quality-common-pitfalls-how-to-avoid-them)

Incomplete generation → generate SBOM in build after dependency resolution.

Missing metadata → always include timestamps, checksums, and tool info.

Inconsistent formats → stick to SPDX/CycloneDX; use extensions sparingly.

Unsigned SBOMs / no provenance → sign and attest artifacts.

No versioning or archival → retain historical SBOMs for audit/incident response.

## Policy & governance (what to write into your SBOM policy)[¶](#policy-governance-what-to-write-into-your-sbom-policy)

Minimum policy items:

- **Required formats**(CycloneDX vX or SPDX vY), and acceptable alternates
- **Required fields**(see section 3)
- **Where to store**(artifact registry, SBOM manager) and retention policy
- **Signing & attestation requirement**(e.g., all public releases must be signed)
- **SLA for vulnerability response**based on severity and impact
- **Supplier SBOM acceptance rules**(e.g., third-party vendors must supply SBOMs in a supported spec)
- **Access controls**for SBOMs containing sensitive metadata (avoid leaking internal repository URLs if not necessary)

## Practical CI/CD snippets & patterns[¶](#practical-cicd-snippets-patterns)

**GitHub Actions (example)** — generate CycloneDX and upload as artifact, then sign with cosign.
```
```
name: Build and SBOM
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build
        run: ./gradlew assemble
      - name: Generate SBOM
        run: |
          syft packages dir:./build/libs -o cyclonedx-json > sbom.json
      - name: Upload SBOM
        uses: actions/upload-artifact@v4
        with:
          name: sbom
          path: sbom.json
      - name: Sign Artifact & SBOM
        run: |
          cosign sign --key ${{ secrets.COSIGN_KEY }} my-registry/my-app:${{ github.sha }}
          cosign sign-blob --key ${{ secrets.COSIGN_KEY }} --output-signature sbom.json.sig sbom.json
      - name: Push image
        run: ./push-image.sh```
```

**Fail-fast vs Warn**: In CI, fail the pipeline if SBOM generation fails, but avoid failing builds on non-actionable low-severity findings — instead surface results to triage dashboards.

## Example workflows (short)[¶](#example-workflows-short)

**Supplier intake**: Vendor provides signed SBOM -> ingest into DT -> auto-enrich -> if critical CVE found, create ticket and notify procurement + security.

**Internal release**: CI builds artifact + sbom -> sign & push -> SBOM ingested to DT -> scheduled scan enrich -> policy engine flags high-sev/forbidden licenses -> create PR to remediate.
