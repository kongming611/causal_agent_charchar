from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key="sk-e5583ffe66144917aeecf7a2ef750d8e",
    base_url="https://api.deepseek.com/v1"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个善良体贴的男生，对女朋友讲话要温柔、有同理心。"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
])

chain = prompt | llm

store = {}
def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

agent_with_memory = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history"
)

print("第一回合：告诉 AI 你的名字")
response1 = agent_with_memory.invoke(
    {"input": "你好，我是蕾蕾男朋友，我叫钟江铭。"},
    config={"configurable": {"session_id": "session_001"}}
)
print(f"🤖 AI: {response1.content}\n")

print("第二回合：测试 AI 的记忆力")
response2 = agent_with_memory.invoke(
    {"input": "你还记得我叫什么名字，女朋友是谁吗？"},
    config={"configurable": {"session_id": "session_001"}}
)
print(f"🤖 AI: {response2.content}")