(() => {
  'use strict';
  const data = window.STORY_DATA;
  const $ = (id) => document.getElementById(id);
  const timeline = $('timeline');
  const inner = $('timelineInner');
  const drawer = $('drawer');
  const backdrop = $('drawerBackdrop');
  const content = $('drawerContent');
  const portraitPreview = document.createElement('div');
  portraitPreview.className = 'portrait-preview';
  portraitPreview.hidden = true;
  portraitPreview.setAttribute('role', 'tooltip');
  document.body.appendChild(portraitPreview);
  const personById = new Map(data.people.map(person => [person.id, person]));
  const laneById = new Map(data.lanes.map(lane => [lane.id, lane]));
  const eventById = new Map(data.events.map(event => [event.id, event]));
  const sequenceById = new Map((data.sequences || []).map(sequence => [sequence.id, sequence]));
  const personSearchByEvent = new Map();
  for (const appearance of data.appearances) {
    const person = personById.get(appearance.person);
    if (!person) continue;
    const names = [person.name, person.wikiTitle, person.id].filter(Boolean).join(' ');
    personSearchByEvent.set(appearance.event, `${personSearchByEvent.get(appearance.event) || ''} ${names}`);
  }
  const firstYear = 2020;
  const lastYear = 2027;
  const years = lastYear - firstYear + 1;
  const start = Date.UTC(firstYear, 0, 1);
  const end = Date.UTC(lastYear + 1, 0, 1);
  const span = end - start;
  const colors = ['#425760','#605660','#5d5949','#536153','#62534b','#36565e','#665559'];
  let scale = 1;
  let filter = 'all';
  let query = '';
  let lastFocus = null;

  function esc(value) {
    return String(value).replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
  }
  function leftPx() { return parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--left')) || 210; }
  function yearPx() { return 305 * scale; }
  function xOf(date) { return ((Date.parse(date + 'T00:00:00Z') - start) / span) * (yearPx() * years); }
  function yearX(year) { return ((Date.UTC(year, 0, 1) - start) / span) * (yearPx() * years); }
  function shortDate(date) { return date.replaceAll('-', '.'); }
  function displayDate(event) { return event.dateStatus === 'projected' ? `${event.projectionMonth.replace('-', '.')} 추정` : shortDate(event.date); }
  function typeLabel(type) { return type === 'main' ? 'MAIN THEME' : type === 'collection' ? 'STORY COLLECTION' : 'SIDE STORY'; }
  function artUrl(event) { return data.art[event.id] || ''; }
  function laneEmblemHtml(lane, extraClass = '') {
    return `<span class="lane-icon ${lane.emblemKind === 'game-asset' ? 'official-icon' : ''}${lane.secondaryEmblem ? ' dual-icon' : ''} ${extraClass}" style="--lane-color:${esc(lane.color)}" aria-hidden="true"><img src="${esc(lane.emblem)}" alt="">${lane.secondaryEmblem ? `<img src="${esc(lane.secondaryEmblem)}" alt="">` : ''}</span>`;
  }

  function render() {
    const range = yearPx() * years;
    document.documentElement.style.setProperty('--year', `${yearPx()}px`);
    document.documentElement.style.setProperty('--range', `${range}px`);
    document.documentElement.style.setProperty('--total', `calc(var(--left) + ${range + 90}px)`);
    document.documentElement.style.setProperty('--lane-count', String(data.lanes.length));
    const axis = document.createElement('div');
    axis.className = 'axis';
    axis.innerHTML = '<div class="axis-corner">FACTION / YEAR</div><div class="axis-track"></div>';
    const axisTrack = axis.lastElementChild;
    const futureX = xOf(data.asOf);
    axisTrack.innerHTML = `<div class="future-axis" style="left:${futureX}px;width:${range-futureX}px"></div>`;
    for (let year = firstYear; year <= lastYear; year++) {
      const mark = document.createElement('div');
      mark.className = 'year-mark';
      mark.style.left = `${yearX(year)}px`;
      mark.innerHTML = `<strong>${year}</strong><small>01</small>`;
      axisTrack.appendChild(mark);
      for (const month of [4, 7, 10]) {
        const tick = document.createElement('div');
        tick.className = 'quarter-mark';
        tick.style.left = `${xOf(`${year}-${String(month).padStart(2,'0')}-01`)}px`;
        tick.textContent = String(month).padStart(2,'0');
        axisTrack.appendChild(tick);
      }
    }
    inner.replaceChildren(axis);
    data.lanes.forEach((lane, index) => {
      const row = document.createElement('section');
      row.className = 'lane-row';
      row.style.setProperty('--lane-color', lane.color);
      row.innerHTML = `<button class="lane-label" type="button" data-lane="${esc(lane.id)}" aria-label="${esc(lane.name)} 정보 보기">${laneEmblemHtml(lane)}<span class="lane-copy"><strong>${esc(lane.name)}</strong><span>${esc(lane.sub)}</span></span></button><div class="lane-track"></div>`;
      const track = row.lastElementChild;
      track.innerHTML = `<div class="future-zone" style="left:${futureX}px;width:${range-futureX}px"></div><div class="today-line" style="left:${futureX}px"></div>`;
      data.events.filter(event => event.lane === lane.id).forEach(event => {
        const x = xOf(event.date);
        if (event.dateStatus !== 'projected') {
          const stem = document.createElement('span');
          stem.className = `event-stem ${event.type}`;
          stem.style.left = `${x}px`;
          track.appendChild(stem);
        }
        const card = document.createElement('button');
        card.type = 'button';
        card.className = `event-card ${event.type}${event.koreanStatus === 'provisional' ? ' provisional' : ''}${event.dateStatus === 'projected' ? ' projected' : ''}${artUrl(event) ? ' has-art' : ''}`;
        card.dataset.event = event.id;
        card.style.left = `${x}px`;
        card.style.setProperty('--card-color', colors[index % colors.length]);
        card.setAttribute('aria-label', `${event.title}, ${displayDate(event)}${event.dateStatus === 'projected' ? ' 예상' : ''}, ${lane.name}`);
        const art = artUrl(event) ? `<span class="art" style="background-image:url('${esc(artUrl(event))}')"></span>` : '';
        card.innerHTML = `${art}<span class="card-content"><span class="card-kicker">${typeLabel(event.type)}${event.dateStatus === 'projected' ? ' · 예상' : ''}${data.artKind?.[event.id] === 'shared' ? ' · 공통 이미지' : ''}</span><strong class="card-title">${esc(event.title)}</strong><span class="card-date">${displayDate(event)}</span></span>`;
        track.appendChild(card);
      });
      inner.appendChild(row);
    });
    applyFilter();
  }

  function applyFilter() {
    for (const card of inner.querySelectorAll('.event-card')) {
      const event = eventById.get(card.dataset.event);
      const lane = laneById.get(event.lane);
      const sequenceNames = (event.sequences || []).map(id => sequenceById.get(id)?.name || '').join(' ');
      const haystack = `${event.title} ${event.original} ${lane.name} ${lane.sub} ${event.summary || ''} ${(event.factions || []).join(' ')} ${event.storyFocus || ''} ${event.storyArc || ''} ${sequenceNames} ${personSearchByEvent.get(event.id) || ''}`.toLowerCase();
      const match = (filter === 'all' || event.type === filter) && (!query || haystack.includes(query));
      card.classList.toggle('hidden-card', !match);
      card.tabIndex = match ? 0 : -1;
    }
  }

  function peopleHtml(ids, protagonistIds = [], lowImpactIds = [], highlightOperators = false) {
    if (!ids.length) return '<p class="empty-note">등록된 인물 없음</p>';
    const protagonists = new Set(protagonistIds);
    const lowImpact = new Set(lowImpactIds);
    return `<div class="person-list">${ids.map(id => {
      const person = personById.get(id);
      const isProtagonist = protagonists.has(id);
      return `<span class="person-pill${isProtagonist ? ' protagonist' : ''}${lowImpact.has(id) ? ' low-impact' : ''}${highlightOperators && person.kind === 'operator' ? ' operator' : ''}" tabindex="0" data-person-id="${esc(person.id)}"${isProtagonist ? ` aria-label="${esc(person.name)}, 주역"` : ''}>${esc(person.name)}</span>`;
    }).join('')}</div>`;
  }
  function openDrawer(html) {
    if (!drawer.classList.contains('open')) lastFocus = document.activeElement;
    portraitPreview.hidden = true;
    content.innerHTML = html;
    backdrop.hidden = false;
    drawer.classList.add('open');
    drawer.setAttribute('aria-hidden', 'false');
    $('drawerClose').focus();
  }
  function closeDrawer() {
    drawer.classList.remove('open');
    drawer.setAttribute('aria-hidden', 'true');
    backdrop.hidden = true;
    portraitPreview.hidden = true;
    if (lastFocus && lastFocus.isConnected) lastFocus.focus();
  }
  function openEvent(eventId) {
    const event = eventById.get(eventId);
    const lane = laneById.get(event.lane);
    const people = event.peopleOrder;
    const actions = data.actions.filter(action => action.event === eventId);
    const art = artUrl(event);
    const actionsHtml = actions.map(action => `<p class="action-item"><strong>${esc(personById.get(action.person)?.name || '')}</strong> · ${esc(action.text)}</p>`).join('');
    const sequenceHtml = (event.sequences || []).map(sequenceId => {
      const sequence = sequenceById.get(sequenceId);
      const links = sequence.events.map((id, index) => {
        const linked = eventById.get(id);
        return `<button class="sequence-link${id === eventId ? ' current' : ''}" type="button" data-open-event="${esc(id)}"${id === eventId ? ' aria-current="page"' : ''}><span>${String(index + 1).padStart(2, '0')}</span><strong>${esc(linked.title)}</strong><small>${displayDate(linked)}</small></button>`;
      }).join('');
      const sources = `${sequence.source ? `<a class="source-link" href="${esc(sequence.source)}" target="_blank" rel="noopener noreferrer">연결 자료 ↗</a>` : ''}${sequence.additionalSource ? ` <a class="source-link" href="${esc(sequence.additionalSource)}" target="_blank" rel="noopener noreferrer">후속 이야기 ↗</a>` : ''}`;
      return `<details class="story-sequence"><summary>${sequence.kind === 'theme' ? '함께 보기' : '이어 읽기'} <small>${esc(sequence.name)} · ${sequence.events.length}</small></summary><div class="sequence-list">${links}</div>${sources}</details>`;
    }).join('');
    const crosslinks = (data.crosslinks || []).filter(link => link.from === eventId || link.to === eventId)
      .map(link => ({ ...link, other: eventById.get(link.from === eventId ? link.to : link.from) }))
      .sort((left, right) => left.other.date.localeCompare(right.other.date));
    const crosslinksHtml = crosslinks.length ? `<details class="story-sequence story-crosslinks"><summary>이야기를 잇는 장면 <small>${crosslinks.length}</small></summary><div class="crosslink-list">${crosslinks.map(link => `<div class="crosslink-item"><button class="crosslink-target" type="button" data-open-event="${esc(link.other.id)}"><span>${esc(link.label)}</span><strong>${esc(link.other.title)}</strong><small>${displayDate(link.other)}</small></button><p>${esc(link.note)}</p><a class="source-link" href="${esc(link.source)}" target="_blank" rel="noopener noreferrer">연결 자료 ↗</a></div>`).join('')}</div></details>` : '';
    openDrawer(`
      <div class="drawer-heading">${laneEmblemHtml(lane, 'drawer-emblem')}<div class="drawer-heading-copy"><p class="drawer-kicker">${typeLabel(event.type)} / ${esc(lane.name)}</p>
      <h2>${esc(event.title)}</h2><div class="drawer-original">${esc(event.original)}</div></div></div>
      <div class="drawer-banner" style="background:linear-gradient(135deg,${esc(lane.color)}88,#21343b)">${art ? `<img src="${esc(art)}" alt="${esc(event.title)} 행사 이미지">` : ''}</div>
      <div class="drawer-section"><h3>줄거리 요약</h3><p class="story-summary">${esc(event.summary)}</p></div>
      ${crosslinksHtml}
      ${sequenceHtml}
      <div class="drawer-section"><h3>기본 정보</h3><dl class="fact-grid"><dt>한국 공개</dt><dd>${event.dateStatus === 'projected' ? displayDate(event) : shortDate(event.krDate || event.date)}</dd><dt>중국 공개</dt><dd>${shortDate(event.cnDate)}</dd><dt>세력</dt><dd>${(event.factions || [lane.name]).map(esc).join(' · ')}</dd><dt>형식</dt><dd>${event.type === 'main' ? '메인 스토리' : event.type === 'collection' ? '스토리 모음' : '사이드 스토리 / 삽화'}</dd></dl></div>
      ${people.length ? `<div class="drawer-section"><h3>확인된 등장인물 <small>${people.length}</small></h3>${peopleHtml(people, event.protagonists, event.lowImpactPeople, true)}</div>` : ''}
      ${actions.length ? `<div class="drawer-section"><h3>이야기 속 주요 행동</h3>${actionsHtml}</div>` : ''}
      <div class="drawer-section"><h3>자료</h3>${event.koreanStoryUrl ? `<a class="source-link" href="${esc(event.koreanStoryUrl)}" target="_blank" rel="noopener noreferrer">줄거리 자료 (한국어) ↗</a> ` : ''}${event.koreanStoryExtraUrl ? `<a class="source-link" href="${esc(event.koreanStoryExtraUrl)}" target="_blank" rel="noopener noreferrer">4장 요약 (한국어) ↗</a> ` : ''}${event.koreanInfoUrl ? `<a class="source-link" href="${esc(event.koreanInfoUrl)}" target="_blank" rel="noopener noreferrer">사건 정보 (한국어) ↗</a> ` : ''}<a class="source-link" href="${esc(event.source)}" target="_blank" rel="noopener noreferrer">스토리 출처 ↗</a>${event.summarySource ? ` <a class="source-link" href="${esc(event.summarySource)}" target="_blank" rel="noopener noreferrer">줄거리 자료 (영어) ↗</a>` : ''}${event.krSource ? ` <a class="source-link" href="${esc(event.krSource)}" target="_blank" rel="noopener noreferrer">한국 게임 데이터 ↗</a>` : ''}${data.artCredits?.[event.id] ? ` <a class="source-link" href="${esc(data.artCredits[event.id])}" target="_blank" rel="noopener noreferrer">이미지 출처 ↗</a>` : ''}${event.dateStatus === 'projected' ? `<p class="empty-note">최근 공통 공개작의 서버 간 차이 ${data.projection.offsetDays}일을 적용해 예상 월을 표시했습니다.</p>` : ''}</div>
    `);
  }
  function openLane(laneId) {
    const lane = laneById.get(laneId);
    const associated = [...new Set(data.affiliations.filter(relation => relation.lane === laneId).map(relation => relation.person))];
    const linkedEvents = data.events.filter(event => event.lane === laneId);
    const eventList = linkedEvents.map(event => `<button class="lane-event-link" type="button" data-open-event="${esc(event.id)}"><strong>${esc(event.title)}</strong><small>${displayDate(event)}${event.storyFocus ? ` · ${esc(event.storyFocus)}` : ''}</small></button>`).join('');
    const relatedList = (lane.relatedEvents || []).map(id => eventById.get(id)).filter(Boolean).map(event => `<button class="lane-event-link" type="button" data-open-event="${esc(event.id)}"><strong>${esc(event.title)}</strong><small>${esc(event.storyFocus || '')}</small></button>`).join('');
    openDrawer(`<div class="drawer-heading">${laneEmblemHtml(lane, 'drawer-emblem')}<div class="drawer-heading-copy"><p class="drawer-kicker">FACTION / REGION</p><h2>${esc(lane.name)}</h2><div class="drawer-original">${esc(lane.sub)}</div></div></div>
      <div class="drawer-section"><h3>이 연표의 이야기 <small>${linkedEvents.length}</small></h3><div class="lane-event-list">${eventList}</div></div>
      ${relatedList ? `<div class="drawer-section"><h3>다른 행의 연결 이야기</h3><div class="lane-event-list">${relatedList}</div></div>` : ''}
      ${associated.length ? `<div class="drawer-section"><h3>연결된 인물 <small>${associated.length}</small></h3>${peopleHtml(associated)}</div>` : ''}`);
  }

  inner.addEventListener('click', event => {
    const card = event.target.closest('[data-event]');
    if (card) return openEvent(card.dataset.event);
    const label = event.target.closest('[data-lane]');
    if (label) openLane(label.dataset.lane);
  });
  content.addEventListener('click', event => {
    const link = event.target.closest('[data-open-event]');
    if (link) openEvent(link.dataset.openEvent);
  });
  function positionPortrait(x, y) {
    const width = 126;
    const height = 151;
    portraitPreview.style.left = `${Math.max(8, Math.min(window.innerWidth - width - 8, x + 14))}px`;
    portraitPreview.style.top = `${Math.max(8, Math.min(window.innerHeight - height - 8, y + 14))}px`;
  }
  function showPortrait(pill, x, y) {
    const person = personById.get(pill.dataset.personId);
    if (!person?.portrait) return;
    const crop = person.portraitCrop;
    let cropStyle = '';
    if (crop) {
      const scale = Math.max(112 / crop.width, 112 / crop.height) * crop.zoom;
      const width = Math.round(crop.width * scale);
      const height = Math.round(crop.height * scale);
      const left = Math.round(56 - width * crop.x);
      const top = Math.round(56 - height * crop.y);
      cropStyle = ` class="face-crop" style="width:${width}px;height:${height}px;left:${left}px;top:${top}px"`;
    }
    portraitPreview.innerHTML = `<span class="portrait-frame"><img${cropStyle} src="${esc(person.portrait)}" alt="${esc(person.name)} 얼굴"></span><span class="portrait-name">${esc(person.name)}</span>`;
    positionPortrait(x, y);
    portraitPreview.hidden = false;
  }
  content.addEventListener('pointerover', event => {
    const pill = event.target.closest('.person-pill');
    if (pill && !pill.contains(event.relatedTarget)) showPortrait(pill, event.clientX, event.clientY);
  });
  content.addEventListener('pointermove', event => {
    if (!portraitPreview.hidden && event.target.closest('.person-pill')) positionPortrait(event.clientX, event.clientY);
  });
  content.addEventListener('pointerout', event => {
    const pill = event.target.closest('.person-pill');
    if (pill && !pill.contains(event.relatedTarget)) portraitPreview.hidden = true;
  });
  content.addEventListener('focusin', event => {
    const pill = event.target.closest('.person-pill');
    if (pill) {
      const box = pill.getBoundingClientRect();
      showPortrait(pill, box.left, box.bottom);
    }
  });
  content.addEventListener('focusout', event => {
    if (event.target.closest('.person-pill')) portraitPreview.hidden = true;
  });
  $('drawerClose').addEventListener('click', closeDrawer);
  backdrop.addEventListener('click', closeDrawer);
  document.addEventListener('keydown', event => { if (event.key === 'Escape' && drawer.classList.contains('open')) closeDrawer(); });
  $('search').addEventListener('input', event => { query = event.target.value.trim().toLowerCase(); applyFilter(); });
  document.querySelectorAll('.chip').forEach(button => button.addEventListener('click', () => {
    filter = button.dataset.type;
    document.querySelectorAll('.chip').forEach(chip => chip.classList.toggle('active', chip === button));
    applyFilter();
  }));
  function setZoom(next) {
    const oldRange = yearPx() * years;
    const focal = (timeline.scrollLeft + timeline.clientWidth / 2 - leftPx()) / oldRange;
    scale = Math.max(.5, Math.min(2, next));
    render();
    timeline.scrollLeft = leftPx() + focal * (yearPx() * years) - timeline.clientWidth / 2;
    $('zoomValue').textContent = `x${scale}`;
    $('zoomIn').disabled = scale >= 2;
    $('zoomOut').disabled = scale <= .5;
  }
  $('zoomOut').addEventListener('click', () => setZoom(scale / 2));
  $('zoomIn').addEventListener('click', () => setZoom(scale * 2));
  let drag = null;
  let suppressClick = false;
  timeline.addEventListener('pointerdown', event => {
    if (event.pointerType !== 'mouse' || event.button !== 0) return;
    drag = {x:event.clientX, y:event.clientY, left:timeline.scrollLeft, top:timeline.scrollTop, active:false};
  });
  timeline.addEventListener('pointermove', event => {
    if (!drag) return;
    const dx = event.clientX - drag.x;
    const dy = event.clientY - drag.y;
    if (!drag.active && Math.hypot(dx, dy) < 6) return;
    if (!drag.active) {
      drag.active = true;
      timeline.classList.add('dragging');
      timeline.setPointerCapture(event.pointerId);
    }
    timeline.scrollLeft = drag.left - dx;
    timeline.scrollTop = drag.top - dy;
    event.preventDefault();
  });
  const stopDrag = () => {
    if (drag?.active) {
      suppressClick = true;
      setTimeout(() => { suppressClick = false; }, 0);
    }
    drag = null;
    timeline.classList.remove('dragging');
  };
  timeline.addEventListener('pointerup', stopDrag);
  timeline.addEventListener('pointercancel', stopDrag);
  timeline.addEventListener('click', event => {
    if (suppressClick) { event.stopImmediatePropagation(); event.preventDefault(); suppressClick = false; }
  }, true);
  $('dataCount').textContent = `${data.events.length}개 스토리 항목`;
  render();
})();
