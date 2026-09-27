"""Cache Korean names and appearance notes for synopsis-linked characters."""
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
catalog = json.loads((ROOT / 'wiki_character_catalog.json').read_text(encoding='utf-8'))
titles = sorted({record['page'] for record in catalog['characters'].values()})
agent = 'StoryGraphic/1.0 (personal story research)'
metadata = {}

def field(text, name):
    match = re.search(r'^\|' + re.escape(name) + r'[ \t]*=[ \t]*(.*?)(?=^\|[A-Za-z][\w ]*[ \t]*=|^}}|\Z)',
                      text, flags=re.M | re.S)
    return match.group(1).strip() if match else ''

for offset in range(0, len(titles), 20):
    batch = titles[offset:offset + 20]
    params = {'action': 'query', 'titles': '|'.join(batch), 'prop': 'revisions',
              'rvslots': 'main', 'rvprop': 'content', 'redirects': '1',
              'format': 'json', 'formatversion': '2'}
    for attempt in range(4):
        try:
            url = 'https://arknights.wiki.gg/api.php?' + urllib.parse.urlencode(params)
            request = urllib.request.Request(url, headers={'User-Agent': agent})
            with urllib.request.urlopen(request, timeout=60) as response:
                result = json.load(response)
            for page in result['query']['pages']:
                if 'missing' in page or not page.get('revisions'):
                    continue
                text = page['revisions'][0]['slots']['main']['content']
                metadata[page['title']] = {
                    'krname': field(text, 'krname').split('\n', 1)[0].strip(),
                    'appearance': field(text, 'appearance')[:1800],
                }
            break
        except (OSError, ValueError) as exc:
            if attempt == 3:
                raise RuntimeError(f'Failed at batch {offset}: {exc}') from exc
            time.sleep(2 ** attempt)
    if offset % 200 == 0:
        print(f'Fetched {min(offset + 20, len(titles))}/{len(titles)} character pages', flush=True)
    time.sleep(.15)

(ROOT / 'wiki_character_metadata.json').write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'Saved {len(metadata)} character page records')
