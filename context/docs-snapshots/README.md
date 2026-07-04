# Docs Snapshots

Store point-in-time copies of external documentation or API specs here
when a prompt needs to reference them as context. Snapshotting (rather
than linking live) keeps prompts reproducible even if the source changes
or disappears.

Name files as `<source>-YYYY-MM-DD.md` so it's obvious how stale a
reference is, e.g. `stripe-webhooks-api-2026-05-10.md`.