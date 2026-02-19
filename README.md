# 📈 CIL Assistant - 数据分析与趋势预测智能体

> 本项目为 Causal Agent 考核的最终交付物。CIL 是一款基于 LangGraph 状态图架构构建的专业级数据分析 Agent。它融合了底层手工封装的数学建模引擎与前沿的 GraphRAG（图向量双路检索）技术，实现了从感知、思考到精确执行的完整闭环。

## 🌟 核心技术亮点 (Key Innovations)

* **智能体工作流 (Agentic Workflow)**：**[核心驱动]** 采用 LangGraph `StateGraph` 构建系统控制中枢。通过严密的“感知 -> 思考 -> 工具调用 -> 响应” (ReAct) 状态机循环，彻底解决了原生大模型因自由发挥导致的逻辑失控问题，实现了复杂数据分析任务的确定性编排。
* **纯净的数学计算引擎**：拒绝依赖大模型内部容易产生幻觉的数学推断，也未直接调用臃肿的高级库。纯手工基于 `numpy` 封装普通最小二乘法 (OLS) 线性回归算法，实现精准预测与 Matplotlib 动态图表渲染。
* **混合检索引擎 (Hybrid GraphRAG)**：
  * **逻辑精确打击**：引入 `networkx` 构建原子级实体关系图谱，并自主实现基于本体映射 (Ontology Mapping) 的同义词对齐与一跳子图 (1-hop Subgraph) 提取，保证核心人物与架构关系的 100% 召回。
  * **语义模糊兜底**：结合 HuggingFace `m3e-base` 词嵌入与 FAISS 向量数据库，实现海量文本片段的高效语义匹配。
* **三层异步持久化架构**：采用 `st.session_state` (内存) + `Queue` (多线程缓冲) + `SQLAlchemy / SQLite` (物理硬盘) 的分布式设计理念，实现聊天记录的非阻塞落盘与高可用管理。
* **沉浸式交互体验**：脱离传统命令行，基于 Streamlit 深度定制极简 Web UI，支持大模型流式打字机输出、动态思考状态感知及一键清除历史记录。

## 🛠️ 技术栈 (Tech Stack)
* **架构控制**：LangChain / LangGraph (`StateGraph`)
* **自然语言处理**：DeepSeek API / HuggingFace Embeddings
* **检索引擎**：FAISS / NetworkX
* **数据持久化**：SQLAlchemy / SQLite3 / Threading
* **科学计算与可视化**：Numpy / Matplotlib
* **前端渲染**：Streamlit

## 🚀 快速启动 (Quick Start)

1. **环境准备**：
   确保环境中已安装所需依赖：
   ```bash
   pip install -r requirements.txt
   ```
2. **预热核心模型**： 运行环境部署脚本，提前拉取并缓存 RAG 核心嵌入模型（m3e-base），确保系统启动时秒级响应： 
   ```bash
   python download_model.py
   ```
3. **配置密钥**： 
   在 **final_backend.py** 中填入有效的 LLM API Key，并确保根目录下存在 **knowledge.txt** 文件。
4. **一键自动化运行**： 直接运行项目内置的启动脚本 **start.py** ，系统将自动绑定运行环境、拉起后端服务并强行唤醒浏览器进入可视化界面：
   ```Bash
   python start.py
   ```

## 👨‍💻 开发者信息
### 作者：钟江铭 (广东工业大学 · 材料类)

### 项目归属：Causal Agent 考核项目
