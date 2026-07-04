# ADR-001: Use PostgreSQL for main database

## Title
ADR-001: Use PostgreSQL for main database

## Status
Accepted

## Context
We need a relational database to store relational transactions and user profiles with strong ACID guarantees.

## Decision
We will use PostgreSQL (v16) hosted on Amazon RDS.

## Consequences
- **Positive:** Gives us robust relational database support, standard SQL queries, ACID compliance, and excellent support for JSON payloads.
- **Negative:** Requires strict schema migrations for deployment, and scaling RDS clusters requires maintenance window planning.
