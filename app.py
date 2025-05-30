
import streamlit as st

# 頁面設定
st.set_page_config(page_title="水色之夜：程設專題解謎遊戲", layout="centered")

# 側邊欄角色選擇
st.sidebar.title("🎭 選擇你的角色")
role = st.sidebar.radio("請選擇要扮演的角色：", ["甯（設計組）", "逸晨（程式組）", "芊芊（音效組）"])

# 顯示標題
st.title("🌌 水色之夜：程設專題解謎遊戲")
st.markdown("---")

# 顯示目前角色
st.markdown(f"#### 🎮 你目前的身份：**{role}**")

# 日期輸入（1~21天）
day = st.number_input("📅 今天是第幾天？（1-21）", min_value=1, max_value=21, step=1)
st.markdown("---")

# 劇情資料（示範 Day 1）
story = {
    1: {
        "甯（設計組）": "【Day 1】你正在整理專題介面草稿，突然系統彈出一個陌生訊息視窗，上面寫著：『宥晴，不該消失的人。』",
        "逸晨（程式組）": "【Day 1】你在 debug 資料夾中，發現一段陌生 commit 記錄，上面寫著 'yo_ching_last_push'，但你從未見過這串帳號。",
        "芊芊（音效組）": "【Day 1】你今天剪音檔時發現，背景裡夾雜著一段低語：『那天，其實我沒走。』"
    }
}

# 顯示對應劇情
if day in story and role in story[day]:
    st.subheader(f"📖 第 {day} 天")
    st.write(story[day][role])
else:
    st.warning("這一天尚未完成劇情建置，請等待後續開發。")

# 模擬互動選項（未來可擴充）
if day == 1:
    st.markdown("### 🧩 請選擇你的行動：")
    if st.button("打開訊息視窗"):
        st.info("你發現一段加密訊息：yo_ching0410.txt，但你無法立即打開。")
    if st.button("關閉並繼續作業"):
        st.success("你決定先無視異常，專心設計今天的 prototype 流程圖。")
