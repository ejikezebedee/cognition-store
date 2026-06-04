## Summary

Describe the change and why it is needed.

## Verification

- [ ] `python3 scripts/smoke_test.py`
- [ ] `python3 -m compileall cognition_store scripts`
- [ ] `pytest` if available

## Data Hygiene

- [ ] No private paths
- [ ] No credentials, tokens, or API keys
- [ ] No personal emails or server IPs
- [ ] Examples use synthetic or approved sanitized data

## Guardrails

- [ ] No production, finance, contract, or external communication action is executed automatically
- [ ] Approval-sensitive behavior remains draft-only
