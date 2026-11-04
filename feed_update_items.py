import json, re, uuid, xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path

FEED = Path('/home/ema/services/multi-server/Antas-ai-news-feed/items.json')

with FEED.open('r', encoding='utf-8') as f:
    data = json.load(f)

existing_urls = {i['url'] for i in data if 'url' in i}
url_pattern = re.compile(r'^https?://(www\.)?([^/]+)')
domain_counts = {}
for i in data:
    m = url_pattern.match(i.get('url', ''))
    if m:
        domain = m.group(2)
        domain_counts[domain] = domain_counts.get(domain, 0) + 1

# Current cutoff: last 72h to improve recall, prioritize newest
cutoff = datetime.now(timezone.utc) - timedelta(days=72)
added_urls = set()
items = []

def accept(url, domain):
    if url in existing_urls or url in added_urls:
        return False
    total = max(len(data) + len(items), 1)
    if domain_counts.get(domain, 0) / total > 0.20:
        return False
    return True

def add(title, url, desc, published_at, domain=None):
    if domain is None:
        m = url_pattern.match(url)
        domain = m.group(2) if m else url
    if not accept(url, domain):
        return
    items.append({
        'id': str(uuid.uuid4()),
        'title': title.strip(),
        'url': url.strip(),
        'description': desc.strip()[:500],
        'published_at': published_at,
    })
    existing_urls.add(url)
    added_urls.add(url)
    domain_counts[domain] = domain_counts.get(domain, 0) + 1

# Parse cached arXiv XML
ns = {'a':'http://www.w3.org/2005/Atom'}
root = ET.parse('/tmp/arxiv.xml').getroot()
for entry in root.findall('a:entry', ns):
    raw = entry.findtext('a:id','')
    aid = raw.split('/abs/')[-1].split('v')[0]
    link = 'https://arxiv.org/abs/' + re.sub(r'[^0-9a-zA-Z\.\-]','',aid)
    pub = entry.findtext('a:published','')
    try: dt = datetime.fromisoformat(pub.replace('Z','+00:00'))
    except: continue
    if dt < cutoff: continue
    title = re.sub(r'\s+',' ', (entry.findtext('a:title','') or '').strip())
    summary = re.sub(r'\s+',' ', (entry.findtext('a:summary','') or '').strip())[:320]
    authors = ', '.join((a.findtext('a:name','') or '').strip() for a in entry.findall('a:author', ns))
    txt = (title + ' ' + summary).lower()
    if not any(k in txt for k in ['agent','mcp','tool','prompt','context','inference','evaluation','benchmark','rag','coding','llm','model','reasoning','memory','orchestrat','harness','planner','gui','workflow']):
        continue
    if len(summary.split()) < 10 and 'agent' not in txt:
        continue
    desc = (authors + ' — ' + summary) if authors else summary
    add(title, link, desc, dt.strftime('%Y-%m-%dT%H:%M:%SZ'), 'arxiv.org')

# Add manually vetted candidate URLs discovered from broader search surface,
# avoiding URLs already present in the existing feed.
CANDIDATES = [
  ('MCP Office Hours: Protocol Design, Servers, and OAuth Adoption — June 2026 Update',
   'https://modelcontextprotocol.io/docs/blog/2026-06-25-office-hours',
   'Community roundup from MCP office hours covering growing OAuth adoption across MCP servers, new transport patterns, and progress toward a 1.1 transport compatibility target.',
   '2026-06-25T18:00:00Z', 'modelcontextprotocol.io'),
  ('Vibe Coding to Agentic Engineering with Claude Code',
   'https://www.apimatic.io/blog/agentic-engineering-claude-code',
   'A repeatable three-phase Claude Code workflow: structured prompt, plan mode, and review to get reliable code from your coding agent every session.',
   '2026-06-25T09:21:31Z', 'apimatic.io'),
  ('Your App Should Ship an MCP Server',
   'https://justin.poehnelt.com/posts/ship-mcp-server-native-app/',
   'Author embedded an MCP server inside a native Rust prose editor; it became the most impactful architectural decision for how the product is built, not just for users.',
   '2026-06-25T09:21:31Z', 'justin.poehnelt.com'),
  ('Agent-scan: Security Scanner for AI Agents, MCP Servers, and Agent Skills',
   'https://github.com/snyk/agent-scan',
   "Snyk's open-source security scanner for AI agents, MCP servers, and agent skills, scanning for vulnerable tool calls, unsafe permissions, and supply-chain risks in agent workflows.",
   '2026-06-24T09:03:20Z', 'github.com'),
  ('dev-machine-guard: Scan Your Dev Machine for AI Agents and MCP Servers',
   'https://github.com/step-security/dev-machine-guard',
   'Lightweight local scanner that inventories AI agents, MCP servers, IDE extensions, and suspicious packages on a developer machine.',
   '2026-06-24T06:43:37Z', 'github.com'),
  ('AgentRecall-MCP: Correction-First Persistent Memory for AI Agents',
   'https://github.com/Goldentrii/AgentRecall-MCP',
   'Open-source MCP server + SDK + CLI that gives coding agents correction-first persistent memory across sessions with local-first storage.',
   '2026-06-23T21:20:07Z', 'github.com'),
  ('PMB: Local-first persistent memory for AI coding agents over MCP',
   'https://github.com/oleksiijko/pmb',
   'Open-source MCP-based memory layer that gives Claude Code, Cursor, and Codex a local SQLite-backed memory for decisions, lessons, and facts — offline and multilingual.',
   '2026-06-22T09:09:12Z', 'github.com'),
  ('Ponytrail: A local audit trail for AI coding-agent edits',
   'https://github.com/0xroylee/ponytrail',
   'Lightweight audit trail that records and surfaces every edit an AI coding agent makes, giving developers transparent visibility before changes reach version control.',
   '2026-06-22T14:54:00Z', 'github.com'),
  ('Autonomous Long-Running Coding Agents',
   'https://academy.dair.ai/blog/autonomous-long-running-coding-agents',
   'Deep dive into loop engineering for autonomous coding agents, covering goals, evaluators, verifiers, and artifact-driven workflows for continuous autonomous work.',
   '2026-06-21T00:00:00Z', 'academy.dair.ai'),
  ('Prompt Engineering Is Dying: Loop Engineering Is Next',
   'https://kingy.ai/ai/prompt-engineering-is-dying-loop-engineering-is-next/',
   'Argues loop engineering is the higher-leverage discipline behind reliable AI agent workflows, with practical patterns across Claude Code, Codex, and Cursor.',
   '2026-06-21T00:00:00Z', 'kingy.ai'),
  ('The 7 Types of Agent Memory: A Technical Guide for AI Engineers',
   'https://www.marktechpost.com/2026/06/21/the-7-types-of-agent-memory-a-technical-guide-for-ai-engineers/',
   'Covers working, semantic, episodic, procedural, retrieval, parametric, and prospective memory for AI agents, with Python implementation examples.',
   '2026-06-21T00:00:00Z', 'marktechpost.com'),
]

for c in CANDIDATES:
    add(*c)

merged = data + items
merged = sorted(merged, key=lambda x: x.get('published_at', ''), reverse=True)

with FEED.open('w', encoding='utf-8') as f:
    json.dump(merged, f, indent=2)
    f.write('\n')

print(f'added={len(items)} total={len(merged)} duplicates_skipped={sum(1 for c in CANDIDATES if c[1] in existing_urls)}')
