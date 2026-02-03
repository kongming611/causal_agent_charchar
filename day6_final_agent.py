import numpy as np
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

x_data = np.array([1, 2, 3, 4])
y_data = np.array([450, 470, 485, 500])

k, b = np.polyfit(x_data, y_data, 1)
x_future = 5
y_future = k * x_future + b

history_str = "，".join(map(str, y_data))
future_score = round(y_future, 1)
print(f"✅ 本地计算完成！预测第5次分数为：{future_score}")

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key="sk-***",
    base_url="https://api.deepseek.com/v1"
)

template = """
你现在是广东工业大学计算机学院的王牌导师。
有一个大一学生正在备考转专业，他的前四次测试成绩是：{history}。
我用最小二乘法帮他预测了，第5次他能考到：{prediction} 分。

请根据这组数据，用简短、有力、像工科导师一样的口吻：
1. 分析他的成绩趋势（他进步有多快？）。
2. 给他针对转专业（特别是 C语言和离散数学）的最后冲刺建议。
"""

prompt = PromptTemplate(
    input_variables=["history", "prediction"],
    template=template
)

chain = prompt | llm
print("🚀 正在将数据发送给 DeepSeek 进行专家分析...")

response = chain.invoke({
    "history": history_str,
    "prediction": future_score
})

print("-" * 50)
print(f"👨‍🏫 导师分析报告:\n{response.content}")
print("-" * 50)