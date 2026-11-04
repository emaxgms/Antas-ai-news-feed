import json, re
from datetime import datetime
import uuid

path = '/home/ema/services/multi-server/Antas-ai-news-feed/items.json'

with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

existing_urls = {i['url'] for i in data if 'url' in i}
existing_domains = [re.sub(r'^https?://(www\.)?', '', i['url']).split('/')[0] for i in data if 'url' in i]
domain_counts = {}
for d in existing_domains:
    domain_counts[d] = domain_counts.get(d, 0) + 1

def make(title, url, desc, pub, domain):
    if url in existing_urls:
        return None
    if not title or not url:
        return None
    # enforce diversity: no more than 20% per domain in final set; use coarse check
    proposed = domain_counts.get(domain, 0)
    total = max(len(data), 1)
    if proposed / total > 0.20:
        return None
    item = {
        "id": str(uuid.uuid4()),
        "title": title.strip(),
        "url": url.strip(),
        "description": desc.strip()[:500],
        "published_at": pub,
    }
    existing_urls.add(url)
    domain_counts[domain] = domain_counts.get(domain, 0) + 1
    return item

def domain_of(url):
    return re.sub(r'^https?://(www\.)?', '', url).split('/')[0]

candidates = []

# New arXiv / tech-heavy papers
candidates += [
    ("Beyond Function Calling: Benchmarking Tool-Using Agents under Tool-Environment Unreliability", "https://arxiv.org/abs/2606.25819v1", "Benchmarks LLM agents in unstable tool environments, exposing robustness gaps in current tool-use evaluations.", "2026-06-24T13:34:34Z"),
    ("NatureBench: Can Coding Agents Match Published SOTA?", "https://arxiv.org/abs/2606.24530v1", "90-task benchmark drawn from Nature-family publications testing whether coding agents can do science, not just reproduce it.", "2026-06-23T12:58:23Z"),
    ("OpenThoughts-Agent: Data Recipes for Agentic Models", "https://arxiv.org/abs/2606.24855", "Open-source data recipes targeting broadly capable agentic models beyond single-benchmark training sets.", "2026-06-23T00:00:00Z"),
    ("World Models in Pieces: Structural Certification for General Agents", "https://arxiv.org/abs/2606.24842", "Formal framework for certifying general agents by specializing guarantees across world-model pieces.", "2026-06-23T00:00:00Z"),
    ("SHERLOC: Structured Diagnostic Localization for Code Repair Agents", "https://arxiv.org/abs/2606.24820", "Structured fault-localization framework giving code-repair agents actionable root-cause diagnoses rather than just file locations.", "2026-06-23T00:00:00Z"),
    ("Are We Ready For An Agent-Native Memory System?", "https://arxiv.org/abs/2606.24775", "Tracks agent memory evolution from RAG-style retrieval toward persistent, consolidating, lifecycle-governed data-management systems.", "2026-06-23T00:00:00Z"),
    ("Grad Detect: Gradient-Based Hallucination Detection in LLMs", "https://arxiv.org/abs/2606.24790", "Hallucination detector using internal gradients and activations to flag false claims before downstream use.", "2026-06-23T00:00:00Z"),
    ("CrossPool: Efficient Multi-LLM Serving for Cold MoE Models", "https://arxiv.org/abs/2606.24506", "Disaggregates KV-cache and model weights to reduce GPU memory waste when cold MoE requests hit uncommon expert shards.", "2026-06-23T00:00:00Z"),
    ("Privacy-Preserving RAG via Multi-Agent Semantic Rewriting", "https://arxiv.org/abs/2606.24623", "Multi-agent semantic rewriting framework that sanitizes RAG context for confidentiality while preserving factual fidelity.", "2026-06-23T00:00:00Z"),
    ("Grading the Grader: Lessons from Evaluating an Agentic Data Analysis System", "https://arxiv.org/abs/2606.24839", "Separates genuine disagreements from grader noise when benchmarking complex code-and-text data-analysis agents.", "2026-06-23T00:00:00Z"),
    ("GroundEval: Deterministic Replacement for LLM-as-Judge in Stateful Agent Evaluation", "https://arxiv.org/abs/2606.22737v1", "Deterministic agent evaluation by checking searched/fetched/cited/written evidence, removing stochastic LLM-judge bias.", "2026-06-22T21:41:34Z"),
    ("EnterpriseClawBench: Benchmarking Agents from Real Workplace Sessions", "https://arxiv.org/abs/2606.23654v1", "Agent benchmark built from proprietary enterprise sessions measuring tool calls, heterogeneous files, and business-artifact generation.", "2026-06-22T17:39:43Z"),
    ("Self-Compacting Language Model Agents", "https://arxiv.org/abs/2606.23525v1", "Trajectory-aware context compaction for long-lived agents that reduces token bloat more effectively than fixed threshold compaction.", "2026-06-22T16:08:34Z"),
    ("Agent-as-a-Router: Agentic Model Routing for Coding Tasks", "https://arxiv.org/abs/2606.22902v1", "Treats model routing as a Context->Action->Feedback loop, achieving lower cumulative regret than static routers on coding benchmarks.", "2026-06-22T06:37:31Z"),
    ("From Fragments to Paths: Task-Level Context Recovery for Large Industrial Codebases", "https://arxiv.org/abs/2606.22906", "DeepDiscovery two-stage Location-Inference pipeline that recovers task-relevant context across large repositories, achieving 78.6% SWE-bench Verified.", "2026-06-22T00:00:00Z"),
    ("LLM-as-Code: Agentic Programming for Agent Harness", "https://arxiv.org/abs/2606.15874", "KDD 2026 workshop paper proposing 'Agentic Programming' — host control flow with LLM invoked adaptively to avoid orchestrator-only bugs.", "2026-06-14T00:00:00Z"),
]

# Tier 2 engineering blogs
candidates += [
    ("Vibe Coding to Agentic Engineering with Claude Code", "https://www.apimatic.io/blog/agentic-engineering-claude-code", "Three-phase Claude Code workflow: structured prompt, plan mode, and review for consistent results.", "2026-06-25T09:21:31Z", "apimatic.io"),
    ("How to run any model inside Claude Code", "https://www.zyte.com/blog/how-to-run-any-model-inside-claude-code/", "Demonstrates backend-agnostic model routing inside Claude Code by swapping in GLM 5.2 with three environment variables.", "2026-06-23T14:01:30Z", "zyte.com"),
    ("Forecasting Enterprise AI Spend: See the Bill Before It Lands", "https://www.truefoundry.com/blog/forecasting-ai-cost", "Practical guide to AI cost forecasting with SARIMAX and Prophet, addressing unexpected budget overruns.", "2026-06-23T00:00:00Z", "truefoundry.com"),
    ("How a Poisoned Coding Test Turned an AI Agent Into an Attacker", "https://www.mitiga.io/blog/poisoned-coding-test-ai-agent-attack", "Security research detailing how a tampered coding assessment can trick AI agents into exfiltrating credentials and destructive actions.", "2026-06-22T00:00:00Z", "mitiga.io"),
]

# Tier 1 individuals
candidates += [
    ("OPFS + Pyodide test harness", "https://simonwillison.net/2026/Jun/23/opfs-pyodide/", "Technical walkthrough on building a test harness using Origin Private File System and Pyodide for browser-native agent evaluation workflows.", "2026-06-23T18:58:54Z", "simonwillison.net"),
    ("Prompt Injection as Role Confusion", "https://simonwillison.net/2026/Jun/22/prompt-injection-as-role-confusion/", "Research revealing LLMs prioritize text style over explicit role tags, increasing prompt injection success until 'destyling' reduces it from 61% to 10%.", "2026-06-22T00:00:00Z", "simonwillison.net"),
    ("Temporary Cloudflare Accounts for AI Agents", "https://simonwillison.net/2026/Jun/21/", "Cloudflare now lets AI agents deploy Workers without precreated accounts via temporary deployments, demonstrated with Codex Desktop and GPT-5.5.", "2026-06-21T00:00:00Z", "simonwillison.net"),
    ("AI Governance Checklist That Maps to Your Stack", "https://openrouter.ai/blog/insights/ai-governance-checklist/", "Governance checklists must map to LLM routing architecture, comparing managed versus self-hosted gateway defaults for audit, spend, and sovereignty.", "2026-06-22T00:00:00Z", "openrouter.ai"),
    ("Enforce AI Data Residency at the Routing Layer", "https://openrouter.ai/blog/insights/ai-data-residency/", "Step-by-step enforcement of geographic data residency via routing constraints with provider-order and Zero Data Retention examples.", "2026-06-22T00:00:00Z", "openrouter.ai"),
    ("OpenAI Codex OSS Mode: Run Codex with Any Open-Source Model", "https://developers.openai.com/codex/config-advanced", "OpenAI adds an OSS mode to Codex CLI allowing local/open-source model providers via Ollama, LM Studio, MLX, or vLLM, including GPT-OSS-20B and GPT-OSS-120B.", "2026-06-22T00:00:00Z", "openai.com"),
]

# GitHub open source and tooling
candidates += [
    ("PMB: Local-first persistent memory for AI coding agents over MCP", "https://github.com/oleksiijko/pmb", "Open-source MCP-based memory layer giving Claude Code, Cursor, and Codex a local SQLite-backed memory for decisions, lessons, and facts.", "2026-06-22T09:09:12Z", "github.com"),
    ("Ponytrail: Local audit trail for AI coding-agent edits", "https://github.com/0xroylee/ponytrail", "Lightweight audit trail recording every edit an AI coding agent makes before changes reach version control.", "2026-06-22T14:54:00Z", "github.com"),
    ("AgentRecall-MCP: Correction-First Persistent Memory for AI Agents", "https://github.com/Goldentrii/AgentRecall-MCP", "Open-source MCP server/SDK/CLI giving coding agents correction-first persistent memory with local-first storage across sessions.", "2026-06-23T21:20:07Z", "github.com"),
    ("agent-scan: Security Scanner for AI Agents, MCP Servers, and Agent Skills", "https://github.com/snyk/agent-scan", "Snyk's open-source security scanner for AI agents scanning vulnerable tool calls, unsafe permissions, and agent-workflow supply-chain risks.", "2026-06-24T09:03:20Z", "github.com"),
    ("dev-machine-guard: Scan Your Dev Machine for AI Agents and MCP Servers", "https://github.com/step-security/dev-machine-guard", "Lightweight local scanner that inventories AI agents, MCP servers, IDE extensions, and suspicious packages to surface shadow AI tooling.", "2026-06-24T06:43:37Z", "github.com"),
    ("lkerriso/agentic-ai-local-to-kubernetes — GitHub", "https://github.com/lkerriso/agentic-ai-local-to-kubernetes", "Companion repository for the talk 'Agentic AI: Going from Local to Kubernetes' with infrastructure and deployment patterns.", "2026-06-24T17:29:16Z", "github.com"),
    ("rickicode/patchright-browser — GitHub", "https://github.com/rickicode/patchright-browser", "MCP server for browser automation via Patchright: multi-profile Chromium, headed/headless, StreamableHTTP protocol with dashboard and AI agent setup.", "2026-06-24T12:33:48Z", "github.com"),
    ("AnswerJournal: MCP server to save and share AI answers", "https://answerjournal.com/", "MCP server that captures and shares AI agent answers across sessions into a searchable knowledge base.", "2026-06-23T22:26:23Z", "answerjournal.com"),
    ("Tecture: navigable architecture map from your coding agent", "https://tecture.io/", "HN-discussed tool letting coding agents generate an interactive architecture map of a repository to understand structure after autonomous refactors.", "2026-06-24T14:05:20Z", "tecture.io"),
]

# Engineering writeups
candidates += [
    ("Show HN: AnswerJournal – An MCP server to save and share AI answers", "https://news.ycombinator.com/item?id=43920624", "HN thread discussing the AnswerJournal MCP server and its approach to capturing AI agent outputs as a searchable team knowledge base.", "2026-06-23T22:40:00Z", "news.ycombinator.com"),
    ("Autonomous Long-Running Coding Agents", "https://academy.dair.ai/blog/autonomous-long-running-coding-agents", "Deep dive into loop engineering for autonomous coding agents, covering goals, evaluators, verifiers, and artifact-driven workflows.", "2026-06-21T00:00:00Z", "academy.dair.ai"),
    ("Prompt Engineering Is Dying: Loop Engineering Is Next", "https://kingy.ai/ai/prompt-engineering-is-dying-loop-engineering-is-next/", "Argues loop engineering is the higher-leverage discipline behind reliable agent workflows across Claude Code, Codex, and Cursor.", "2026-06-21T00:00:00Z", "kingy.ai"),
    ("The 7 Types of Agent Memory: A Technical Guide for AI Engineers", "https://www.marktechpost.com/2026/06/21/the-7-types-of-agent-memory-a-technical-guide-for-ai-engineers/", "Breaks down agent memory types with use-case mapping and Python implementations for production agent stacks.", "2026-06-21T00:00:00Z", "marktechpost.com"),
    ("Daily AI Agent News Roundup — June 21, 2026", "https://harness-engineering.ai/blog/daily-ai-agent-news-roundup-june-21-2026/", "Curated roundup on harness engineering as the new bottleneck in AI agent systems, covering observability, control loops, and agent-loop architecture.", "2026-06-21T00:00:00Z", "harness-engineering.ai"),
    ("AI Builders Digest — Sunday, June 21, 2026", "https://buttondown.com/soumyo/archive/ai-builders-digest-sunday-june-21-2026/", "Curated digest covering Vercel CEO on Markdown as the new programming language for AI agents and developer-plus-agent systems hybrid skill.", "2026-06-21T00:00:00Z", "buttondown.com"),
]

items = []
for c in candidates:
    if len(c) == 5:
        title, url, desc, pub, domain = c
    else:
        title, url, desc, pub = c
        domain = domain_of(url)
    item = make(title, url, desc, pub, domain)
    if item:
        items.append(item)

existing_data = data if isinstance(data, list) else []
merged = existing_data + items
merged = sorted(merged, key=lambda x: x.get('published_at', ''), reverse=True)

with open(path, 'w', encoding='utf-8') as f:
    json.dump(merged, f, indent=2)
    f.write('\n')

added = len(items)
total = len(merged)
print(f'added={added} total={total}')
