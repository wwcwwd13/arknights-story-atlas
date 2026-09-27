import datetime as dt
import json
import struct
from collections import Counter
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
base = json.loads((ROOT / 'work' / 'data-base.json').read_text(encoding='utf-8'))
cn = json.loads((ROOT / 'work' / 'activity_zh_CN.json').read_text(encoding='utf-8'))['basicInfo']
kr = json.loads((ROOT / 'work' / 'activity_ko_KR_latest.json').read_text(encoding='utf-8'))['basicInfo']
cn_by_name = {item['name']: item for item in cn.values()}

def offset(date, days=162):
    return (dt.date.fromisoformat(date) + dt.timedelta(days=days)).isoformat()

def month_anchor(date):
    return date[:7] + '-15'

for event in base['events']:
    event['cnDate'] = event['date']
    item = cn_by_name.get(event['original'])
    korea = kr.get(item['id']) if item else None
    if korea:
        event['date'] = dt.datetime.fromtimestamp(korea['startTime'], dt.timezone.utc).date().isoformat()
        event['krDate'] = event['date']
        event['title'] = korea['name']
        event['koreanStatus'] = 'official'
        event['dateStatus'] = 'confirmed'
        event['krSource'] = 'https://github.com/PuppiizSunniiz/ArknightsGameData_YoStar/blob/master/ko_KR/gamedata/excel/activity_table.json'
    else:
        event['projectionMonth'] = offset(event['cnDate'])[:7]
        event['date'] = month_anchor(event['projectionMonth'])
        event['krDate'] = None
        event['dateStatus'] = 'projected'
        event['koreanStatus'] = 'provisional'

event_lanes = {
    'ursas-children':'ursus',
    'forge-rekindled':'babel',
    'dossoles':'bolivar',
    'path-of-life':'iberia',
    'people-us':'ursus',
    'mass-travels':'laterano',
    'red-velvet':'columbia',
    'mirror':'yan',
    'ruins':'higashi',
    'unpromised':'columbia',
    'arsenus':'minos',
    'lime':'rim-billiton',
}
for event in base['events']:
    event['lane'] = event_lanes.get(event['id'], event['lane'])

renamed_lanes = {
    'reunion':('리유니온','감염자 운동 · 탈룰라'),
    'babel':('카즈델 · 바벨','살카즈 · 테레시아의 조직'),
    'sargon':('사르곤','아카후알라 · 황야'),
    'iberia':('이베리아 · 에기르','심해 연작 · 어비설 헌터스'),
}
for lane in base['lanes']:
    if lane['id'] in renamed_lanes:
        lane['name'], lane['sub'] = renamed_lanes[lane['id']]
base['lanes'].extend([
    {'id':'ursus','name':'우르수스','sub':'체르노보그 · 제국','color':'#b4a8a0'},
    {'id':'bolivar','name':'볼리바르','sub':'도솔레스 · 내전','color':'#c5a578'},
    {'id':'higashi','name':'극동','sub':'미츠쿠에 · 카지마치','color':'#b66e73'},
    {'id':'minos','name':'미노스','sub':'고대 도시국가 · 영웅 전승','color':'#c7a67a'},
    {'id':'rim-billiton','name':'림 빌리턴','sub':'광산 · 황야 · 여행','color':'#a2be9e'},
    {'id':'siesta','name':'시스타','sub':'화산 · 휴양 도시','color':'#dcaa7a'},
    {'id':'sami','name':'사미','sub':'북쪽 빙원 · 부족','color':'#9fc6ce'},
])
lane_context = {
    'reunion':'리유니온은 감염자 운동 조직입니다. 우르수스에서 성장했지만 우르수스 제국과 같은 세력이 아닙니다.',
    'ursus':'우르수스는 국가입니다. 리유니온의 발생지이자 대립 상대이지만 리유니온 자체는 아닙니다.',
    'babel':'카즈델은 살카즈의 국가·지역이고 바벨은 테레시아의 조직입니다. 동일한 개념은 아니지만 카즈델 내전과 바벨의 흐름을 함께 읽을 수 있도록 한 행에 묶었습니다.',
    'sargon':'사르곤은 볼리바르와 다른 국가입니다. 도솔레스 이야기는 볼리바르 행으로 옮겼습니다.',
    'bolivar':'볼리바르는 독립된 국가이며 도솔레스가 그 안에 있습니다.',
    'iberia':'이베리아와 에기르는 서로 다른 국가입니다. 언더 타이즈부터 삶의 길까지 연결되는 심해 연작을 한 행에 묶었습니다. 아이린은 이베리아 심문회 출신이고 어비설 헌터스는 에기르 출신 전투 조직입니다. 기병과 사냥꾼에는 스카디가 등장하지만 주 무대는 카시미어라 그 행에 남겼습니다.',
    'higashi':'극동은 염국과 다른 국가입니다. 「墟」의 중심 도시가 이곳에 있어 염국 행에서 옮겼습니다.',
    'minos':'「雅赛努斯复仇记」의 중심은 미노스의 도시국가입니다. 사르곤 인물이 등장하지만 주 무대인 미노스에 배치했습니다.',
    'rim-billiton':'「直到大地变成一颗酸橙」의 여행은 림 빌리턴에서 전개됩니다.',
    'siesta':'화람지심과 화산의 꿈은 시스타의 화산을 중심으로 이어집니다.',
    'sami':'사미의 숲과 빙원에서 벌어지는 탐사 이야기입니다.',
}
for lane in base['lanes']:
    if lane['id'] in lane_context:
        lane['context'] = lane_context[lane['id']]
    if lane['id'] == 'iberia':
        lane['relatedEvents'] = ['grani']

story_details = {
    'grani':('카시미어 마을 · 스카디 등장','심해 연작의 초기 연결점'),
    'under-tides':('이베리아 살비엔토 · 어비설 헌터스','심해 연작'),
    'stultifera':('이베리아 우인호 · 심문회와 어비설 헌터스','심해 연작'),
    'path-of-life':('에기르 해저 도시 · 이베리아 사절단','심해 연작'),
    'pale-sea':('이베리아 창백한 바다 · 쏜즈','심해 연작'),
    'darknights':('카즈델 내전 · 바벨','카즈델·바벨 흐름'),
    'babel':('카즈델 내전 · 바벨','카즈델·바벨 흐름'),
    'forge-rekindled':('카즈델 · 살카즈','카즈델·바벨 흐름'),
    'people-us':('우르수스 제국 · 학생자치단의 활동','우르수스 학생들의 이야기'),
    'mass-travels':('라테라노 · 두 번째 만국 정상회담','라테라노 흐름'),
    'red-velvet':('컬럼비아 · 랭크우드 촬영지','컬럼비아 이야기'),
    'mirror':('염국 · 망산 일대','염국 연작'),
    'ruins':('극동 · 미츠쿠에의 카지마치','극동 이야기'),
    'unpromised':('컬럼비아 · 항공 박람회','컬럼비아 이야기'),
    'arsenus':('미노스 · 아테니우스','미노스 이야기'),
    'lime':('림 빌리턴 · 길 위의 여행','림 빌리턴 이야기'),
}
for event in base['events']:
    if event['id'] in story_details:
        event['storyFocus'], event['storyArc'] = story_details[event['id']]
        if event['id'] in {'grani','under-tides','stultifera','path-of-life','pale-sea'}:
            event['storyArcSource'] = 'https://arknights.wiki.gg/wiki/Story/Movements/Glimpse_of_the_Depths'
        elif event['id'] == 'people-us':
            event['storyArcSource'] = 'https://arknights.wiki.gg/wiki/People%2C_A_People/Synopsis'

base['appearances'].extend([
    {'event':'under-tides','person':'irene','role':'appears','certainty':'wiki',
     'source':'https://arknights.wiki.gg/wiki/Under_Tides/Synopsis'},
    {'event':'path-of-life','person':'irene','role':'appears','certainty':'wiki',
     'source':'https://arknights.wiki.gg/wiki/Path_of_Life/Synopsis'},
])
base['actions'].extend([
    {'event':'under-tides','person':'irene','text':'이베리아 심문관으로 살비엔토를 조사하며 스카디와 마주합니다.','spoiler':'low'},
    {'event':'path-of-life','person':'irene','text':'이베리아 사절단의 일원으로 에기르 해저 도시를 방문합니다.','spoiler':'low'},
])

enrichment = json.loads((ROOT / 'work' / 'story_enrichment.json').read_text(encoding='utf-8'))
for field in ('people', 'affiliations', 'appearances', 'actions'):
    base[field].extend(enrichment[field])

main = [
    ('main-00-04','2020-01-16','메인 0–4장 · 체르노보그와 용문','序章—第四章','rhodes','2019-04-30','editorial'),
    ('main-05','2020-02-26','5장 · 표적치료','靶向药物','rhodes','2019-06-09','official'),
    ('main-06','2020-06-30','6장 · 부분괴사','局部坏死','reunion','2019-12-24','official'),
    ('main-07','2020-12-30','7장 · 고난의 요람','苦难摇篮','reunion','2020-04-25','official'),
    ('main-08','2021-04-30','8장 · 울부짖는 광명','怒号光明','reunion','2020-11-01','official'),
    ('main-09','2022-03-17','9장 · 스톰워치','风暴瞭望','victoria','2021-09-17','official'),
    ('main-10','2022-10-19','10장 · 섀터 포인트','破碎日冕','victoria','2022-04-14','official'),
    ('main-11','2023-04-27','11장 · 리턴 투 미스트','淬火尘霾','victoria','2022-10-11','official'),
    ('main-12','2023-10-24','12장 · 천둥 속의 고요','惊霆无声','victoria','2023-04-06','official'),
    ('main-13','2024-04-16','13장 · 흉조의 소용돌이','恶兆湍流','victoria','2023-10-08','official'),
    ('main-14','2024-10-31','14장 · 자비의 등대','慈悲灯塔','victoria','2024-05-01','official'),
    ('main-15','2025-09-16','15장 · 해리성 결합','解离复合','rhodes','2025-04-07','official'),
    ('main-16','2026-03-19','16장 · 비정상 스펙트럼','异常谱线','rhodes','2025-10-09','official'),
    ('main-17',month_anchor(offset('2026-05-01')),'17장 · 임계 상전이','相变临界','rhodes','2026-05-01','provisional'),
]
for id, date, title, original, lane, cn_date, translation in main:
    projected = id == 'main-17'
    if id in {f'main-{number:02d}' for number in range(5, 14)}:
        translation = 'wiki'
    base['events'].append(dict(id=id, date=date, title=title, original=original, lane=lane, type='main',
        koreanStatus=translation, dateStatus='projected' if projected else 'confirmed',
        cnDate=cn_date, krDate=None if projected else date,
        projectionMonth=date[:7] if projected else None,
        source='https://arknights.wiki.gg/wiki/Main_Theme',
        krSource='https://github.com/PuppiizSunniiz/ArknightsGameData_YoStar/blob/master/ko_KR/gamedata/excel/activity_table.json' if id in ('main-14','main-15','main-16') else None))

story_index = json.loads((ROOT / 'work' / 'story_index.json').read_text(encoding='utf-8'))
summary_expansions = json.loads((ROOT / 'work' / 'summary_expansions.json').read_text(encoding='utf-8'))
wiki_map = json.loads((ROOT / 'work' / 'event-wiki-map.json').read_text(encoding='utf-8'))
korean_story_links = json.loads((ROOT / 'work' / 'korean_story_links.json').read_text(encoding='utf-8'))
korean_info_links = json.loads((ROOT / 'work' / 'korean_info_links.json').read_text(encoding='utf-8'))
if set(korean_story_links) - set(story_index):
    raise ValueError('Korean story link refers to an unknown story')
if set(korean_info_links) - set(story_index) or set(korean_info_links) & set(korean_story_links):
    raise ValueError('Korean information link is invalid or duplicates a story link')
if set(summary_expansions) - set(story_index):
    raise ValueError('Summary expansion refers to an unknown story')
for event in base['events']:
    story = story_index[event['id']]
    event['lane'] = story.get('lane', event['lane'])
    event['summary'] = story['summary'] + (' ' + summary_expansions[event['id']] if event['id'] in summary_expansions else '')
    event['factions'] = story['factions']
    titles = wiki_map.get(event['id'], [])
    wiki_title = story.get('wikiTitle') or next((title for title in titles if '/' not in title), None)
    if event['type'] == 'main':
        wiki_title = f"Episode {event['id'][-2:]}" if (ROOT / 'work' / 'synopses' / (event['id'] + '.txt')).is_file() else 'Story/Movements/Main Theme'
    if wiki_title:
        event['summarySource'] = 'https://arknights.wiki.gg/wiki/' + quote(wiki_title.replace(' ', '_'), safe='/_()')
        if (ROOT / 'work' / 'synopses' / (event['id'] + '.txt')).is_file():
            event['summarySource'] += '/Synopsis'
    if story.get('summaryUrl'):
        event['summarySource'] = story['summaryUrl']
    if event['id'] == 'main-00-04':
        event['summarySource'] = 'https://arknights.wiki.gg/wiki/Story/Movements/Main_Theme'
    if event['id'] in korean_story_links:
        page, section = korean_story_links[event['id']]
        event['koreanStoryUrl'] = 'https://namu.moe/w/' + quote(page, safe='/') + (f'#s-{section}' if section else '')
        if event['id'] == 'main-00-04':
            event['koreanStoryExtraUrl'] = 'https://namu.moe/w/' + quote('명일방주/스토리/메인 Act Ⅰ', safe='/') + '#s-2'
    if event['id'] in korean_info_links:
        page, section = korean_info_links[event['id']]
        event['koreanInfoUrl'] = 'https://namu.moe/w/' + quote(page, safe='/') + (f'#s-{section}' if section else '')

story_people = json.loads((ROOT / 'work' / 'story_people.json').read_text(encoding='utf-8'))
known_people = {person['id'] for person in base['people']}
for person in story_people:
    if person['id'] in known_people:
        raise ValueError(f"Duplicate story person: {person['id']}")
    base['people'].append(person)
    known_people.add(person['id'])
for person in json.loads((ROOT / 'work' / 'story_people_sourced.json').read_text(encoding='utf-8')):
    if person['id'] in known_people:
        raise ValueError(f"Duplicate sourced person: {person['id']}")
    base['people'].append(person)
    known_people.add(person['id'])
prts_cast = json.loads((ROOT / 'work' / 'story_prts_cast.json').read_text(encoding='utf-8'))
for records in prts_cast.values():
    for person_id, name, cn_name in records:
        full_id = 'prts-' + person_id
        if full_id in known_people:
            raise ValueError(f'Duplicate PRTS person: {full_id}')
        base['people'].append({'id': full_id, 'name': name, 'kind': 'nonoperator', 'cnName': cn_name})
        known_people.add(full_id)
future_operator_cast = json.loads((ROOT / 'work' / 'story_future_operator_cast.json').read_text(encoding='utf-8'))
for person in future_operator_cast['people']:
    if person['id'] in known_people:
        raise ValueError(f"Duplicate future person: {person['id']}")
    base['people'].append(person)
    known_people.add(person['id'])

story_cast = json.loads((ROOT / 'work' / 'story_event_cast.json').read_text(encoding='utf-8'))
event_lookup = {event['id']: event for event in base['events']}
if set(story_cast) != set(event_lookup):
    raise ValueError('Story cast does not cover the exact event set')
existing_appearances = {(item['event'], item['person']) for item in base['appearances']}
existing_action_events = {item['event'] for item in base['actions']}
for event_id, record in story_cast.items():
    cast = record['cast']
    if not cast or len(cast) != len(set(cast)) or record['lead'] not in cast:
        raise ValueError(f'Invalid story cast: {event_id}')
    if not record['action']:
        raise ValueError(f'Missing story action: {event_id}')
    source = event_lookup[event_id]['summarySource']
    for person_id in cast:
        if person_id not in known_people:
            raise ValueError(f'Unknown story person: {event_id} / {person_id}')
        pair = (event_id, person_id)
        if pair not in existing_appearances:
            base['appearances'].append({
                'event': event_id, 'person': person_id, 'role': 'appears',
                'certainty': 'story', 'source': source,
            })
            existing_appearances.add(pair)
    if event_id not in existing_action_events:
        base['actions'].append({
            'event': event_id, 'person': record['lead'], 'text': record['action'],
            'spoiler': 'medium', 'source': source,
        })

cast_expansions = json.loads((ROOT / 'work' / 'story_cast_expansions.json').read_text(encoding='utf-8'))
action_expansions = json.loads((ROOT / 'work' / 'story_action_expansions.json').read_text(encoding='utf-8'))
if set(cast_expansions) - set(event_lookup) or set(action_expansions) != set(event_lookup):
    raise ValueError('Story detail expansions refer to an invalid event set')
for event_id, cast in cast_expansions.items():
    if len(cast) != len(set(cast)):
        raise ValueError(f'Duplicate cast expansion: {event_id}')
    for person_id in cast:
        if person_id not in known_people:
            raise ValueError(f'Unknown cast expansion: {event_id} / {person_id}')
        pair = (event_id, person_id)
        if pair not in existing_appearances:
            base['appearances'].append({
                'event': event_id, 'person': person_id, 'role': 'appears',
                'certainty': 'story', 'source': event_lookup[event_id]['summarySource'],
            })
            existing_appearances.add(pair)
for event_id, actions in action_expansions.items():
    if len(actions) < 2 or len({text for _, text in actions}) != len(actions):
        raise ValueError(f'Invalid action expansion: {event_id}')
    for person_id, action_text in actions:
        if person_id not in known_people or not action_text.strip():
            raise ValueError(f'Invalid story action: {event_id} / {person_id}')
        pair = (event_id, person_id)
        if pair not in existing_appearances:
            base['appearances'].append({
                'event': event_id, 'person': person_id, 'role': 'appears',
                'certainty': 'story', 'source': event_lookup[event_id]['summarySource'],
            })
            existing_appearances.add(pair)
        base['actions'].append({
            'event': event_id, 'person': person_id, 'text': action_text,
            'spoiler': 'medium', 'source': event_lookup[event_id]['summarySource'],
        })

sourced_cast = json.loads((ROOT / 'work' / 'story_cast_sourced.json').read_text(encoding='utf-8'))
for event_id, cast in sourced_cast.items():
    if event_id not in event_lookup or len(cast) != len(set(cast)):
        raise ValueError(f'Invalid sourced cast: {event_id}')
    for person_id in cast:
        if person_id not in known_people:
            raise ValueError(f'Unknown sourced person: {event_id} / {person_id}')
        pair = (event_id, person_id)
        if pair not in existing_appearances:
            base['appearances'].append({
                'event': event_id, 'person': person_id, 'role': 'appears',
                'certainty': 'synopsis', 'source': event_lookup[event_id]['summarySource'],
            })
            existing_appearances.add(pair)

prts_source = 'https://prts.wiki/w/%E5%89%A7%E6%83%85%E8%A7%92%E8%89%B2%E4%B8%80%E8%A7%88'
for event_id, records in prts_cast.items():
    if event_id not in event_lookup:
        raise ValueError(f'Unknown PRTS cast event: {event_id}')
    for person_id, _, _ in records:
        full_id = 'prts-' + person_id
        pair = (event_id, full_id)
        if pair not in existing_appearances:
            base['appearances'].append({
                'event': event_id, 'person': full_id, 'role': 'appears',
                'certainty': 'story', 'source': prts_source,
            })
            existing_appearances.add(pair)
for event_id, cast in future_operator_cast['events'].items():
    if event_id not in event_lookup or len(cast) != len(set(cast)):
        raise ValueError(f'Invalid future cast: {event_id}')
    for person_id in cast:
        if person_id not in known_people:
            raise ValueError(f'Unknown future person: {event_id} / {person_id}')
        pair = (event_id, person_id)
        if pair not in existing_appearances:
            base['appearances'].append({
                'event': event_id, 'person': person_id, 'role': 'appears',
                'certainty': 'story', 'source': event_lookup[event_id]['summarySource'],
            })
            existing_appearances.add(pair)

sourced_actions = json.loads((ROOT / 'work' / 'story_action_sourced.json').read_text(encoding='utf-8'))
prts_actions = json.loads((ROOT / 'work' / 'story_prts_actions.json').read_text(encoding='utf-8'))
for action_set, action_source in ((sourced_actions, None), (prts_actions, prts_source)):
    for event_id, actions in action_set.items():
        if event_id not in event_lookup:
            raise ValueError(f'Unknown sourced action event: {event_id}')
        source = action_source or event_lookup[event_id]['summarySource']
        for person_id, action_text in actions:
            if person_id not in known_people or not action_text.strip():
                raise ValueError(f'Invalid sourced action: {event_id} / {person_id}')
            pair = (event_id, person_id)
            if pair not in existing_appearances:
                base['appearances'].append({
                    'event': event_id, 'person': person_id, 'role': 'appears',
                    'certainty': 'synopsis', 'source': source,
                })
                existing_appearances.add(pair)
            base['actions'].append({
                'event': event_id, 'person': person_id, 'text': action_text,
                'spoiler': 'medium', 'source': source,
            })

protagonist_overrides = json.loads((ROOT / 'work' / 'story_protagonists.json').read_text(encoding='utf-8'))
sourced_evidence = json.loads((ROOT / 'work' / 'story_cast_evidence.json').read_text(encoding='utf-8'))
if set(protagonist_overrides) - set(event_lookup):
    raise ValueError('Protagonist list refers to an unknown story')
people_by_id = {person['id']: person for person in base['people']}
for event_id, event in event_lookup.items():
    present = {item['person'] for item in base['appearances'] if item['event'] == event_id}
    activity = Counter(item['person'] for item in base['actions'] if item['event'] == event_id)
    cast_seed = list(dict.fromkeys(story_cast[event_id]['cast'] + cast_expansions.get(event_id, []) + sourced_cast.get(event_id, [])
                                    + ['prts-' + person_id for person_id, _, _ in prts_cast.get(event_id, [])]
                                    + future_operator_cast['events'].get(event_id, [])))
    cast_rank = {person_id: index for index, person_id in enumerate(cast_seed)}
    protagonists = protagonist_overrides.get(event_id)
    if protagonists is None:
        lead = story_cast[event_id]['lead']
        other_leads = sorted((person_id for person_id in present if person_id != lead and activity[person_id] >= 2),
                             key=lambda person_id: (-activity[person_id], cast_rank.get(person_id, 999)))
        protagonists = [lead, *other_leads]
    if not protagonists or len(protagonists) != len(set(protagonists)) or set(protagonists) - present:
        raise ValueError(f'Invalid protagonists: {event_id} / {protagonists}')
    lead_rank = {person_id: index for index, person_id in enumerate(protagonists)}
    core_cast = set(story_cast[event_id]['cast'])
    expanded_cast = set(cast_expansions.get(event_id, []))
    def influence(person_id):
        name = people_by_id[person_id]['name']
        summary_mentions = event['summary'].count(name) if len(name) > 1 else 0
        synopsis_mentions = sourced_evidence.get(event_id, {}).get(person_id, {}).get('mentions', 0)
        return (12 * activity[person_id] + min(synopsis_mentions, 20)
                + 5 * (person_id in core_cast) + 2 * (person_id in expanded_cast)
                + 5 * min(summary_mentions, 2))
    def prominence(person_id):
        if person_id in lead_rank:
            return (0, lead_rank[person_id], 0, '')
        name = people_by_id[person_id]['name']
        return (1, -influence(person_id), cast_rank.get(person_id, 999), name)
    event['protagonists'] = protagonists
    event['peopleOrder'] = sorted(present, key=prominence)
    event['lowImpactPeople'] = [person_id for person_id in event['peopleOrder']
                                if person_id not in lead_rank and influence(person_id) < 5]

base['sequences'] = json.loads((ROOT / 'work' / 'story_sequences.json').read_text(encoding='utf-8'))
events_by_id = {event['id']: event for event in base['events']}
for event in base['events']:
    event['sequences'] = []
for sequence in base['sequences']:
    for event_id in sequence['events']:
        if event_id not in events_by_id:
            raise ValueError(f"Unknown sequence event: {sequence['id']} / {event_id}")
    sequence['events'].sort(key=lambda event_id: (events_by_id[event_id]['date'], event_id))
    for event_id in sequence['events']:
        if sequence['id'] in events_by_id[event_id]['sequences']:
            raise ValueError(f"Duplicate member: {sequence['id']} / {event_id}")
        events_by_id[event_id]['sequences'].append(sequence['id'])
if any(not event['sequences'] for event in base['events']):
    raise ValueError('A story is missing from the reading links')

base['crosslinks'] = json.loads((ROOT / 'work' / 'story_crosslinks.json').read_text(encoding='utf-8'))
seen_crosslinks = set()
for link in base['crosslinks']:
    if link['from'] not in events_by_id or link['to'] not in events_by_id or link['from'] == link['to']:
        raise ValueError(f'Invalid crosslink: {link}')
    pair = frozenset((link['from'], link['to']))
    if pair in seen_crosslinks:
        raise ValueError(f'Duplicate crosslink: {link}')
    seen_crosslinks.add(pair)

portrait_sources = json.loads((ROOT / 'work' / 'portrait_sources.json').read_text(encoding='utf-8'))
portrait_focus = {
    'prts-arbiter': (.45, .085, 6.3),
    'prts-ashton-lime': (.49, .155, 6.3),
    'prts-betty-crossroads': (.43, .115, 5.6),
    'prts-bokuka': (.47, .185, 5.6),
    'prts-dream-midnight': (.51, .095, 6.3),
    'prts-felice-godou': (.48, .065, 5.6),
    'prts-giulio': (.54, .105, 5.6),
    'prts-grandmother-petra': (.50, .175, 7.7),
    'prts-hanke': (.48, .105, 5.25),
    'prts-inala': (.45, .115, 6.3),
    'prts-ken-amada': (.62, .085, 5.6),
    'prts-kyra': (.52, .105, 7.7),
    'prts-madison-lime': (.50, .195, 7.0),
    'prts-morphis': (.47, .135, 6.3),
    'prts-old-jose': (.41, .135, 5.6),
    'prts-paula-meminger': (.47, .125, 6.3),
    'prts-perla': (.50, .075, 6.3),
    'prts-sami-shaman': (.55, .195, 5.6),
    'prts-shale-radoslav': (.49, .165, 6.3),
    'prts-sunny-valley-contact': (.43, .065, 5.6),
    'prts-tin': (.46, .105, 6.3),
    'prts-wall-ash': (.51, .145, 6.3),
    'prts-wolf-dream': (.59, .09, 5.6),
    'wiki-alistair-ii': (.50, .44, 7.0),
    'wiki-amma': (.54, .54, 4.2),
    'wiki-behnui-enshi-pah': (.50, .085, 5.6),
    'wiki-deathless-black-snake': (.50, .075, 5.6),
    'wiki-lugalszargus': (.50, .30, 2.8),
    'wiki-twin-empresses': (.50, .075, 5.6),
}
for person in base['people']:
    portrait = ROOT / 'assets' / 'portraits' / (person['id'] + '.png')
    if portrait.exists():
        person['portrait'] = str(portrait.relative_to(ROOT)).replace('\\', '/')
        person['portraitSource'] = portrait_sources.get(person['id'], prts_source if person['id'].startswith('prts-') else None)
        if person['id'].startswith('prts-') or person['id'] in portrait_focus:
            width, height = struct.unpack('>II', portrait.read_bytes()[16:24])
            focus_x, focus_y, zoom = portrait_focus.get(person['id'], (.50, .08, 6.3))
            person['portraitCrop'] = {'width': width, 'height': height,
                                      'x': focus_x, 'y': focus_y, 'zoom': zoom}

used_lanes = {event['lane'] for event in base['events']}
base['lanes'] = [lane for lane in base['lanes'] if lane['id'] in used_lanes]
base['events'].sort(key=lambda event: (event['date'], event['id']))
main_theme_lanes = ('rhodes', 'reunion', 'victoria', 'ursus')
main_theme_rank = {lane_id: index for index, lane_id in enumerate(main_theme_lanes)}
base['lanes'].sort(key=lambda lane: (
    0 if lane['id'] in main_theme_rank else 1,
    main_theme_rank.get(lane['id'], 0),
    '9999-99-99' if lane['id'] == 'other' else min(
        (event['date'] for event in base['events'] if event['lane'] == lane['id']),
        default='9999-99-99'),
    lane['name'],
))
for lane in base['lanes']:
    official = ROOT / 'assets' / 'emblems-official' / (lane['id'] + '.png')
    lane['emblem'] = str(official.relative_to(ROOT)).replace('\\', '/') if official.exists() else f"assets/emblems/{lane['id']}.svg"
    lane['emblemKind'] = 'game-asset' if official.exists() else 'custom'
    if lane['id'] == 'babel':
        lane['secondaryEmblem'] = 'assets/emblems/kazdel.svg'
    elif lane['id'] == 'iberia':
        lane['secondaryEmblem'] = 'assets/emblems-official/aegir.png'
base['dateBasis'] = 'KR_FIRST_RELEASE_WITH_CN_PROJECTIONS'
base['asOf'] = '2026-09-26'
base['projection'] = {'basis': '2026-09-16 KR 사람들, 우리들 − 2026-04-07 CN 人们，我们', 'offsetDays': 162,
                      'display': '월 단위 예상 표기. 카드 좌표는 표시를 위해 해당 월 15일에 둠.',
                      'note': '향후 한국 공개일의 공식 발표가 아닙니다.'}
base['source'] = 'https://github.com/PuppiizSunniiz/ArknightsGameData_YoStar/blob/master/ko_KR/gamedata/excel/activity_table.json'
base['art'] = {path.stem.replace('-mobile', ''): str(path.relative_to(ROOT)).replace('\\', '/')
               for path in (ROOT / 'assets' / 'banners').iterdir() if path.suffix in ('.jpg', '.png', '.webp')}
base['artKind'] = {'main-00-04': 'shared'}
base['artCredits'] = {
    'babel':'https://arknights.wiki.gg/images/2/2e/EN_Babel_banner.png',
    'obsidian':'https://wiki.biligame.com/arknights/火蓝之心',
    'code-brawl':'https://wiki.biligame.com/arknights/喧闹法则',
    'gavial':'https://wiki.biligame.com/arknights/密林悍将归来',
    'near-light':'https://webusstatic.yo-star.com/uy0news/ae/291289bcbe46b27d7c1907830c432249.png',
    'siracusano':'https://i0.wp.com/news.qoo-app.com/en/wp-content/uploads/sites/3/2023/05/Arknights_IL_SIracusano_Event_Feature.jpg',
    'stultifera':'https://i0.wp.com/news.qoo-app.com/en/wp-content/uploads/sites/3/2022/11/Stultifera_navis_available_now_feature.jpg',
    'under-tides':'https://ak.hycdn.cn/announce/images/20210424/5b73957f1556ecd805b62d4f08967af0.jpg',
    'lone-trail':'https://pic.kts.g.mi.com/7dd485aae2b0540ddef84754b16067534142784951818178541.jpg',
    'darknights':'https://pinoygamer.ph/attachments/darknights-memoir-png.2320/',
    'break-ice':'https://media.pocketgamer.com/artwork/na-31007-1656651840/arknights-break-the-ice-header_jpg_820.jpg',
}
banner_sources = ROOT / 'work' / 'banner_sources.json'
if banner_sources.exists():
    base['artCredits'].update(json.loads(banner_sources.read_text(encoding='utf-8')))
recent_banner_sources = ROOT / 'work' / 'recent_banner_sources.json'
if recent_banner_sources.exists():
    base['artCredits'].update(json.loads(recent_banner_sources.read_text(encoding='utf-8')))
for filename in ('remaining_banner_sources.json', 'terra_log_banner_sources.json', 'final_banner_sources.json'):
    source_file = ROOT / 'work' / filename
    if source_file.exists():
        base['artCredits'].update(json.loads(source_file.read_text(encoding='utf-8')))
(ROOT / 'data.js').write_text('/* 한국 서버 공개일과 공식 명칭을 우선으로 정리한 로컬 데이터. 상세 출처: README.md */\nwindow.STORY_DATA = '
                              + json.dumps(base, ensure_ascii=False, indent=2) + ';\n', encoding='utf-8')
print('events', len(base['events']), 'confirmed', sum(e['dateStatus']=='confirmed' for e in base['events']),
      'projected', sum(e['dateStatus']=='projected' for e in base['events']))
print('lanes', [(l['name'], min((e['date'] for e in base['events'] if e['lane']==l['id']), default='-')) for l in base['lanes']])
