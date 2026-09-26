"""Restore the original horizontal Babel banner recorded in data-base.json."""
import json
import urllib.request
from pathlib import Path

root = Path(__file__).resolve().parents[1]
base = json.loads((root / 'work' / 'data-base.json').read_text(encoding='utf-8'))
url = base['art']['babel']
request = urllib.request.Request(url, headers={
    'User-Agent': 'StoryGraphic/1.0 (local fan timeline)',
    'Referer': 'https://arknights.wiki.gg/',
})
with urllib.request.urlopen(request, timeout=30) as response:
    content = response.read()
if not content.startswith(b'\x89PNG\r\n\x1a\n'):
    raise ValueError('Original Babel banner is not a PNG')
width = int.from_bytes(content[16:20], 'big')
height = int.from_bytes(content[20:24], 'big')
if width < 100 or height < 100:
    raise ValueError(f'Unexpected original Babel banner size: {width}x{height}')
target = root / 'assets' / 'banners' / 'babel.png'
target.write_bytes(content)
print(target.name, width, height, len(content), url)
