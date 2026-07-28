---
title: OWASP dep-scan
source: owasp.org
url: https://owasp.org/www-project-dep-scan/
collector: owasp
category: web-security
tags:
- web-security
- depscan
- server
- dep-scan
- use
date_collected: '2026-07-26T12:44:55.074250Z'
language: unknown
---

# OWASP dep-scan

# Introduction

OWASP dep-scan is a next-generation security and risk audit tool based on known vulnerabilities, advisories, and license limitations for project dependencies. Both local repositories and container images are supported as the input, and the tool is ideal for integration with ASPM/VM platforms and in CI environments.

## Features

- Scan most application code - local repos, Linux container images, Kubernetes manifests, and OS - to identify known CVEs with prioritization
- Perform advanced reachability analysis for multiple languages (See reachability analysis)
- Package vulnerability scanning is performed locally and is quite fast. No server is used!
- Generate Software Bill-of-Materials (SBOM) with Vulnerability Disclosure Report (VDR) information
- Generate a Common Security Advisory Framework (CSAF) 2.0 VEX document (check out the [CSAF Readme](https://github.com/owasp-dep-scan/dep-scan/blob/master/contrib/CSAF_README.md))
- Perform deep packages risk audit for dependency confusion attacks and maintenance risks (See risk audit)

### Vulnerability Data sources

- OSV
- NVD
- GitHub
- NPM
- Linux [vuln-list](https://github.com/appthreat/vuln-list)(Use
  ```
  --cache-os
  ```

  )

### Linux distros

- AlmaLinux
- Debian
- Alpine
- Amazon Linux
- Arch Linux
- RHEL/CentOS
- Rocky Linux
- Ubuntu
- OpenSUSE/SLES
- Photon
- Chainguard
- Wolfi OS

Application vulnerabilities would be reported for all Linux distros and Windows. To download the full vulnerability database suitable for scanning OS, invoke dep-scan with
```
--cache-os
```

for the first time. dep-scan would also download the appropriate database based on project type automatically.

## Usage

dep-scan is ideal for use during continuous integration (CI) and as a local development tool.

### OCI Artifacts via ORAS cli

Use [ORAS cli](https://oras.land/docs/installation/) to download the dep-scan binary and the vulnerability database for effortless integration. Example workflow is [here](https://github.com/appthreat/images-info/blob/main/.github/workflows/build.yml#L13).
```
```
export VDB_HOME=depscan
mkdir -p $VDB_HOME
oras pull ghcr.io/appthreat/vdb:v5 -o $VDB_HOME
oras pull ghcr.io/appthreat/depscan:v4 -o $VDB_HOME```
```

### Server mode

dep-scan and cdxgen could be run in server mode. Use the included docker compose file to get started.
```
```
git clone https://github.com/owasp-dep-scan/dep-scan
docker compose up```
```
```
```
depscan --server --server-host 0.0.0.0 --server-port 7070```
```

In server mode, use
```
/cache
```

endpoint to cache the vulnerability database.
```
```
# This would take over 5 minutes
curl http://0.0.0.0:7070/cache```
```

Use the
```
/scan
```

endpoint to perform scans.

> [!NOTE] The
>
> ```
> type
> ```
>
> parameter is mandatory in server mode.

- Scanning a local directory.
  ```
  curl --json '{"path": "/tmp/vulnerable-aws-koa-app", "type": "js"}' http://0.0.0.0:7070/scan
  ```
- Scanning an SBOM file (present locally).
  ```
  curl --json '{"path": "/tmp/vulnerable-aws-koa-app/sbom_file.json", "type": "js"}' http://0.0.0.0:7070/scan
  ```
- Scanning a GitHub repo.
  ```
  curl --json '{"url": "https://github.com/HooliCorp/vulnerable-aws-koa-app", "type": "js"}' http://0.0.0.0:7070/scan -o app.vdr.json
  ```
- Uploading an SBOM file and generating results based on it.
  ```
  curl -X POST -H 'Content-Type: multipart/form-data' -F 'file=@/tmp/app/sbom_file.json' http://0.0.0.0:7070/scan?type=js
  ```

### Scanning projects locally (Python version)
```
```
sudo npm install -g @cyclonedx/cdxgen
pip install owasp-depscan```
```

This would install two commands called
```
cdxgen
```

and
```
depscan
```

.

You can invoke the scan command directly with the various options.
```
```
cd <project to scan>
depscan --src $PWD --reports-dir $PWD/reports```
```

The full list of options is below:
```
```
usage: cli.py [-h] [--no-banner] [--cache] [--csaf] [--sync] [--profile {appsec,research,operational,threat-modeling,license-compliance,generic}] [--no-suggest] [--risk-audit] [--private-ns PRIVATE_NS] [-t PROJECT_TYPE] [--bom BOM] [-i SRC_DIR_IMAGE] [-o REPORT_FILE]
              [--reports-dir REPORTS_DIR] [--deep] [--no-universal] [--no-vuln-table] [--threatdb-server THREATDB_SERVER] [--threatdb-username THREATDB_USERNAME] [--threatdb-password THREATDB_PASSWORD] [--threatdb-token THREATDB_TOKEN] [--server]
              [--server-host SERVER_HOST] [--server-port SERVER_PORT] [--cdxgen-server CDXGEN_SERVER] [--debug] [--explain] [--reachables-slices-file REACHABLES_SLICES_FILE] [-v]

Fully open-source security and license audit for application dependencies and container images based on known vulnerabilities and advisories.

options:
  -h, --help            show this help message and exit
  --no-banner           Do not display banner
  --cache               Cache vulnerability information in platform specific user_data_dir
  --csaf                Generate a OASIS CSAF VEX document
  --sync                Sync to receive the latest vulnerability data. Should have invoked cache first.
  --profile {appsec,research,operational,threat-modeling,license-compliance,generic}
                        Profile to use while generating the BOM.
  --no-suggest          Disable suggest mode
  --risk-audit          Perform package risk audit (slow operation). Npm only.
  --private-ns PRIVATE_NS
                        Private namespace to use while performing oss risk audit. Private packages should not be available in public registries by default. Comma separated values accepted.
  -t PROJECT_TYPE, --type PROJECT_TYPE
                        Override project type if auto-detection is incorrect
  --bom BOM             Examine using the given Software Bill-of-Materials (SBOM) file in CycloneDX format. Use cdxgen command to produce one.
  -i SRC_DIR_IMAGE, --src SRC_DIR_IMAGE
                        Source directory or container image or binary file
  -o REPORT_FILE, --report_file REPORT_FILE
                        DEPRECATED. Use reports directory since multiple files are created. Report filename with directory
  --reports-dir REPORTS_DIR
                        Reports directory
  --deep                Perform deep scan by passing this --deep argument to cdxgen. Useful while scanning docker images and OS packages.
  --no-universal        Depscan would attempt to perform a single universal scan instead of individual scans per language type.
  --no-vuln-table       Do not print the table with the full list of vulnerabilities. This can help reduce console output.
  --threatdb-server THREATDB_SERVER
                        ThreatDB server url. Eg: https://api.sbom.cx
  --threatdb-username THREATDB_USERNAME
                        ThreatDB username
  --threatdb-password THREATDB_PASSWORD
                        ThreatDB password
  --threatdb-token THREATDB_TOKEN
                        ThreatDB token for token based submission
  --server              Run depscan as a server
  --server-host SERVER_HOST
                        depscan server host
  --server-port SERVER_PORT
                        depscan server port
  --cdxgen-server CDXGEN_SERVER
                        cdxgen server url. Eg: http://cdxgen:9090
  --debug               Run depscan in debug mode.
  --explain             Makes depscan to explain the various analysis. Useful for creating detailed reports.
  --reachables-slices-file REACHABLES_SLICES_FILE
                        Path for the reachables slices file created by atom.
  -v, --version         Display the version```
```

### Scanning containers locally (Python version)

Scan
```
latest
```

tag of the container
```
shiftleft/scan-slim
```
```
```
depscan --cache --src shiftleft/scan-slim -o containertests/depscan-scan.json -t docker```
```

Include
```
license
```

to the type to perform license audit.
```
```
depscan --cache --src shiftleft/scan-slim -o containertests/depscan-scan.json -t docker,license```
```

You can also specify the image using the sha256 digest
```
```
depscan --src redmine@sha256:a5c5f8a64a0d9a436a0a6941bc3fb156be0c89996add834fe33b66ebeed2439e -o containertests/depscan-redmine.json -t docker```
```

You can also save container images using docker or podman save command and pass the archive to depscan for scanning.
```
```
docker save -o /tmp/scanslim.tar shiftleft/scan-slim:latest
# podman save --format oci-archive -o /tmp/scanslim.tar shiftleft/scan-slim:latest
depscan --src /tmp/scanslim.tar -o reports/depscan-scan.json -t docker```
```

Refer to the docker tests under GitHub action workflow for this repo for more examples.

### Scanning projects locally (Docker container)
```
ghcr.io/appthreat/dep-scan
```

or
```
public.ecr.aws/appthreat/dep-scan:latest
```

container image can be used to perform the scan.

To scan with default settings
```
```
docker run --rm -v $PWD:/app ghcr.io/appthreat/dep-scan --src /app --reports-dir /app/reports```
```

Using AWS public ECR image
```
```
docker run --rm -v $PWD:/app public.ecr.aws/appthreat/dep-scan --src /app --reports-dir /app/reports```
```

To scan with custom environment variables based configuration
```
```
docker run --rm \
    -e VDB_HOME=/db \
    -e NVD_START_YEAR=2010 \
    -e GITHUB_PAGE_COUNT=5 \
    -e GITHUB_TOKEN=<token> \
    -v /tmp:/db \
    -v $PWD:/app ghcr.io/appthreat/dep-scan --src /app --reports-dir /app/reports```
```

In the above example,
```
/tmp
```

is mounted as
```
/db
```

into the container. This directory is then specified as
```
VDB_HOME
```

for caching the vulnerability information. This way the database can be cached and reused to improve performance.

## Supported languages and package format

dep-scan uses [cdxgen](https://github.com/CycloneDX/cdxgen) command internally to create Software Bill-of-Materials (SBoM) file for the project. This is then used for performing the scans.

The following projects and package-dependency format is supported by cdxgen.

LanguagePackage formatnode.jspackage-lock.json, pnpm-lock.yaml, yarn.lock, rush.js, bower.json, .min.jsjavamaven (pom.xml [1]), gradle (build.gradle, .kts), scala (sbt), bazelphpcomposer.lockpythonsetup.py, requirements.txt [2], Pipfile.lock, poetry.lock, bdist\_wheel, .whl, .egg-infogobinary, go.mod, go.sum, Gopkg.lockrubyGemfile.lock, gemspecrustbinary, Cargo.toml, Cargo.lock.Net.csproj, packages.config, project.assets.json [3], packages.lock.json, .nupkgdartpubspec.lock, pubspec.yamlhaskellcabal.project.freezeelixirmix.lockc/c++conan.lock, conanfile.txtclojureClojure CLI (deps.edn), Leiningen (project.clj)docker / oci imageAll supported languages and Linux OS packagesGitHub Actions Workflows.github/workflows/\*.ymlJenkins Plugins.hpi filesYAML manifestsdocker-compose, kubernetes, kustomization, skaffold, tekton etc

**NOTE**

The docker image for dep-scan currently doesn’t bundle suitable java and maven commands required for bom generation. To workaround this limitation, you can -

- Use python-based execution from a VM containing the correct versions for java, maven and gradle.
- Generate the bom file by invoking
  ```
  cdxgen
  ```

  command locally and subsequently passing this to
  ```
  dep-scan
  ```

  via the
  ```
  --bom
  ```

  argument.

## Reachability analysis

Depscan can perform reachability analysis for Java, JavaScript, TypeScript and Python with built-in support for parsing [atom](https://github.com/AppThreat/atom) reachables slicing. Simply invoke depscan with the
```
research
```

profile and language type to enable this feature.

To receive a verbose output including the reachable flows, pass the argument
```
--explain
```
```
```
--profile research -t language [--explain]```
```

### Example analysis for a Java project
```
```
depscan --profile research -t java -i <source directory> --reports-dir <reports directory> --explain```
```

### Example analysis for a JavaScript project
```
```
depscan --profile research -t js -i <source directory> --reports-dir <reports directory> --explain```
```

## Customization through environment variables

The following environment variables can be used to customise the behaviour.

- VDB\_HOME - Directory to use for caching database. For docker based execution, this directory should get mounted as a volume from the host
- NVD\_START\_YEAR - Default: 2018. Supports upto 2002
- GITHUB\_PAGE\_COUNT - Default: 2. Supports upto 20

## GitHub Security Advisory

To download security advisories from GitHub, a personal access token with the following scope is necessary.

- read:packages
```
```
export GITHUB_TOKEN="<PAT token>"```
```

## Suggest mode

Fix version for each vulnerability is retrieved from the sources. Sometimes, there might be known vulnerabilities in the fix version reported. Eg: in the below screenshot the fix versions suggested for jackson-databind might contain known vulnerabilities.

By passing an argument
```
--suggest
```

it is possible to force depscan to recheck the fix suggestions. This way the suggestion becomes more optimal for a given package group.

Notice, how the new suggested version is
```
2.9.10.5
```

which is an optimal fix version. Please note that the optimal fix version may not be the appropriate version for your application based on compatibility.

## Package Risk audit
```
--risk-audit
```

argument enables package risk audit. Currently, only npm and pypi packages are supported in this mode. A number of risk factors are identified and assigned weights to compute a final risk score. Packages that then exceed a maximum risk score (
```
config.pkg_max_risk_score
```

) are presented in a table.

Use
```
--private-ns
```

to specify the private package namespace that should be checked for dependency confusion type issues where a private package is available on public npm/pypi registry.

For example, to check if private packages with namespaces @appthreat and @shiftleft are not accidentally made public, use the below argument.
```
```
--private-ns appthreat,shiftleft```
```

Risk categoryDefault WeightReasonpkg\_private\_on\_public\_registry4Private package is available on a public registrypkg\_min\_versions2Packages with less than 3 versions represent an extreme where they could be either super stable or quite recent. Special heuristics are applied to ignore older stable packagesmod\_create\_min\_seconds1Less than 12 hours difference between modified and creation time. This indicates that the upload had a defect that had to be rectified immediately. Sometimes, such a rapid update could also be maliciouslatest\_now\_min\_seconds0.5Less than 12 hours difference between the latest version and the current time. Depending on the package such a latest version may or may not be desirablelatest\_now\_max\_seconds0.5Package versions that are over 6 years old are in use. Such packages might have vulnerable dependencies that are known or yet to be foundpkg\_min\_maintainers2Package has less than 2 maintainers. Many opensource projects have only 1 or 2 maintainers so special heuristics are used to ignore older stable packagespkg\_min\_users0.25Package has less than 2 npm userspkg\_install\_scripts2Package runs a custom pre or post installation scripts. This is often malicious and a downside of npm.pkg\_node\_version0.5Package supports outdated version of node such as 0.8, 0.10, 4 or 6.x. Such projects might have prototype pollution or closure related vulnerabilitiespkg\_scope4 or 0.5Packages that are used directly in the application (required scope) gets a score with a weight of 4. Optional packages get a score of 0.25deprecated1Latest version is deprecated

Refer to
```
pkg_query.py::get_category_score
```

method for the risk formula.

### Automatic adjustment

A parameter called
```
created_now_quarantine_seconds
```

is used to identify packages that are safely past the quarantine period (1 year). Certain risks such as
```
pkg_min_versions
```

and
```
pkg_min_maintainers
```

are suppressed for packages past the quarantine period. This adjustment helps reduce noise since it is unlikely that a malicious package can exist in a registry unnoticed for over a year.

### Configuring weights

All parameters can be customized by using environment variables. For eg:

export PKG\_MIN\_VERSIONS=4 to increase and set the minimum versions category to 4.

## Live OS scan

By passing
```
-t os
```

, depscan can generate an SBoM for a live operating system or a VM with OS packages and kernel information. Optionally, pass the argument
```
--deep
```

to generate an SBoM with both OS and application packages and to check for application vulnerabilities.

All OS packages.
```
```
depscan -t os -i . -o reports/depscan.json```
```

All OS and application packages.
```
```
depscan -t os --deep -i . -o reports/depscan.json```
```

## License scan

dep-scan can scan the dependencies for any license limitations and report them directly on the console log. To enable license scanning set the environment variable
```
FETCH_LICENSE
```

to
```
true
```

.
```
```
export FETCH_LICENSE=true```
```

The license data is sourced from choosealicense.com and is quite limited. If the license of a given package cannot be reliably matched against this list it will get silently ignored to reduce any noise. This behavior could change in the future once the detection logic gets improved.

## Kubernetes and Cloud apps

dep-scan could auto-detect most cloud applications and Kubernetes manifest files. Pass the argument
```
-t yaml-manifest
```

to manually specify the type.

## PDF reports

Ensure [wkhtmltopdf](https://wkhtmltopdf.org/downloads.html) is installed or use the official container image to generate pdf reports. Use with
```
--explain
```

for more detailed reports.

## Discord support

The developers could be reached via the [discord](https://discord.gg/DCNxzaeUpd) channel.
