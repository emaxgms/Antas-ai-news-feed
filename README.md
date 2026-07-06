# Antas AI News Feed

Automated AI engineering news feed, updated daily by Hermes Agent cron job.

## Content

Curated articles, papers, blog posts, and discussions about:
- AI agents & agent orchestration
- MCP (Model Context Protocol)
- AI coding agents (Claude Code, Cursor, Codex, etc.)
- Open-source AI infrastructure
- Local LLMs & edge AI
- LLM observability & evaluation
- AI developer tooling & workflows

## Sources

- Individual builders & researchers (Simon Willison, Sebastian Raschka, Armin Ronacher, etc.)
- Engineering blogs (Anthropic, Vercel, OpenRouter, Sourcegraph, etc.)
- GitHub trending repositories
- arXiv research papers (cs.AI, cs.LG, cs.CL)
- Hacker News, technical newsletters

## Format

Each entry: `{id, title, url, description, published_at}`

Sorted by `published_at` descending.

## Automation

Updated via cron on Raspberry Pi using Hermes Agent.
