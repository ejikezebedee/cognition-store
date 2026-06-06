# Cognition Store v0.2.0

Cognition Store v0.2.0 upgrades the project from a clean v0.1.0 release into a more polished public developer product.

## Highlights

- Added clearer README sections for who needs Cognition Store and where it can be implemented.
- Added a product positioning guide for commercial, internal, and open-source presentation.
- Added an examples gallery that explains the generated artifacts from each demo.
- Added a public roadmap covering v0.3.0, team review workflows, and future API/SaaS possibilities.
- Added a GitHub Actions CI workflow for smoke tests, compile checks, and pytest.
- Added a `dev` extra so contributors can install pytest with `pip install -e ".[dev]"`.
- Updated release audit files to match the repository's public GitHub state.
- Added `.gitignore` rules for Python caches, virtual environments, build output, and generated run artifacts.

## Verification Targets

Before publishing this release, run:

```bash
python3 scripts/smoke_test.py
python3 -m compileall cognition_store scripts
pytest
```

Also run a private-reference scan to confirm there are no private paths, internal workspace paths, credentials, tokens, or buyer-confusing staging references in public files.
