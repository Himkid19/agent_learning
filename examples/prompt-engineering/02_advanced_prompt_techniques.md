# 高级Prompt技巧

## 📖 简介

在掌握了基础Prompt编写技能后，我们需要学习更高级的技巧来应对复杂场景。本教程将介绍思维链(Chain of Thought)、少样本学习(Few-shot Learning)、角色扮演等高级技术，帮助你构建更强大的LLM应用。

## 🎯 学习目标

- 掌握思维链(Chain of Thought)推理
- 学会Few-shot Learning技巧
- 理解角色扮演的深度应用
- 掌握Prompt链式组合
- 学会处理复杂任务分解

## 🧠 思维链(Chain of Thought)

### 基本概念

思维链是一种引导模型逐步推理的技术，通过显式地展示思考过程来提高推理质量。

### 基础思维链

```markdown
# 基础示例:
问题: 一个班级有30个学生，其中60%是女生，女生中有75%参加了数学竞赛。请问有多少女生参加了数学竞赛？

Prompt:
请一步步解决这个问题:

1. 首先计算女生总数
2. 然后计算参加竞赛的女生数量
3. 给出最终答案

解答:
第一步: 女生总数 = 30 × 60% = 18人
第二步: 参加竞赛的女生 = 18 × 75% = 13.5 ≈ 14人
最终答案: 14名女生参加了数学竞赛
```

### 复杂推理链

```markdown
# 复杂业务分析示例:
你是一位资深的商业分析师。请分析以下电商数据，并提供策略建议。

数据:
- 网站月访问量: 100万
- 转化率: 2%
- 平均订单价值: 150元
- 客户获取成本: 30元
- 客户生命周期价值: 500元

分析思路:
1. 计算当前收入指标
2. 分析盈利能力
3. 识别改进机会
4. 制定具体策略
5. 预测策略效果

请按照这个思路逐步分析。
```

## 🎓 Few-shot Learning (少样本学习)

### 零样本 vs 少样本

```markdown
# 零样本 (Zero-shot):
请将以下句子翻译成英文:
"今天天气很好"

# 少样本 (Few-shot):
请参考以下例子，将中文翻译成英文:

例子1:
中文: "我喜欢苹果"
英文: "I like apples"

例子2:
中文: "明天是周末"
英文: "Tomorrow is weekend"

现在请翻译:
中文: "今天天气很好"
英文:
```

### 格式化Few-shot示例

```markdown
# 情感分析Few-shot示例:
请根据以下例子，分析文本的情感倾向:

### 示例 ###
输入: "这个产品质量真的很棒，我非常满意！"
输出: {"sentiment": "正面", "confidence": 0.95, "keywords": ["质量", "棒", "满意"]}

输入: "客服态度太差了，完全不耐烦"
输出: {"sentiment": "负面", "confidence": 0.90, "keywords": ["态度差", "不耐烦"]}

输入: "还可以吧，没什么特别的"
输出: {"sentiment": "中性", "confidence": 0.75, "keywords": ["还可以", "没什么特别"]}

### 现在请分析 ###
输入: "物流速度还行，但包装有点粗糙"
输出:
```

## 🎭 高级角色扮演

### 多层次角色定义

```markdown
# 复合角色示例:
你是一位具有以下背景的专家:

## 主要角色:
高级Python开发工程师

## 专业背景:
- 10年+后端开发经验
- 精通Django, FastAPI框架
- 擅长数据库设计和优化
- 有大型项目架构经验

## 性格特点:
- 注重代码质量和性能
- 善于解释复杂概念
- 倾向于提供实用的解决方案
- 会考虑可维护性和扩展性

## 回答风格:
- 提供代码示例
- 解释设计思路
- 指出潜在风险
- 给出最佳实践建议

现在请帮我设计一个用户认证系统...
```

### 动态角色切换

```markdown
# 多角色协作示例:
现在我们要进行一个产品评审会议。你需要扮演以下三个角色，轮流发言:

**产品经理**: 关注用户需求和商业价值
**技术负责人**: 关注技术实现和风险
**设计师**: 关注用户体验和界面设计

主题: 设计一个AI写作助手功能

请按照以下格式进行讨论:
[产品经理]: [观点]
[技术负责人]: [观点]  
[设计师]: [观点]
```

## 🔗 Prompt链式组合

### 任务分解链

```markdown
# 复杂任务分解示例:
任务: 为一个在线教育平台编写完整的商业计划书

## 第一步: 市场分析
你是一位市场研究专家。请分析在线教育市场的现状、机会和挑战。
输出格式: 市场规模、目标用户、竞争分析、SWOT分析

## 第二步: 产品规划  
基于市场分析结果，你现在是产品经理。请设计产品功能和特色。
输入: [第一步的输出]
输出格式: 产品定位、核心功能、差异化优势

## 第三步: 商业模式
你是商业策略顾问。请基于产品规划设计盈利模式。
输入: [第二步的输出]
输出格式: 收入模式、成本结构、盈利预测

## 第四步: 技术架构
你是技术总监。请设计系统架构和技术选型。
输入: [第三步的输出]
输出格式: 系统架构图、技术栈、开发计划
```

### 条件分支Prompt

```markdown
# 智能客服条件分支示例:
你是智能客服助手。根据用户问题类型，采用不同的处理方式:

## 判断逻辑:
1. 如果是技术问题 → 转向技术支持流程
2. 如果是订单问题 → 转向订单处理流程  
3. 如果是投诉建议 → 转向客户关怀流程
4. 如果无法判断 → 转向人工客服

## 技术支持流程:
- 收集设备信息
- 提供故障排查步骤
- 记录问题详情

## 订单处理流程:
- 验证订单信息
- 查询订单状态
- 提供解决方案

用户问题: "我的订单已经下单3天了，为什么还没发货？"

请按照流程处理。
```

## 💻 实际应用案例

### 案例1: 代码审查助手

```python
# 代码审查Prompt模板
CODE_REVIEW_PROMPT = """
你是一位经验丰富的代码审查专家。请按照以下标准审查代码:

## 审查维度:
1. 代码质量 (可读性、命名规范)
2. 性能优化 (算法效率、资源使用)
3. 安全性 (潜在漏洞、输入验证)
4. 可维护性 (模块化、注释)
5. 最佳实践 (设计模式、编码规范)

## 输出格式:
### 总体评分: [1-10分]
### 详细评价:
- **优点**: [列出优点]
- **问题**: [列出问题，按严重程度排序]
- **建议**: [具体改进建议]
- **重构建议**: [如需重构，提供方案]

## 代码:
```python
{code_content}
```

请开始审查:
"""
```

### 案例2: 文档生成助手

```markdown
# API文档生成示例:
你是技术文档专家。请为以下API生成完整的文档:

## 输入信息:
- API端点: POST /api/users
- 功能: 创建新用户
- 参数: username, email, password
- 返回: 用户ID和创建时间

## 文档结构要求:
1. **接口概述**
2. **请求说明** (方法、URL、headers)
3. **参数说明** (类型、必填、格式要求)
4. **响应说明** (成功/失败格式)
5. **示例代码** (curl、Python、JavaScript)
6. **错误码说明**
7. **注意事项**

请生成完整的API文档。
```

## 🔗 项目链接

### 相关代码示例:
- [基础Prompt编写](./01_basic_prompt_writing.md) - Prompt基础知识
- [LLM客户端](../llm-basics/test_llm_client.py) - API调用实现
- [智能体实现](../agents/) - 在智能体中应用高级技巧

### 实践项目:
- [工作流编排](../workflows/) - 链式Prompt在工作流中的应用
- [MCP工具集成](../mcp-tools/) - 与工具调用结合的Prompt设计

### 下一步学习:
- [上下文管理](./03_context_management.md) - 学习长对话上下文处理

## 🎯 高级练习

### 练习1: 思维链推理
设计一个Prompt，让AI逐步分析一个创业项目的可行性，包括市场、技术、资金、团队四个维度。

### 练习2: Few-shot学习
创建一个Few-shot示例集，训练AI识别并分类不同类型的客户投诉。

### 练习3: 角色扮演
设计一个多角色协作的Prompt，模拟产品开发会议，包含产品、技术、运营三个角色。

### 练习4: Prompt链
构建一个完整的内容创作流程：主题研究 → 大纲设计 → 内容撰写 → 质量检查。

## 💡 进阶技巧

### 1. 温度控制策略
```markdown
不同任务使用不同的温度参数:
- 创意写作: temperature=0.8-1.0
- 代码生成: temperature=0.1-0.3  
- 数据分析: temperature=0.0-0.2
- 头脑风暴: temperature=0.7-0.9
```

### 2. 长度控制技术
```markdown
精确控制输出长度:
- "请用exactly 150字回答"
- "分为3个段落，每段约100字"
- "提供5个要点，每个要点1-2句话"
```

### 3. 格式强制技术
```markdown
强制JSON输出:
请严格按照以下JSON格式输出，不要包含任何其他文字:
{
  "analysis": "分析内容",
  "score": 数值,
  "recommendations": ["建议1", "建议2"]
}
```

## 📊 效果评估

### 评估维度:
1. **准确性**: 输出是否符合预期
2. **一致性**: 多次运行结果的稳定性
3. **创造性**: 输出的新颖程度
4. **实用性**: 结果的可执行性

### 测试方法:
```python
# A/B测试框架示例
def compare_prompts(prompt_a, prompt_b, test_cases):
    results_a = []
    results_b = []
    
    for case in test_cases:
        result_a = llm_call(prompt_a.format(**case))
        result_b = llm_call(prompt_b.format(**case))
        
        results_a.append(evaluate(result_a, case['expected']))
        results_b.append(evaluate(result_b, case['expected']))
    
    return compare_results(results_a, results_b)
```

---

**上一节**: [基础Prompt编写](./01_basic_prompt_writing.md)
**下一节**: [上下文管理](./03_context_management.md)
**返回**: [项目主页](../../README.md) 