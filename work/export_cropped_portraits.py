"""Export the site's explicitly cropped portraits as reviewable square PNGs."""

import json
import math
import re
import hashlib
from html import escape
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'review' / 'cropped-thumbnails'
SIZE = 112  # The hover preview's portrait frame in app.js.
SCALE = 2   # Save at 224 px so the crop is easier to inspect.
BACKGROUND = (48, 64, 68, 255)  # .portrait-frame in style.css.


def js_round(value):
    return math.floor(value + 0.5)


def export(person):
    crop = person['portraitCrop']
    source = ROOT / person['portrait']
    with Image.open(source) as image:
        image = image.convert('RGBA')
        if image.size != (crop['width'], crop['height']):
            raise ValueError(f"Portrait dimensions changed: {person['id']}")
        scale = max(SIZE / crop['width'], SIZE / crop['height']) * crop['zoom']
        width = js_round(crop['width'] * scale)
        height = js_round(crop['height'] * scale)
        left = js_round(SIZE / 2 - width * crop['x'])
        top = js_round(SIZE / 2 - height * crop['y'])
        rendered = image.resize((width * SCALE, height * SCALE), Image.Resampling.LANCZOS)
        square = Image.new('RGBA', (SIZE * SCALE, SIZE * SCALE), BACKGROUND)
        square.alpha_composite(rendered, (left * SCALE, top * SCALE))
        filename = re.sub(r'[<>:"/\\|?*]', '_', person['name']).strip().rstrip('.')
        filename += f"__{person['id']}.png"
        square.convert('RGB').save(OUT / filename, optimize=True)
    return filename


def main():
    raw = (ROOT / 'data.js').read_text(encoding='utf-8')
    data = json.loads(raw.split('window.STORY_DATA = ', 1)[1].rsplit(';', 1)[0])
    people = sorted((person for person in data['people'] if person.get('portraitCrop')),
                    key=lambda person: (person['name'], person['id']))
    OUT.mkdir(parents=True, exist_ok=True)
    cards = []
    for person in people:
        filename = export(person)
        version = hashlib.sha256(json.dumps(person['portraitCrop'], sort_keys=True).encode()).hexdigest()[:8]
        original = '../../' + person['portrait']
        cards.append(f'<div class="card"><a class="thumb" href="{escape(filename, quote=True)}">'
                     f'<img src="{escape(filename, quote=True)}?v={version}" alt="{escape(person["name"])}" '
                     f'width="112" height="112">'
                     f'<strong>{escape(person["name"])}</strong>'
                     f'<small>{escape(person["id"])}</small></a>'
                     f'<a class="original" href="{escape(original, quote=True)}">원본 보기</a></div>')
    html = '''<!doctype html><html lang="ko"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>얼굴 크롭 검토</title>
<style>
body{margin:0;padding:24px;background:#152125;color:#eee9da;font:15px system-ui,sans-serif}
h1{margin:0 0 6px;font-size:24px}p{margin:0 0 22px;color:#aebeb9}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(148px,1fr));gap:14px}
.card{display:flex;flex-direction:column;align-items:center;gap:8px;padding:14px 8px;
background:#213137;border:1px solid #526863;color:inherit;text-align:center}
.card:hover{border-color:#d4bf93;background:#2a3b40}
.thumb{display:flex;flex-direction:column;align-items:center;gap:5px;color:inherit;text-decoration:none}
.original{color:#d4bf93;font-size:12px}
img{width:112px;height:112px;object-fit:cover;border:1px solid #71847c}
strong{font-size:14px}small{max-width:100%%;color:#aebeb9;font-size:11px;overflow-wrap:anywhere}
</style><h1>얼굴 크롭 검토</h1><p>웹페이지의 마우스 오버 썸네일과 같은 구도입니다. 이미지를 누르면 2배 크기로 볼 수 있습니다. 총 %d개.</p>
<div class="grid">%s</div></html>''' % (len(cards), ''.join(cards))
    (OUT / 'index.html').write_text(html, encoding='utf-8')
    print(f'Exported {len(cards)} cropped portraits to {OUT}')


if __name__ == '__main__':
    main()
