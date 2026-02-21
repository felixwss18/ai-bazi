import streamlit as st
import datetime
import google.generativeai as genai
from lunar_python import Solar, Lunar

# ==========================================
# 1. 底层引擎：绝对精准的排盘计算器
# ==========================================
def calculate_bazi(year, month, day, hour, minute, is_lunar=False):
    if is_lunar:
        date_obj = Lunar.fromYmdHms(year, month, day, hour, minute, 0)
    else:
        date_obj = Solar.fromYmdHms(year, month, day, hour, minute, 0)
        
    lunar_obj = date_obj if is_lunar else date_obj.getLunar()
    bazi = lunar_obj.getEightChar()
    
    return {
        "bazi_str": f"{bazi.getYear()} {bazi.getMonth()} {bazi.getDay()} {bazi.getTime()}",
        "day_master": bazi.getDay()[0]
    }

# ==========================================
# 2. AI 引擎：自动呼叫大模型写报告
# ==========================================
def generate_reading(bazi_str, day_master, api_key):
    # 配置你的 API 钥匙
    genai.configure(api_key=api_key)
    # 我们调用极其聪明的 gemini-1.5-flash 模型
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # 注入我们之前写好的灵魂提示词！
    prompt = f"""
    # Role: 现代派子平八字命理咨询师
    # Profile: 
    你是一位精通中国传统子平八字理论，同时具备现代心理学素养和生活洞察力的命理咨询师。目标是通过八字排盘数据，提供客观、温暖、具有建设性的人生指导。
    
    # Style & Tone:
    1. 专业且通俗：准确运用八字术语并用现代白话文解释。
    2. 客观且赋能：拒绝宿命论，强调“命不可改，运可调”。
    3. 语气：温和、坚定。
    
    # Workflow: 严格用 Markdown 格式输出以下5个模块：
    1. 🌟 【核心原厂设定】 (结合日主性格底色)
    2. 💼 【事业与财富指南】 
    3. ❤️ 【人际与情感洞察】 
    4. ⏳ 【近期运势导航】 
    5. 🛠️ 【专属行动锦囊】 
    
    # Constraints: 绝对禁止预测寿命、死亡、重大疾病。绝对禁止负面词汇。
    
    =========
    用户输入数据如下：
    八字：{bazi_str}
    核心日主：{day_master}
    
    请立刻开始生成专属解析报告：
    """
    
    # 呼叫 AI 开始写作文
    response = model.generate_content(prompt)
    return response.text

# ==========================================
# 3. 前端网页：华丽的交互界面
# ==========================================
st.set_page_config(page_title="AI 命理师", page_icon="🔮", layout="wide")

# 【新增功能】在左侧边栏输入 API Key，保护隐私
with st.sidebar:
    st.header("⚙️ 引擎设置")
    api_key_input = st.text_input("🔑 请输入您的 Gemini API Key", type="password")
    st.caption("没有 Key？[点此免费获取](https://aistudio.google.com/app/apikey)")
    st.divider()
    st.write("💡 提示：将 Key 填入上方后，右侧的算命按钮才会真正激活哦！")

st.title("🔮 我的专属 AI 命理师 (全自动版)")
st.write("输入出生信息，一键排盘并自动生成万字命理解析报告。")
st.divider()

col1, col2 = st.columns(2)
with col1:
    calendar_type = st.selectbox("📅 选择历法", ["公历 (阳历)", "农历 (阴历)"])
    is_lunar = True if calendar_type == "农历 (阴历)" else False

with col2:
    birthday = st.date_input("🎂 出生日期", datetime.date(1979, 11, 18), min_value=datetime.date(1900, 1, 1))
    birth_time = st.time_input("⏰ 出生时间", datetime.time(9, 33))

# 终极大按钮
if st.button("✨ 立即排盘 & 呼叫 AI 解读 ✨", type="primary", use_container_width=True):
    if not api_key_input:
        st.error("⚠️ 启动失败！请先在左侧边栏输入您的 API Key。")
    else:
        # 当输入了 Key 后，显示一个酷炫的加载动画
        with st.spinner("🔮 八字引擎与 AI 模型正在高速运转中，请稍候 10 秒..."):
            try:
                # 1. 跑计算代码
                result = calculate_bazi(birthday.year, birthday.month, birthday.day, birth_time.hour, birth_time.minute, is_lunar)
                
                # 2. 跑 AI 代码
                ai_report = generate_reading(result['bazi_str'], result['day_master'], api_key_input)
                
                # 3. 把结果展示在网页上
                st.success("🎉 解析完成！请查收您的专属报告。")
                st.subheader("📜 您的生辰八字：")
                st.code(result['bazi_str'], language="text")
                
                st.divider()
                st.markdown(ai_report) # 完美排版输出 AI 报告
            
            except Exception as e:
                st.error(f"❌ 哎呀，AI 接口调用出错啦。请检查您的 API Key 是否正确。错误详情：{e}")
