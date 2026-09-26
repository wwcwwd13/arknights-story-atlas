"""Fetch verified wiki character icons for the expanded story cast."""
import concurrent.futures
import json
import urllib.parse
import urllib.request
from pathlib import Path

root = Path(__file__).resolve().parents[1]
seed = json.loads((root / 'work' / 'story_people_seed.json').read_text(encoding='utf-8'))
english = json.loads((root / 'work' / 'character_table_en_US.json').read_text(encoding='utf-8'))
korean = json.loads((root / 'work' / 'character_table_ko_KR.json').read_text(encoding='utf-8'))
name_map = {value['name'].casefold(): (key, korean[key]['name']) for key, value in english.items()
            if key in korean and value.get('name')}
sources_path = root / 'work' / 'portrait_sources.json'
sources = json.loads(sources_path.read_text(encoding='utf-8'))

def fetch(person):
    local = root / 'assets' / 'portraits' / f"{person['id']}.png"
    if local.is_file() and person['id'] in sources:
        return person, sources[person['id']], None
    title = f"File:{person['wiki']} icon.png"
    params = urllib.parse.urlencode({'action': 'query', 'titles': title, 'prop': 'imageinfo',
                                     'iiprop': 'url', 'format': 'json'})
    request = urllib.request.Request('https://arknights.wiki.gg/api.php?' + params,
                                     headers={'User-Agent': 'StoryGraphic/1.0 (local fan timeline)'})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            data = json.load(response)
        page = next(iter(data['query']['pages'].values()))
        if 'imageinfo' not in page:
            return person, None, 'missing icon page'
        url = page['imageinfo'][0]['url']
        with urllib.request.urlopen(urllib.request.Request(url, headers={
                'User-Agent': 'StoryGraphic/1.0 (local fan timeline)'}), timeout=30) as response:
            content = response.read()
        if not content.startswith(b'\x89PNG\r\n\x1a\n'):
            return person, None, 'not PNG'
        (root / 'assets' / 'portraits' / f"{person['id']}.png").write_bytes(content)
        return person, url, None
    except Exception as error:
        return person, None, str(error)

with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
    results = list(pool.map(fetch, seed))

people = []
for person, url, error in results:
    match = name_map.get(person['wiki'].casefold())
    name = person.get('name') or (match[1] if match else person['wiki'])
    kind = person.get('kind') or ('operator' if match else 'nonoperator')
    people.append({'id': person['id'], 'name': name, 'kind': kind, 'wikiTitle': person['wiki']})
    if url:
        sources[person['id']] = url
    print(person['id'], 'OK' if url else error)

(root / 'work' / 'story_people.json').write_text(json.dumps(people, ensure_ascii=False, indent=2), encoding='utf-8')
sources_path.write_text(json.dumps(sources, ensure_ascii=False, indent=2), encoding='utf-8')
print('portraits', sum(bool(url) for _, url, _ in results), '/', len(seed))
