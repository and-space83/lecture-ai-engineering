import streamlit as st
import pandas as pd
import numpy as np
import time
import datetime

# ============================================
# ページ設定
# ============================================
st.set_page_config(
    page_title="旅行プラン作成アプリ",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# タイトルと説明
# ============================================
st.title("✈️ あなただけの旅行プランを作ろう！")
st.markdown("旅行先や日程、アクティビティを選んで、オリジナルの旅程表を作成しましょう。")

# ============================================
# サイドバー 
# ============================================
st.sidebar.header("旅行設定")
destination = st.sidebar.selectbox("行きたい場所", ["東京", "京都", "沖縄", "北海道", "大阪"])
start_date = st.sidebar.date_input("出発日", datetime.date.today())
days = st.sidebar.slider("旅行日数", 1, 14, 3)
travelers = st.sidebar.number_input("参加人数", min_value=1, value=2)

# ============================================
# 基本的なUI要素
# ============================================
# メインコンテンツ
st.subheader("旅行プラン概要")
st.info(f"""
**行き先**: {destination}  
**出発日**: {start_date.strftime('%Y-%m-%d')}  
**日数**: {days}泊  
**人数**: {int(travelers)}人
""")

# タブで日程を作成
st.subheader("日程を決めよう")
tabs = st.tabs([f"Day {i+1}" for i in range(days)])
for i in range(days):
    with tabs[i]:
        st.write(f"🗓️ Day {i+1}: {start_date + datetime.timedelta(days=i)}")
        morning = st.text_input(f"午前の予定 (Day {i+1})", key=f"morning_{i}")
        afternoon = st.text_input(f"午後の予定 (Day {i+1})", key=f"afternoon_{i}")
        night = st.text_input(f"夜の予定 (Day {i+1})", key=f"night_{i}")
        st.success(f"予定：午前「{morning}」、午後「{afternoon}」、夜「{night}」")

# 画像アップロード（オプション）
st.subheader("参考画像をアップロード（任意）")
uploaded = st.file_uploader("旅先の写真や参考画像をアップロード", type=["png", "jpg", "jpeg"])
if uploaded:
    st.image(uploaded, caption="アップロードされた画像", use_column_width=True)

# ============================================
# データ表示
# ============================================

# 旅程表の表示
if st.button("📝 最終プランを表示"):
    st.balloons()
    st.subheader("🎉 あなたの旅行プラン")
    plan_data = []
    for i in range(days):
        day = start_date + datetime.timedelta(days=i)
        morning = st.session_state.get(f"morning_{i}", "")
        afternoon = st.session_state.get(f"afternoon_{i}", "")
        night = st.session_state.get(f"night_{i}", "")
        plan_data.append([day.strftime("%Y-%m-%d"), morning, afternoon, night])
    df_plan = pd.DataFrame(plan_data, columns=["日付", "午前", "午後", "夜"])
    st.table(df_plan)


# メトリクス表示
st.subheader(f"{destination}の気候")
col1, col2, col3 = st.columns(3)
col1.metric("温度", "23°C", "1.5°C")
col2.metric("湿度", "45%", "-5%")
col3.metric("気圧", "1013hPa", "0.1hPa")

# ============================================
# グラフ表示
# ============================================


# ============================================
# インタラクティブ機能
# ============================================


# ============================================
# カスタマイズ
# ============================================

st.markdown("""
<style>
h1 {
    color: #0066cc;
}
[data-testid="stSidebar"] {
    background-color: #161726;
}
</style>
""", unsafe_allow_html=True)

# ============================================
# デモの使用方法
# ============================================
st.divider()
st.subheader("このデモの使い方")
st.markdown("""
1. コードエディタでコメントアウトされた部分を見つけます（#で始まる行）
2. 確認したい機能のコメントを解除します（先頭の#を削除）
3. 変更を保存して、ブラウザで結果を確認します
4. 様々な組み合わせを試して、UIがどのように変化するか確認しましょう
""")

st.code("""
# コメントアウトされた例:
# if st.button("クリックしてください"):
#     st.success("ボタンがクリックされました！")

# コメントを解除した例:
if st.button("クリックしてください"):
    st.success("ボタンがクリックされました！")
""")