"""Flag cast names not visible in saved wiki synopsis text for editorial review."""
import json
from pathlib import Path

root = Path(__file__).resolve().parent
cast = json.loads((root / 'story_event_cast.json').read_text(encoding='utf-8'))
people = {}
for file, field in [('data-base.json', 'people'), ('story_enrichment.json', 'people')]:
    people.update({p['id']: p for p in json.loads((root / file).read_text(encoding='utf-8'))[field]})
people.update({p['id']: p for p in json.loads((root / 'story_people.json').read_text(encoding='utf-8'))})
aliases = {
    'executor': 'Federico', 'reed': 'Loughshinny', 'eblana': 'Necrass',
    'vigil': 'Leontuzzo', 'demetri': 'Bellone', 'siege': 'Vina',
}
for event_id, record in cast.items():
    path = root / 'synopses' / f'{event_id}.txt'
    if not path.exists():
        continue
    text = path.read_text(encoding='utf-8').casefold()
    for person_id in record['cast']:
        person = people[person_id]
        names = [person.get('wikiTitle', ''), aliases.get(person_id, '')]
        if not any(name and name.casefold() in text for name in names):
            print(event_id, person_id, person.get('wikiTitle', person['name']))
