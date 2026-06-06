# Roadmap

Cognition Store is developed as a local-first cognition layer for agent systems that need evidence-backed memory, traceable reasoning, and bounded simulation output.

## v0.2.0 - Public Product Polish

- Clearer README positioning for buyers, builders, and reviewers.
- Developer test extras through `pip install -e ".[dev]"`.
- GitHub Actions CI for smoke tests, compile checks, and pytest.
- Public example gallery explaining generated artifacts.
- Updated release audit language for the published repository state.

## v0.3.0 - SaaS-Ready Product Layer

- Add common-user product positioning.
- Add SaaS blueprint for dashboard, backend, auth, billing, storage, and deployment.
- Add static dashboard prototype for non-technical user workflows.
- Add onboarding language that explains the product without developer terms.
- Add commercial release audit notes for the SaaS-readiness milestone.

## v0.4.0 - Stronger Developer Workflow

- Add richer command examples for each supported domain.
- Add optional export formats for summaries and verdicts.
- Add more graph validation tests.
- Add configurable evidence schemas for new domains.
- Add packaging guidance for PyPI distribution.

## v0.5.0 - Team Review Layer

- Add reviewer-friendly report templates.
- Add run comparison utilities.
- Add stricter approval gate configuration.
- Add domain starter packs for compliance, sales operations, and internal knowledge workflows.

## Future API/SaaS Possibilities

Cognition Store can become an API or SaaS product later, but the core product should stay local-first and defensive:

- encrypted workspace sync
- private team review dashboards
- role-based approval workflows
- hosted artifact review
- managed compliance reports

Any hosted version should preserve the current rule: simulation output supports decisions, but it does not execute production, finance, legal, or external communication actions automatically.
