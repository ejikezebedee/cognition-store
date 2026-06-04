# Security Policy

## Supported Versions

The current public release branch is supported for security reports.

## Reporting a Vulnerability

Please report suspected vulnerabilities privately to the project maintainers before opening a public issue. Include:

- affected version or commit
- reproduction steps
- expected and actual behavior
- impact assessment
- any relevant logs with secrets removed

Do not include real credentials, private customer data, access tokens, or production system details in a public issue.

## Scope

In scope:

- secret redaction failures
- unsafe handling of local files
- approval-gate bypasses
- generated output that could trigger unintended external actions
- packaging or documentation issues that expose private data

Out of scope:

- attacks requiring direct write access to the local repository
- reports without reproduction detail
- social engineering or spam

## Security Model

Cognition Store is a local decision-support engine. It does not authorize production changes, financial actions, contract actions, external communications, or sensitive-data processing on its own. Outputs that mention approval-sensitive actions are written as review drafts.
