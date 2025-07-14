# MCP Tools System

简单的MCP (Model Context Protocol) 工具系统，支持Agent调用各种工具完成任务。

## 功能特点

- 🛠️ **多种工具**：计算器、文件操作、时间获取、目录列表
- 🤖 **Agent集成**：与AutoGen无缝集成
- 🔧 **易于扩展**：简单的装饰器模式添加新工具
- 🛡️ **安全限制**：文件访问安全检查

## 文件结构

```
examples/mcp-tools/
├── mcp_server.py           # MCP工具服务器
├── mcp_client.py           # MCP客户端
├── autogen_with_mcp.py     # AutoGen + MCP集成示例
└── README.md               # 使用说明
```

## 快速开始

### 1. 测试MCP工具

```bash
# 查看可用工具
python mcp_client.py

# 测试计算器
python mcp_client.py calculator "2 + 3 * 4"

# 获取当前时间
python mcp_client.py current_time readable

# 列出文件
python mcp_client.py list_files

# 读取文件
python mcp_client.py file_read README.md
```

### 2. 运行AutoGen集成示例

```bash
# 确保已设置环境变量
export OPENROUTER_API_KEY="your_key_here"

# 运行集成示例
python autogen_with_mcp.py
```

## 可用工具

### 📊 calculator
执行基本数学计算

**参数:**
- `expression` (string): 数学表达式，如 "2 + 3 * 4"

**示例:**
```bash
python mcp_client.py calculator "10 * 5 + 2"
```

### 📁 file_read
读取文件内容

**参数:**
- `file_path` (string): 文件路径
- `encoding` (string, 可选): 编码格式，默认utf-8

**示例:**
```bash
python mcp_client.py file_read README.md
```

### ✏️ file_write
写入文件内容

**参数:**
- `file_path` (string): 文件路径
- `content` (string): 文件内容
- `encoding` (string, 可选): 编码格式，默认utf-8

**示例:**
```bash
python mcp_client.py file_write test.txt "Hello World"
```

### 🕐 current_time
获取当前时间

**参数:**
- `format` (string, 可选): 时间格式
  - `iso`: ISO格式 (默认)
  - `readable`: 可读格式
  - `timestamp`: 时间戳

**示例:**
```bash
python mcp_client.py current_time readable
```

### 📋 list_files
列出目录文件

**参数:**
- `directory` (string, 可选): 目录路径，默认当前目录
- `pattern` (string, 可选): 文件模式，默认 "*"

**示例:**
```bash
python mcp_client.py list_files
python mcp_client.py list_files src
```

## Agent集成

### 基本用法

```python
from mcp_client import MCPClient
from autogen_with_mcp import MCPToolAgent

# 创建MCP客户端
mcp_client = MCPClient()

# 创建工具代理
tool_agent = MCPToolAgent(mcp_client)

# 调用工具
result = tool_agent.call_tool("current_time", {"format": "readable"})
print(result)
```

### 工具调用格式

在Agent系统中，使用以下格式调用工具：

```
TOOL_CALL: {
    "tool_name": "calculator",
    "parameters": {"expression": "2 + 3"}
}
```

## 扩展新工具

### 1. 添加工具函数

```python
@mcp_server.register_tool(
    name="my_tool",
    description="我的自定义工具",
    parameters={
        "type": "object",
        "properties": {
            "param1": {
                "type": "string",
                "description": "参数1描述"
            }
        },
        "required": ["param1"]
    }
)
def my_tool(param1: str) -> Dict[str, Any]:
    """自定义工具实现"""
    try:
        # 工具逻辑
        result = f"处理: {param1}"
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}
```

### 2. 更新客户端

在 `mcp_client.py` 中添加参数解析逻辑：

```python
elif tool_name == "my_tool":
    parameters = {"param1": sys.argv[2]}
```

## 安全注意事项

- 文件操作限制在当前目录及子目录
- 数学计算使用安全的字符白名单
- 工具调用错误会被捕获并返回错误信息
- 不允许访问上级目录或绝对路径

## 故障排除

### 常见问题

1. **工具调用失败**
   - 检查参数格式是否正确
   - 确认工具名称拼写无误

2. **文件访问被拒绝**
   - 确保文件路径在允许范围内
   - 检查文件权限

3. **Agent集成问题**
   - 确认API密钥配置正确
   - 检查网络连接

### 调试技巧

```bash
# 查看工具schema
python -c "from mcp_client import mcp_client; print(mcp_client.get_available_tools())"

# 测试单个工具
python -c "from mcp_client import mcp_client; print(mcp_client.call_tool_sync('current_time'))"
```

## 开发计划

- [ ] 添加更多工具类型
- [ ] 实现HTTP服务器模式
- [ ] 添加工具调用日志
- [ ] 支持异步工具调用
- [ ] 增强错误处理和监控 