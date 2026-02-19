import os
import json
from typing import Annotated
from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from final_my_tools import calculate, search_knowledge_tool


os.environ["OPENAI_API_KEY"] = "sk-e5583ffe66144917aeecf7a2ef750d8e"
os.environ["OPENAI_API_BASE"] = "https://api.deepseek.com/v1"


# LangGraph 构建区域
# 1. 定义状态
class State(TypedDict):
    messages: Annotated[list, add_messages]


# 2. 初始化大模型并绑定工具
llm = ChatOpenAI(model="deepseek-chat", temperature=0)
tools = [calculate, search_knowledge_tool]
llm_with_tools = llm.bind_tools(tools)

# System Prompt
system_prompt = SystemMessage(content="""
你是一个名为 CIL 的专业数据分析智能体。

【你的核心原则】
1. **数学限制**：你绝对不能使用自己的大脑进行任何复杂的数学推断。
2. **工具依赖**：遇到任何需要预测趋势或包含坐标的数据，你必须调用 `calculate` 工具。
3. **精准性**：你的预测结果必须直接引用工具返回的数值，绝不能篡改或自己估算。

【语气与人设设定】
你是一位专业但具备“些许人情味”的数据分析助手。
在客观、精准地汇报完数据和计算结果后，你应该结合数据趋势，用一到两句简短的自然语言给出一点关怀或中肯的洞察（例如：面对工资增长可以说“涨幅可观，继续保持高质量的输出”，面对成绩可以给一句简短的鼓励）。
**严格注意**：必须克制！保持高知精英的专业素养，绝不要过度热情、不要废话连篇，点到为止即可，但是可以发表情包。

【最终输出格式】
你最终给用户的回复必须严格遵守 JSON 格式，不要输出任何 Markdown 标记（如 ```json）：
{
    "answer": "这里写你的回复内容（包含数据结果+几句简短关怀）",
    "image_file": "trend_plot.png" (如果工具返回了图表路径则填入，否则填 null)
}
""")


# 3. 定义大模型节点处理逻辑
def chatbot_node(state: State):
    messages = state["messages"]
    if not messages or not isinstance(messages[0], SystemMessage):
        current_messages = [system_prompt] + messages
    else:
        current_messages = messages

    response = llm_with_tools.invoke(current_messages)
    return {"messages": [response]}


# 4. 构建图表
graph_builder = StateGraph(State)

# 添加节点
graph_builder.add_node("chatbot", chatbot_node)
tool_node = ToolNode(tools=tools)
graph_builder.add_node("tools", tool_node)

# 添加边和流转条件
graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", tools_condition)
graph_builder.add_edge("tools", "chatbot")

agent_graph = graph_builder.compile()


def stream_agent_response(user_input, history):
    langchain_messages = []
    for msg in history:
        if msg["role"] == "user":
            langchain_messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            langchain_messages.append(AIMessage(content=msg["content"]))

    langchain_messages.append(HumanMessage(content=user_input))

    for event in agent_graph.stream({"messages": langchain_messages}, stream_mode="updates"):
        yield event

    final_state = agent_graph.invoke({"messages": langchain_messages})

    final_message = final_state["messages"][-1]

    return {"output": final_message.content}