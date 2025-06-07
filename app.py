            "last_result": "none",
            "user_data": {}
        }, f, indent=4)

# 載入進度
def load_progress():
    with open("data/progress.json", "r") as f:
        return json.load(f)

# 儲存進度
def save_progress(data):
    with open("data/progress.json", "w") as f:
        json.dump(data, f, indent=4)

# Streamlit 頁面設定
st.set_page_config(page_title="水色之夜：整合版", layout="centered")

st.sidebar.title("🎭 選擇角色")
role = st.sidebar.radio("請選擇要扮演的角色：", ["甯（設計組）", "逸晨（程式組）", "芊芊（音效組）"])

st.title("🌌 水色之夜：健康解謎專題整合版")
st.markdown("---")
st.markdown(f"#### 🎮 目前角色：**{role}**")

# 載入進度
progress = load_progress()
current_day = progress["current_day"]
st.markdown(f"### 📅 今天是第 {current_day} 天")

# 取得使用者資料（身高體重地區）
user_data = progress.get("user_data", {})

height = st.number_input("請輸入你的身高 (cm)：", value=user_data.get("height", 160))
weight = st.number_input("請輸入你的體重 (kg)：", value=user_data.get("weight", 50))
location = st.text_input("請輸入你所在的地區：", value=user_data.get("location", "台北"))

if st.button("📌 儲存個人資料"):
    progress["user_data"] = {
        "height": height,
        "weight": weight,
        "location": location
    }
    save_progress(progress)
    st.success("已儲存！")

# 建議值
suggested_water = weight * 30
suggested_steps = 8000

st.markdown(f"### 今日建議：\n- 建議喝水量：{suggested_water} cc\n- 建議步數：{suggested_steps} 步")

real_water = st.number_input("實際喝水量（cc）：", min_value=0)
real_steps = st.number_input("實際步數：", min_value=0)

# 打卡與故事顯示按鈕
if st.button("✅ 提交打卡"):
    if real_water >= suggested_water and real_steps >= suggested_steps:
        story_path = f"story/day{current_day}.txt"
        if os.path.exists(story_path):
            with open(story_path, "r", encoding="utf-8") as f:
                story_text = f.read()
        else:
            story_text = f"Day {current_day} 的故事還沒寫喔！"

        st.success(f"🎉 Day {current_day} 打卡成功！")
        st.info(story_text)

        # 更新進度
        if current_day < 21:
            progress["current_day"] += 1
        progress["max_day"] = max(progress["max_day"], progress["current_day"])
        progress["story_unlocked"].append(current_day)
        progress["last_result"] = "success"
        save_progress(progress)
    else:
        st.error("喝水或步數未達標，進度已重置！")
        progress["current_day"] = 1
        progress["story_unlocked"] = []
        progress["last_result"] = "fail"
        save_progress(progress)

# 顯示當前劇情（測試用）
st.markdown("---")
if st.checkbox("📖 顯示當前日劇情（開發用）"):
    story_path = f"story/day{current_day}.txt"
    if os.path.exists(story_path):
        with open(story_path, "r", encoding="utf-8") as f:
            st.text(f.read())
    else:
        st.info("今天的劇情尚未建立。")
