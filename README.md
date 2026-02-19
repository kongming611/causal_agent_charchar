# 📈 CIL Assistant - 数据分析与趋势预测智能体

> 本项目为 Causal Agent 考核的最终交付物。CIL 是一款基于 LangGraph 状态图架构构建的专业级数据分析 Agent。它融合了底层手工封装的数学建模引擎与前沿的 GraphRAG（图向量双路检索）技术，实现了从感知、思考到精确执行的完整闭环。

## 🌟 核心技术亮点
* **智能体工作流**：采用 **LangGraph `StateGraph`** 构建系统控制中枢。通过严密的**感知 -> 思考 -> 工具调用 -> 响应**状态机循环，彻底解决了原生大模型因自由发挥导致的逻辑失控问题，实现了复杂数据分析任务的确定性编排。
* **纯净的数学计算引擎**：拒绝依赖大模型内部容易产生幻觉的数学推断，也未直接调用臃肿的高级库。纯手工基于 `numpy` 封装普通**最小二乘法 线性回归**算法，实现精准预测与 **Matplotlib** 动态图表渲染。
* **混合检索引擎**：
  * **逻辑精确打击**：引入 `networkx` 构建原子级实体关系图谱，并自主实现基于**本体映射**的同义词对齐与**一跳子图 (1-hop Subgraph)** 提取，保证核心人物与架构关系的 100% 召回。
  * **语义模糊兜底**：结合**HuggingFace** `m3e-base` 词嵌入与 **FAISS** 向量数据库，实现海量文本片段的高效语义匹配。
* **三层异步持久化架构**：采用 `st.session_state` (内存) + `Queue` (多线程缓冲) + `SQLAlchemy / SQLite` (物理硬盘) 的分布式设计理念，实现聊天记录的非阻塞落盘与高可用管理。
* **沉浸式交互体验**：脱离传统命令行，基于 **Streamlit** 深度定制极简 Web UI，支持大模型流式打字机输出、动态思考状态感知及一键清除历史记录。

## 🛠️ 技术栈
 - **架构控制**：LangChain / LangGraph (`StateGraph`)
 - **自然语言处理**：DeepSeek API / HuggingFace Embeddings
 - **检索引擎**：FAISS / NetworkX
 - **数据持久化**：SQLAlchemy / SQLite3 / Threading
 - **科学计算与可视化**：Numpy / Matplotlib
 - **前端渲染**：Streamlit

## 🚀 快速启动
> **前置要求**：建议使用 Python 3.10+ 环境。

### 1. 环境构建与隔离
为了避免依赖冲突，请务必在虚拟环境中运行：
```bash
# 创建并激活虚拟环境
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# 安装黄金版本依赖矩阵
pip install -r requirements.txt --no-cache-dir
```

### 2. 核心模型预热
运行环境部署脚本。该步骤会自动校验本地缓存，秒级完成 RAG 核心嵌入模型（m3e-base）的就位：
```bash
python final_download_model.py
```
### 3. 系统配置
   - 密钥配置：在 **final_backend.py** 中填入你的 DEEPSEEK_API_KEY。
   - 知识库准备：确保根目录下存在 knowledge.txt 文件，内容为您需要智能体检索的知识。

### 4. 一键点火运行
运行内置的自适应启动脚本。该脚本会自动锁定环境路径并唤醒浏览器界面：
```bash
python start.py
```
   - 💡 小贴士：若在 Windows 终端遇到乱码，请确保您的终端已切换至 UTF-8 编码，或直接在 VS Code 内核终端中运行。

## 👨‍💻 开发者信息
### 作者：钟江铭 (广东工业大学 · 材料类)

### 项目归属：Causal Agent 考核项目

