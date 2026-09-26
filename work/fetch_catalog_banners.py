"""Download exact-match event banner files from the public Arknights Fandom catalog."""

import json
import ssl
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = {item['title'] for item in json.loads((ROOT / 'work' / 'banner-catalog.json').read_text(encoding='utf-8'))}
OUT = ROOT / 'assets' / 'banners'
SOURCES = ROOT / 'work' / 'banner_sources.json'

TARGETS = {
    'grani': "EN Grani and the Knights' Treasure banner.png",
    'main-05': 'EN Episode 5 Necessary Solutions banner.png',
    'operational': 'EN Operational Intelligence banner.png',
    'main-06': 'EN Episode 6 Partial Necrosis banner.png',
    'ancient-forge': 'CN Ancient Forge banner.png',
    'afternoon': 'CN Stories of Afternoon banner.png',
    'ursas-children': 'EN Children of Ursus banner.png',
    'wolumonde': 'EN Twilight of Wolumonde banner.png',
    'main-07': 'EN Episode 7 The Birth of Tragedy banner.png',
    'rewinding': 'EN Rewinding Breeze banner.png',
    'maria': 'EN Maria Nearl event banner.png',
    'main-08': 'EN Episode 8 Roaring Flare banner.png',
    'mansfield': 'EN Mansfield Break banner.png',
    'beyond': 'EN Beyond Here banner.png',
    'who-is-real': 'EN Who is Real banner.png',
    'originium-dust': 'EN Operation Originium Dust banner.png',
    'walk-dust': 'EN A Walk in the Dust banner.png',
    'preluding': 'EN Preluding Lights banner.png',
    'dossoles': 'EN Dossoles Holiday banner.png',
    'vigilo': 'EN Vigilo banner.png',
    'main-09': 'EN Episode 9 Stormwatch banner.png',
    'pinus': 'EN Pinus Sylvestris event banner.png',
    'invitation': 'EN Invitation to Wine banner.png',
    'spark': 'EN A Light Spark in Darkness banner.png',
    'guide-ahead': 'CN Guiding Ahead banner.png',
    'main-10': 'EN Episode 10 Shatterpoint banner.png',
    'lingering': 'EN Lingering Echoes banner.png',
    'ideal-city': 'EN Ideal City banner.png',
    'unfinished': 'EN To Be Continued banner.png',
    'dorothy': "EN Dorothy's Vision banner.png",
    'to-be-continued': 'EN An Obscure Wanderer banner.png',
    'long-time': "EN It's Been A While banner.png",
    'main-11': 'EN Episode 11 Return to Mist banner.png',
    'firelight': 'CN What the Firelight Casts banner.png',
    'where-vernal': 'EN Where Vernal Winds Will Never Blow banner.png',
    'springtime': 'EN A Death in Chunfen banner.png',
    'flurry': 'EN A Flurry to the Flame banner.png',
    'main-12': 'CN Episode 12 All Quiet Under the Thunder banner.png',
    'hortus': 'CN Hortus de Escapismo banner.png',
    'so-long-adele': 'CN So Long, Adele banner.png',
    'come-catastrophes': 'CN Come Catastrophes or Wakes of Vultures banner.png',
}

for event_id, filename in TARGETS.items():
    if 'File:' + filename not in CATALOG:
        raise ValueError(f'File not in public event banner catalog: {event_id} -> {filename}')

def fetch_json(titles):
    url = 'https://arknights.fandom.com/api.php?' + urllib.parse.urlencode({
        'action': 'query', 'prop': 'imageinfo', 'iiprop': 'url', 'format': 'json',
        'titles': '|'.join('File:' + title for title in titles),
    })
    request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(request, timeout=25) as response:
        return json.load(response)

sources = json.loads(SOURCES.read_text(encoding='utf-8')) if SOURCES.exists() else {}
items = list(TARGETS.items())
for offset in range(0, len(items), 12):
    chunk = items[offset:offset + 12]
    pages = fetch_json([filename for _, filename in chunk])['query']['pages'].values()
    by_title = {page['title'].replace('_', ' '): page for page in pages}
    for event_id, filename in chunk:
        title = ('File:' + filename).replace('_', ' ')
        page = by_title.get(title)
        if not page or 'imageinfo' not in page:
            print(event_id, 'missing file page')
            continue
        url = page['imageinfo'][0]['url']
        target = OUT / f'{event_id}.png'
        if target.exists():
            sources[event_id] = url
            print(event_id, 'already present')
            continue
        original = url + ('&' if '?' in url else '?') + 'format=original'
        request = urllib.request.Request(original, headers={
            'User-Agent': 'Mozilla/5.0', 'Referer': 'https://arknights.fandom.com/',
        })
        try:
            with urllib.request.urlopen(request, context=ssl._create_unverified_context(), timeout=30) as response:
                content = response.read()
            if not content.startswith(b'\x89PNG\r\n\x1a\n'):
                raise ValueError('not a PNG')
            width = int.from_bytes(content[16:20], 'big')
            height = int.from_bytes(content[20:24], 'big')
            if width < 700 or height < 200:
                raise ValueError(f'unexpected size {width}x{height}')
            target.write_bytes(content)
            sources[event_id] = url
            print(event_id, f'{width}x{height}', len(content))
        except Exception as exc:
            print(event_id, 'FAILED', exc)
    SOURCES.write_text(json.dumps(sources, ensure_ascii=False, indent=2), encoding='utf-8')

print('downloaded', len([id for id in TARGETS if (OUT / f'{id}.png').exists()]), '/', len(TARGETS))
