"""
✌️✊🖐️ 가위바위보 독심술 - Streamlit 버전
-------------------------------------------------
로컬 실행:
    pip install -r requirements.txt
    streamlit run app.py

Streamlit Community Cloud 배포:
    1. GitHub 저장소에 app.py 와 requirements.txt 를 올린다
    2. share.streamlit.io 에서 New app -> 저장소 선택 -> Main file: app.py
    3. Deploy 를 누르면 공유 가능한 링크가 만들어진다
"""

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="가위바위보 독심술",
    page_icon="✌️",
    layout="centered",
)

# 스트림릿 기본 여백과 헤더를 줄여서 게임 화면이 꽉 차 보이게 한다
st.markdown(
    """
    <style>
      .block-container {padding-top: 1rem; padding-bottom: 0rem; max-width: 1000px;}
      #MainMenu, footer {visibility: hidden;}
      iframe {border: none;}
    </style>
    """,
    unsafe_allow_html=True,
)

GAME_HTML = """
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>묵찌빠 독심술 · 가위바위보 대결</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=Gowun+Dodum&display=swap" rel="stylesheet">
<style>
:root{
  --paper:#F4EEFF;
  --ink:#2B1B52;
  --ink-soft:#6B5C90;
  --line:#D9CCF5;
  --card:#FFFFFF;
  --scissors:#FF4D82;
  --rock:#3D5AFE;
  --paper-hand:#00B08B;
  --gold:#FFC53D;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --paper:#1A1230;
    --ink:#F0E9FF;
    --ink-soft:#A797D0;
    --line:#3A2C63;
    --card:#241A45;
  }
}
:root[data-theme="dark"]{
  --paper:#1A1230; --ink:#F0E9FF; --ink-soft:#A797D0; --line:#3A2C63; --card:#241A45;
}

*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{
  background:var(--paper);
  color:var(--ink);
  font-family:'Gowun Dodum', 'Apple SD Gothic Neo', sans-serif;
  line-height:1.65;
  -webkit-text-size-adjust:100%;
}
h1,h2,h3,.display{font-family:'Black Han Sans', 'Apple SD Gothic Neo', sans-serif; font-weight:400; letter-spacing:.01em}

.wrap{max-width:960px;margin:0 auto;padding:28px 20px 64px}

/* ── 상단 ───────────────────────────────── */
header{display:flex;align-items:baseline;justify-content:space-between;gap:16px;flex-wrap:wrap;margin-bottom:22px}
h1{font-size:clamp(28px,5vw,42px);margin:0;line-height:1.1}
h1 .sub{display:block;font-family:'Gowun Dodum',sans-serif;font-size:14px;color:var(--ink-soft);margin-top:8px;letter-spacing:0}
.level{display:flex;gap:6px;background:var(--card);border:2px solid var(--line);border-radius:999px;padding:4px}
.level button{
  font:inherit;font-size:13px;border:0;background:transparent;color:var(--ink-soft);
  padding:7px 13px;border-radius:999px;cursor:pointer;white-space:nowrap;
}
.level button[aria-pressed="true"]{background:var(--ink);color:var(--paper)}
.level button:focus-visible,.hand:focus-visible,.ghost:focus-visible{outline:3px solid var(--gold);outline-offset:3px}

/* ── 대결 무대 ──────────────────────────── */
.arena{
  position:relative;background:var(--card);border:3px solid var(--ink);
  border-radius:26px;padding:26px 20px 22px;
  box-shadow:8px 8px 0 var(--line);
}
.duel{display:grid;grid-template-columns:1fr auto 1fr;align-items:center;gap:8px;min-height:190px}
.fighter{text-align:center}
.glyph{font-size:clamp(64px,15vw,104px);line-height:1;display:block;filter:saturate(1.1)}
.fighter.me .glyph{transform:scaleX(-1)}
.who{font-size:13px;color:var(--ink-soft);margin-top:6px}
.vs{font-family:'Black Han Sans',sans-serif;font-size:clamp(20px,4vw,30px);color:var(--line)}

.shake .glyph{animation:shake .32s ease-in-out 3}
@keyframes shake{
  0%,100%{transform:rotate(0) translateY(0)}
  50%{transform:rotate(-24deg) translateY(-16px)}
}
.me.shake .glyph{animation-name:shakeMe}
@keyframes shakeMe{
  0%,100%{transform:scaleX(-1) rotate(0) translateY(0)}
  50%{transform:scaleX(-1) rotate(-24deg) translateY(-16px)}
}
.pop{animation:pop .4s cubic-bezier(.3,1.6,.5,1)}
@keyframes pop{from{transform:scale(.6)}to{transform:scale(1)}}
.me.pop .glyph{animation:popMe .4s cubic-bezier(.3,1.6,.5,1)}
@keyframes popMe{from{transform:scaleX(-1) scale(.6)}to{transform:scaleX(-1) scale(1)}}

.verdict{text-align:center;margin-top:14px;min-height:64px}
.verdict .big{font-family:'Black Han Sans',sans-serif;font-size:clamp(24px,6vw,38px);display:block;line-height:1.2}
.verdict .note{font-size:14px;color:var(--ink-soft)}
.win .big{color:var(--paper-hand)} .lose .big{color:var(--scissors)} .draw .big{color:var(--ink-soft)}

/* ── 손 고르기 ──────────────────────────── */
.hands{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:22px}
.hand{
  font:inherit;cursor:pointer;background:var(--card);
  border:3px solid var(--ink);border-radius:20px;padding:16px 6px 13px;
  color:var(--ink);box-shadow:5px 5px 0 var(--accent);
  transition:transform .12s, box-shadow .12s;
}
.hand span{display:block;font-size:clamp(34px,9vw,46px);line-height:1.1}
.hand b{font-family:'Black Han Sans',sans-serif;font-weight:400;font-size:17px}
.hand small{display:block;font-size:11px;color:var(--ink-soft)}
.hand:hover{transform:translate(2px,2px);box-shadow:3px 3px 0 var(--accent)}
.hand:active{transform:translate(5px,5px);box-shadow:0 0 0 var(--accent)}
.hand[disabled]{opacity:.45;cursor:default;transform:none;box-shadow:5px 5px 0 var(--accent)}
.hand.s{--accent:var(--scissors)} .hand.r{--accent:var(--rock)} .hand.p{--accent:var(--paper-hand)}

/* ── 기록 ───────────────────────────────── */
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:26px}
.stat{background:var(--card);border:2px solid var(--line);border-radius:16px;padding:12px 10px;text-align:center}
.stat b{display:block;font-family:'Black Han Sans',sans-serif;font-size:26px;line-height:1.2}
.stat span{font-size:12px;color:var(--ink-soft)}

.read{margin-top:26px;background:var(--card);border:2px dashed var(--line);border-radius:18px;padding:18px}
.read h2{font-size:17px;margin:0 0 4px}
.read p{margin:0 0 14px;font-size:13px;color:var(--ink-soft)}
.habit{display:grid;gap:9px}
.row{display:grid;grid-template-columns:52px 1fr 44px;align-items:center;gap:10px;font-size:14px}
.track{height:12px;background:var(--line);border-radius:999px;overflow:hidden}
.fill{height:100%;border-radius:999px;transition:width .5s ease}
.row.s .fill{background:var(--scissors)} .row.r .fill{background:var(--rock)} .row.p .fill{background:var(--paper-hand)}
.row em{font-style:normal;color:var(--ink-soft);font-size:12px;text-align:right}

.log{margin-top:22px}
.log h2{font-size:16px;margin:0 0 10px}
.log ol{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:7px}
.log li{background:var(--card);border:2px solid var(--line);border-radius:12px;padding:5px 9px;font-size:15px;white-space:nowrap}
.log li.w{border-color:var(--paper-hand)} .log li.l{border-color:var(--scissors)}
.empty{font-size:13px;color:var(--ink-soft)}

footer{margin-top:30px;display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;font-size:12px;color:var(--ink-soft)}
.ghost{font:inherit;font-size:13px;background:transparent;border:2px solid var(--line);color:var(--ink-soft);border-radius:999px;padding:7px 15px;cursor:pointer}
.ghost:hover{border-color:var(--ink);color:var(--ink)}

@media (max-width:560px){
  .stats{grid-template-columns:repeat(2,1fr)}
  .arena{padding:20px 14px 18px;box-shadow:5px 5px 0 var(--line)}
}
@media (prefers-reduced-motion:reduce){
  *{animation:none!important;transition:none!important}
}
</style>
</head>
<body>
<div class="wrap">

  <header>
    <h1>가위바위보 독심술<span class="sub">컴퓨터가 당신의 손버릇을 외웁니다. 같은 패턴을 반복하면 읽힙니다.</span></h1>
    <div class="level" role="group" aria-label="상대 난이도">
      <button data-rate="0" aria-pressed="false">운에 맡기기</button>
      <button data-rate="0.5" aria-pressed="true">눈치 빠른 상대</button>
      <button data-rate="0.88" aria-pressed="false">독심술사</button>
    </div>
  </header>

  <section class="arena">
    <div class="duel">
      <div class="fighter me" id="meSide">
        <span class="glyph" id="meGlyph">✊</span>
        <span class="who">나</span>
      </div>
      <div class="vs" id="vs">VS</div>
      <div class="fighter foe" id="foeSide">
        <span class="glyph" id="foeGlyph">✊</span>
        <span class="who">컴퓨터</span>
      </div>
    </div>
    <div class="verdict" id="verdict">
      <span class="big">손을 고르세요</span>
      <span class="note">키보드 1·2·3으로도 낼 수 있습니다.</span>
    </div>
  </section>

  <div class="hands">
    <button class="hand s" data-move="가위"><span>✌️</span><b>가위</b><small>1</small></button>
    <button class="hand r" data-move="바위"><span>✊</span><b>바위</b><small>2</small></button>
    <button class="hand p" data-move="보"><span>🖐️</span><b>보</b><small>3</small></button>
  </div>

  <div class="stats">
    <div class="stat"><b id="sWin">0</b><span>승</span></div>
    <div class="stat"><b id="sLose">0</b><span>패</span></div>
    <div class="stat"><b id="sDraw">0</b><span>무</span></div>
    <div class="stat"><b id="sStreak">0</b><span id="streakLabel">연승</span></div>
  </div>

  <section class="read">
    <h2>컴퓨터가 본 내 손버릇</h2>
    <p id="readNote">아직 읽을 패턴이 없습니다. 몇 판 두면 여기가 채워집니다.</p>
    <div class="habit">
      <div class="row s"><span>✌️ 가위</span><div class="track"><div class="fill" id="barS" style="width:0"></div></div><em id="numS">0회</em></div>
      <div class="row r"><span>✊ 바위</span><div class="track"><div class="fill" id="barR" style="width:0"></div></div><em id="numR">0회</em></div>
      <div class="row p"><span>🖐️ 보</span><div class="track"><div class="fill" id="barP" style="width:0"></div></div><em id="numP">0회</em></div>
    </div>
  </section>

  <section class="log">
    <h2>지난 판</h2>
    <ol id="log"><li class="empty" style="border:0;background:none;padding:0">기록이 쌓이면 여기에 나옵니다.</li></ol>
  </section>

  <footer>
    <span id="rateText">승률 —</span>
    <button class="ghost" id="reset">기록 지우기</button>
  </footer>
</div>

<script>
const MOVES = ["가위","바위","보"];
const ICON  = {"가위":"✌️","바위":"✊","보":"🖐️"};
const BEATS = {"가위":"보","바위":"가위","보":"바위"};          // key가 value를 이긴다
const COUNTER = {"보":"가위","가위":"바위","바위":"보"};        // key를 이기려면 value
const KEY = "rps-duel-v1";

let rate = 0.5;
let busy = false;
let state = { w:0, l:0, d:0, streak:0, best:0, moves:[], link:{}, log:[] };

// 저장된 기록 불러오기
try{
  const saved = localStorage.getItem(KEY);
  if(saved) state = Object.assign(state, JSON.parse(saved));
}catch(e){}

function save(){
  try{ localStorage.setItem(KEY, JSON.stringify(state)); }catch(e){}
}

const $ = id => document.getElementById(id);

// 난이도 선택
document.querySelectorAll(".level button").forEach(b=>{
  b.onclick = ()=>{
    document.querySelectorAll(".level button").forEach(x=>x.setAttribute("aria-pressed","false"));
    b.setAttribute("aria-pressed","true");
    rate = parseFloat(b.dataset.rate);
  };
});

// 컴퓨터가 손을 고른다: 직전에 낸 손 다음에 무엇을 냈는지 기억해 되받아친다
function think(){
  const last = state.moves[state.moves.length-1];
  const table = last ? state.link[last] : null;
  if(table && Math.random() < rate){
    let guess = null, top = -1;
    for(const m of MOVES){ if((table[m]||0) > top){ top = table[m]||0; guess = m; } }
    if(top > 0) return { move: COUNTER[guess], guess };
  }
  return { move: MOVES[Math.floor(Math.random()*3)], guess:null };
}

async function play(mine){
  if(busy) return;
  busy = true;
  document.querySelectorAll(".hand").forEach(h=>h.disabled = true);

  const { move: foe, guess } = think();

  // 카운트다운: 가위 · 바위 · 보!
  $("meSide").classList.remove("pop"); $("foeSide").classList.remove("pop");
  $("meGlyph").textContent = "✊"; $("foeGlyph").textContent = "✊";
  $("verdict").className = "verdict";
  $("meSide").classList.add("shake"); $("foeSide").classList.add("shake");
  const beats = ["가위","바위","보!"];
  for(const word of beats){
    $("vs").textContent = word;
    $("verdict").innerHTML = '<span class="big">&nbsp;</span>';
    await wait(330);
  }
  $("meSide").classList.remove("shake"); $("foeSide").classList.remove("shake");
  $("vs").textContent = "VS";

  // 공개
  $("meGlyph").textContent = ICON[mine];
  $("foeGlyph").textContent = ICON[foe];
  $("meSide").classList.add("pop"); $("foeSide").classList.add("pop");

  const result = mine === foe ? "draw" : (BEATS[mine] === foe ? "win" : "lose");
  const head = { win:"이겼습니다", lose:"졌습니다", draw:"비겼습니다" }[result];
  const note = guess
      ? `컴퓨터는 당신이 ${ICON[guess]} ${guess}를 낼 거라 봤습니다.`
      : "이번 판은 컴퓨터도 찍었습니다.";
  $("verdict").className = "verdict " + result;
  $("verdict").innerHTML = `<span class="big">${head}</span><span class="note">${note}</span>`;

  // 기록 갱신
  if(result==="win"){ state.w++; state.streak++; state.best = Math.max(state.best, state.streak); }
  else if(result==="lose"){ state.l++; state.streak = 0; }
  else state.d++;

  const prev = state.moves[state.moves.length-1];
  if(prev){
    state.link[prev] = state.link[prev] || {};
    state.link[prev][mine] = (state.link[prev][mine]||0) + 1;
  }
  state.moves.push(mine);
  state.log.unshift({ m:mine, f:foe, r:result });
  state.log = state.log.slice(0,14);

  save(); render();
  document.querySelectorAll(".hand").forEach(h=>h.disabled = false);
  busy = false;
}

const wait = ms => new Promise(r=>setTimeout(r,ms));

function render(){
  $("sWin").textContent = state.w;
  $("sLose").textContent = state.l;
  $("sDraw").textContent = state.d;
  $("sStreak").textContent = state.streak;
  $("streakLabel").textContent = state.best ? `연승 (최고 ${state.best})` : "연승";

  const total = state.w + state.l + state.d;
  $("rateText").textContent = total ? `${total}판 · 승률 ${(state.w/total*100).toFixed(0)}%` : "승률 —";

  // 손버릇
  const count = {"가위":0,"바위":0,"보":0};
  state.moves.forEach(m=>count[m]++);
  const max = Math.max(1, ...Object.values(count));
  const ids = {"가위":["barS","numS"],"바위":["barR","numR"],"보":["barP","numP"]};
  for(const m of MOVES){
    const [bar,num] = ids[m];
    $(bar).style.width = (count[m]/max*100) + "%";
    $(num).textContent = count[m] + "회";
  }
  if(state.moves.length >= 6){
    let fav = "가위";
    for(const m of MOVES) if(count[m] > count[fav]) fav = m;
    const share = (count[fav]/state.moves.length*100).toFixed(0);
    $("readNote").textContent =
      `${ICON[fav]} ${fav}를 ${share}% 냈습니다. 독심술사 상대는 이 습관부터 노립니다.`;
  }else{
    $("readNote").textContent = "아직 읽을 패턴이 없습니다. 몇 판 두면 여기가 채워집니다.";
  }

  // 지난 판
  const log = $("log");
  if(!state.log.length){
    log.innerHTML = '<li class="empty" style="border:0;background:none;padding:0">기록이 쌓이면 여기에 나옵니다.</li>';
  }else{
    log.innerHTML = state.log.map(e=>{
      const cls = e.r==="win" ? "w" : e.r==="lose" ? "l" : "";
      return `<li class="${cls}">${ICON[e.m]} <span style="color:var(--ink-soft)">:</span> ${ICON[e.f]}</li>`;
    }).join("");
  }
}

document.querySelectorAll(".hand").forEach(b=>{
  b.onclick = ()=>play(b.dataset.move);
});
document.addEventListener("keydown", e=>{
  const map = {"1":"가위","2":"바위","3":"보"};
  if(map[e.key]) play(map[e.key]);
});
$("reset").onclick = ()=>{
  state = { w:0, l:0, d:0, streak:0, best:0, moves:[], link:{}, log:[] };
  save(); render();
  $("verdict").className = "verdict";
  $("verdict").innerHTML = '<span class="big">기록을 지웠습니다</span><span class="note">컴퓨터도 당신의 버릇을 잊었습니다.</span>';
  $("meGlyph").textContent = "✊"; $("foeGlyph").textContent = "✊";
};

render();
</script>
</body>
</html>
"""

components.html(GAME_HTML, height=1500, scrolling=True)
