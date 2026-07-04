# ADR-002: Adopt Tailwind CSS

## Title
ADR-002: Adopt Tailwind CSS

## Status
Proposed

## Context
Developing custom layouts with custom CSS stylesheets takes a lot of time and results in unmaintainable styling.

## Decision
We will adopt Tailwind CSS for utility-first styling across all new pages.

## Consequences
- **Positive:** Speeds up UI layout assembly, standardizes spacing/colors, reduces size of shipped CSS bundles.
- **Negative:** Requires introducing a build step compiler pipeline.
