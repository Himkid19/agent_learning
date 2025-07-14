# 🤖 AutoGen Agents 快速开始

## 概述

基于AutoGen + OpenRouter的多Agent协作系统，展示如何让多个AI Agent协作完成复杂任务。

## 🎯 Demo功能

- **研究员Agent**: 深入研究和分析问题
- **编写员Agent**: 基于研究结果创作内容  
- **评审员Agent**: 评审内容质量并提供建议
- **协调者**: 管理整个工作流程

## 🔧 环境准备

### 1. 安装依赖
```bash
pip install pyautogen>=0.2.0
```

### 2. 设置API密钥
确保已设置OpenRouter API密钥：
```bash
python ../../setup_env.py
```

## 🚀 运行Demo

### 基础运行
```bash
python autogen_demo.py
```

### 预期输出
```
🤖 AutoGen + OpenRouter Demo
================================================================================
演示多Agent协作回答问题：'llm是什么'

✅ LLM配置完成，使用模型: anthropic/claude-3-sonnet

🤖 创建Agents...
✅ 创建了4个Agents: 研究员、编写员、评审员、协调者

💬 创建群聊...
✅ 群聊创建完成，最大轮次: 12

🎬 开始多Agent协作...
任务: llm是什么
================================================================================

[协调者 → 研究员]: 请团队协作完成以下任务：llm是什么
[研究员]: 作为研究员，我将深入分析LLM的概念...
[编写员]: 基于研究员的分析，我来写一篇通俗易懂的文章...
[评审员]: 我来评审这篇文章的质量...

✅ 任务执行完成！
```

## 🔍 工作流程

1. **任务分发**: 协调者接收任务并分发给团队
2. **研究阶段**: 研究员深入分析"llm是什么"
3. **创作阶段**: 编写员基于研究结果写文章
4. **评审阶段**: 评审员检查内容质量
5. **总结输出**: 整合所有Agent的贡献

## ⚙️ 自定义配置

### 修改Agent角色
```python
# 在autogen_demo.py中修改system_message
researcher = autogen.AssistantAgent(
    name="研究员",
    system_message="你的自定义角色描述...",
    llm_config=llm_config,
)
```

### 更换任务
```python
# 修改main()函数中的任务
result = asyncio.run(execute_task("你的自定义任务"))
```

### 调整模型参数
```python
llm_config = {
    "config_list": [...],
    "temperature": 0.5,  # 调整创造性
    "timeout": 180,      # 调整超时时间
}
```

## 🛠️ 扩展示例

### 添加新的Agent
```python
def create_agents(llm_config):
    # 现有Agent...
    
    # 新增：数据分析师Agent
    analyst = autogen.AssistantAgent(
        name="数据分析师",
        system_message="你是数据分析专家，负责数据分析和可视化...",
        llm_config=llm_config,
    )
    
    return researcher, writer, reviewer, analyst, user_proxy
```

### 不同的任务类型
```python
# 技术问题
execute_task("如何优化深度学习模型性能")

# 商业分析
execute_task("分析电商行业的发展趋势")

# 创意写作
execute_task("写一个关于AI的科幻故事")
```

## 🔧 故障排除

### 常见问题

1. **导入错误**
```bash
# 安装AutoGen
pip install pyautogen
```

2. **API密钥错误**
```bash
# 重新设置环境变量
python ../../setup_env.py
```

3. **网络连接问题**
- 检查网络连接
- 确认OpenRouter服务状态

### 调试技巧

1. **查看详细日志**
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

2. **减少轮次**
```python
groupchat = autogen.GroupChat(
    agents=[...],
    max_round=6,  # 减少轮次
)
```

## 📊 性能优化

### 减少API调用
- 调整`max_round`参数
- 优化Agent的system_message
- 使用更快的模型

### 提升响应质量
- 增加`temperature`获得更有创意的回答
- 调整`timeout`避免超时
- 优化prompt设计

## 🎯 学习成果

完成本Demo后，你将掌握：

- ✅ AutoGen的基本使用方法
- ✅ 多Agent协作机制
- ✅ OpenRouter API集成
- ✅ 群聊管理和工作流控制
- ✅ Agent角色设计和任务分配

## 📖 下一步

1. **尝试不同任务**: 修改任务内容，观察Agent如何协作
2. **添加新Agent**: 扩展团队，加入更多专业角色
3. **集成工具**: 添加文件操作、网络搜索等工具
4. **优化流程**: 改进工作流程和Agent协作方式

## 🤝 贡献

欢迎提交改进建议和新的Agent设计！ 