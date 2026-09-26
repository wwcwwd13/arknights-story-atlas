"""Retrieve event artwork from Terra Log for still-unfilled events."""
import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'data.js').read_text(encoding='utf-8').split('window.STORY_DATA = ', 1)[1].rsplit(';', 1)[0])
CN = json.loads((ROOT / 'work' / 'activity_zh_CN.json').read_text(encoding='utf-8'))['basicInfo']
ACTIVITY = {item['name']: item['id'] for item in CN.values()}
SOURCES = ROOT / 'work' / 'terra_log_banner_sources.json'
sources = json.loads(SOURCES.read_text(encoding='utf-8')) if SOURCES.exists() else {}

for event in DATA['events']:
    event_id = event['id']
    if event_id in DATA['art'] or (ROOT / 'assets' / 'banners' / f'{event_id}.jpg').exists():
        continue
    activity = ACTIVITY.get(event['original'])
    if not activity:
        continue
    url = f'https://terra-log.org/images/chapters/{activity}.webp'
    try:
        request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(request, timeout=20) as response:
            content = response.read()
        if not content.startswith(b'RIFF') or content[8:12] != b'WEBP' or len(content) < 50000:
            raise ValueError('not a substantive WebP file')
        (ROOT / 'assets' / 'banners' / f'{event_id}.webp').write_bytes(content)
        sources[event_id] = url
        print(event_id, 'OK', activity, len(content), flush=True)
    except Exception as exc:
        print(event_id, 'MISSING', activity, type(exc).__name__, str(exc), flush=True)
SOURCES.write_text(json.dumps(sources, ensure_ascii=False, indent=2), encoding='utf-8')
