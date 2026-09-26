"""Fetch exact event artwork from each Chinese event's public Bwiki page."""
import json
import re
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets' / 'banners'
SOURCES = ROOT / 'work' / 'remaining_banner_sources.json'
DATA = json.loads((ROOT / 'data.js').read_text(encoding='utf-8').split('window.STORY_DATA = ', 1)[1].rsplit(';', 1)[0])
MISSING = [event for event in DATA['events'] if event['id'] not in DATA['art'] and event['id'] != 'main-00-04']


class EventBanner(HTMLParser):
    def __init__(self):
        super().__init__()
        self.candidates = []

    def handle_starttag(self, tag, attrs):
        if tag != 'img':
            return
        item = dict(attrs)
        width = int(item.get('data-file-width') or 0)
        height = int(item.get('data-file-height') or 0)
        if width >= 1200 and 2.7 < width / max(height, 1) < 3.5:
            src = item.get('src', '')
            if '/images/arknights/thumb/' in src:
                original = src.replace('/images/arknights/thumb/', '/images/arknights/').rsplit('/', 1)[0]
                self.candidates.append((item.get('alt', ''), original, width, height))


def fetch(event):
    event_id = event['id']
    title = event['original']
    url = 'https://wiki.biligame.com/arknights/' + urllib.parse.quote(title)
    request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(request, timeout=35) as response:
            page = response.read().decode('utf-8', 'replace')
        parser = EventBanner()
        parser.feed(page)
        # The first 1560x500 image on each event page is its event artwork.
        matching = [candidate for candidate in parser.candidates if candidate[2:4] == (1560, 500)]
        if not matching:
            return event_id, None, f'no 1560x500 art ({len(parser.candidates)} candidates)'
        alt, image_url, width, height = matching[0]
        if not alt.startswith('CN ') and not alt.startswith('EN '):
            return event_id, None, f'unexpected art name {alt}'
        image_request = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0', 'Referer': url})
        with urllib.request.urlopen(image_request, timeout=35) as response:
            content = response.read()
        if not content.startswith(b'\xff\xd8\xff') or len(content) < 50000:
            return event_id, None, f'invalid image {alt} ({len(content)} bytes)'
        (OUT / f'{event_id}.jpg').write_bytes(content)
        return event_id, image_url, f'{alt} {width}x{height}, {len(content)} bytes'
    except Exception as exc:
        return event_id, None, f'{type(exc).__name__}: {exc}'


sources = json.loads(SOURCES.read_text(encoding='utf-8')) if SOURCES.exists() else {}
with ThreadPoolExecutor(max_workers=4) as pool:
    futures = [pool.submit(fetch, event) for event in MISSING]
    for future in as_completed(futures):
        event_id, source, message = future.result()
        if source:
            sources[event_id] = source
        print(event_id, 'OK' if source else 'MISSING', message, flush=True)
SOURCES.write_text(json.dumps(sources, ensure_ascii=False, indent=2), encoding='utf-8')
print('event banners recovered', len(sources), '/', len(MISSING))
