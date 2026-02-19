import numpy as np
import matplotlib.pyplot as plt
import os
import networkx as nx

# 配置HuggingFace国内镜像源
os.environ['http_proxy'] = ''
os.environ['https_proxy'] = ''
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
os.environ["HF_HUB_OFFLINE"] = "1"

try:
    from langchain_core.tools import tool
except ImportError:
    from langchain.tools import tool

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# 配置画图字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False


@tool
def calculate(data_str: str) -> str:
    """
    【必须调用】当且仅当用户提供了一组或多组坐标数据（如 "1,450; 2,470..."），并要求预测、分析趋势或计算下一项时，必须调用此工具。
    严禁使用大模型内部知识进行口算或推断。
    本工具基于"最小二乘法"进行精确计算。
    输入格式示例: "1,450; 2,470; 3,485"
    """
    try:
        points = []
        clean_str = data_str.replace('（', '(').replace('）', ')').replace('；', ';').replace('，', ',')

        for pair in clean_str.split(';'):
            if not pair.strip():
                continue
            pair_clean = pair.strip().strip('()')
            if not pair_clean:
                continue
            x_str, y_str = pair_clean.split(',')
            points.append((float(x_str), float(y_str)))

        if len(points) < 2:
            return "数据点太少，无法计算趋势，请至少提供两个坐标点。"

        X = np.array([p[0] for p in points])
        Y = np.array([p[1] for p in points])

        n = len(X)
        mean_x = np.mean(X)
        mean_y = np.mean(Y)

        numerator = np.sum(X * Y) - n * mean_x * mean_y
        denominator = np.sum(X ** 2) - n * (mean_x ** 2)

        if denominator == 0:
            return "计算失败：数据垂直共线（X值完全相同），无法拟合。"

        w = numerator / denominator
        b = mean_y - w * mean_x

        next_x = X[-1] + 1
        prediction = w * next_x + b

        plt.figure(figsize=(8, 5))
        plt.scatter(X, Y, color='blue', label='历史数据', s=100)
        x_line = np.linspace(min(X), next_x, 100)
        y_line = w * x_line + b
        plt.plot(x_line, y_line, color='red', linestyle='--', label=f'拟合线')
        plt.scatter([next_x], [prediction], color='green', marker='*', s=200, label=f'预测值')

        plt.title("线性回归趋势预测")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.legend()
        plt.grid(True, linestyle=':', alpha=0.6)

        img_path = "trend_plot.png"
        plt.savefig(img_path, bbox_inches='tight')
        plt.close()

        return f"计算完成。拟合方程: y={w:.2f}x+{b:.2f}。基于最小二乘法，x={next_x}时的预测值为: {prediction:.2f}。图表已保存至: {img_path}"

    except Exception as e:
        return f"计算过程出错: {str(e)}"


knowledge_graph = nx.DiGraph()
# 实体原子化解耦
knowledge_graph.add_edge("CIL系统", "钟江铭", relation="开发者")
knowledge_graph.add_edge("钟江铭", "广东工业大学", relation="就读高校")
knowledge_graph.add_edge("钟江铭", "材料类", relation="就读专业")
knowledge_graph.add_edge("CIL系统", "CausalAgent", relation="所属考核项目")
knowledge_graph.add_edge("CIL系统", "最小二乘法", relation="核心数学引擎")
knowledge_graph.add_edge("CIL系统", "LangGraph", relation="底层控制架构")

# 概念本体映射表 (Ontology Mapping) - 工业界用于高精度实体对齐
ontology_mapping = {
    "CIL系统": ["系统", "助手", "智能体", "项目"],
    "钟江铭": ["作者", "开发", "同学", "谁做", "哪位"],
    "广东工业大学": ["学校", "哪所大学", "院校"],
    "材料类": ["专业", "读什么", "哪个系"],
    "LangGraph": ["架构", "控制", "底层", "工作流"],
    "最小二乘法": ["怎么算", "算法", "原理", "核心引擎"]
}


def retrieve_from_graph(query: str) -> str:
    """基于本体映射的图谱子图生成器"""
    graph_context = []
    matched_nodes = set()

    # 实体链接将自然语言锚定到图谱节点
    for node, aliases in ontology_mapping.items():
        if node in query:
            matched_nodes.add(node)
        else:
            for alias in aliases:
                if alias in query:
                    matched_nodes.add(node)
                    break

    # 如果找到了实体，提取其一跳子图
    for node in matched_nodes:
        for neighbor in knowledge_graph.successors(node):
            rel = knowledge_graph.edges[node, neighbor]['relation']
            graph_context.append(f"【知识图谱事实】: {node} 的 {rel} 是 {neighbor}。")
        for predecessor in knowledge_graph.predecessors(node):
            rel = knowledge_graph.edges[predecessor, node]['relation']
            graph_context.append(f"【知识图谱事实】: {predecessor} 的 {rel} 是 {node}。")

    return "\n".join(list(set(graph_context))) if graph_context else ""


@tool
def search_knowledge_tool(query: str) -> str:
    """
    【最高优先级调用】当用户问“你是谁”、“谁做了你”、“你的作者是谁”、“你的身世”，以及询问CIL项目介绍、考核要求时，必须调用此工具！
    输入参数为用户的查询问题。本工具采用了 GraphRAG（图+向量双路检索）架构。
    """
    final_context = []

    # --- 路径 A：知识图谱精确检索 ---
    graph_info = retrieve_from_graph(query)
    if graph_info:
        final_context.append("--- 知识图谱结构化数据 ---")
        final_context.append(graph_info)
        print("\n命中图谱数据！抓取到：", graph_info)

    # --- 路径 B：HuggingFace + FAISS 向量模糊检索 ---
    if os.path.exists("knowledge.txt"):
        try:
            loader = TextLoader("knowledge.txt", encoding="utf-8")
            docs = loader.load()

            splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
            texts = splitter.split_documents(docs)

            # 这里就是HuggingFace
            embeddings = HuggingFaceEmbeddings(model_name="moka-ai/m3e-base")
            vector_store = FAISS.from_documents(texts, embeddings)

            retriever = vector_store.as_retriever(search_kwargs={"k": 2})
            results = retriever.invoke(query)

            vector_info = "\n".join([doc.page_content for doc in results])
            if vector_info:
                final_context.append("--- 向量库语义匹配数据 ---")
                final_context.append(vector_info)
                print("\n命中向量库！抓取到：", vector_info[:50], "...")

        except Exception as e:
            print(f"向量库检索失败: {str(e)}")

    if final_context:
        return "\n".join(final_context)
    else:
        return "本地双路知识库中未找到相关信息。"