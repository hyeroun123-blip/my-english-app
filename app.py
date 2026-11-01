import difflib
import json
import re
from functools import partial
from pathlib import Path

import streamlit as st

# 1. 페이지 기본 설정 (가장 위에 배치)
st.set_page_config(page_title="대학영어 워크북 영작하기", layout="wide")

# data 폴더 위치 (app.py와 같은 폴더 안의 data 폴더)
DATA_DIR = Path(__file__).parent / "data"


# 2. 텍스트 비교 및 차이점 HTML 생성 함수
def get_diff_html(correct, user):
    correct_words = re.findall(r"\S+", correct)
    user_words = re.findall(r"\S+", user)

    diff = list(difflib.ndiff(correct_words, user_words))

    res = []
    for token in diff:
        word = token[2:]
        if token.startswith(" "):
            res.append(f"<span style='color: black;'>{word}</span>")
        elif token.startswith("- "):
            res.append(
                f"<span style='color: blue; text-decoration: underline;' title='빠뜨린 단어'>{word}</span>"
            )
        elif token.startswith("+ "):
            res.append(
                f"<span style='color: red; text-decoration: line-through;' title='틀린 단어'>{word}</span>"
            )

    html_str = " ".join(res)
    return f'<div style="background-color: #f9f9f9; padding: 15px; border-radius: 5px; line-height: 1.6; font-size: 16px;">{html_str}</div>'


# 3. data 폴더의 unit*.json 파일을 모두 읽어오기 (파일 이름순)
def load_units():
    units = []
    for f in sorted(DATA_DIR.glob("unit*.json")):
        with open(f, encoding="utf-8") as fp:
            units.append((f.stem, json.load(fp)))
    return units


units = load_units()


# 4. 이전/다음 단원 이동 버튼
def nav_buttons(idx, position):
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        if idx > 0:
            if st.button(
                "⬅️ 이전 단원",
                key=f"prev_{position}_{idx}",
                use_container_width=True,
            ):
                st.switch_page(pages[idx - 1])
    with col3:
        if idx < len(pages) - 1:
            if st.button(
                "다음 단원 ➡️",
                key=f"next_{position}_{idx}",
                use_container_width=True,
            ):
                st.switch_page(pages[idx + 1])


# 5. 공통 렌더링 함수
def render_unit(unit_title, unit_prefix, data_list, idx):
    st.title(f"📖 {unit_title}")
    nav_buttons(idx, "top")

    st.markdown(
        """
    본문 전체를 파트별로 나누었습니다. 각 파트의 한국어 해석을 보고 전체 영어 문단을 완성해 보세요.
    * 💡 **채점 규칙**: 제출 후 단어 단위로 비교하여, **잘못 쓰거나 스펠링이 틀린 단어는 <span style='color:red; text-decoration:line-through;'>빨간색 취소선</span>**으로, **빼먹은 단어는 <span style='color:blue; text-decoration:underline;'>파란색 밑줄</span>**로 표시됩니다.
    """,
        unsafe_allow_html=True,
    )

    st.divider()

    for i, item in enumerate(data_list):
        st.subheader(f"📝 {item['part']}")
        st.info(item["korean"])

        user_input = st.text_area(
            f"{item['part']} 영어로 작성:",
            key=f"{unit_prefix}_input_{i}",
            height=150,
            placeholder="여기에 전체 영어 문단을 입력하세요...",
        )

        if st.button(
            f"{item['part']} 채점하기", key=f"{unit_prefix}_btn_{i}"
        ):
            if not user_input.strip():
                st.warning("영작 내용을 먼저 입력해 주세요!")
            else:
                st.markdown("### 🔍 채점 결과")
                diff_html = get_diff_html(item["english"], user_input)
                st.markdown(diff_html, unsafe_allow_html=True)

                st.markdown("### ✅ 완벽한 정답")
                st.success(item["english"])

        st.divider()

    nav_buttons(idx, "bottom")


# 6. JSON 파일 하나당 페이지 하나를 자동으로 만들기
def make_page(idx, prefix, unit):
    render_unit(unit["title"], prefix, unit["parts"], idx)


pages = [
    st.Page(
        partial(make_page, idx, prefix, unit),
        title=unit["title"],
        url_path=prefix,
        default=(idx == 0),
    )
    for idx, (prefix, unit) in enumerate(units)
]

pg = st.navigation(pages)
pg.run()
