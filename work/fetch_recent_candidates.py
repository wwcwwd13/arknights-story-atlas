import json
import ssl
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'work' / 'candidates'
OUT.mkdir(exist_ok=True)
IMAGES = {
    'path-of-life.jpg':'https://image.gamer.ne.jp/news/2024/20241203/0050238ca348930b94f554bf173bc7aa3f23/o/1.jpg',
    'pale-sea.jpg':'https://webusstatic.yo-star.com/uy0news/ae/fae62b10057c4a682f17f8df61256cdd.jpg',
    'forge-rekindled.jpg':'https://webusstatic.yo-star.com/uy0news/ae/5d74dd17d4d67d37768a870939ede748.jpg',
    'sylvan.jpg':'https://web.hycdn.cn/announce/images/20231128/b447e95de0aefbdf9d24c45e764bac25.jpg',
    'crystal-arrow.jpg':'https://web.hycdn.cn/announce/images/20240228/9ccc0a3a61daa0c6ac9989280b50dd06.jpg',
    'here-a-people.jpg':'https://media.pocketgamer.com/artwork/na-31007-1722487825/arknights-ios-android-4.5-anniv-cover.jpg',
}
for name, url in IMAGES.items():
    try:
        request=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
        with urllib.request.urlopen(request,context=ssl._create_unverified_context(),timeout=25) as response:
            content=response.read()
            mime=response.headers.get('Content-Type','')
        if not content.startswith((b'\xff\xd8',b'\x89PNG')):
            raise ValueError(f'unexpected file: {mime}')
        (OUT/name).write_bytes(content)
        print(name,mime,len(content))
    except Exception as exc:
        print(name,'FAILED',exc)
