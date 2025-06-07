
import streamlit as st
import os
import json

# 初始化資料夾與檔案
os.makedirs("data", exist_ok=True)
os.makedirs("story", exist_ok=True)
progress_path = "data/progress.json"
if not os.path.exists(progress_path):
    with open(progress_path, "w") as f:
        json.dump({
            "current_day": 1,
            "max_day": 1,
            "story_unlocked": [],
            "last_result": "none",
            "user_data": {}
        }, f, indent=4)

def load_progress():
    with open(progress_path, "r") as f:
        return json.load(f)

def save_progress(data):
    with open(progress_path, "w") as f:
        json.dump(data, f, indent=4)

quiz_data = {
    1: {
        "title": "Day 1：變數與輸出",
        "lesson": "# 🌟 教學亮點：\n# - 使用變數儲存字串與數字\n# - 使用 print() 印出字串與變數內容\n\nname = \"Alice\"\nage = 20\nprint(name, \"is\", age, \"years old\")",
        "story": "📖 你打開信箱，赫然發現一封寄件人不明的加密郵件，\n標題寫著：「我知道那天晚上誰動了主程式…」",
        "question": "請完成以下程式碼，使其印出：Tom is 15 years old",
        "code": "name = \"____\"\nage = ____\nprint(name, \"is\", age, \"years old\")",
        "answer": ["Tom", "15"],
        "hint": "請注意：字串需要加上雙引號，數字不用。",
        "note": "📌 你得知：當晚主程式的時間戳與伺服器紀錄不一致…"
    }
}

st.set_page_config(page_title="水色之夜：整合版", layout="centered")
st.sidebar.title("🎭 選擇角色")
role = st.sidebar.radio("請選擇要扮演的角色：", ["甯（設計組）", "逸晨（程式組）", "芊芊（音效組）"])

st.title("🌌 水色之夜：健康解謎專題整合版")
st.markdown(f"#### 🎮 目前角色：**{role}**")
st.markdown("---")

progress = load_progress()
current_day = progress["current_day"]
st.markdown(f"### 📅 今天是第 {current_day} 天")

user_data = progress.get("user_data", {})
height = st.number_input("請輸入你的身高 (cm)：", value=user_data.get("height", 160))
weight = st.number_input("請輸入你的體重 (kg)：", value=user_data.get("weight", 50))
location = st.text_input("請輸入你所在的地區：", value=user_data.get("location", "台北"))

if st.button("📌 儲存個人資料"):
    progress["user_data"] = {"height": height, "weight": weight, "location": location}
    save_progress(progress)
    st.success("已儲存！")

suggested_water = weight * 30
suggested_steps = 8000
st.markdown(f"### 今日建議：\n- 建議喝水量：{suggested_water} cc\n- 建議步數：{suggested_steps} 步")

real_water = st.number_input("實際喝水量（cc）：", min_value=0)
real_steps = st.number_input("實際步數：", min_value=0)

if st.button("✅ 提交打卡"):
    if real_water >= suggested_water and real_steps >= suggested_steps:
        quiz = quiz_data.get(current_day)
        if quiz:
            st.success("🎉 打卡成功，解鎖任務挑戰！")
            st.markdown(f"### 📖 故事：\n{quiz['story']}")
            st.code(quiz["lesson"], language="python")
            st.markdown(f"### ❓ 題目：{quiz['question']}")
            st.code(quiz["code"], language="python")
            answer = st.text_input("請輸入填空內容（以逗號分隔）")

            if st.button("🚀 提交答案"):
                inputs = [s.strip() for s in answer.split(",")]
                if inputs == quiz["answer"]:
                    st.success("✅ 答對了！")
                    st.markdown(quiz["note"])
                    if current_day < 21:
                        progress["current_day"] += 1
                    progress["story_unlocked"].append(current_day)
                    progress["last_result"] = "success"
                    save_progress(progress)
                else:
                    st.error("❌ 錯誤，再試一次！")
                    st.info(quiz.get("hint"))
        else:
            st.info(f"Day {current_day} 的故事還沒寫喔！")
    else:
        st.error("喝水或步數未達標，進度已重置！")
        progress["current_day"] = 1
        progress["story_unlocked"] = []
        progress["last_result"] = "fail"
        save_progress(progress)

st.markdown("---")
if st.checkbox("📖 顯示當前日劇情（開發用）"):
    story_path = f"story/day{current_day}.txt"
    if os.path.exists(story_path):
        with open(story_path, "r", encoding="utf-8") as f:
            st.text(f.read())
    else:
        st.info("今天的劇情尚未建立。")
