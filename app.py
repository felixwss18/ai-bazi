import streamlit as st
import datetime
import google.generativeai as genai
from lunar_python import Solar, Lunar

# ==========================================
# 1. 底层引擎：排盘计算器
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
    genai.configure(api_key=api_key)
    # 使用最新的稳定版模型
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = f"""
    # Role: AI 命理预测大师 (传统玄学与现代心理学双修)
    # Profile: 
    你是一位顶级的命理咨询师。你不仅精通子平八字底层的“五行生克制化”与“神煞造化”，更具备深厚的现代心理咨询视角。你能将晦涩的玄学密码，翻译成直击灵魂、温暖且极具实操性的人生指南。
    
    # Style & Tone:
    1. 骨相为玄学：分析必须带有极强的专业度，明确点出原局的“五行喜忌”、“生克关系”以及关键的“神煞”（如贵人、桃花、驿马、羊刃、文昌等）。
    2. 皮相为心理学：将神煞和五行生克转化为现代人的性格特质、潜意识驱动力以及人际互动模式。
    3. 灵魂为赋能：拒绝宿命论！强调“知命而造命”。语气要像一位睿智、包容且极具洞察力的老友。
    
    # Workflow: 请严格按以下 5 个模块使用 Markdown 输出排版精美的万字报告：
    
    1. 🌌 【原局拆解：五行生克与生命底色】
       - 解析日主特质，并重点分析八字原局的五行强弱、生克制化关系。说明这种五行结构造就了怎样的内在性格底色与核心矛盾。
    
    2. 🌟 【神煞造化：隐藏的潜能天赋】
       - 找出命局中的关键神煞，用现代视角重新定义。例如：“桃花”不仅是情感，更是自带观众缘和品牌感染力，适合社交或视觉展现；“文昌”不仅是读书，更是卓越的内容创作与审美能力；“驿马”代表跨界与变动。
    
    3. 🧠 【心理画像：情感与人际深度洞察】
       - 结合五行与十神，用心理学视角分析其在亲密关系、合伙团队中的互动模式、防御机制，并给出疗愈建议。
    
    4. 💼 【财富与事业定位：顺势而为的策略】
       - 根据五行喜忌，精准推荐适合的行业属性与工作节奏。如果是喜火/社交，如何利用人脉操盘项目；如果喜木/水，如何沉淀技能。给出最容易拿到结果的搞钱策略。
    
    5. ⏳ 【造化流转：近期运势与专属行动锦囊】
       - 点评近一两年的大运流年气象。
       - 给出 3 条具体到极点的现代开运行动（可涵盖穿搭色彩、生活微习惯、饮食偏好或社交策略）。
    
    # Constraints: 绝对禁止预测寿命、死亡、重大疾病。严禁使用“克夫/克妻/命中破财”等绝对化的恐惧营销词汇。
    
    =========
    用户输入数据如下：
    八字：{bazi_str}
    核心日主：{day_master}
    
    请立刻开始生成您的深度专业解析报告：
    """
    
    response = model.generate_content(prompt)
    return response.text

# ==========================================
# 3. 前端网页：极简版 UI
# ==========================================
st.set_page_config(page_title="AI 命理师", page_icon="🔮", layout="wide")
# ==========================================
# 💎 注入高级 UI 样式 (CSS 魔法)
# ==========================================
st.markdown("""
<style>
    /* 1. 隐藏 Streamlit 官方的右上角菜单、底部水印和顶部装饰条 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 2. 全局背景优化 (打造高级的暗夜玄学风) */
    .stApp {
        background-color: #0E1117;
        font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
    }
    
    /* 3. 让输入框看起来更高端 */
    div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {
        background-color: #1E2329 !important;
        border-radius: 8px !important;
        border: 1px solid #333 !important;
        color: white !important;
    }
    
    /* 4. 🌟 终极必杀：极光渐变色大按钮 */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #FF416C 0%, #FF4B2B 100%) !important;
        color: white !important;
        font-size: 18px !important;
        font-weight: bold !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 15px 24px !important;
        box-shadow: 0 4px 15px rgba(255, 65, 108, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    
    /* 按钮悬停时的动态发光效果 */
    div.stButton > button:first-child:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(255, 65, 108, 0.6) !important;
    }
    
    /* 5. 优化分割线的质感 */
    hr {
        border-top: 1px solid #2B2B2B !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("🔮 我的 AI 命理师 🔮")
st.write("输入出生信息，一键排盘并自动生成命理解析报告。")
st.divider()

col1, col2 = st.columns(2)
with col1:
    calendar_type = st.selectbox("📅 选择历法", ["公历 (阳历)", "农历 (阴历)"])
    is_lunar = True if calendar_type == "农历 (阴历)" else False

with col2:
    birthday = st.date_input("🎂 出生日期", datetime.date(2000, 1, 1), min_value=datetime.date(1900, 1, 1))
    birth_time = st.time_input("⏰ 出生时间", datetime.time(12, 0))

# ==========================================
# 🚀 魔法核心：从云端保险箱自动读取 Key
# ==========================================
# 无论谁打开网页，代码都会自动去刚才设置的 Secrets 里找钥匙
api_key_secret = st.secrets["GEMINI_API_KEY"]

if st.button("✨ 立即排盘 & AI 解读 ✨", type="primary", use_container_width=True):
    with st.spinner("🔮 八字引擎与 AI 模型正在高速运转中，请稍候 15 秒..."):
        try:
            result = calculate_bazi(birthday.year, birthday.month, birthday.day, birth_time.hour, birth_time.minute, is_lunar)
            # 使用保险箱里的钥匙呼叫 AI
            ai_report = generate_reading(result['bazi_str'], result['day_master'], api_key_secret)
            
            st.success("🎉 解析完成！请查收您的专属报告。")
            st.subheader("📜 您的生辰八字：")
            st.code(result['bazi_str'], language="text")
            
            st.divider()
            st.markdown(ai_report) 
            
            try:
                # 这里的 "qr.jpg" 必须和你上传的图片名字一模一样
                st.image("qr.jpg", width=250, caption="支持 Touch 'n Go / DuitNow 扫码")
            except Exception as e:
                st.info("💡 提示：请确保已将打赏二维码 (qr.jpg) 上传至系统。")
            
        except Exception as e:
            st.error(f"❌ 哎呀，AI 接口调用出错啦。错误详情：{e}")
