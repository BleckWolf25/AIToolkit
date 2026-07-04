<adr_document>
# ADR: Database Migration to PostgreSQL
## Context
MongoDB lacks strict multi-document ACID transactions needed for billing.
## Decision
Migrate core data schemas to PostgreSQL.
## Consequences
Requires migration scripts and changes to query bindings.
</adr_document>