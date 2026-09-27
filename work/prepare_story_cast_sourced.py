"""Build a source-backed cast expansion from saved wiki story synopses."""
import json
import re
import unicodedata
import urllib.parse
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
work = ROOT / 'work'
data = json.loads((ROOT / 'data.js').read_text(encoding='utf-8').split('window.STORY_DATA = ', 1)[1].rsplit(';', 1)[0])
base_people = json.loads((work / 'data-base.json').read_text(encoding='utf-8'))['people']
base_people += json.loads((work / 'story_enrichment.json').read_text(encoding='utf-8'))['people']
base_people += json.loads((work / 'story_people.json').read_text(encoding='utf-8'))
catalog = json.loads((work / 'wiki_character_catalog.json').read_text(encoding='utf-8'))
metadata = json.loads((work / 'wiki_character_metadata.json').read_text(encoding='utf-8'))
kind = {record['page']: record['kind'] for record in catalog['characters'].values()}
by_wiki = {person['wikiTitle'].casefold(): person['id'] for person in base_people if person.get('wikiTitle')}
by_korean = {person['name'].casefold(): person['id'] for person in base_people}
by_id = {person['id'] for person in base_people}
english_table = json.loads((work / 'character_table_en_US.json').read_text(encoding='utf-8'))
korean_table = json.loads((work / 'character_table_ko_KR.json').read_text(encoding='utf-8'))
game_korean = {record['name'].casefold(): korean_table[key]['name']
               for key, record in english_table.items()
               if key in korean_table and record.get('name') and korean_table[key].get('name')}

aliases = {
    'Adele Keller': 'eyjafjalla',
    'Kristen Wright': 'kristen',
    'Vina Victoria': 'siege',
    'Wiš\'adel': 'w',
    'Mitm': 'nymph',
    "Ch'en the Holungday": 'chen',
    "Ch'en the Dawnstreak": 'chen',
    'Nearl the Radiant Knight': 'nearl',
    'Specter the Unchained': 'specter',
    'Skadi the Corrupting Heart': 'skadi',
    'Kroos the Keen Glint': 'kroos',
    'Lava the Purgatory': 'lava',
    'Astgenne the Lightchaser': 'astgenne',
    'Leizi the Thunderbringer': 'leizi',
    'SilverAsh the Reignfrost': 'silverash',
    'Pramanix the Prerita': 'pramanix',
    'Thorns the Lodestar': 'thorns',
    'Executor': 'executor',
    'Reed': 'reed',
}
kr_overrides = {
    '054': '054', 'Black Mark': '블랙 마크', 'Bellingham': '벨링햄',
    'Behnui Enshi-Pah': '베누이 엔시파', 'Ch\'en Chao-ch\'ien': '첸 차오첸',
    'Dijkstra': '데이크스트라', 'Elisabeth': '엘리자베트', 'Gustave': '귀스타브',
    'Hekádemos': '헤카데모스', 'Gromov': '그로모프', 'Hou': '허우', 'Ju': '쥐',
    'Kereseira': '케레세이라', 'Lydia': '리디아', 'Lykeion': '리케이온',
    'Lupina': '루피나', 'Mercia Selene': '메르시아 셀레네',
    'Períandros': '페리안드로스', 'Sky Jagger': '스카이 재거',
    "Suzuran's Father": '스즈란의 아버지', 'Taraxacum': '타락사쿰',
    'Tosia': '토샤', 'PRTS': 'PRTS', 'Vasily Gorchikov': '바실리 고르치코프',
    'Wan Qincheng': '완친청', 'Yan Li': '옌리', 'ZOOT': '주트',
    'Olga Trepleva': '올가 다닐로브나 트레플레바',
    'Red (NPC)': '레드 (NPC)', 'Mio (Ato)': '미오 (아토)',
}

def slug(title):
    ascii_name = unicodedata.normalize('NFKD', title).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', ascii_name).strip('-')

def story_page(event):
    return urllib.parse.unquote(event['summarySource'].split('/wiki/', 1)[-1]).replace('_', ' ').removesuffix('/Synopsis')

def direct_npc_appearance(page, event_title):
    lines = [line for line in metadata[page]['appearance'].splitlines()
             if f'[[{event_title}' in line]
    return bool(lines) and not all(any(word in line.lower() for word in
                                       ('mentioned', 'unseen', 'flashback', 'dream', 'illusion'))
                                   for line in lines)

new_people = {}
page_to_id = {}
for page in sorted(metadata):
    krname = kr_overrides.get(page) or metadata[page]['krname'].strip() or game_korean.get(page.casefold(), '')
    krname = krname.strip('"“”')
    person_id = aliases.get(page) or by_wiki.get(page.casefold()) or by_korean.get(krname.casefold())
    if not person_id and slug(page) in by_id:
        person_id = slug(page)
    if not person_id:
        person_id = 'wiki-' + slug(page)
        if not krname:
            raise ValueError(f'Missing Korean name: {page}')
        new_people[person_id] = {'id': person_id, 'name': krname, 'kind': kind[page], 'wikiTitle': page}
    page_to_id[page] = person_id

cast = {}
evidence = {}
for event in data['events']:
    event_id = event['id']
    path = work / 'synopses' / f'{event_id}.txt'
    if not path.exists():
        continue
    text = path.read_text(encoding='utf-8')
    selected = []
    event_evidence = {}
    for page in catalog['events'].get(event_id, []):
        occurrences = len(re.findall(re.escape(page), text, re.I)) if len(page) >= 4 else 0
        direct = kind[page] == 'nonoperator' and direct_npc_appearance(page, story_page(event))
        explicitly_mentioned = any(f'[[{story_page(event)}' in line and 'mentioned' in line.lower()
                                   for line in metadata[page]['appearance'].splitlines())
        supported = (kind[page] == 'operator' and occurrences >= 2) or direct or (occurrences >= 3 and not explicitly_mentioned)
        if supported:
            person_id = page_to_id[page]
            if person_id not in selected:
                selected.append(person_id)
            event_evidence[person_id] = {'page': page, 'mentions': occurrences,
                                         'evidence': 'appearance-list' if direct else 'synopsis'}
    selected.sort(key=lambda person_id: -event_evidence[person_id]['mentions'])
    cast[event_id] = selected
    evidence[event_id] = event_evidence

(work / 'story_cast_sourced.json').write_text(json.dumps(cast, ensure_ascii=False, indent=2), encoding='utf-8')
(work / 'story_cast_evidence.json').write_text(json.dumps(evidence, ensure_ascii=False, indent=2), encoding='utf-8')
used_new_people = {person_id for members in cast.values() for person_id in members if person_id in new_people}
for actions in json.loads((work / 'story_action_sourced.json').read_text(encoding='utf-8')).values():
    used_new_people.update(person_id for person_id, _ in actions if person_id in new_people)
(work / 'story_people_sourced.json').write_text(json.dumps([new_people[person_id] for person_id in sorted(used_new_people)], ensure_ascii=False, indent=2), encoding='utf-8')
print(f'Prepared {len(used_new_people)} new people and {sum(map(len, cast.values()))} sourced cast entries across {len(cast)} stories')
