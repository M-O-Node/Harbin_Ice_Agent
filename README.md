# 📋 Harbin-Ice-Agent 2.0: ❄️ 哈尔滨冬季智能导游

> **A Production-Ready Multi-Agent System for Harbin Tourism built with LangGraph, Milvus, and Tavily.**

## 🌟 项目综述 (Overview)
本项目不仅是一个简单的旅游问答机器人，而是一个基于 **ReAct (Reasoning and Acting)** 架构的智能体系统。它能够精准理解南方游客（“小土豆”）的复杂意图，通过自主规划逻辑，联动 **私有知识库 (RAG)** 与 **全网实时搜索**，提供具备时效性、专业性且极具东北人情味的旅游方案。

---

## 🚀 架构演进史 (Evolution of Thought)
*这是我从近 10 年 Java 后端老兵向 AI 架构师转型的技术思考结晶：*

### V1.0: 基础 RAG 模式 (Sequential Pipeline)
*   **实现**：基于 LangChain + Milvus 的线性流程。
*   **痛点**：无法处理长难句和复合需求。系统只是“人找知识”，缺乏主动思考。
*   **总结**：仅能解决 40% 的静态知识问答。

### V2.0: LangGraph 多代理智能体 (Agentic State Machine)
*   **升级点**：引入 **LangGraph** 将线性流程重构为**状态机图架构**。
*   **核心逻辑**：
    *   **Intent Dispatcher (意图分发)**：利用 LLM 自动拆解复杂长句。
    *   **Autonomous Routing (自主路由)**：基于 **Function Calling** 决定调用私有库 (Milvus) 还是实时网 (Tavily)。
    *   **ReAct Loop**：实现了 [思考 -> 行动 -> 观察 -> 再思考] 的闭环，直到获取完美答案。

---

## 🧠 技术核心 (Technical Highlights)

### 1. 模型微调经验 (Fine-tuning Background)
在早期研发中，为了追求极致的文案风格化（如：纪录片级叙事风格），我曾基于 **Qwen1.5-14B** 进行 **SFT (监督微调)** 和 **QLoRA** 训练，产出了 **2.3GB 的适配器 (Adapter)**。
*   **经验所得**：微调决定了模型的“性格与风格”，而 RAG 决定了模型的“事实准确度”。
*   **当前选择**：V2.0 采用 **Qwen2.5-72B API** 作为核心大脑，旨在利用大参数模型的强推理能力来保障 Agent 决策的稳定性。

### 2. 知识库与检索 (RAG & VectorDB)
*   **Milvus**：在阿里云部署企业级 Milvus 集群，存储哈尔滨本地正宗的美食与避坑攻略。
*   **Hybrid Search**：结合 **sentence-transformers** 多语言模型实现高精度的语义检索。

### 3. 可观测性与工程化 (Observability)
*   **Logging System**：完全参照 Java 生产级标准，构建了详细的 `thought.log`，记录 Agent 每一轮的决策链路。
*   **Streamlit UI**：基于 Python 原生界面框架，实现了打字机流式 (Streaming) 输出效果。

---

## 🛠️ 技术栈 (Tech Stack)
*   **Orchestration**: LangGraph, LangChain
*   **LLM**: Qwen2.5-72B-Instruct (via SiliconFlow)
*   **Vector Database**: Milvus (Deployed on Alibaba Cloud ECS)
*   **Real-time Search**: Tavily Search API
*   **UI Framework**: Streamlit
*   **Backend Mindset**: Nearly 10 years of Java Architecture thinking (Design Patterns, Decoupling)

---

## 📦 快速开始 (Quick Start)

1.  **克隆仓库**：
    ```bash
    git clone https://github.com/M-O-Node/Harbin_Ice_Agent.git
    ```
2.  **安装依赖**：
    ```bash
    pip install -r requirements.txt
    ```
3.  **配置环境**：
    在根目录创建 `.env` 文件并填入你的 `OPENAI_API_KEY`, `TAVILY_API_KEY`, `MILVUS_HOST`。
4.  **启动应用**：
    ```bash
    streamlit run ui/app.py
    ```

---

## 🤝 关于作者 (Author)
一名在 Java 后端领域深耕近 10 年，现全身心拥抱 AIGC 浪潮的开发者。我坚信 **"Attention is all you need, but Logic is all you earn"**。我擅长将深厚的后端架构经验与前沿的 Agent 技术结合，构建稳定、高效且能解决实际商业问题的 AI 应用。

---
