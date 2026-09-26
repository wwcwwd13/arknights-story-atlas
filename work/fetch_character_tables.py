"""Cache paired EN/KR game character names for portrait and cast matching."""
from pathlib import Path
from urllib.request import Request, urlopen
import json

root = Path(__file__).resolve().parent
base = 'https://raw.githubusercontent.com/PuppiizSunniiz/ArknightsGameData_YoStar/master'
for language in ('en_US', 'ko_KR'):
    url = f'{base}/{language}/gamedata/excel/character_table.json'
    with urlopen(Request(url, headers={'User-Agent': 'StoryGraphic/1.0'}), timeout=60) as response:
        content = response.read()
    data = json.loads(content)
    output = root / f'character_table_{language}.json'
    output.write_bytes(content)
    print(language, len(data), len(content))
