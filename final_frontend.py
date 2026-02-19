import streamlit as st
import json
import os
import time
from final_backend import stream_agent_response
from database import init_db, save_message, get_all_history
from async_db import async_save_to_db, clear_history, db_queue

# 1. 启动时初始化数据库
init_db()

# 2. 修改消息初始化逻辑：优先从数据库读取
if "messages" not in st.session_state:
    db_history = get_all_history()
    if db_history:
        # 如果数据库有数据，转换格式存入 session_state
        st.session_state.messages = [
            {"role": msg.role, "content": msg.content, "image": msg.image_path}
            for msg in db_history
        ]
    else:
        st.session_state.messages = []

st.set_page_config(page_title="CIL 数据助手", page_icon="📈", layout="centered")
col1, col2 = st.columns([9, 1])
with col2:
    # 巧妙利用 help 参数，鼠标悬停时会有提示
    if st.button("🗑️", help="清空当前历史对话", use_container_width=True):
        clear_history()
        st.session_state.messages = []
        time.sleep(0.1)
        st.rerun()

# ================= CSS 魔法区域 =================
st.markdown("""
<style>
    .stApp {
        background-color: #ffffff;
        color: #333333;
    }

    header, footer, #MainMenu {visibility: hidden;}
    [data-testid="stSidebar"] {display: none;}

    .hero-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 60vh;
        animation: fadeIn 1s ease-in-out;
    }
    .hero-title {
        font-family: -apple-system, BlinkMacSystemFont, sans-serif;
        font-weight: 700;
        font-size: 3.5rem;
        background: linear-gradient(120deg, #1d1d1f, #434344);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    .hero-subtitle {
        color: #86868b;
        font-size: 1.2rem;
        font-weight: 400;
    }

    .top-header {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 60px;
        background-color: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-bottom: 1px solid #f0f0f0;
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1000;
        animation: slideDown 0.5s ease-out;
    }
    .header-title {
        font-family: -apple-system, BlinkMacSystemFont, sans-serif;
        font-weight: 600;
        font-size: 1.1rem;
        color: #333;
    }

    .stChatInputContainer {
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        width: 60%;
        max-width: 800px;
        z-index: 999;
    }


    [data-testid="stChatInput"] {
        border: 1px solid #f0f0f0 !important;
        border-radius: 30px !important;
        background-color: white !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08) !important; /* 浅阴影 */
        color: #333 !important;
    }


    [data-testid="stChatInput"]:focus-within {
        border-color: #FFFFFF !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15) !important; 
        outline: none !important; 
    }

    [data-testid="stChatInput"] input {
        caret-color: #007aff !important; 
    }

    /* 聊天气泡优化 */
    .stChatMessage {
        background-color: transparent !important;
        padding: 1rem 0;
    }
    [data-testid="chatAvatarIcon-user"] {
        background-color: #007aff !important;
        color: white;
    }
    [data-testid="chatAvatarIcon-assistant"] {
        background-color: #f2f2f7 !important;
        color: black;
    }

    /* 动画定义 */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes slideDown {
        from { transform: translateY(-100%); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }

    .main .block-container {
        padding-top: 80px;
        padding-bottom: 120px;
    }
</style>
""", unsafe_allow_html=True)



# 逻辑控制核心

if "messages" not in st.session_state:
    st.session_state.messages = []

# 状态判断
if len(st.session_state.messages) == 0:
    st.markdown("""
        <div class="hero-container">
            <div class="hero-title">CIL Assistant</div>
            <div class="hero-subtitle">专注数据分析 · 极简智能体验</div>
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <div class="top-header">
            <div class="header-title">CIL Assistant</div>
        </div>
    """, unsafe_allow_html=True)

# 聊天流逻辑

# 显示历史记录
for msg in st.session_state.messages:
    avatar = "👤" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])
        if msg.get("image") and os.path.exists(msg["image"]):
            st.image(msg["image"])

# 处理输入
if prompt := st.chat_input("问问 CIL"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    async_save_to_db(role="user", content=prompt)
    st.rerun()

# AI回复逻辑
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":

    with st.chat_message("assistant", avatar="🤖"):
        # 【修改 1】不再提前声明占位符，避免在 Thinking 时显示空行或旧数据

        # 1. 优先声明状态框
        with st.status("⏳ CIL 接收到您的需求，正在分析...", expanded=False) as status:
            try:
                user_msg = st.session_state.messages[-1]["content"]
                raw_output = ""

                # 遍历后端的实时事件流
                for event in stream_agent_response(user_msg, st.session_state.messages[:-1]):
                    if "chatbot" in event:
                        # 获取消息列表
                        curr_messages = event["chatbot"]["messages"]
                        if curr_messages:
                            msg = curr_messages[-1]
                            # 【修改 2】核心过滤逻辑：只有当消息是真正的 AI 回复且有内容时才赋值
                            # 这样可以避免抓取到历史消息或空的 tool_call 消息
                            if hasattr(msg, 'content') and msg.content.strip():
                                raw_output = msg.content

                        # 工具调用逻辑判断
                        if hasattr(msg, 'tool_calls') and msg.tool_calls:
                            for tc in msg.tool_calls:
                                tool_name = tc['name']
                                if tool_name == "calculate":
                                    status.update(label="🔧 正在启动数学引擎，执行最小二乘法计算...")
                                elif tool_name == "search_knowledge_tool":
                                    status.update(label="📚 正在检索本地数据分析知识库...")
                                else:
                                    status.update(label=f"🔧 正在调用工具: {tool_name}...")

                    elif "tools" in event:
                        last_tool_msg = event["tools"]["messages"][-1]
                        finished_tool_name = getattr(last_tool_msg, 'name', '')
                        if finished_tool_name == "calculate":
                            status.update(label="✅ 数据测算完成，正在生成分析报告...")
                        elif finished_tool_name == "search_knowledge_tool":
                            status.update(label="✅ 知识库检索完毕，正在为您整理信息...")
                        else:
                            status.update(label="✅ 工具调用完成，正在汇总...")

                status.update(label="🎯 分析完成！", state="complete")

                # 解析最终的 JSON (增加防御性逻辑)
                answer_text = raw_output
                image_path = None
                try:
                    start_idx = raw_output.find("{")
                    end_idx = raw_output.rfind("}") + 1
                    if start_idx != -1 and end_idx != -1:
                        data = json.loads(raw_output[start_idx:end_idx])
                        answer_text = data.get("answer", raw_output)
                        image_path = data.get("image_file")
                except:
                    pass  # 如果解析失败，直接使用原始 text

            except Exception as e:
                status.update(label="❌ 分析出错", state="error")
                answer_text = f"抱歉，处理时遇到了点问题: {e}"
                image_path = None

        # 2. 状态框处理完毕后，【唯一一次】声明文字占位符
        text_placeholder = st.empty()

        # 流式打字机效果
        full_response = ""
        step = 2
        for i in range(0, len(answer_text), step):
            chunk = answer_text[i:i + step]
            full_response += chunk
            text_placeholder.markdown(full_response + "▌")
            time.sleep(0.01)

        text_placeholder.markdown(full_response)

        # 显示图片
        if image_path and os.path.exists(image_path):
            st.image(image_path)

        # 存入记忆
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer_text,
            "image": image_path
        })

        # 扔给异步队列，后台慢慢存数据库
        async_save_to_db(role="assistant", content=answer_text, image_path=image_path)

        # 强制刷新一下，确保 UI 显示最新状态
        st.rerun()