# Release Notes v0.3.0

v0.3.0 moves Cognition Store from a polished developer MVP toward a SaaS-ready product direction.

## Added

- Common-user onboarding guide.
- SaaS blueprint covering dashboard, API, database, auth, billing, security, and deployment.
- Static dashboard prototype for a non-technical user journey.
- README section explaining the common-user version.
- Product positioning language for business owners, operators, consultants, researchers, and AI users.

## Changed

- Package version updated to `0.3.0`.
- Project description now reflects the broader product direction: evidence, memory, and decision records.
- Roadmap updated so SaaS readiness is the v0.3.0 milestone.

## Release Level

This release is SaaS-readiness, not a hosted production SaaS.

The repository now contains the product direction, prototype, onboarding language, and build sequence needed to start the hosted commercial version.

## Verification Targets

Before publishing or tagging this release, run:

```bash
python3 scripts/smoke_test.py
python3 -m compileall cognition_store scripts
pytest
```
