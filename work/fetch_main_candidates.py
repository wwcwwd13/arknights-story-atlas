import ssl
import urllib.request
from pathlib import Path

OUT=Path(__file__).resolve().parent/'candidates'
IMAGES={
 'main-13.jpg':'https://www.droidgamers.com/wp-content/uploads/2024/04/Arknights-Episode-13.jpg',
 'main-14.jpg':'https://media.pocketgamer.com/artwork/na-31007-1730478390/arknights-ep14.jpg',
 'main-15.png':'https://web.hycdn.cn/upload/image/20250407/90f10678e95f97a91051d169277a881a.png',
 'main-16.jpg':'https://pbs.twimg.com/media/HD1x5qibcAAYJVf.jpg',
}
for name,url in IMAGES.items():
 try:
  request=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
  with urllib.request.urlopen(request,context=ssl._create_unverified_context(),timeout=25) as response:
   data=response.read()
   mime=response.headers.get('Content-Type','')
  if not data.startswith((b'\xff\xd8',b'\x89PNG')):raise ValueError(mime)
  (OUT/name).write_bytes(data)
  print(name,mime,len(data))
 except Exception as exc:print(name,'FAILED',exc)
