# Agent Learning - LLM应用与智能体学习项目

这是一个综合性的学习项目，用于展示和探索不同的LLM应用、智能体(Agents)技术和MCP(Model Context Protocol)调用等前沿技术。

## 🎯 项目目标

- 从基础到高级，系统性地学习LLM应用开发
- 掌握智能体(Agents)技术的实际应用
- 学习MCP工具调用和集成
- 提供可运行的代码示例和最佳实践

## 📁 项目结构

```
agent_learning/
├── docs/                    # 文档和教程
│   ├── tutorials/          # 详细教程
│   ├── api-docs/           # API文档
│   └── best-practices/     # 最佳实践
├── examples/               # 代码示例
│   ├── llm-basics/        # LLM基础应用
│   ├── prompt-engineering/ # Prompt工程
│   ├── agents/            # 智能体应用
│   ├── mcp-tools/         # MCP工具集成
│   └── workflows/         # 工作流应用
├── src/                   # 核心源代码
│   ├── core/             # 核心功能模块
│   ├── agents/           # 智能体实现
│   ├── tools/            # 工具集成
│   └── utils/            # 工具函数
├── config/               # 配置文件
├── tests/                # 测试文件
└── requirements.txt      # 依赖管理
```

## 🚀 学习路径

### 1. LLM基础应用 → [examples/llm-basics/QUICK_START.md](examples/llm-basics/QUICK_START.md) ✅
- ✅ OpenAI API调用
- ✅ OpenRouter API调用
- ✅ 参数调优和配置

### 2. Prompt工程 ✅
- ✅ [基础Prompt编写](examples/prompt-engineering/01_basic_prompt_writing.md) - 掌握清晰指令和结构化Prompt
- ✅ [高级Prompt技巧](examples/prompt-engineering/02_advanced_prompt_techniques.md) - 思维链、Few-shot Learning、角色扮演
- ✅ [上下文管理](examples/prompt-engineering/03_context_management.md) - 长对话处理和记忆机制

### 3. 智能体应用
- [x] 基础智能体实现
- [x] 多智能体协作
- [x] 工作流编排

### 4. MCP工具集成
- [x] MCP协议基础
- [x] 自定义工具开发
- [x] 工具链集成

### 5. 实际应用案例
- [x] 网页爬虫 + LLM分析
- [x] 文档处理智能体
- [x] 代码生成助手

## 🛠️ 技术栈

- **Python**: 主要开发语言
- **OpenAI/OpenRouter**: LLM API
- **LangChain**: 智能体框架
- **MCP**: 模型上下文协议
- **FastAPI**: Web服务框架
- **Streamlit**: 快速原型开发

## 📖 快速开始

1. 克隆项目
```bash
git clone <repository-url>
cd agent_learning
```

2. 安装依赖
```bash
pip install -r requirements-minimal.txt
```

3. 配置环境变量

### Windows环境（推荐）
```bash
python setup_env.py
```
然后编辑生成的 `.env` 文件，填入你的API密钥

### 手动设置
```bash
# 创建.env文件
copy config\env_template.txt .env
# 编辑 .env 文件，添加你的API密钥
```

4. 运行测试
```bash
python examples/llm-basics/test_llm_client.py
```

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个项目！

## 📄 许可证

MIT License

