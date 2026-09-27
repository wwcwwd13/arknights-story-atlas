"""Fetch the square character images shown on the PRTS cast page."""
import concurrent.futures
import hashlib
import json
import re
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / 'work' / 'prts_story_characters.wikitext').read_text(encoding='utf-8')
cast = json.loads((ROOT / 'work' / 'story_prts_cast.json').read_text(encoding='utf-8'))
event_headings = {
    'people-us': '人们，我们', 'main-17': '第十七章 相变临界',
    'foam-thunder': '泡影苍霆', 'jungle-knot': '丛林症结',
    'lime': '直到大地变成一颗酸橙', 'moon-water': '月行水上',
    'under-tides': '覆潮之下', 'crossroads': '十字路口', 'dreamtalk': '无忧梦呓',
}
agent = 'StoryGraphic/1.0 (personal story research)'

records = []
for event_id, heading in event_headings.items():
    match = re.search(r'^====' + re.escape(heading) + r'====$', source, re.M)
    if not match:
        raise ValueError(f'Missing PRTS heading: {heading}')
    next_heading = re.search(r'^={2,4}[^=\n].*?={2,4}$', source[match.end() + 1:], re.M)
    section = source[match.end() + 1:match.end() + 1 + next_heading.start() if next_heading else len(source)]
    for person_id, name, cn_name in cast[event_id]:
        rows = re.split(r'\n\|-\s*\n', section)
        row = next((row for row in rows if row.splitlines() and cn_name in row.splitlines()[0].lstrip('|')), None)
        if not row:
            print('Missing PRTS row:', cn_name)
            continue
        template = re.search(r'\{\{剧情角色立绘\|([^}|]+)', row)
        if template:
            records.append((person_id, template.group(1)))

def fetch(record):
    person_id, template = record
    image_name = 'Avg_' + template.split(';', 1)[0].strip().replace(' ', '_') + '.png'
    image_hash = hashlib.md5(image_name.encode('utf-8')).hexdigest()
    url = ('https://media.prts.wiki/' + image_hash[0] + '/' + image_hash[:2] + '/'
           + urllib.parse.quote(image_name, safe='_$-'))
    path = ROOT / 'assets' / 'portraits' / f'prts-{person_id}.png'
    if path.is_file():
        return person_id, url, None
    request = urllib.request.Request(url, headers={'User-Agent': agent})
    try:
        with urllib.request.urlopen(request, timeout=18) as response:
            image = response.read()
    except (OSError, ValueError) as exc:
        return person_id, None, str(exc)
    if not image.startswith(b'\x89PNG\r\n\x1a\n'):
        return person_id, None, 'not PNG'
    path.write_bytes(image)
    return person_id, url, None

with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
    result = list(pool.map(fetch, records))
sources_path = ROOT / 'work' / 'portrait_sources.json'
sources = json.loads(sources_path.read_text(encoding='utf-8'))
for person_id, url, error in result:
    if error:
        print(person_id, error)
    else:
        sources['prts-' + person_id] = url
sources_path.write_text(json.dumps(sources, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'PRTS portraits {sum(url is not None for _, url, _ in result)}/{len(records)} available; {sum(map(len, cast.values()))} cast')
