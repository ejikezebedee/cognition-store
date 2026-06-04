# Sanitization Trace Ledger

Package: `public-downloads/cognition-store`

Date: 2026-06-04

## Scope

Prepared a GitHub-ready local staging package from the internal cognition engine. No remote repository was initialized, pushed, or published.

## Actions

- Created a separate public staging directory.
- Excluded generated run artifacts and Python bytecode caches.
- Renamed the import package from the internal name to `cognition_store`.
- Replaced public-facing internal product references with neutral Cognition Store language.
- Replaced the runtime default project name with `local-runtime`.
- Added Apache-2.0 project metadata.
- Added public README, security policy, contribution guide, issue templates, and pull request template.
- Added public example folders for standard B2B sales and market compliance scenarios.

## Sanitization Rules

Scanned for:

- private absolute system paths
- private workspace references
- internal server language
- IP-address patterns
- personal email patterns
- token and credential-like strings
- private operational terms
- copied-source positioning language

## Result

- Private path and internal workspace scan: passed.
- Internal product/person/reference scan: passed.
- Email, IP-address, and common token-prefix scan: no actionable private finding.
- Python bytecode and cache scan: passed after cleanup.
- Smoke test: passed.
- Compile check: passed.
- Pytest: unavailable in local runtime.

## External Gate

Public release is not authorized by this package. Publishing requires a separate explicit approval.
