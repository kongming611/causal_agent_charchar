import numpy as np
import json
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool


@tool
def calc_score(scores_str: str) -> str:
    """
    这是一个数学计算工具。
    只有当用户询问“预测”、“下一次分数”或“趋势”时，一定要调用此工具。
    输入：包含历史分数的字符串，用逗号分隔（例如 "450, 470"）。
    输出：预测结果。
    """
    print(f"AI 正在偷偷调用计算器，处理数据: {scores_str}")
    try:
        y_data = [float(x) for x in scores_str.split(",")]
        x_data = np.arange(1, len(y_data) + 1)

        k, b = np.polyfit(x_data, y_data, 1)
        next_val = k * (len(y_data) + 1) + b
        result = {
            "slope": round(k, 2),
            "prediction": round(next_val, 1),
            "message": "计算成功"
        }
        return json.dumps(result, ensure_ascii=False)

    except Exception as e:
           return f"计算出错: {str(e)}"

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key="sk-e5583ffe66144917aeecf7a2ef750d8e",
    base_url="https://api.deepseek.com/v1"
)

tools = [calc_score]
llm_with_tools = llm.bind_tools(tools)

question = "我是车队的新人，前三次测试数据是 450, 470, 485，帮我预测下一次数据。"

print(f"🗣️ 问: {question}")
print("🤖 AI 正在思考...")

ai_response = llm_with_tools.invoke(question)
print("-" * 30)
print("👀 看看 AI 决定做什么 (Function Calling):")
print(ai_response.tool_calls)
print("-" * 30)