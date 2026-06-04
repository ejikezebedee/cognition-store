Cognition Store v0.1.0 is now prepared for public release review.

Cognition Store is a local-first cognition layer for agent systems: it indexes approved local documents, redacts sensitive markers, extracts evidence-backed claims, builds lightweight knowledge graphs, and runs bounded simulations that produce reviewable JSON verdicts.

This first release focuses on practical agent memory infrastructure:
- working memory for current run context
- episodic memory through immutable action logs
- semantic memory through evidence-backed graph relationships
- procedural memory through reusable lessons and approval-aware recommendations

The project is intentionally conservative. It does not execute production changes, financial actions, contracts, external communications, or sensitive-data workflows from simulation output. Approval-sensitive findings remain draft artifacts for human review.

Included in v0.1.0:
- local evidence ingestion
- claim extraction
- file-based knowledge graph generation
- buyer-committee simulation examples
- market-risk simulation examples
- runtime completion capture
- secret redaction checks
- Apache-2.0 licensing
- public contribution and security documentation

Cognition Store is for developers and teams building agent systems that need local auditability, transparent reasoning traces, and practical memory structures without depending on a cloud memory backend.
