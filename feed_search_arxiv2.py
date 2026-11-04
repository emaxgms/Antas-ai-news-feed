from datetime import datetime, timedelta, timezone
import urllib.request, xml.etree.ElementTree as ET, re
cutoff = datetime.now(timezone.utc) - timedelta(days=1)
ns = {'a': 'http://www.w3.org/2005/Atom'}
FEEDS = [
    'https://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=15',
    'https://export.arxiv.org/api/query?search_query=cat:cs.CL&sortBy=submittedDate&sortOrder=descending&max_results=10',
    'https://export.arxiv.org/api/query?search_query=all:agent+framework+or+MCP+server&sortBy=submittedDate&sortOrder=descending&max_results=10',
    'https://export.arxiv.org/api/query?search_query=all:tool+use+or+function+calling&sortBy=submittedDate&sortOrder=descending&max_results=10',
    'https://export.arxiv.org/api/query?search_query=all:evaluation+harness+LLM&sortBy=submittedDate&sortOrder=descending&max_results=10',
    'https://export.arxiv.org/api/query?search_query=all:context+engineering+or+prompt+engineering&sortBy=submittedDate&sortOrder=descending&max_results=10',
    'https://export.arxiv.org/api/query?search_query=all:inference+optimization+or+serving&sortBy=submittedDate&sortOrder=descending&max_results=10',
]
seen=set()
rows=[]
for url in FEEDS:
    try:
        data=urllib.request.urlopen(url,timeout=25).read().decode('utf-8','ignore')
    except Exception as e:
        print('ERR',url,e); continue
    root=ET.fromstring(data)
    for entry in root.findall('a:entry',ns):
        def t(x):
            el=entry.find(x,ns)
            return el.text.strip() if el is not None and el.text else ''
        raw=t('a:id'); aid=raw.split('/abs/')[-1].split('v')[0]
        link='https://arxiv.org/abs/'+re.sub(r'[^0-9a-zA-Z\.\-]','',aid)
        if link in seen: continue
        pub=t('a:published')
        try: dt=datetime.fromisoformat(pub.replace('Z','+00:00'))
        except: continue
        if dt < cutoff: continue
        title=re.sub(r'\s+',' ',t('a:title').strip())
        summary=re.sub(r'\s+',' ',t('a:summary').strip())[:260]
        if not any(k in (title+' '+summary).lower() for k in ['agent','mcp','tool','prompt','context','inference','evaluation','benchmark','rag','coding','llm','model']): continue
        if len(summary.split()) < 8: continue
        rows.append(f'{link}|||{title}|||{dt.strftime("%Y-%m-%dT%H:%M:%SZ")}|||{summary}')
        seen.add(link)
print('ARXIV_FOUND')
for r in rows: print(r)
