from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key="sk-e5583ffe66144917aeecf7a2ef750d8e",
    base_url="https://api.deepseek.com/v1"
)

print("正在连线 DeepSeek 大脑...")
response = llm.invoke("你好，我是一个正在准备转专业的广东工业大学大一学生，请用一句话鼓励我。")

print(f"AI 说: {response.content}")