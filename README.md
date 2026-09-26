# 명일방주 이야기 지도

`index.html`을 브라우저에서 열면 됩니다. 이 폴더의 데이터와 적용된 이미지만으로 연표가 작동합니다. 별도 설치나 서버는 필요하지 않습니다.
전체 내용을 글로 읽으려면 `STORY-MAP.md`를 열면 됩니다. 89개 이야기의 요약, 등장인물, 주요 행동과 서로 다른 흐름 사이의 연결을 세력별로 정리했습니다.

## 화면 사용

- 가로 위치는 **한국 서버에서 이야기가 처음 공개된 시기**입니다. 2026년 9월 26일 오른쪽의 빗금 배경은 아직 한국에 공개되지 않은 이야기입니다. 해당 카드에는 `2026.10 추정`처럼 예상 월을 표시합니다. 카드 좌표에 쓰인 매월 15일은 배치용 기준점입니다.
- 빈 공간이나 카드를 마우스로 잡아 끌면 차트를 이동할 수 있습니다. 카드를 짧게 클릭하면 상세 정보가 열립니다. 터치 화면에서는 손가락으로 스크롤합니다.
- `−` / `+`는 가로 배율만 바꿉니다. 이전 `x0.5` 화면을 새 `x1`로 삼았습니다. 한 번 누를 때마다 절반/두 배가 되며, 범위는 `x0.5`~`x2`입니다. 축소해 카드가 겹치는 것은 허용합니다.
- 진영 행은 메인 스토리의 큰 흐름인 로도스 아일랜드 → 리유니온 → 빅토리아 → 우르수스를 맨 위에 놓고, 그 아래는 첫 한국 공개일 순서입니다. 카시미어 → 시스타 → 염국 순으로 이어집니다.
- 메인 스토리, 사이드 스토리, 스토리 모음을 필터로 구분할 수 있습니다.
- 검색에는 이야기 제목·줄거리·세력·흐름과 함께 등장인물의 이름이 포함됩니다.
- 상세 패널에는 줄거리 요약, 공개일, 연관 세력, 등장인물, 주요 행동과 자료 링크가 있습니다. 등장인물은 주역과 활약 비중에 따라 정렬하고, 주역은 두꺼운 테두리로 표시합니다. 인물 이름에 마우스를 올리거나 키보드로 초점을 맞추면 정사각형 얼굴 이미지가 뜹니다.
- 상세 패널의 `줄거리 자료 (한국어)`는 해당 이야기의 한국어 장면별 요약으로 이동합니다. 프롤로그~4장 합본은 초기 장과 4장의 요약을 각각 연결했습니다. 최근 중국 공개작 중 요약이 없는 경우에는 `사건 정보 (한국어)`로 표시합니다.
- 상세 패널의 `이어 읽기`와 `함께 보기`를 펼치면 연작의 전후 이야기 또는 같은 주제의 다른 이야기를 바로 열 수 있습니다. **89개 카드 모두** 18개 묶음 중 적어도 하나에 들어갑니다. 각 목록은 한국 공개 순서이며 연작·주제 이름도 검색할 수 있습니다.
- `이야기를 잇는 장면`에는 메인 장과 외전 등 서로 다른 묶음 사이의 연결 31건을 짧은 설명과 출처로 표시합니다. 양쪽 이야기 어느 쪽에서 열어도 상대편으로 이동할 수 있습니다.

## 수록 범위와 정확도

- 이야기 항목 **89개**: 기존 이벤트 75개와 메인 스토리 묶음 14개. 프롤로그~4장은 한국 출시일이 같아 한 카드로 묶었습니다.
- 84개 항목은 이미 공개된 한국 날짜를 표시합니다. 일반 이벤트 71개의 제목과 날짜는 한국 게임 데이터 파일의 이벤트 ID로 연결했습니다. 메인 5~13장은 위키의 글로벌 공개일과 한국어 표기를 대조했고, 메인 14~16장은 한국 게임 데이터에서도 확인했습니다.
- 한국 기록에 없는 5개 항목은 **공식 일정이 아닌 월 단위 추정치**입니다. 최근 공통 이야기 `人们，我们`(중국 2026-04-07, 한국 `사람들, 우리들` 2026-09-16)의 162일 차이를 중국 공개일에 적용한 뒤 월만 표시합니다. 단일 사례를 기준으로 하므로 실제 공개 순서와 월은 바뀔 수 있습니다.
- 진영·지역 **20행**은 이야기의 주 무대 순으로 배치했습니다. 새로 시스타와 사미 행을 추가하고, 빈 ‘그 밖의 테라’ 행을 없앴습니다. `막을 여는 자들`은 시라쿠사, `나무 그늘 속에 잠들다`는 사미, `그리닝 밸리를 향해`는 림 빌리턴, `정글의 매듭`은 볼리바르로 옮겼습니다.
- **89개 이야기 모두 100자 이상의 한국어 줄거리 요약과 연관 세력 목록**을 갖습니다. 연표에는 한 이야기당 주 무대 한 행을 사용하고, 상세 패널의 ‘세력’에는 함께 얽힌 지역과 조직을 표시합니다. 82개 카드는 개별 시놉시스에, 「편안한 잠꼬대」는 마지막 장면의 게임 대사에 직접 연결합니다. 나머지 6개는 해당 편의 소개·중국 자료·메인 스토리 자료에 연결했습니다.
- **89개 항목 모두 로컬 이미지가 있습니다.** 88개에는 해당 이벤트 이미지, 프롤로그~4장 합본에는 명일방주 공통 대표 이미지가 들어갑니다. 이 합본 카드에는 `공통 이미지`라고 표시했습니다. 행에는 게임 리소스 로고 14개와 약식 표식 6개를 사용하며 두 묶음 행에는 표식 두 개를 함께 보여줍니다.
- 89개 이야기 모두에 등장인물과 주요 행동이 있습니다. 인물 196명 모두 로컬 얼굴 이미지가 있으며, 이야기·인물 연결은 556건, 행동 기록은 386건입니다. 모든 이야기에는 행동 기록이 4건 이상 있습니다.
- 한국어 위키의 장면별 줄거리 또는 장 요약을 85개 이야기에 연결했습니다. 최근 중국 공개작 3개는 한국어 사건 소개 페이지로 연결했고, `월행수상`은 한국어 줄거리 페이지를 찾지 못해 기존 원문 링크만 표시합니다.

## 파일

- `index.html`, `style.css`, `cycle2.css`, `cycle3.css`, `app.js` — 화면과 동작
- `data.js` — 표시 데이터, 출처 링크, 예상 여부, 이미지 경로
- `assets/banners/` — 출처를 확인한 로컬 행사 이미지 및 합본 1개의 공통 대표 이미지
- `assets/emblems-official/` — 게임 리소스에서 가져온 진영 로고(행 표식 14개와 에기르 보조 표식 1개)
- `assets/emblems/` — 전용 게임 로고를 확보하지 못한 행에 사용하는 약식 문양 원본
- `assets/portraits/` — 등장인물 196명의 로컬 얼굴 이미지
- `work/story_index.json` — 89개 이야기의 요약, 연관 세력, 주 무대 수정
- `work/summary_expansions.json` — 시놉시스와 게임 대사로 보강한 57개 이야기의 후속 내용
- `work/story_sequences.json` — 18개 이야기 묶음의 순서와 원자료
- `work/story_crosslinks.json` — 메인 장과 외전을 잇는 31개 교차 참조와 설명
- `work/story_event_cast.json` — 89개 이야기의 등장인물과 핵심 행동
- `work/story_cast_expansions.json`, `work/story_action_expansions.json` — 이야기별 추가 인물과 행동
- `work/story_protagonists.json` — 여러 인물이 이야기를 이끄는 경우의 주역 지정과 순서
- `work/korean_story_links.json`, `work/korean_info_links.json` — 한국어 줄거리와 사건 정보 링크
- `work/story_people_seed.json`, `work/story_people.json` — 한국어 인물 이름, 유형, 얼굴 이미지 원본 대응
- `STORY-MAP.md` — 위 데이터를 세력별로 펼쳐 놓은 읽기용 목록
- `work/synopses/` — 대조에 사용한 개별 시놉시스의 텍스트 스냅샷
- `work/` — 한국·중국 게임 데이터 원본 스냅샷과 데이터 생성 도구

## 주요 자료

- [한국 서버 게임 데이터 스냅샷](https://github.com/PuppiizSunniiz/ArknightsGameData_YoStar/blob/master/ko_KR/gamedata/excel/activity_table.json)
- [중국 서버 게임 데이터](https://github.com/Kengxxiao/ArknightsGameData/blob/master/zh_CN/gamedata/excel/activity_table.json)
- [BWIKI 활동 관문](https://wiki.biligame.com/arknights/活动关卡)
- [Arknights Terra Wiki 메인 스토리](https://arknights.wiki.gg/wiki/Main_Theme)
- [ArknightsResource camplogo](https://github.com/fexli/ArknightsResource/tree/main/camplogo) — 게임에서 추출한 진영 로고
- [Reunion](https://arknights.wiki.gg/wiki/Reunion), [Ursus](https://arknights.wiki.gg/wiki/Ursus), [Babel](https://arknights.wiki.gg/wiki/Babel), [Kazdel](https://arknights.wiki.gg/wiki/Kazdel) — 조직과 국가의 관계
- [심해 연작 목록](https://arknights.wiki.gg/wiki/Story/Movements/Glimpse_of_the_Depths), [아이린 인사 기록](https://arknights.wiki.gg/wiki/Irene/File), [삶의 길 줄거리](https://arknights.wiki.gg/wiki/Path_of_Life/Synopsis) — 이베리아·에기르와 어비설 헌터스의 관계
- [Arknights Fandom 행사 배너 목록](https://arknights.fandom.com/wiki/Category:Event_banners) — 확장 이미지의 행사명 대조. 개별 이미지 주소는 `data.js`에 있습니다.
- [중국 BWIKI](https://wiki.biligame.com/arknights/别传), [Terra Log](https://terra-log.org/en), [중국 공식 행사 공지](https://ak.hypergryph.com/news/9681) — 마지막 22개 이미지의 행사명과 그림을 대조했습니다.
- [사람들, 우리들 줄거리](https://arknights.wiki.gg/wiki/People%2C_A_People/Synopsis), [언더 타이즈 줄거리](https://arknights.wiki.gg/wiki/Under_Tides/Synopsis) — 주 무대와 주요 등장인물, 행동 기록을 확인했습니다.
- [스토리 연작별 소개](https://arknights.wiki.gg/wiki/Story/Movements), [이벤트별 시놉시스](https://arknights.wiki.gg/wiki/Story) — 전체 이야기의 내용과 행 배치 대조
- [한국어 스토리라인과 장면 요약](https://namu.moe/w/%EB%AA%85%EC%9D%BC%EB%B0%A9%EC%A3%BC/%EC%8A%A4%ED%86%A0%EB%A6%AC) — 각 이야기의 한국어 자료 링크를 대조
- [중국 BWIKI 행사 소개](https://wiki.biligame.com/arknights/别传), [몬스터 헌터 협업 제작진 공지](https://ak.hypergryph.com/news/2823), [우르수스 및 볼리바르의 이야기 연대기](https://arknights.wiki.gg/wiki/Timeline) — 최근 중국 공개작의 무대와 내용 대조
- [Arknights Terra Wiki 얼굴 아이콘](https://arknights.wiki.gg/wiki/Category:Operator_icons) — 인물별 이미지 원본 주소는 `work/portrait_sources.json`에 있습니다.

이미지는 개인용 로컬 열람을 위한 자료입니다. 원저작권은 명일방주 권리자에게 있습니다. 각 이미지의 원본 링크는 해당 이벤트 상세 패널 또는 `data.js`의 `artCredits`에 기록했습니다.

마지막 정리일: 2026-09-26.
#   a r k n i g h t s - s t o r y - a t l a s  
 