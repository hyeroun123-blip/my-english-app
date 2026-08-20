import streamlit as st

sentences = [
    {
        "ko": "바이러스는 유기체의 살아 있는 세포 내에서만 복제되는 초미세한 전염성 물질이다.",
        "en": "A virus is a submicroscopic infectious agent that replicates only inside the living cells of an organism."
    },
    {
        "ko": "바이러스는 동물과 식물에서부터 미생물까지 모든 생명체를 감염시킨다.",
        "en": "Viruses infect all life forms, from animals and plants to microorganisms."
    },
    {
        "ko": "바이러스 연구는 바이러스학이라고 하며, 이는 미생물학의 일부이다.",
        "en": "The study of viruses is called virology, which is a part of microbiology."
    },
    {
        "ko": "바이러스는 단백질 보호막으로 둘러싸여 있으며, 이는 미생물 유전 물질로 구성되어 있어 세균보다 죽이기 더 어렵다.",
        "en": "Viruses consist of genetic materials surrounded by a protective coat of protein, so they are more difficult to kill than bacteria."
    }
]

st.title("📖 대학영어 워크북: 해석보고 영작하기")
st.write("제공된 한국어 해석을 읽고 알맞은 영어 문장을 입력해보세요!")

if "index" not in st.session_state:
    st.session_state.index = 0

idx = st.session_state.index

if idx < len(sentences):
    current_quiz = sentences[idx]
    st.subheader(f"[문제 {idx + 1} / {len(sentences)}]")
    st.markdown(f"**[해석]**\n> {current_quiz['ko']}")
    
    with st.form(key=f"quiz_form_{idx}"):
        user_input = st.text_input("영어 문장을 입력하세요:")
        submit_button = st.form_submit_button(label="정답 확인")
        
        if submit_button:
            if user_input.strip() == current_quiz['en']:
                st.success("🎉 정답입니다! 완벽해요!")
            else:
                st.error("❌ 오답입니다. 정답을 확인해보세요.")
                st.markdown(f"**정답:** `{current_quiz['en']}`")
                st.markdown(f"**내가 쓴 글:** `{user_input}`")
                
    if st.button("다음 문제 ➡️"):
        st.session_state.index += 1
        st.rerun()
else:
    st.success("🎉 모든 문제를 다 풀었습니다! 수고하셨습니다.")
    if st.button("처음부터 다시 풀기"):
        st.session_state.index = 0
        st.rerun()
