import numpy as np
import json
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langchain.agents import create_agent

@tool
def calc_score(scores_str: str) -> str:
    """预测分数的工具。输入用逗号分隔的数字，如 "450, 470" """
    try:
        y_data = [float(x) for x in scores_str.split(",")]
        x_data = np.arange(1, len(y_data) + 1)
        k, b = np.polyfit(x_data, y_data, 1)
        next_val = k * (len(y_data) + 1) + b
        result = {"slope": round(k, 2), "prediction": round(next_val, 1)}
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        return f"出错: {str(e)}"

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key="sk-",
    base_url="https://api.deepseek.com/v1"
)

agent = create_agent(llm, tools=[calc_score])

print("\n========== 第一回合：算数与身份录入 ==========")
input1 = "学长你好，我是广工准备转专业去计算机的学弟，我女朋友叫蕾蕾。前三次C语言成绩是 450, 470, 485，预测下一次？"
print(f"🗣️ 问: {input1}")

res1 = agent.invoke({"messages": [HumanMessage(content=input1)]})
print(f"🤖 AI: {res1['messages'][-1].content}")

print("\n========== 第二回合：记忆大考验 ==========")
input2 = "学长，我刚才给你的三次分数分别是多少？还有，记得我女朋友叫什么吗？"
print(f"🗣️ 问: {input2}")

new_messages = res1['messages'] + [HumanMessage(content=input2)]
res2 = agent.invoke({"messages": new_messages})
print(f"🤖 AI: {res2['messages'][-1].content}")