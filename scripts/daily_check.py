#!/usr/bin/env python3
"""Daily discovery, NOT automatic release-date verification.
Searches indexed official-domain articles and records candidate links for human review.
No game dates or platforms are changed without an approved edit to games.json.
"""
import datetime as dt
import json
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'
NOW=dt.datetime.now(dt.timezone.utc)
SITES=['nintendo.com','blog.playstation.com','news.xbox.com','square-enix-games.com','capcom-games.com','sega.com']
SEARCHES=['game release date', 'game delayed', 'launch date announced']
UA='AAA-Calendar-Monitor/1.0 (public RSS metadata checker)'

def fetch(query):
    url='https://news.google.com/rss/search?q='+urllib.parse.quote(query)+'&hl=en-US&gl=US&ceid=US:en'
    req=urllib.request.Request(url,headers={'User-Agent':UA})
    with urllib.request.urlopen(req,timeout=20) as resp:
        data=resp.read(2_000_000)
    root=ET.fromstring(data)
    return [(x.findtext('title',''),x.findtext('link',''),x.findtext('pubDate','')) for x in root.findall('./channel/item')]

def tokens(name):
    s=re.sub(r'（[^）]*）|\([^)]*\)',' ',name).lower()
    return [t for t in re.findall(r'[a-z0-9]{3,}|[\u4e00-\u9fff]{2,}',s) if t not in {'the','game','edition','new','remake'}]

def main():
    games=json.loads((DATA/'games.json').read_text(encoding='utf-8'))
    previous=json.loads((DATA/'review_queue.json').read_text(encoding='utf-8'))
    existing={x['url']:x for x in previous.get('items',[]) if x.get('url')}
    names=[(g['name'],tokens(g['name'])) for g in games['events']+games['watch']]
    errors=[];count=0
    for site in SITES:
        for search in SEARCHES:
            try:
                rows=fetch(f'site:{site} {search} when:7d')
                count+=1
                for title,url,published in rows:
                    if not url or not title:continue
                    # Match only reasonably distinctive game names; avoid broad generic hits.
                    matches=[name for name,ts in names if any(len(t)>=5 and t in title.lower() for t in ts)]
                    if not matches:continue
                    if url not in existing:
                        existing[url]={'title':title,'url':url,'published':published,'matched_games':matches[:5], 'source_query_domain':site,'status':'待人工核實','discovered_at':NOW.isoformat(timespec='seconds')}
            except Exception as e:
                errors.append({'source':site,'query':search,'error':str(e)[:250]})
    # Preserve unreviewed queue; bound to prevent indefinite growth.
    queue=sorted(existing.values(),key=lambda x:x.get('discovered_at',''),reverse=True)[:300]
    out={'checked_at':NOW.isoformat(timespec='seconds'),'sources_checked':count,'items':queue,'errors':errors,
         'policy':'候選新聞僅供人工核對，不代表已確認上市日期；本程序不修改 games.json。'}
    (DATA/'review_queue.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'checked={count}, candidates={len(queue)}, errors={len(errors)}')
    if count==0:raise SystemExit('All feeds failed: refusing to report successful check')

if __name__=='__main__':main()
