import os, json, re, urllib.request

TOKEN  = os.environ['ADS_TOKEN']
# EDIT: your author query
QUERY  = 'author:"Fritzewski, Dario"'
FIELDS = 'title,author,year,bibcode,pub,volume,page,doi,property,identifier'
ROWS   = 50

url = (
    'https://api.adsabs.harvard.edu/v1/search/query'
    f'?q={urllib.parse.quote(QUERY)}'
    f'&fl={urllib.parse.quote(FIELDS)}'
    f'&sort=date+desc'
    f'&rows={ROWS}'
)

import urllib.parse
req = urllib.request.Request(url, headers={'Authorization': f'Bearer {TOKEN}'})
with urllib.request.urlopen(req) as r:
    docs = json.loads(r.read())['response']['docs']

# Inject into index.html between the two marker comments
pub_json = json.dumps(docs, ensure_ascii=False)
with open('index.html', 'r') as f:
    html = f.read()

html = re.sub(
    r'<!-- PUB_DATA_START -->.*?<!-- PUB_DATA_END -->',
    f'<!-- PUB_DATA_START --><script>window.__PUB_DATA__={pub_json};</script><!-- PUB_DATA_END -->',
    html, flags=re.DOTALL
)

with open('index.html', 'w') as f:
    f.write(html)

print(f"Wrote {len(docs)} publications to index.html")