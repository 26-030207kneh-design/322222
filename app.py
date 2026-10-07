import random
import streamlit as st

st.set_page_config(
    page_title="AI 판사: 균형의 법정 v12.2",
    page_icon="⚖️",
    layout="wide"
)

# ---------------------------------------------------------
# 판사 사법 성향 진단 로직
# ---------------------------------------------------------
def analyze_judge_persona(humanity, law, public, trust):
    if law >= 65 and humanity < 45:
        return {
            "title": "⚖️ 엄격한 법치주의 원칙관",
            "desc": "법조문과 객관적 증거를 철저히 존중하며 엄벌을 통해 법의 엄정함을 세우는 스타일입니다. 감정이나 동정표에 흔들리지 않는 냉철한 판결을 내립니다."
        }
    elif humanity >= 65 and law < 45:
        return {
            "title": "❤️ 온건한 인권 중심 재판관",
            "desc": "피고인의 성장 환경, 교화 가능성, 심신 상태를 깊이 참작하는 스타일입니다. 형벌보다는 치료와 교화를 통한 사회 복귀를 중요하게 여깁니다."
        }
    elif public >= 65 and trust >= 65:
        return {
            "title": "🛡️ 사회 안전 및 공익 수호관",
            "desc": "공공의 안전과 법질서 유지, 국민적 법감정과 사회적 신뢰 회복을 최우선으로 고려하는 스타일입니다. 강력범죄에 단호하게 대응합니다."
        }
    else:
        return {
            "title": "⚖️ 균형 잡힌 중용의 사법관",
            "desc": "법적 엄격함과 피고인의 사정, 공공의 이익을 다각도로 양립시키며 조화로운 판결을 내리는 성숙한 재판 스타일입니다."
        }

# ---------------------------------------------------------
# 실제 살인/중범죄 판례 기반 사건 데이터베이스
# ---------------------------------------------------------
ALL_CASES = [
    {
        "id": "c1",
        "title": "고유정 전 남편 살인 사건",
        "category": "실제 판례 / 약물 이용 계획 살인",
        "story": "피고인은 전 남편에게 졸피뎀을 투여한 후 살해하고 사체를 훼손·유기한 혐의로 기소되었습니다. 피고인은 성폭행 시도에 대응한 우발적 정당방위라고 주장합니다.",
        "img1": "https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1532187863486-abf9dbad1b69?w=800&q=80",
        "prosecution": "치밀하게 계획된 범행이며 범행 수법이 극도로 잔혹하므로 무기징역 선고가 필요합니다.",
        "defense": "우발적인 정당방위였으며, 사체 유기 장소의 직접 증거가 부족합니다.",
        "ev2": "[국과수 정밀 감정] 피고인의 자택 및 차량에서 피해자의 DNA와 함께 계획적 졸피뎀 구입 검색 기록이 확보되었습니다.",
        "real_verdict": "무기징역 확정 (대법원)",
        "real_reason": "대법원은 졸피뎀 사전 구입 및 검색 기록을 바탕으로 우발적 정당방위를 배척하고 치밀한 계획 살인으로 인정하여 무기징역을 확정했습니다.",
        "choices": [
            {"label": "무기징역 선고 (유죄)", "effects": {"humanity": -5, "law": 15, "public": 10, "trust": 10}},
            {"label": "증거불충분 및 정당방위 인정 (무죄)", "effects": {"humanity": 10, "law": -15, "public": -15, "trust": -10}},
            {"label": "징역 20년 감형 선고", "effects": {"humanity": 5, "law": 2, "public": -5, "trust": -2}}
        ],
        "post_choices": [
            {"label": "⚖️ [보강판결] 치밀한 계획살인 입증으로 무기징역 선고", "effects": {"humanity": -5, "law": 15, "public": 12, "trust": 15}},
            {"label": "⚖️ [보강판결] 범행의 잔혹성 및 사체유기 중벌로 사형 선고", "effects": {"humanity": -15, "law": 20, "public": 15, "trust": 10}},
            {"label": "⚖️ [보강판결] 자백 및 우발적 요소 일부 참작 징역 30년 선고", "effects": {"humanity": 8, "law": 5, "public": -5, "trust": 2}}
        ]
    },
    {
        "id": "c2",
        "title": "정유정 또래 무차별 살인 사건",
        "category": "실제 판례 / 사이코패스 신종 범죄",
        "story": "과외 앱을 통해 알게 된 또래 피해자를 살해하고 시신을 유기했습니다. 피고인은 심신미약과 불우한 환경을 주장합니다.",
        "img1": "https://images.unsplash.com/photo-1553531384-cc64ac80f931?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?w=800&q=80",
        "prosecution": "사이코패스 고위험군이며 신분 탈취를 목적으로 한 흉악 범죄이므로 무기징역이 마땅합니다.",
        "defense": "불우한 성장 환경과 정신과적 질환으로 인한 심신미약 상태였습니다.",
        "ev2": "[PCLR 감정] 사이코패스 점수 28점(고위험군) 감정 및 사전 범죄 수법 검색 기록 완벽 입증.",
        "real_verdict": "무기징역 확정 (대법원)",
        "real_reason": "대법원은 일면식도 없는 피해자를 잔혹하게 살해하고 시신을 유기한 점, 사회와 영원히 격리할 필요성을 인정하여 무기징역을 확정했습니다.",
        "choices": [
            {"label": "무기징역 및 위치추적 장치 부착", "effects": {"humanity": -5, "law": 15, "public": 10, "trust": 12}},
            {"label": "심신미약 인정 및 무죄 (치료감호)", "effects": {"humanity": 10, "law": -15, "public": -20, "trust": -15}}
        ],
        "post_choices": [
            {"label": "⚖️ [보강판결] 심신미약 배척 및 무기징역 선고", "effects": {"humanity": -5, "law": 15, "public": 12, "trust": 15}},
            {"label": "⚖️ [보강판결] 사이코패스 성향 감안 사회 영구 격리(사형)", "effects": {"humanity": -15, "law": 20, "public": 15, "trust": 8}},
            {"label": "⚖️ [보강판결] 성장 환경 참작 징역 30년 및 위치추적장치 부착", "effects": {"humanity": 10, "law": 5, "public": -8, "trust": 0}}
        ]
    },
    {
        "id": "c3",
        "title": "계곡 살인 사건 (이은해 사건)",
        "category": "실제 판례 / 부작위에 의한 살인",
        "story": "수영을 못하는 남편을 계곡에 다이빙하게 한 후 구조하지 않아 사망에 이르게 했습니다. 직접 밀지 않았으므로 살인이 아니라는 주장이 맞섭니다.",
        "img1": "https://images.unsplash.com/photo-1432405972618-c60b0225b8f9?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=800&q=80",
        "prosecution": "보험금을 노리고 피해자를 가스라이팅하여 구조 의무를 버린 '부작위에 의한 살인'입니다.",
        "defense": "피해자 스스로 다이빙한 사고사이며, 직접적인 살해 행위가 없었습니다.",
        "ev2": "[포렌식 결과] 피해자의 심리를 지속적으로 지배(가스라이팅)하고 구조장비를 치운 정황 입증.",
        "real_verdict": "무기징역 확정 (대법원)",
        "real_reason": "대법원은 직접적 위해를 가하지 않았더라도 구조할 의무가 있는 자가 의도적으로 방치하여 사망에 이르게 한 부작위 살인을 인정하여 무기징역을 선고했습니다.",
        "choices": [
            {"label": "부작위에 의한 간접살인 인정 (무기징역)", "effects": {"humanity": 5, "law": 15, "public": 12, "trust": 10}},
            {"label": "직접 살해 증거 불충분으로 무죄 (과실치사만 인정)", "effects": {"humanity": -10, "law": -10, "public": -15, "trust": -12}}
        ],
        "post_choices": [
            {"label": "⚖️ [보강판결] 심리 지배 및 부작위 살인 인정 무기징역 선고", "effects": {"humanity": 5, "law": 15, "public": 15, "trust": 15}},
            {"label": "⚖️ [보강판결] 직접적 물리력 미행사 감안 징역 25년 선고", "effects": {"humanity": -2, "law": 8, "public": -5, "trust": -2}},
            {"label": "⚖️ [보강판결] 살인 고의 입증 부족으로 과실치사죄 적용 (징역 7년)", "effects": {"humanity": -10, "law": -10, "public": -18, "trust": -15}}
        ]
    },
    {
        "id": "c4",
        "title": "강남역 살인 사건",
        "category": "실제 판례 / 조현병과 심신미약",
        "story": "노래방 화장실에서 불특정 여성을 흉기로 살해했습니다. 조현병 심신미약 주장과 표적 계획범죄 주장이 맞섰습니다.",
        "img1": "https://images.unsplash.com/photo-1517048676732-d65bc937f952?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=800&q=80",
        "prosecution": "남성을 보낸 뒤 여성만을 표적으로 대기하여 범행한 치밀한 계획 범죄입니다.",
        "defense": "심각한 조현병으로 사물 변별 능력이 미약한 상태였습니다.",
        "ev2": "[정신감정서] 피해망상이 심각하나 범행 당시 최소한의 변별 능력과 계획성은 존재했음.",
        "real_verdict": "징역 30년 확정 (대법원)",
        "real_reason": "대법원은 심신미약 상태는 인정하되 범행의 잔혹성과 사회적 위험성을 고려하여 징역 30년 및 치료감호를 확정했습니다.",
        "choices": [
            {"label": "심신미약 참작 징역 30년 및 치료감호", "effects": {"humanity": 8, "law": 10, "public": 5, "trust": 8}},
            {"label": "책임무능력 인정 무죄 (치료감호 처분)", "effects": {"humanity": 5, "law": -12, "public": -15, "trust": -10}}
        ],
        "post_choices": [
            {"label": "⚖️ [보강판결] 심신미약 인정 및 징역 30년 + 치료감호", "effects": {"humanity": 8, "law": 10, "public": 8, "trust": 10}},
            {"label": "⚖️ [보강판결] 대기 행위의 계획성 중시 무기징역 선고", "effects": {"humanity": -5, "law": 15, "public": 12, "trust": 10}},
            {"label": "⚖️ [보강판결] 심신상실 인정을 통한 무죄 및 치료감호 명령", "effects": {"humanity": 10, "law": -15, "public": -20, "trust": -15}}
        ]
    },
    {
        "id": "c5",
        "title": "부산 돌려차기 강간 살인미수 사건",
        "category": "실제 판례 / 성폭행 목적 살인미수",
        "story": "귀가하던 여성의 뒤를 쫓아가 묻지마 폭행으로 의식을 잃게 한 후 성폭행을 시도했습니다.",
        "img1": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=800&q=80",
        "prosecution": "성폭행 목적의 살인 미수 범죄로 중형에 처해야 합니다.",
        "defense": "술에 취해 기억이 나지 않으며 살해 의도는 없었습니다.",
        "ev2": "[DNA 재감정] 피해자의 의복에서 피고인의 DNA가 새로 검출되어 성범죄 목적이 명백해짐.",
        "real_verdict": "징역 20년 확정 (대법원)",
        "real_reason": "대법원은 재감정을 통해 성폭행 목적의 강간살인미수 혐의를 인정하여 항소심에서 증형된 징역 20년을 확정했습니다.",
        "choices": [
            {"label": "강간 살인미수 인정 (징역 20년)", "effects": {"humanity": 10, "law": 15, "public": 15, "trust": 15}},
            {"label": "단순 중상해죄 인정 (징역 12년)", "effects": {"humanity": -10, "law": -8, "public": -12, "trust": -10}}
        ],
        "post_choices": [
            {"label": "⚖️ [보강판결] DNA 입증에 따른 강간살인미수 징역 20년 선고", "effects": {"humanity": 10, "law": 15, "public": 15, "trust": 15}},
            {"label": "⚖️ [보강판결] 보복 위험성 감안 무기징역 선고", "effects": {"humanity": -5, "law": 18, "public": 12, "trust": 10}},
            {"label": "⚖️ [보강판결] 미수범 참작 및 반성문 제출 반영 징역 15년 선고", "effects": {"humanity": 5, "law": 5, "public": -8, "trust": -5}}
        ]
    }
]

def clamp(v):
    return max(0, min(100, v))

# 세션 초기화
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.judge_name = "전자고사법관"
    st.session_state.humanity = 50
    st.session_state.law = 50
    st.session_state.public = 50
    st.session_state.trust = 60
    st.session_state.case_index = 0
    st.session_state.is_postponed = False
    st.session_state.history = []

    # 전체 풀 중 무작위 3개 사건 추출
    selected = random.sample(ALL_CASES, min(3, len(ALL_CASES)))
    st.session_state.cases = selected

st.title("⚖️ AI 판사: 균형의 법정 v12.2")

# 사이드바
with st.sidebar:
    st.header(f"🏛️ {st.session_state.judge_name}")
    st.divider()
    st.subheader("📊 현재 사법 지표")
    st.progress(st.session_state.humanity / 100, text=f"❤️ 인간 중심: {st.session_state.humanity}")
    st.progress(st.session_state.law / 100, text=f"📜 법적 엄격함: {st.session_state.law}")
    st.progress(st.session_state.public / 100, text=f"🏛️ 공공 이익: {st.session_state.public}")
    st.progress(st.session_state.trust / 100, text=f"🛡️ 사회적 신뢰: {st.session_state.trust}")
    st.divider()
    if st.button("🔄 새 게임 시작 (사건 3개 무작위 뽑기)"):
        st.session_state.clear()
        st.rerun()

# 게임 진행 (3개 사건)
if st.session_state.case_index < len(st.session_state.cases):
    case = st.session_state.cases[st.session_state.case_index]
    
    st.caption(f"📍 재판 진행도: {st.session_state.case_index + 1} / 3")
    st.subheader(f"⚖️ 사건 {st.session_state.case_index + 1}: {case['title']}")
    st.caption(f"분야: {case['category']}")

    col_img, col_info = st.columns([1, 1.2])
    with col_img:
        if not st.session_state.is_postponed:
            st.image(case["img1"], caption="📸 1차 제출 현장 증거 사진", use_container_width=True)
        else:
            st.image(case["img2"], caption="🔍 2차 정밀 포렌식/부검 증거 사진", use_container_width=True)

    with col_info:
        st.info(f"**사건 개요:**\n\n{case['story']}")
        t1, t2 = st.tabs(["⚖️ 검찰 구형", "🛡️ 변호인 변론"])
        with t1:
            st.write(case["prosecution"])
        with t2:
            st.write(case["defense"])

    if st.session_state.is_postponed:
        st.success(f"🔍 **2차 추가 증거 개시:**\n\n{case['ev2']}")

    st.divider()
    st.subheader("⚖️ 최종 판결을 내리십시오")

    if not st.session_state.is_postponed:
        if st.button("🔍 판결 유예 및 2차 정밀 증거 요청 (다음 기일로 연기)", key=f"postpone_{st.session_state.case_index}"):
            st.session_state.is_postponed = True
            st.rerun()

        st.write("")
        for idx, choice in enumerate(case["choices"]):
            with st.container(border=True):
                st.markdown(f"**{choice['label']}**")
                if st.button("⚖️ 이 판결 선고", key=f"btn_{st.session_state.case_index}_{idx}"):
                    for k, v in choice["effects"].items():
                        st.session_state[k] = clamp(st.session_state[k] + v)
                    
                    st.session_state.history.append({
                        "case": case["title"],
                        "my_decision": choice["label"],
                        "real_verdict": case["real_verdict"],
                        "real_reason": case["real_reason"]
                    })
                    st.session_state.case_index += 1
                    st.session_state.is_postponed = False
                    st.rerun()

    else:
        for idx, choice in enumerate(case["post_choices"]):
            with st.container(border=True):
                st.markdown(f"**{choice['label']}**")
                if st.button("⚖️ 이 보강 판결 선고", key=f"btn_post_{st.session_state.case_index}_{idx}"):
                    for k, v in choice["effects"].items():
                        st.session_state[k] = clamp(st.session_state[k] + v)
                    
                    st.session_state.history.append({
                        "case": f"{case['title']} (2차 증거 제출)",
                        "my_decision": choice["label"],
                        "real_verdict": case["real_verdict"],
                        "real_reason": case["real_reason"]
                    })
                    st.session_state.case_index += 1
                    st.session_state.is_postponed = False
                    st.rerun()

# ---------------------------------------------------------
# 최종 결과 화면 (성향 분석 + 대법원 판례 비교)
# ---------------------------------------------------------
else:
    st.balloons()
    st.title("🏛️ 재판 종결: 판사 성향 및 판례 비교 리포트")
    st.success(f"**{st.session_state.judge_name}** 님, 3개 사건의 모든 재판이 끝났습니다.")

    # 1. 사법 성향 리포트
    persona = analyze_judge_persona(
        st.session_state.humanity,
        st.session_state.law,
        st.session_state.public,
        st.session_state.trust
    )
    
    st.container(border=True).markdown(f"""
    ## 🧐 전자고사법관님의 사법 성향 진단
    ### **{persona['title']}**
    
    {persona['desc']}
    """)

    st.write("")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("❤️ 인간 중심", st.session_state.humanity)
    col2.metric("📜 법적 엄격함", st.session_state.law)
    col3.metric("🏛️ 공공 이익", st.session_state.public)
    col4.metric("🛡️ 사회적 신뢰", st.session_state.trust)

    st.divider()
    st.subheader("📜 내 판결 VS 실제 대법원 판례 비교 분석")

    for idx, item in enumerate(st.session_state.history):
        with st.expander(f"사건 {idx+1}: {item['case']}", expanded=True):
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("### 🧑‍⚖️ 내가 내린 판결")
                st.warning(f"**{item['my_decision']}**")
            with col_b:
                st.markdown("### 🏛️ 실제 대법원 최종 판결")
                st.success(f"**{item['real_verdict']}**")
            
            st.markdown(f"**💡 실제 판례의 법적 판단 근거:**\n{item['real_reason']}")

    if st.button("🔄 새 사건 3개 무작위 뽑아서 다시 하기", type="primary", use_container_width=True):
        st.session_state.clear()
        st.rerun()
