"""Remove only generated wiki portraits that are absent from the current cast."""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
portrait_dir = (root / 'assets' / 'portraits').resolve()
used = {person['id'] for person in json.loads((root / 'work' / 'story_people_sourced.json').read_text(encoding='utf-8'))}
generated = set(json.loads((root / 'work' / 'story_portrait_candidates.json').read_text(encoding='utf-8')))
removed = []
for person_id in sorted(generated - used):
    path = (portrait_dir / f'{person_id}.png').resolve()
    if path.parent != portrait_dir or not person_id.startswith('wiki-'):
        raise ValueError(f'Unsafe portrait path: {path}')
    if path.is_file():
        path.unlink()
        removed.append(person_id)

sources_path = root / 'work' / 'portrait_sources.json'
sources = json.loads(sources_path.read_text(encoding='utf-8'))
for person_id in generated - used:
    sources.pop(person_id, None)
sources_path.write_text(json.dumps(sources, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'Removed {len(removed)} unused sourced portraits')
