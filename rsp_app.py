"""
✂️🪨📄 나만의 가위바위보 대결 앱
--------------------------------------------------
실행 방법:
    pip install streamlit pillow
    streamlit run rps_app.py

주요 기능
  1) 기본 모드   : 난이도(랜덤 / 패턴 예측 AI)를 고를 수 있는 버튼 대결
  2) AI 인식 모드 : Teachable Machine 모델로 손 모양을 인식해서 대결
                   - 사진 모드 (안정적, 폰/PC 모두 OK)
                   - 실시간 웹캠 모드 (3·2·1 카운트다운 후 자동 판정)
  3) 전적 분석   : 승률, 연승 기록, 내가 자주 내는 손 모양 통계
"""

import random
from collections import Counter
from io import BytesIO
import base64

import streamlit as st
import streamlit.components.v1 as components
from PIL import Image

# =====================================================================
# 기본 설정
# =====================================================================
st.set_page_config(page_title="나만의 가위바위보 대결 앱", page_icon="✂️", layout="wide")

CHOICES = ["가위", "바위", "보"]
EMOJI = {"가위": "✂️", "바위": "🪨", "보": "📄"}

# key가 value를 이긴다  (가위 > 보)
BEATS = {"가위": "보", "바위": "가위", "보": "바위"}
# key를 이기려면 value를 내야 한다  (가위를 이기려면 바위)
COUNTER = {v: k for k, v in BEATS.items()}


def judge(player: str, computer: str) -> str:
    if player == computer:
        return "무승부"
    if BEATS[player] == computer:
        return "승리"
    return "패배"


# =====================================================================
# 세션 상태 초기화
# =====================================================================
def init_state():
    defaults = {
        "score": {"승리": 0, "패배": 0, "무승부": 0},
        "history": [],            # 최근 기록 (최신이 앞)
        "my_moves": [],           # 내가 낸 손 모양 순서
        "transition": {},         # 패턴 학습용: (직전 손) -> Counter(다음 손)
        "streak": 0,              # 현재 연승
        "best_streak": 0,         # 최고 연승
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_state()


# =====================================================================
# 컴퓨터 두뇌: 난이도에 따라 다음 손을 결정
# =====================================================================
def computer_move(level: str) -> str:
    """내가 지금까지 낸 패턴을 보고 컴퓨터가 손을 고른다."""
    predict_rate = {"😴 쉬움 (완전 랜덤)": 0.0,
                    "🙂 보통 (반반)": 0.5,
                    "😈 어려움 (패턴 간파)": 0.85}[level]

    last = st.session_state.my_moves[-1] if st.session_state.my_moves else None
    table = st.session_state.transition.get(last)

    if table and random.random() < predict_rate:
        predicted = table.most_common(1)[0][0]   # 내가 다음에 낼 것 같은 손
        return COUNTER[predicted]                # 그걸 이기는 손을 낸다
    return random.choice(CHOICES)


def record_round(player: str, computer: str, mode: str = "기본"):
    result = judge(player, computer)
    st.session_state.score[result] += 1

    # 연승 관리
    if result == "승리":
        st.session_state.streak += 1
        st.session_state.best_streak = max(st.session_state.best_streak,
                                           st.session_state.streak)
    elif result == "패배":
        st.session_state.streak = 0

    # 패턴 학습 (직전 손 -> 이번 손)
    if st.session_state.my_moves:
        prev = st.session_state.my_moves[-1]
        st.session_state.transition.setdefault(prev, Counter())[player] += 1
    st.session_state.my_moves.append(player)

    st.session_state.history.insert(0, {
        "모드": mode,
        "내 선택": f"{EMOJI[player]} {player}",
        "컴퓨터 선택": f"{EMOJI[computer]} {computer}",
        "결과": result,
    })
    return result


# =====================================================================
# 화면 구성
# =====================================================================
st.title("✂️🪨📄 나만의 가위바위보 대결 앱")
st.caption("버튼으로도, 손 모양 사진으로도 대결할 수 있어요!")

tab_basic, tab_ai, tab_stat = st.tabs(
    ["🖐️ 기본 모드", "🤖 AI 인식 모드", "📊 전적 분석"]
)

# ---------------------------------------------------------------------
# 1) 기본 모드
# ---------------------------------------------------------------------
with tab_basic:
    level = st.select_slider(
        "컴퓨터 난이도",
        options=["😴 쉬움 (완전 랜덤)", "🙂 보통 (반반)", "😈 어려움 (패턴 간파)"],
        value="🙂 보통 (반반)",
    )
    if level.startswith("😈"):
        st.caption("어려움 모드에서는 컴퓨터가 내 손버릇을 기억했다가 되받아칩니다. 규칙적으로 내면 계속 집니다!")

    st.subheader("무엇을 낼까요?")
    cols = st.columns(3)
    player_choice = None
    for col, choice in zip(cols, CHOICES):
        if col.button(f"{EMOJI[choice]} {choice}", use_container_width=True, key=f"btn_{choice}"):
            player_choice = choice

    if player_choice:
        comp = computer_move(level)
        result = record_round(player_choice, comp, mode="기본")

        st.markdown(f"<h1 style='text-align:center;'>{EMOJI[player_choice]} &nbsp;VS&nbsp; {EMOJI[comp]}</h1>",
                    unsafe_allow_html=True)
        if result == "승리":
            st.success("🎉 이겼습니다!")
            st.balloons()
        elif result == "패배":
            st.error("😢 졌습니다!")
        else:
            st.warning("🤝 비겼습니다!")

    st.markdown("---")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("🎉 승리", st.session_state.score["승리"])
    m2.metric("😢 패배", st.session_state.score["패배"])
    m3.metric("🤝 무승부", st.session_state.score["무승부"])
    m4.metric("🔥 연승", st.session_state.streak, f"최고 {st.session_state.best_streak}연승")

    if st.button("🔄 기록 전체 초기화"):
        for key in ["score", "history", "my_moves", "transition", "streak", "best_streak"]:
            del st.session_state[key]
        init_state()
        st.rerun()

# ---------------------------------------------------------------------
# 2) AI 인식 모드
# ---------------------------------------------------------------------
with tab_ai:
    st.subheader("손 모양을 AI가 알아맞혀 대결합니다")
    st.write(
        "Teachable Machine에서 **가위 / 바위 / 보** 3개 클래스로 학습한 모델을 "
        "`Export Model → Upload (Shareable link)`로 게시한 뒤, 주소를 아래에 붙여넣으세요."
    )

    model_url = st.text_input(
        "Teachable Machine 모델 URL",
        value="https://teachablemachine.withgoogle.com/models/pc8DpzFoM/",
        key="model_url",
    )
    if model_url and not model_url.endswith("/"):
        model_url += "/"

    ai_mode = st.radio(
        "입력 방식",
        ["📸 사진으로 판정", "🎥 실시간 웹캠으로 판정"],
        horizontal=True,
        key="ai_mode",
    )

    # 자바스크립트로 넘겨줄 공통 조각 -----------------------------------
    COMMON_JS = """
      const BEATS = {"가위":"보","바위":"가위","보":"바위",
                     "scissors":"paper","rock":"scissors","paper":"rock"};
      const KOR   = {"scissors":"가위","rock":"바위","paper":"보"};
      const EMOJI = {"가위":"✂️","바위":"🪨","보":"📄"};
      function normalize(label){
        const t = label.trim();
        return KOR[t.toLowerCase()] || t;
      }
      function bar(name, prob){
        const pct = (prob*100).toFixed(1);
        return `<div style="margin-bottom:6px;">
          <div style="display:flex;justify-content:space-between;font-size:13px;">
            <span>${name}</span><span>${pct}%</span></div>
          <div style="background:#eee;border-radius:6px;height:10px;">
            <div style="background:#4C8BF5;width:${pct}%;height:10px;border-radius:6px;"></div>
          </div></div>`;
      }
    """

    # ---------------- 사진 모드 ----------------
    if ai_mode.startswith("📸"):
        src = st.radio("사진 가져오기", ["카메라로 촬영", "파일 업로드"],
                       horizontal=True, key="photo_src")
        if src == "카메라로 촬영":
            uploaded = st.camera_input("가위/바위/보 손 모양을 촬영하세요", key="cam_in")
        else:
            uploaded = st.file_uploader("손 모양 사진", type=["png", "jpg", "jpeg"], key="file_in")

        if model_url and uploaded:
            image = Image.open(uploaded).convert("RGB")
            buf = BytesIO()
            image.save(buf, format="PNG")
            img_url = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

            comp_choice = random.choice(CHOICES)

            left, right = st.columns([1, 1.3])
            with left:
                st.image(image, caption="내가 낸 손 모양", use_container_width=True)
            with right:
                html = """
                <div style="font-family:-apple-system,'Malgun Gothic',sans-serif;">
                  <div id="status" style="color:#555;margin-bottom:10px;">AI가 손 모양을 분석 중입니다... ⏳</div>
                  <img id="img" src="__IMG__" style="display:none;" crossorigin="anonymous"/>
                  <div id="result"></div>
                  <div id="labels" style="margin-top:14px;"></div>
                </div>
                <script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@4.20.0/dist/tf.min.js"></script>
                <script src="https://cdn.jsdelivr.net/npm/@teachablemachine/image@0.8.5/dist/teachablemachine-image.min.js"></script>
                <script>
                __COMMON__
                const BASE = "__MODEL__";
                const COMP = "__COMP__";
                async function run(){
                  const s = document.getElementById("status");
                  try{
                    const model = await tmImage.load(BASE+"model.json", BASE+"metadata.json");
                    const img = document.getElementById("img");
                    const go = async () => {
                      const preds = (await model.predict(img)).sort((a,b)=>b.probability-a.probability);
                      document.getElementById("labels").innerHTML =
                        preds.map(p=>bar(p.className,p.probability)).join("");
                      const me = normalize(preds[0].className);
                      if(BEATS[me]===undefined){
                        s.innerHTML="⚠️ 클래스 이름을 '가위/바위/보' 또는 'scissors/rock/paper'로 맞춰주세요.";
                        return;
                      }
                      if(preds[0].probability < 0.6){
                        s.innerHTML = `🤔 확신이 부족해요 (${(preds[0].probability*100).toFixed(0)}%). 배경을 단순하게 하고 다시 찍어보세요.`;
                      }else{
                        s.innerHTML = `✅ AI가 인식한 내 손: <b>${EMOJI[me]} ${me}</b>`;
                      }
                      let msg = (me===COMP) ? "🤝 무승부입니다!"
                              : (BEATS[me]===COMP) ? "🎉 승리했습니다!" : "😢 패배했습니다!";
                      document.getElementById("result").innerHTML =
                        `<h2 style="margin:6px 0;">${EMOJI[me]} VS ${EMOJI[COMP]}</h2>
                         <p style="font-size:20px;margin:0;">${msg}</p>
                         <p style="color:#888;font-size:13px;">컴퓨터의 선택: ${COMP}</p>`;
                    };
                    if(img.complete) go(); else img.onload = go;
                  }catch(e){
                    s.innerHTML = "❌ 모델을 불러오지 못했습니다. URL을 확인해주세요.<br><small>"+e+"</small>";
                  }
                }
                run();
                </script>
                """
                html = (html.replace("__COMMON__", COMMON_JS)
                            .replace("__IMG__", img_url)
                            .replace("__MODEL__", model_url)
                            .replace("__COMP__", comp_choice))
                components.html(html, height=440, scrolling=True)
        else:
            st.info("모델 URL과 사진이 모두 준비되면 여기에 결과가 나타납니다.")

    # ---------------- 실시간 웹캠 모드 ----------------
    else:
        st.caption("‘대결 시작’을 누르면 3·2·1 카운트다운 후 그 순간의 손 모양으로 승부가 결정됩니다. "
                   "점수는 이 화면 안에서만 따로 집계돼요.")
        if model_url:
            html = """
            <div style="font-family:-apple-system,'Malgun Gothic',sans-serif;text-align:center;">
              <button id="start" style="padding:10px 22px;font-size:16px;border:0;border-radius:8px;
                      background:#4C8BF5;color:#fff;cursor:pointer;">📷 카메라 켜기</button>
              <button id="play" disabled style="padding:10px 22px;font-size:16px;border:0;border-radius:8px;
                      background:#ddd;color:#666;margin-left:8px;">✊ 대결 시작</button>
              <div id="status" style="margin:10px 0;color:#555;"></div>
              <div id="cam" style="display:inline-block;position:relative;"></div>
              <div id="count" style="font-size:64px;font-weight:700;color:#4C8BF5;height:0;
                   position:relative;top:-180px;text-shadow:0 2px 8px rgba(0,0,0,.3);"></div>
              <div id="result" style="font-size:18px;"></div>
              <div id="board" style="margin-top:8px;color:#444;"></div>
              <div id="labels" style="max-width:320px;margin:12px auto;"></div>
            </div>
            <script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@4.20.0/dist/tf.min.js"></script>
            <script src="https://cdn.jsdelivr.net/npm/@teachablemachine/image@0.8.5/dist/teachablemachine-image.min.js"></script>
            <script>
            __COMMON__
            const BASE = "__MODEL__";
            const MOVES = ["가위","바위","보"];
            let model, webcam, latest = null, score = {w:0,l:0,d:0};
            const $ = id => document.getElementById(id);

            function board(){
              $("board").innerHTML = `🎉 ${score.w}승 &nbsp; 😢 ${score.l}패 &nbsp; 🤝 ${score.d}무`;
            }
            async function loop(){
              webcam.update();
              const preds = (await model.predict(webcam.canvas)).sort((a,b)=>b.probability-a.probability);
              latest = preds[0];
              $("labels").innerHTML = preds.map(p=>bar(p.className,p.probability)).join("");
              requestAnimationFrame(loop);
            }
            $("start").onclick = async () => {
              $("status").innerText = "모델을 불러오는 중... ⏳";
              try{
                model = await tmImage.load(BASE+"model.json", BASE+"metadata.json");
                webcam = new tmImage.Webcam(320, 320, true);   // true = 좌우 반전
                await webcam.setup();
                await webcam.play();
                $("cam").appendChild(webcam.canvas);
                $("start").style.display = "none";
                $("play").disabled = false;
                $("play").style.background = "#2BA24C";
                $("play").style.color = "#fff";
                $("play").style.cursor = "pointer";
                $("status").innerText = "준비 완료! 손을 화면에 보이고 '대결 시작'을 누르세요.";
                board();
                requestAnimationFrame(loop);
              }catch(e){
                $("status").innerHTML = "❌ 카메라 또는 모델을 시작할 수 없습니다.<br><small>"+e+"</small>";
              }
            };
            $("play").onclick = async () => {
              $("play").disabled = true;
              $("result").innerHTML = "";
              for(const t of ["3","2","1","✊!"]){
                $("count").innerText = t;
                await new Promise(r=>setTimeout(r, 700));
              }
              $("count").innerText = "";
              if(!latest || BEATS[normalize(latest.className)]===undefined){
                $("result").innerHTML = "⚠️ 손 모양을 인식하지 못했어요. 클래스 이름과 조명을 확인해주세요.";
              }else{
                const me = normalize(latest.className);
                const comp = MOVES[Math.floor(Math.random()*3)];
                let msg;
                if(me===comp){ msg="🤝 무승부!"; score.d++; }
                else if(BEATS[me]===comp){ msg="🎉 승리!"; score.w++; }
                else { msg="😢 패배!"; score.l++; }
                $("result").innerHTML =
                  `<h2 style="margin:8px 0;">${EMOJI[me]} ${me} &nbsp;VS&nbsp; ${EMOJI[comp]} ${comp}</h2>
                   <p style="font-size:20px;margin:0;">${msg}</p>`;
                board();
              }
              $("play").disabled = false;
            };
            </script>
            """
            html = html.replace("__COMMON__", COMMON_JS).replace("__MODEL__", model_url)
            components.html(html, height=720, scrolling=True)
        else:
            st.info("먼저 모델 URL을 입력해주세요.")

# ---------------------------------------------------------------------
# 3) 전적 분석
# ---------------------------------------------------------------------
with tab_stat:
    total = sum(st.session_state.score.values())
    if total == 0:
        st.info("아직 대결 기록이 없습니다. 기본 모드에서 한 판 해보세요!")
    else:
        win_rate = st.session_state.score["승리"] / total * 100
        st.metric("승률", f"{win_rate:.1f}%", f"총 {total}판")
        st.progress(min(win_rate / 100, 1.0))

        st.markdown("#### 내가 자주 내는 손 모양")
        counts = Counter(st.session_state.my_moves)
        st.bar_chart({EMOJI[c] + " " + c: counts.get(c, 0) for c in CHOICES})

        if len(st.session_state.my_moves) >= 6:
            fav = counts.most_common(1)[0][0]
            st.caption(f"💡 {EMOJI[fav]} {fav}를 가장 많이 냈어요. "
                       f"어려움 모드의 컴퓨터는 이 버릇을 노립니다!")

        st.markdown("#### 최근 대결 기록")
        st.table(st.session_state.history[:15])
