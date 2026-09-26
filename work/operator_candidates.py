"""Find unrecorded operator names linked in saved event synopses."""
import collections
import json
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
work = root / 'work'
data = json.loads((root / 'data.js').read_text(encoding='utf-8').split(
    'window.STORY_DATA = ', 1)[1].rsplit(';', 1)[0])
english = json.loads((work / 'character_table_en_US.json').read_text(encoding='utf-8'))
name_by_fold = {value.get('name', '').casefold(): value['name'] for value in english.values()
                if value.get('name')}
existing = collections.defaultdict(set)
for item in data['appearances']:
    existing[item['event']].add(item['person'])
people = {person['id']: person for person in data['people']}
known_by_name = {}
for person in people.values():
    for name in (person.get('wikiTitle'), person.get('name')):
        if name:
            known_by_name[name.casefold()] = person['id']
for event in data['events']:
    path = work / 'synopses' / f"{event['id']}.txt"
    if not path.exists():
        continue
    text = path.read_text(encoding='utf-8')
    found = collections.Counter()
    for title in re.findall(r'\[\[([^|\]]+)(?:\|[^\]]+)?\]\]', text):
        title = title.split('#')[0].strip()
        name = name_by_fold.get(title.casefold())
        if name:
            found[name] += 1
    pending = [(name, count, known_by_name.get(name.casefold())) for name, count in found.most_common()
               if known_by_name.get(name.casefold()) not in existing[event['id']]]
    if pending:
        print(event['id'], event['title'], '|', ', '.join(
            f"{name}:{count}{'*' if known_id else ''}" for name, count, known_id in pending))
