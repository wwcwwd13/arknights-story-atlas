"""Promote reviewed official CN candidates and add one shared launch key art."""
import json
import shutil
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets' / 'banners'
CANDIDATES = ROOT / 'work' / 'candidates'
official_sources = json.loads((ROOT / 'work' / 'future_official_candidates.json').read_text(encoding='utf-8'))
sources = {key: official_sources[key] for key in ('foam-thunder', 'jungle-knot', 'moon-water')}
for event_id, extension in [('foam-thunder', 'jpg'), ('jungle-knot', 'png'), ('moon-water', 'jpg')]:
    shutil.copyfile(CANDIDATES / f'{event_id}-official.{extension}', OUT / f'{event_id}.{extension}')

shutil.copyfile(CANDIDATES / 'lime-second.jpg', OUT / 'lime.jpg')
sources['lime'] = 'https://web.hycdn.cn/upload/image/20260724/1e8b24d5d0d9f2423b7429ccdd71d503.jpg'

for event_id, url in {
    'main-17': 'https://patchwiki.biligame.com/images/arknights/3/3a/bc3r8l2pjecplm2041wb6ou8uvbrmlg.jpg',
    'main-00-04': 'https://images.alphacoders.com/107/1070339.jpg',
}.items():
    request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(request, timeout=30) as response:
        content = response.read()
    if not content.startswith(b'\xff\xd8\xff') or len(content) < 50000:
        raise ValueError(f'invalid image: {event_id}')
    (OUT / f'{event_id}.jpg').write_bytes(content)
    sources[event_id] = url
    print(event_id, len(content))

(ROOT / 'work' / 'final_banner_sources.json').write_text(json.dumps(sources, ensure_ascii=False, indent=2), encoding='utf-8')
print('finished', len(sources), 'images')
