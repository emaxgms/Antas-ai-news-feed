import urllib.request, xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import json, re

search_queries = [
    'cat:cs.AI',
    'cat:cs.CL',
    'cat:cs.LG',
    'all:MCP+agent+framework',
    'all:tool+use+agent',
    'all:context+engineering',
    'all:prompt+engineering',
    'all:inference+optimization',
    'all:local+LLM+inference',
    'all:Azure+AI+inference',
    'all:evaluation+harness+LLM',
]

entries = []
seen = set()
cutoff = datetime.now(datetime.UTC) - timedelta(days=1)

ns = {'a': 'http://www.w3.org/2005/Atom'}

def clean(s):
    return re.sub(r'\s+', ' ', s or '').strip()

for q in search_queries:
    url = f'https://export.arxiv.org/api/query?search_query={q}&sortBy=submittedDate&sortOrder=descending&max_results=15'
    try:
        data = urllib.request.urlopen(url, timeout=25).read().decode('utf-8', 'ignore')
    except Exception as e:
        print('ERR', q, e)
        continue
    try:
        root = ET.fromstring(data)
    except Exception:
        continue
    for entry in root.findall('a:entry', ns):
        def text(x):
            el = entry.find(x, ns)
            return el.text.strip() if el is not None and el.text else ''
        raw = text('a:id')
        aid = raw.split('/abs/')[-1]
        if aid.endswith('v1') or aid.endswith('v2') or aid.endswith('v3'):
            canonical = re.sub(r'v\d+$', '', aid)
        else:
            canonical = aid
        link = f'https://arxiv.org/abs/{canonical}'
        if link in seen:
            continue
        published = text('a:published')
        try:
            if published.endswith('Z'):
                published = published[:-1] + '+00:00'
            dt = datetime.fromisoformat(published)
        except Exception:
            continue
        if dt < cutoff:
            continue
        title = clean(text('a:title'))
        summary = clean(text('a:summary'))
        authors = ', '.join(clean(a.find('a:name', ns).text) for a in entry.findall('a:author', ns))
        cats = ', '.join(c.get('term', '') for c in entry.findall('a:category', ns))
        if not any(k in (title+' '+summary).lower() for k in ['agent','mcp','tool','prompt','context','inference','evaluation','benchmark','rag','function','coding','llm','model']) :
            continue
        if len(summary.split()) < 8:
            continue
        entries.append({
            'id': re.sub(r'[^a-zA-Z0-9-]', '', canonical)[:8] + '-' + str(int(dt.timestamp())),
            'title': title,
            'url': link,
            'published_at': dt.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'description': f'{authors} — {summary[:280]}' if authors else summary[:360],
        })
        seen.add(link)

entries = sorted(entries, key=lambda x: x['published_at'], reverse=True)
print('arxiv_count', len(entries))
for e in entries[:40]:
    print(e['url'])
    print(e['title'])
    print(e['published_at'])
    print(e['description'][:220])
    print('---')
