"""Find character pages linked from the saved story synopses."""
import json
import re
import time
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
synopsis_links = defaultdict(list)
for path in sorted((ROOT / 'synopses').glob('*.txt')):
    text = path.read_text(encoding='utf-8')
    seen = set()
    for title in re.findall(r'\[\[([^|\]]+)(?:\|[^\]]+)?\]\]', text):
        title = title.split('#', 1)[0].strip()
        if not title or ':' in title or title in seen:
            continue
        synopsis_links[path.stem].append(title)
        seen.add(title)

all_titles = sorted({title for titles in synopsis_links.values() for title in titles})
catalog = {}
agent = 'StoryGraphic/1.0 (personal story research)'
for offset in range(0, len(all_titles), 25):
    batch = all_titles[offset:offset + 25]
    params = {'action': 'query', 'titles': '|'.join(batch), 'prop': 'categories',
              'cllimit': 'max', 'redirects': '1', 'format': 'json', 'formatversion': '2'}
    categories = defaultdict(set)
    redirects = {}
    for attempt in range(4):
        try:
            while True:
                url = 'https://arknights.wiki.gg/api.php?' + urllib.parse.urlencode(params)
                request = urllib.request.Request(url, headers={'User-Agent': agent})
                with urllib.request.urlopen(request, timeout=35) as response:
                    result = json.load(response)
                query = result.get('query', {})
                redirects.update({item['from']: item['to'] for item in query.get('normalized', [])})
                redirects.update({item['from']: item['to'] for item in query.get('redirects', [])})
                for page in query.get('pages', []):
                    categories[page['title']].update(item['title'] for item in page.get('categories', []))
                if 'continue' not in result:
                    break
                params.update(result['continue'])
            break
        except (OSError, ValueError) as exc:
            if attempt == 3:
                raise RuntimeError(f'Failed at batch {offset}: {exc}') from exc
            time.sleep(2 ** attempt)
    for title in batch:
        target = title
        while target in redirects:
            target = redirects[target]
        category_set = categories.get(target, set())
        if 'Category:Operator' in category_set or 'Category:NPCs' in category_set:
            catalog[title] = {
                'page': target,
                'kind': 'operator' if 'Category:Operator' in category_set else 'nonoperator',
            }
    if offset % 250 == 0:
        print(f'Checked {min(offset + 25, len(all_titles))}/{len(all_titles)} links; characters {len(catalog)}', flush=True)
    time.sleep(.15)

event_characters = {
    event_id: list(dict.fromkeys(catalog[title]['page'] for title in titles if title in catalog))
    for event_id, titles in synopsis_links.items()
}
out = {'characters': catalog, 'events': event_characters}
(ROOT / 'wiki_character_catalog.json').write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'Saved {len(catalog)} character links in {len(event_characters)} synopsis pages')
