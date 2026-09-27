"""Download wiki character icons for newly sourced cast members."""
import concurrent.futures
import json
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
urls = json.loads((ROOT / 'work' / 'story_portrait_candidates.json').read_text(encoding='utf-8'))
out = ROOT / 'assets' / 'portraits'
out.mkdir(exist_ok=True)
agent = 'StoryGraphic/1.0 (personal story research)'

def fetch(item):
    person_id, url = item
    path = out / f'{person_id}.png'
    if path.exists() and path.read_bytes().startswith(b'\x89PNG\r\n\x1a\n'):
        return person_id, url, None
    for attempt in range(4):
        try:
            request = urllib.request.Request(url, headers={'User-Agent': agent})
            with urllib.request.urlopen(request, timeout=45) as response:
                content = response.read()
            if not content.startswith(b'\x89PNG\r\n\x1a\n'):
                raise ValueError('Not a PNG image')
            path.write_bytes(content)
            return person_id, url, None
        except (OSError, ValueError) as error:
            if attempt == 3:
                return person_id, url, str(error)
            time.sleep(2 ** attempt)

sources_path = ROOT / 'work' / 'portrait_sources.json'
sources = json.loads(sources_path.read_text(encoding='utf-8'))
used = {person['id'] for person in json.loads((ROOT / 'work' / 'story_people_sourced.json').read_text(encoding='utf-8'))}
items = [(person_id, url) for person_id, url in urls.items() if person_id in used]
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    results = list(pool.map(fetch, items))
for person_id, url, error in results:
    if not error:
        sources[person_id] = url
    else:
        print(person_id, error)
sources_path.write_text(json.dumps(sources, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'Downloaded {sum(error is None for _, _, error in results)}/{len(results)} sourced portraits')
