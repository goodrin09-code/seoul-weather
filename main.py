```python
import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(
    page_title="서울 100년 기온 변화",
    page_icon="🌡️",
    layout="wide"
)

# 제목
st.title("🌡️ 서울의 100년 기온 변화")
st.write("1907년 이후 서울의 연평균 기온이 어떻게 변해 왔는지 살펴봅니다.")

# 데이터 주소
DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/seoul.csv"

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL, encoding="utf-8-sig")

    # 날짜를 날짜 형식으로 변환
    df["날짜"] = pd.to_datetime(df["날짜"])

    # 연도 추출
    df["연도"] = df["날짜"].dt.year

    return df


try:
    df = load_data()

    # 연도별 평균기온 계산
    yearly_temp = (
        df.groupby("연도")["평균기온"]
        .mean()
        .reset_index()
    )

    # 연도순 정렬
    yearly_temp = yearly_temp.sort_values("연도")

    # 그래프용 데이터
    chart_data = yearly_temp.set_index("연도")

    # 주요 정보
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "관측 시작 연도",
            f"{yearly_temp['연도'].min()}년"
        )

    with col2:
        st.metric(
            "관측 종료 연도",
            f"{yearly_temp['연도'].max()}년"
        )

    with col3:
        st.metric(
            "분석 연도 수",
            f"{len(yearly_temp)}년"
        )

    st.divider()

    # 그래프 제목
    st.subheader("📈 서울 연평균 기온 변화")

    st.line_chart(
        chart_data,
        y="평균기온",
        height=500,
        use_container_width=True
    )

    st.caption(
        "※ 각 연도의 일평균 기온을 평균하여 연평균 기온을 계산했습니다."
    )

    # 시작과 끝의 기온 비교
    st.subheader("🔎 처음과 최근의 연평균 기온 비교")

    first_year = yearly_temp.iloc[0]
    last_year = yearly_temp.iloc[-1]

    difference = last_year["평균기온"] - first_year["평균기온"]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            f"{int(first_year['연도'])}년",
            f"{first_year['평균기온']:.2f} ℃"
        )

    with col2:
        st.metric(
            f"{int(last_year['연도'])}년",
            f"{last_year['평균기온']:.2f} ℃"
        )

    with col3:
        st.metric(
            "변화량",
            f"{difference:+.2f} ℃"
        )

    st.divider()

    # 연도별 데이터 표
    with st.expander("📋 연도별 평균기온 데이터 보기"):
        display_data = yearly_temp.copy()
        display_data["연도"] = display_data["연도"].astype(int)
        display_data["평균기온"] = display_data["평균기온"].round(2)

        st.dataframe(
            display_data,
            use_container_width=True,
            hide_index=True
        )

except Exception as e:
    st.error("데이터를 불러오는 중 문제가 발생했습니다.")
    st.write(f"오류 내용: {e}")
```
