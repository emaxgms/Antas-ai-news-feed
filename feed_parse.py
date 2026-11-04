import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
import re, json
root = ET.parse('/tmp/arxiv.xml').getroot()
ns = {'a':'http://www.w3.org/2005/Atom','arxiv':'http://arxiv.org/schemas/atom'}
cutoff = datetime.now(timezone.utc) - timedelta(days=72) # extend to 72h to get results if today missing
found=[]
for entry in root.findall('a:entry',ns):
    title = (entry.findtext('a:title','') or '').strip().replace('\n',' ')
    raw = entry.findtext('a:id','')
    aid = raw.split('/abs/')[-1].split('v')[0]
    link = 'https://arxiv.org/abs/'+re.sub(r'[^0-9a-zA-Z\.\-]','',aid)
    pub = entry.findtext('a:published','')
    try: dt=datetime.fromisoformat(pub.replace('Z','+00:00'))
    except: continue
    if dt < cutoff: continue
    authors = ', '.join((a.findtext('a:name','') or '').strip() for a in entry.findall('a:author',ns))
    summary = re.sub(r'\s+',' ', (entry.findtext('a:summary','') or '').strip())[:300]
    cats = ', '.join(c.get('term','') for c in entry.findall('a:category',ns))
    txt = (title+' '+summary).lower()
    if not any(k in txt for k in ['agent','mcp','tool','prompt','context','inference','evaluation','benchmark','rag','coding','llm','model','reasoning','memory','orchestrat','harness']): continue
    found.append({
        'url': link,
        'title': title,
        'published_at': dt.strftime('%Y-%m-%dT%H:%M:%SZ'),
        'description': (authors+' — '+summary) if authors else summary,
        'category': cats,
    })
print('arxiv_count', len(found))
for x in found[:30]: print(x['url'], '|||', x['title'], '|||', x['published_at'], '|||', x['description'][:240], '|||', x['category'])
