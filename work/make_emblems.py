import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
data = json.loads((root / 'work' / 'data-base.json').read_text(encoding='utf-8'))
colors = {lane['id']: lane['color'] for lane in data['lanes']}
colors.update({'kazdel':'#b68ba9'})
marks = {
 'rhodes': '<path d="M32 7 57 53H7Z"/><path d="M23 44V28h5v-5h8v5h5v16M20 44h24"/>',
 'kazimierz': '<path d="M32 8 51 18v18c0 10-9 17-19 22-10-5-19-12-19-22V18Z"/><path d="M21 35h22M24 25l8 8 8-8M32 33v15"/>',
 'yan': '<path d="M48 20c-11-13-32-4-32 12 0 11 8 17 18 17 10 0 16-7 13-15-3-8-17-8-17 1 0 4 4 6 7 4"/><path d="m42 14 8-3-2 9m-25 30-5 7"/>',
 'reunion': '<path d="M23 10c19 15-8 27 18 44M41 10C15 25 48 40 23 54M23 19h18M20 32h24M23 45h18"/>',
 'kazdel': '<path d="M32 7 52 19v26L32 57 12 45V19Z"/><path d="M20 38 32 18l12 20M24 44h16M27 38h10"/>',
 'leithanien': '<path d="M29 16v31a6 6 0 1 1-4-5V19l18-5v27a6 6 0 1 1-4-5V10Z"/>',
 'babel': '<path d="M32 6 56 53H8Z"/><path d="M19 46h26M22 40h20M25 34h14M28 28h8M30 22h4"/>',
 'sargon': '<circle cx="32" cy="32" r="12"/><path d="M32 5v11M32 48v11M5 32h11M48 32h11M13 13l8 8m22 22 8 8m0-38-8 8M21 43l-8 8"/>',
 'columbia': '<path d="M20 11h24l13 21-13 21H20L7 32Z"/><circle cx="32" cy="32" r="7"/><path d="M11 32h42M20 11l24 42M44 11 20 53"/>',
 'iberia': '<path d="M8 22c8-8 16 8 24 0s16 8 24 0M8 33c8-8 16 8 24 0s16 8 24 0M8 44c8-8 16 8 24 0s16 8 24 0"/>',
 'victoria': '<path d="m9 22 8 7 7-16 8 16 8-16 7 16 8-7-5 27H14Z"/><path d="M16 53h32"/>',
 'kjerag': '<path d="M5 49 23 16l9 15 7-11 20 29Z"/><path d="m16 30 7 4 5-3m7 3 4 3 5-3"/>',
 'laterano': '<ellipse cx="32" cy="15" rx="18" ry="7"/><path d="M32 23v28M17 32l15 10 15-10M17 50l15-8 15 8"/>',
 'siracusa': '<path d="m11 52 7-36 14 11 14-11 7 36-21 8Z"/><path d="m21 38 5 3m17-3-5 3M32 44v7"/>',
 'other': '<path d="m32 5 7 20 20 7-20 7-7 20-7-20-20-7 20-7Z"/><circle cx="32" cy="32" r="5"/>',
}
out = root / 'assets' / 'emblems'
out.mkdir(parents=True, exist_ok=True)
for id, path in marks.items():
    color = colors[id]
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img"><g fill="none" stroke="{color}" stroke-width="2.6" stroke-linejoin="round" stroke-linecap="round">{path}</g></svg>'
    (out / f'{id}.svg').write_text(svg, encoding='utf-8')
print('emblems', len(marks))
