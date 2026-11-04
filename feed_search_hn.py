import urllib.request, xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import re

entries = []
cutoff = datetime.utcnow() - timedelta(days=1)
# HN newest + relevant keywords
feeds = [
    'https://hnrss.org/newest?count=60',
    'https://hnrss.org/frontpage?count=80',
]
for url in feeds:
    try:
        data = urllib.request.urlopen(url, timeout=25).read().decode('utf-8', 'ignore')
    except Exception as e:
        print('ERR', url, e)
        continue
    root = ET.fromstring(data)
    for item in root.findall('item'):
        title = (item.findtext('title') or '').strip()
        link = (item.findtext('link') or '').strip()
        pub = (item.findtext('pubDate') or '').strip()
        if not title or not link:
            continue
        try:
            dt = datetime.strptime(pub, '%a, %d %b %Y %H:%M:%S %z')
            dt = dt.astimezone(timedelta(0)).replace(tzinfo=None)
        except Exception:
            continue
        if dt < cutoff:
            continue
        txt = (title + ' ' + (item.findtext('description') or '')).lower()
        if not any(k in txt for k in [
            'agent', 'mcp', 'tool-call', 'context', 'prompt', 'inference', 'evaluation', 'benchmark', 'rag', 'function calling', 'coding', 'llm', 'openai', 'anthropic', 'langchain', 'dex', 'ollama', 'local model', 'router', 'observability', 'latency', 'throughput', 'gpu', 'kernel', 'vllm', 'tgi', 'ggml', 'rwkv', 'smollm', 'phi', 'qwen', 'glm', 'deepseek', 'mistral', 'gemma', 'llama', 'transformer', 'attention', 'training', 'fine-tun'
        ]):
            continue
        score_match = re.search(r'\((\d+) points?\)', item.findtext('description') or '')
        score = int(score_match.group(1)) if score_match else 0
        comments_match = re.search(r'\((\d+) comments?\)', item.findtext('description') or '')
        comments = int(comments_match.group(1)) if comments_match else 0
        entries.append({
            'id': 'hn-' + re.sub(r'[^a-zA-Z0-9-]', '', link.rsplit('/',1)[-1])[-12:],
            'title': title,
            'url': link,
            'published_at': dt.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'description': f'HN #{score} pts / {comments} comments',
        })

entries = sorted(entries, key=lambda x: x['published_at'], reverse=True)
print('hn_count', len(entries))
for e in entries[:40]:
    print(e['url'])
    print(e['title'])
    print(e['published_at'])
    print(e['description'])
    print('---')
