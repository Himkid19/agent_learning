# 上下文管理

## 📖 简介

在长对话和复杂任务中，有效的上下文管理是LLM应用成功的关键。本教程将介绍如何管理对话历史、处理上下文长度限制、实现记忆机制，以及优化上下文使用效率。

## 🎯 学习目标

- 理解上下文窗口和长度限制
- 掌握对话历史管理技巧
- 学会上下文压缩和摘要技术
- 实现持久化记忆机制
- 优化上下文使用效率

## 🧩 上下文基础概念

### 上下文窗口

```markdown
# 不同模型的上下文限制:
- GPT-3.5: 4,096 tokens
- GPT-4: 8,192 tokens (部分版本支持32K)
- GPT-4 Turbo: 128,000 tokens
- Claude-3: 200,000 tokens

# Token估算技巧:
- 1个中文字符 ≈ 2-3 tokens
- 1个英文单词 ≈ 1-2 tokens
- 1页A4文档 ≈ 500-800 tokens
```

### 上下文结构

```markdown
# 标准上下文结构:
[系统消息] + [对话历史] + [当前输入] = 总上下文

示例:
System: "你是一个Python编程助手..."     (50 tokens)
History: 前10轮对话                    (2000 tokens)
User: "请解释装饰器的用法"              (20 tokens)
Total: 2070 tokens
```

## 💾 对话历史管理

### 基础历史管理

```python
class ConversationManager:
    def __init__(self, max_history=10):
        self.messages = []
        self.max_history = max_history
    
    def add_message(self, role, content):
        """添加消息到历史记录"""
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now()
        })
        
        # 保持历史记录在限制范围内
        if len(self.messages) > self.max_history:
            self.messages = self.messages[-self.max_history:]
    
    def get_context(self):
        """获取格式化的上下文"""
        context = ""
        for msg in self.messages:
            context += f"{msg['role']}: {msg['content']}\n"
        return context
```

## 🗜️ 上下文压缩技术

### 对话摘要

```markdown
# 摘要Prompt模板:
你是对话摘要专家。请将以下对话压缩成简洁的摘要，保留关键信息。

## 摘要要求:
1. 保留所有重要决定和结论
2. 记录关键的技术细节
3. 保持用户的核心问题和AI的主要建议
4. 压缩比例: 原文的20-30%

## 对话内容:
{conversation_history}

## 摘要格式:
**主要讨论**: [核心话题]
**关键决定**: [重要结论]
**技术要点**: [技术细节]
**待解决**: [未完成的问题]

请生成摘要:
```

## 🧠 记忆机制

### 分层记忆架构

```python
class MemorySystem:
    def __init__(self):
        self.working_memory = []      # 当前对话
        self.short_term_memory = []   # 最近会话摘要
        self.long_term_memory = {}    # 持久化知识
        self.episodic_memory = []     # 重要事件
    
    def update_working_memory(self, message):
        """更新工作记忆"""
        self.working_memory.append(message)
        
        # 工作记忆满了，转移到短期记忆
        if len(self.working_memory) > 10:
            self.consolidate_to_short_term()
```

## 🔗 项目链接

### 相关代码示例:
- [基础Prompt编写](./01_basic_prompt_writing.md) - Prompt基础知识
- [高级Prompt技巧](./02_advanced_prompt_techniques.md) - 高级Prompt策略
- [LLM客户端](../llm-basics/test_llm_client.py) - API调用实现

### 实践项目:
- [智能体应用](../agents/) - 在智能体中实现记忆机制
- [工作流应用](../workflows/) - 长流程的上下文管理
- [环境配置](../../config/env_template.txt) - 配置不同模型的上下文限制

### 扩展学习:
- [MCP工具集成](../mcp-tools/) - 工具调用中的上下文处理

## 💡 最佳实践

### 1. 上下文设计原则
- **清晰性**: 上下文结构要清晰易懂
- **相关性**: 只包含与当前任务相关的信息
- **时效性**: 优先保留最新和最重要的信息
- **可扩展性**: 设计要考虑未来的扩展需求

### 2. 性能优化技巧
- **预计算**: 提前计算重要信息的摘要
- **缓存策略**: 缓存常用的上下文片段
- **异步处理**: 异步处理耗时的摘要生成
- **渐进加载**: 根据需要逐步加载上下文

---

**上一节**: [高级Prompt技巧](./02_advanced_prompt_techniques.md)
**下一节**: [智能体应用](../agents/) - 将上下文管理应用到智能体系统
**返回**: [项目主页](../../README.md) 