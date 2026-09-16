import streamlit as st
import streamlit.components.v1 as components
import random
import base64
from io import BytesIO
from PIL import Image

st.set_page_config(
    page_title="가위바위보 대결 앱",
    page_icon="✌️",
    layout="centered",
)

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


tab_mindreader, tab_camera = st.tabs(["🧠 독심술 모드", "📸 AI 카메라 인식 모드"])

with tab_mindreader:
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
    const BEATS = {"가위":"보","바위":"가위","보":"바위"};
    const COUNTER = {"보":"가위","가위":"바위","바위":"보"};
    const KEY = "rps-duel-v1";

    let rate = 0.5;
    let busy = false;
    let state = { w:0, l:0, d:0, streak:0, best:0, moves:[], link:{}, log:[] };

    try{
      const saved = localStorage.getItem(KEY);
      if(saved) state = Object.assign(state, JSON.parse(saved));
    }catch(e){}

    function save(){
      try{ localStorage.setItem(KEY, JSON.stringify(state)); }catch(e){}
    }

    const $ = id => document.getElementById(id);

    document.querySelectorAll(".level button").forEach(b=>{
      b.onclick = ()=>{
        document.querySelectorAll(".level button").forEach(x=>x.setAttribute("aria-pressed","false"));
        b.setAttribute("aria-pressed","true");
        rate = parseFloat(b.dataset.rate);
      };
    });

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
    components.html(GAME_HTML, height=1450, scrolling=True)

with tab_camera:
    st.subheader("📸 AI 카메라 인식 모드 (Teachable Machine)")
    st.write(
        "카메라로 촬영하거나 사진을 업로드하면 Teachable Machine AI가 손 모양을 인식해 컴퓨터와 대결합니다."
    )

    CHOICES = ["가위", "바위", "보"]
    EMOJI = {"가위": "✂️", "바위": "🪨", "보": "📄"}

    model_url = st.text_input(
        "Teachable Machine 모델 URL",
        value="https://teachablemachine.withgoogle.com/models/yho698x3u/",
        placeholder="https://teachablemachine.withgoogle.com/models/xxxxxxxx/",
        key="rps_model_url",
    )

    input_method = st.radio(
        "손 모양 입력 방식",
        ["📸 카메라로 찍기", "📁 파일 업로드"],
        horizontal=True,
        key="rps_input_method",
    )

    if input_method.startswith("📸"):
        uploaded_hand = st.camera_input("가위/바위/보 손 모양을 촬영하세요", key="rps_camera")
    else:
        uploaded_hand = st.file_uploader("손 모양 사진 업로드", type=["png", "jpg", "jpeg"], key="rps_upload")

    if model_url and uploaded_hand:
        if not model_url.endswith("/"):
            model_url += "/"

        image = Image.open(uploaded_hand).convert("RGB")
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_data_url = "data:image/png;base64," + base64.b64encode(buffered.getvalue()).decode()

        computer_choice_ai = random.choice(CHOICES)

        col_left, col_right = st.columns([1, 1.4])
        with col_left:
            st.image(image, caption="입력한 손 모양", use_container_width=True)
            st.info(f"컴퓨터의 선택: {EMOJI[computer_choice_ai]} {computer_choice_ai}")

        with col_right:
            html_code = """
            <div style="font-family:-apple-system, sans-serif;">
              <div id="status" style="color:#555; margin-bottom:10px;">AI가 손 모양을 분석 중입니다... ⏳</div>
              <img id="predict-image" src="__IMG_DATA_URL__" style="display:none;" crossorigin="anonymous" />
              <div id="result-box" style="font-size:18px;"></div>
              <div id="label-container" style="margin-top:14px;"></div>
            </div>

            <script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@4.20.0/dist/tf.min.js"></script>
            <script src="https://cdn.jsdelivr.net/npm/@teachablemachine/image@0.8.5/dist/teachablemachine-image.min.js"></script>
            <script type="text/javascript">
              const URL_BASE = "__MODEL_URL__";
              const COMPUTER_CHOICE = "__COMPUTER_CHOICE__";
              const BEATS = { "가위": "보", "바위": "가위", "보": "바위",
                               "scissors": "paper", "rock": "scissors", "paper": "rock" };
              const KOR = { "scissors": "가위", "rock": "바위", "paper": "보" };
              const EMOJI = { "가위": "✂️", "바위": "🪨", "보": "📄",
                               "scissors": "✂️", "rock": "🪨", "paper": "📄" };

              function normalize(label) {
                const trimmed = label.trim();
                return KOR[trimmed.toLowerCase()] || trimmed;
              }

              function renderBar(className, prob) {
                const pct = (prob * 100).toFixed(1);
                return `<div style="margin-bottom:6px;">
                          <div style="display:flex; justify-content:space-between; font-size:13px;">
                            <span>${className}</span><span>${pct}%</span>
                          </div>
                          <div style="background:#eee; border-radius:6px; height:10px;">
                            <div style="background:#4C8BF5; width:${pct}%; height:10px; border-radius:6px;"></div>
                          </div>
                        </div>`;
              }

              async function init() {
                const statusEl = document.getElementById("status");
                try {
                  const model = await tmImage.load(URL_BASE + "model.json", URL_BASE + "metadata.json");
                  statusEl.innerText = "분석 중입니다... 🔍";

                  const imgEl = document.getElementById("predict-image");
                  imgEl.onload = async () => {
                    const predictions = await model.predict(imgEl);
                    predictions.sort((a, b) => b.probability - a.probability);

                    let html = "";
                    predictions.forEach((p) => { html += renderBar(p.className, p.probability); });
                    document.getElementById("label-container").innerHTML = html;

                    const rawTop = predictions[0].className;
                    const player = normalize(rawTop);
                    statusEl.innerHTML = `✅ AI 인식 결과: <b>${EMOJI[player] || ""} ${player}</b>`;

                    const resultBox = document.getElementById("result-box");
                    if (BEATS[player] === undefined) {
                      resultBox.innerHTML =
                        "⚠️ 클래스 이름이 '가위/바위/보' 또는 'scissors/rock/paper'와 일치하지 않아 승패를 판정할 수 없어요.";
                      return;
                    }

                    let outcome;
                    if (player === COMPUTER_CHOICE) outcome = "🤝 무승부입니다!";
                    else if (BEATS[player] === COMPUTER_CHOICE) outcome = "🎉 승리했습니다!";
                    else outcome = "😢 패배했습니다!";

                    resultBox.innerHTML =
                      `<h3>${EMOJI[player] || ""} VS ${EMOJI[COMPUTER_CHOICE]} ${COMPUTER_CHOICE}</h3>` +
                      `<p style="font-size:20px;">${outcome}</p>`;
                  };
                  if (imgEl.complete) imgEl.onload();
                } catch (err) {
                  statusEl.innerHTML =
                    "❌ 모델을 불러오지 못했습니다. 모델 URL을 확인해 주세요.<br><small>" + err + "</small>";
                }
              }
              init();
            </script>
            """
            html_code = (
                html_code
                .replace("__IMG_DATA_URL__", img_data_url)
                .replace("__MODEL_URL__", model_url)
                .replace("__COMPUTER_CHOICE__", computer_choice_ai)
            )
            components.html(html_code, height=450, scrolling=True)
    else:
        st.info("카메라 촬영 또는 파일 업로드를 수행하면 AI 분석 결과와 대결이 표시됩니다.")