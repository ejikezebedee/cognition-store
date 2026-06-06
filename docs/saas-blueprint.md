# SaaS Blueprint

Cognition Store can move from an MVP developer engine to a commercial SaaS by wrapping the local-first cognition engine with a simple dashboard, hosted API, accounts, billing, and review workflows.

## Product Position

Commercial category:

> Business memory and decision-record software for AI-assisted work.

Core promise:

> Store, organize, verify, and reuse important thinking, decisions, source notes, AI work, risks, and lessons.

## SaaS Modules

### 1. Web Dashboard

The dashboard is the customer-facing product. It should let users create workspaces, add notes, review memory records, export reports, and manage team review without touching a command line.

Initial prototype:

- [../prototypes/saas-dashboard/index.html](../prototypes/saas-dashboard/index.html)

### 2. Backend API

The API should expose safe, scoped actions:

- create workspace
- create memory record
- upload approved source text
- run local-first extraction pipeline
- retrieve saved records
- export report
- invite reviewer
- manage API keys

### 3. Database

Recommended commercial structure:

- users
- workspaces
- projects
- source_notes
- memory_records
- extracted_points
- decision_reviews
- exports
- api_keys
- audit_logs
- subscriptions

### 4. Auth And Access Control

Required features:

- email/password or magic-link login
- workspace roles: owner, admin, reviewer, contributor
- API keys per workspace
- record-level permissions for sensitive work
- account deletion and data export

### 5. Billing

Suggested tiers:

- Free: limited records, local exports, single workspace
- Pro: more records, reports, templates, email support
- Team: shared workspaces, reviewers, audit logs, API keys
- Business: retention controls, priority support, advanced exports

### 6. Templates

Starter templates:

- AI work log
- project decision record
- client consultation notes
- research evidence review
- compliance check
- sales opportunity review
- operational incident review

### 7. Security And Compliance

The hosted product should include:

- encrypted data at rest
- TLS in transit
- secret redaction before storage
- rate limits
- audit logs
- workspace-level retention controls
- export and deletion rights
- clear notice that the tool supports decisions but does not replace human approval

### 8. Deployment

Recommended production path:

- web app hosting
- API service
- managed PostgreSQL
- object storage for uploads and exports
- background worker for extraction jobs
- monitoring and alerting
- automated backups
- CI/CD pipeline

## Build Sequence

1. Static dashboard prototype
2. Clickable demo with sample data
3. Backend API skeleton
4. Database schema and migrations
5. Auth and workspace model
6. Hosted extraction job runner
7. Billing integration
8. Production deployment checklist

## Success Test

The SaaS is commercially ready when a new user can sign up, create a workspace, add notes, generate a memory record, understand the review result, and export a useful report without developer help.
