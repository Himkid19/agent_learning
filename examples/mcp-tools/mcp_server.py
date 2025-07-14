"""
简单的MCP Tool Server
提供基础工具给AI Agent使用
"""
import json
import asyncio
import sys
import os
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass
from datetime import datetime
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class Tool:
    """工具定义"""
    name: str
    description: str
    parameters: Dict[str, Any]
    function: Callable

class MCPServer:
    """简单的MCP工具服务器"""
    
    def __init__(self):
        self.tools: Dict[str, Tool] = {}
        self.version = "1.0.0"
        
    def register_tool(self, name: str, description: str, parameters: Dict[str, Any]):
        """注册工具装饰器"""
        def decorator(func: Callable):
            self.tools[name] = Tool(
                name=name,
                description=description,
                parameters=parameters,
                function=func
            )
            return func
        return decorator
    
    def get_tools_schema(self) -> Dict[str, Any]:
        """获取所有工具的schema"""
        tools_schema = {}
        for name, tool in self.tools.items():
            tools_schema[name] = {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.parameters
            }
        return tools_schema
    
    async def call_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """调用工具"""
        if tool_name not in self.tools:
            return {
                "success": False,
                "error": f"Tool '{tool_name}' not found"
            }
        
        try:
            tool = self.tools[tool_name]
            
            # 检查是否是异步函数
            if asyncio.iscoroutinefunction(tool.function):
                result = await tool.function(**parameters)
            else:
                result = tool.function(**parameters)
            
            return {
                "success": True,
                "result": result,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error calling tool {tool_name}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def start_server(self, host: str = "localhost", port: int = 8000):
        """启动服务器"""
        print(f"🚀 MCP Tool Server starting on {host}:{port}")
        print(f"📋 Available tools: {list(self.tools.keys())}")
        
        # 这里可以添加实际的HTTP服务器代码
        # 为了简化，我们提供一个同步接口
        pass

# 创建服务器实例
mcp_server = MCPServer()

# ==================== 工具实现 ====================

@mcp_server.register_tool(
    name="calculator",
    description="执行基本数学计算",
    parameters={
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": "数学表达式，如 '2 + 3 * 4'"
            }
        },
        "required": ["expression"]
    }
)
def calculator(expression: str) -> Dict[str, Any]:
    """计算器工具"""
    try:
        # 安全的数学计算
        allowed_chars = set('0123456789+-*/.() ')
        if not all(c in allowed_chars for c in expression):
            return {"error": "表达式包含不允许的字符"}
        
        result = eval(expression)
        return {
            "expression": expression,
            "result": result,
            "type": type(result).__name__
        }
    except Exception as e:
        return {"error": f"计算错误: {str(e)}"}

@mcp_server.register_tool(
    name="file_read",
    description="读取文件内容",
    parameters={
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "要读取的文件路径"
            },
            "encoding": {
                "type": "string",
                "description": "文件编码，默认utf-8",
                "default": "utf-8"
            }
        },
        "required": ["file_path"]
    }
)
def file_read(file_path: str, encoding: str = "utf-8") -> Dict[str, Any]:
    """读取文件工具"""
    try:
        # 安全检查：只允许读取当前目录及子目录的文件
        if ".." in file_path or file_path.startswith("/"):
            return {"error": "不允许访问该路径"}
        
        with open(file_path, 'r', encoding=encoding) as f:
            content = f.read()
        
        return {
            "file_path": file_path,
            "content": content,
            "size": len(content),
            "lines": len(content.splitlines())
        }
    except Exception as e:
        return {"error": f"读取文件错误: {str(e)}"}

@mcp_server.register_tool(
    name="file_write",
    description="写入文件内容",
    parameters={
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "要写入的文件路径"
            },
            "content": {
                "type": "string",
                "description": "要写入的内容"
            },
            "encoding": {
                "type": "string",
                "description": "文件编码，默认utf-8",
                "default": "utf-8"
            }
        },
        "required": ["file_path", "content"]
    }
)
def file_write(file_path: str, content: str, encoding: str = "utf-8") -> Dict[str, Any]:
    """写入文件工具"""
    try:
        # 安全检查
        if ".." in file_path or file_path.startswith("/"):
            return {"error": "不允许访问该路径"}
        
        # 创建目录（如果不存在）
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w', encoding=encoding) as f:
            f.write(content)
        
        return {
            "file_path": file_path,
            "bytes_written": len(content.encode(encoding)),
            "lines_written": len(content.splitlines())
        }
    except Exception as e:
        return {"error": f"写入文件错误: {str(e)}"}

@mcp_server.register_tool(
    name="current_time",
    description="获取当前时间",
    parameters={
        "type": "object",
        "properties": {
            "format": {
                "type": "string",
                "description": "时间格式，默认ISO格式",
                "default": "iso"
            }
        }
    }
)
def current_time(format: str = "iso") -> Dict[str, Any]:
    """获取当前时间工具"""
    now = datetime.now()
    
    if format == "iso":
        time_str = now.isoformat()
    elif format == "readable":
        time_str = now.strftime("%Y-%m-%d %H:%M:%S")
    elif format == "timestamp":
        time_str = str(int(now.timestamp()))
    else:
        try:
            time_str = now.strftime(format)
        except:
            time_str = now.isoformat()
    
    return {
        "current_time": time_str,
        "format": format,
        "timezone": str(now.astimezone().tzinfo)
    }

@mcp_server.register_tool(
    name="list_files",
    description="列出目录中的文件",
    parameters={
        "type": "object",
        "properties": {
            "directory": {
                "type": "string",
                "description": "要列出的目录路径，默认当前目录",
                "default": "."
            },
            "pattern": {
                "type": "string",
                "description": "文件名模式，支持通配符",
                "default": "*"
            }
        }
    }
)
def list_files(directory: str = ".", pattern: str = "*") -> Dict[str, Any]:
    """列出文件工具"""
    try:
        import glob
        
        # 安全检查
        if ".." in directory or directory.startswith("/"):
            return {"error": "不允许访问该路径"}
        
        # 构建搜索模式
        search_pattern = os.path.join(directory, pattern)
        files = glob.glob(search_pattern)
        
        result = []
        for file_path in files:
            try:
                stat = os.stat(file_path)
                result.append({
                    "name": os.path.basename(file_path),
                    "path": file_path,
                    "size": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "is_directory": os.path.isdir(file_path)
                })
            except:
                continue
        
        return {
            "directory": directory,
            "pattern": pattern,
            "files": result,
            "count": len(result)
        }
    except Exception as e:
        return {"error": f"列出文件错误: {str(e)}"}

# ==================== 主函数 ====================

def main():
    """主函数"""
    print("🛠️  MCP Tool Server")
    print("=" * 50)
    
    # 显示可用工具
    tools = mcp_server.get_tools_schema()
    print(f"✅ 已注册 {len(tools)} 个工具:")
    for name, tool in tools.items():
        print(f"  📋 {name}: {tool['description']}")
    
    print("\n💡 使用示例:")
    print("  python mcp_client.py calculator '2 + 3 * 4'")
    print("  python mcp_client.py current_time")
    print("  python mcp_client.py list_files")
    
    # 启动服务器
    mcp_server.start_server()

if __name__ == "__main__":
    main() 