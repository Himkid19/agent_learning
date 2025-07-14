"""
MCP Tool Client
用于测试MCP工具调用和Agent集成
"""
import asyncio
import sys
import json
from typing import Dict, Any, Optional
from mcp_server import mcp_server

class MCPClient:
    """简单的MCP工具客户端"""
    
    def __init__(self, server_instance=None):
        self.server = server_instance or mcp_server
        
    def get_available_tools(self) -> Dict[str, Any]:
        """获取可用工具列表"""
        return self.server.get_tools_schema()
    
    async def call_tool(self, tool_name: str, parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """调用工具"""
        if parameters is None:
            parameters = {}
        
        return await self.server.call_tool(tool_name, parameters)
    
    def call_tool_sync(self, tool_name: str, parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """同步调用工具"""
        return asyncio.run(self.call_tool(tool_name, parameters))
    
    def format_result(self, result: Dict[str, Any]) -> str:
        """格式化结果显示"""
        if result.get("success"):
            return f"✅ 成功\n{json.dumps(result['result'], indent=2, ensure_ascii=False)}"
        else:
            return f"❌ 失败: {result.get('error', 'Unknown error')}"

# 创建客户端实例
mcp_client = MCPClient()

def main():
    """主函数 - 命令行工具测试"""
    if len(sys.argv) < 2:
        print("🛠️  MCP Tool Client")
        print("=" * 50)
        print("用法: python mcp_client.py <tool_name> [parameters...]")
        print("\n可用工具:")
        
        tools = mcp_client.get_available_tools()
        for name, tool in tools.items():
            print(f"  📋 {name}: {tool['description']}")
        
        print("\n使用示例:")
        print("  python mcp_client.py calculator '2 + 3 * 4'")
        print("  python mcp_client.py current_time")
        print("  python mcp_client.py list_files")
        print("  python mcp_client.py file_read README.md")
        return
    
    tool_name = sys.argv[1]
    
    # 解析参数
    parameters = {}
    if len(sys.argv) > 2:
        if tool_name == "calculator":
            parameters = {"expression": sys.argv[2]}
        elif tool_name == "current_time":
            parameters = {"format": sys.argv[2] if len(sys.argv) > 2 else "iso"}
        elif tool_name == "file_read":
            parameters = {"file_path": sys.argv[2]}
        elif tool_name == "file_write":
            if len(sys.argv) < 4:
                print("❌ file_write需要文件路径和内容参数")
                return
            parameters = {"file_path": sys.argv[2], "content": sys.argv[3]}
        elif tool_name == "list_files":
            parameters = {"directory": sys.argv[2] if len(sys.argv) > 2 else "."}
    
    # 调用工具
    try:
        result = mcp_client.call_tool_sync(tool_name, parameters)
        print(mcp_client.format_result(result))
    except Exception as e:
        print(f"❌ 调用失败: {e}")

if __name__ == "__main__":
    main() 