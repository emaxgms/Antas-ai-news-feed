import urllib.request, json
from datetime import datetime, timedelta
import re

queries = [
    'agent+framework+in:name,description OR MCP+server+in:name,description OR tool+calling+in:name,description OR context+engineering+in:name,description OR llm+inference+optimization+in:name,description',
    'coding+agent OR AI+agent+orchestration OR evaluation+harness+LLM OR RAG+system+OR prompt+engineering+in:name,description',
]
entries = []
cutoff = datetime.utcnow() - timedelta(days=1)
for q in queries:
    url = f'https://api.github.com/search/repositories?q={q}&sort=stars&order=desc&per_page=30'
    req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0','Accept':'application/vnd.github+json'})
    try:
        data = json.loads(urllib.request.urlopen(req, timeout=30).read().decode())
    except Exception as e:
        print('ERR', e)
        continue
    for item in data.get('items', []):
        updated = item.get('updated_at') or ''
        if not updated:
            continue
        try:
            dt = datetime.fromisoformat(updated.replace('Z', '+00:00')).astimezone(timedelta(0)).replace(tzinfo=None)
        except Exception:
            continue
        if dt < cutoff:
            continue
        name = item.get('full_name') or ''
        desc = item.get('description') or ''
        html = item.get('html_url') or ''
        stars = item.get('stargazers_count') or 0
        if stars < 20:
            continue
        entries.append({
            'id': 'gh-' + re.sub(r'[^a-zA-Z0-9-]', '', name),
            'title': f'{name} — {desc}',
            'url': html,
            'published_at': dt.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'description': f'GitHub trending signal: {stars} stars. {desc}',
        })

entries = sorted(entries, key=lambda x: x['published_at'], reverse=True)
print('github_count', len(entries))
for e in entries[:40]:
    print(e['url'])
    print(e['title'])
    print(e['published_at'])
    print(e['description'][:220])
    print('---')
