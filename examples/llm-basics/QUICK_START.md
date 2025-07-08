# 🚀 LLM基础应用快速开始

## 概述

本目录包含LLM基础应用的示例代码，帮助你快速上手不同的LLM API调用。

## 📁 文件结构

```
examples/llm-basics/
├── QUICK_START.md          # 本文件 - 快速开始指南
├── test_llm_client.py      # LLM客户端测试脚本
├── openai_demo.py          # OpenAI API示例
├── openrouter_demo.py      # OpenRouter API示例
└── anthropic_demo.py       # Anthropic API示例
```

## 🎯 学习目标

- 掌握不同LLM API的基本调用方法
- 了解参数调优和配置技巧
- 学会处理API响应和错误
- 为后续智能体开发打下基础

## 🔧 环境准备

### 1. 安装依赖
```bash
pip install -r ../../requirements-minimal.txt
```

### 2. 配置API密钥
在项目根目录创建 `.env` 文件：
```
OPENAI_API_KEY=your_openai_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```
(可以在[openrouter](https://openrouter.ai/)注册key使用)

## 🚀 快速开始

### 1. 测试LLM客户端
```bash
python test_llm_client.py
```

## 📚 核心概念

### LLM客户端架构
- `BaseLLMClient`: 抽象基类，定义统一接口
- `OpenAIClient`: OpenAI API实现
- `OpenRouterClient`: OpenRouter API实现
- `AnthropicClient`: Anthropic API实现
- `LLMClient`: 统一管理器，支持动态切换

### 主要方法
- `chat_completion()`: 聊天完成接口
- `text_completion()`: 文本完成接口
- `switch_provider()`: 切换LLM提供商

## 🔍 示例代码

### 基础对话
```python
from src.core.llm_client import LLMClient

# 创建客户端
client = LLMClient(provider="openai")

# 发送消息
messages = [
    {"role": "user", "content": "你好，请介绍一下自己"}
]

response = await client.chat_completion(messages)
print(response["content"])
```

### 文本完成
```python
prompt = "人工智能的未来是"
response = await client.text_completion(prompt, max_tokens=100)
print(f"{prompt}{response}")
```

## 🛠️ 参数调优

### 常用参数
- `max_tokens`: 最大输出token数
- `temperature`: 创造性控制 (0-2)
- `top_p`: 核采样参数 (0-1)
- `frequency_penalty`: 频率惩罚
- `presence_penalty`: 存在惩罚

### 示例
```python
response = await client.chat_completion(
    messages,
    max_tokens=500,
    temperature=0.7,
    top_p=0.9,
    frequency_penalty=0.1
)
```

## 🔧 故障排除

### 常见问题
1. **API密钥错误**: 检查环境变量设置
2. **网络连接**: 确认网络连接正常
3. **配额限制**: 检查API使用额度
4. **模型不可用**: 确认模型名称正确

### 调试技巧
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# 启用详细日志
client = LLMClient(provider="openai")
```

## 📖 下一步

完成LLM基础应用学习后，可以继续：

1. **Prompt工程** → [../prompt-engineering/](../prompt-engineering/)
2. **智能体应用** → [../agents/](../agents/)
3. **MCP工具集成** → [../mcp-tools/](../mcp-tools/)

## 🤝 贡献

欢迎提交改进建议和代码示例！ 