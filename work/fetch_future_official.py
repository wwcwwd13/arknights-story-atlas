"""Download candidate lead art from official CN event announcements."""
import html
import json
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NEWS = {'main-17': '3046', 'foam-thunder': '0701', 'jungle-knot': '9686',
        'lime': '8571', 'moon-water': '9681'}
sources = {}
for event_id, news_id in NEWS.items():
    page_url = f'https://ak.hypergryph.com/news/{news_id}'
    try:
        request = urllib.request.Request(page_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(request, timeout=25) as response:
            page = html.unescape(response.read().decode('utf-8', 'replace')).replace('\\/', '/')
        urls = list(dict.fromkeys(re.findall(r'https?://[^\s"<>]+?\.(?:jpg|png|webp)', page)))
        if not urls:
            raise ValueError('no official images')
        url = urls[0]
        with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=25) as response:
            content = response.read()
        if len(content) < 50000 or not content.startswith((b'\xff\xd8\xff', b'\x89PNG')):
            raise ValueError('invalid image')
        ext = 'png' if content.startswith(b'\x89PNG') else 'jpg'
        (ROOT / 'work' / 'candidates' / f'{event_id}-official.{ext}').write_bytes(content)
        sources[event_id] = url
        print(event_id, len(content), url, flush=True)
    except Exception as exc:
        print(event_id, type(exc).__name__, str(exc), flush=True)
(ROOT / 'work' / 'future_official_candidates.json').write_text(json.dumps(sources, ensure_ascii=False, indent=2), encoding='utf-8')
