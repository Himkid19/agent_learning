"""
AutoGen + MCP Tools Demo
展示如何在多Agent系统中集成MCP工具
"""
import asyncio
import os
import sys
import json
from datetime import datetime
from typing import Dict, Any, List, Optional

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from dotenv import load_dotenv
import autogen
from config.settings import get_settings
from mcp_client import MCPClient

# 加载环境变量
load_dotenv()

class MCPToolAgent:
    """集成MCP工具的Agent包装器"""
    
    def __init__(self, mcp_client: MCPClient):
        self.mcp_client = mcp_client
        self.tools = mcp_client.get_available_tools()
    
    def get_tools_description(self) -> str:
        """获取工具描述"""
        descriptions = []
        for name, tool in self.tools.items():
            descriptions.append(f"- {name}: {tool['description']}")
        return "\n".join(descriptions)
    
    def call_tool(self, tool_name: str, parameters: Optional[Dict[str, Any]] = None) -> str:
        """调用工具并返回格式化结果"""
        if parameters is None:
            parameters = {}
        
        result = self.mcp_client.call_tool_sync(tool_name, parameters)
        
        if result.get("success"):
            return f"✅ 工具调用成功\n结果: {json.dumps(result['result'], indent=2, ensure_ascii=False)}"
        else:
            return f"❌ 工具调用失败: {result.get('error', 'Unknown error')}"

def setup_llm_config():
    """设置LLM配置"""
    settings = get_settings()
    
    if not settings.openrouter_api_key:
        print("❌ 未找到OPENROUTER_API_KEY，请设置环境变量")
        sys.exit(1)
    
    llm_config = {
        "config_list": [
            {
                "model": "google/gemini-2.5-flash",
                "api_key": settings.openrouter_api_key,
                "base_url": "https://openrouter.ai/api/v1",
                "api_type": "openai",
            }
        ],
        "temperature": 0.7,
        "timeout": 120,
    }
    
    print(f"✅ LLM配置完成，使用模型: google/gemini-2.5-flash")
    return llm_config

def create_mcp_enhanced_agents(llm_config, mcp_tool_agent: MCPToolAgent):
    """创建集成了MCP工具的Agents"""
    print("\n🤖 创建集成MCP工具的Agents...")
    
    # 工具描述
    tools_description = mcp_tool_agent.get_tools_description()
    
    # 1. 工具操作员Agent
    tool_operator = autogen.AssistantAgent(
        name="工具操作员",
        system_message=f"""你是一名专业的工具操作员。
        职责：
        - 使用各种MCP工具完成任务
        - 根据需要调用适当的工具
        - 将工具结果整理成有用的信息
        
        可用工具：
        {tools_description}
        
        工具调用格式：
        当需要使用工具时，请用以下格式：
        TOOL_CALL: {{
            "tool_name": "工具名称",
            "parameters": {{参数}}
        }}
        
        工作风格：实用、准确、高效
        """,
        llm_config=llm_config,
    )
    
    # 2. 数据分析师Agent
    data_analyst = autogen.AssistantAgent(
        name="数据分析师",
        system_message="""你是一名数据分析师。
        职责：
        - 分析工具操作员提供的数据
        - 提供数据洞察和建议
        - 生成报告和总结
        
        工作风格：分析性、客观、详细
        """,
        llm_config=llm_config,
    )
    
    # 3. 项目协调员Agent
    project_coordinator = autogen.AssistantAgent(
        name="项目协调员",
        system_message="""你是项目协调员。
        职责：
        - 协调团队成员间的工作
        - 确保任务按计划进行
        - 提供最终总结和建议
        
        工作风格：组织性、全面、决策导向
        """,
        llm_config=llm_config,
    )
    
    # 4. 用户代理（协调者）
    user_proxy = autogen.UserProxyAgent(
        name="协调者",
        system_message="你是任务协调者，负责管理整个工作流程。",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=15,
        code_execution_config=False,
    )
    
    print(f"✅ 创建了4个Agents: 工具操作员、数据分析师、项目协调员、协调者")
    return tool_operator, data_analyst, project_coordinator, user_proxy

class MCPGroupChatManager:
    """集成MCP工具的群聊管理器"""
    
    def __init__(self, agents, llm_config, mcp_tool_agent: MCPToolAgent):
        self.agents = agents
        self.llm_config = llm_config
        self.mcp_tool_agent = mcp_tool_agent
        
        # 创建群聊
        self.groupchat = autogen.GroupChat(
            agents=agents,
            messages=[],
            max_round=20,
            speaker_selection_method="round_robin",
        )
        
        # 创建管理器
        self.manager = autogen.GroupChatManager(
            groupchat=self.groupchat,
            llm_config=llm_config,
        )
    
    def process_message(self, message: str) -> str:
        """处理消息，检查是否包含工具调用"""
        if "TOOL_CALL:" in message:
            # 提取工具调用
            try:
                tool_start = message.find("TOOL_CALL:") + len("TOOL_CALL:")
                tool_end = message.find("}", tool_start) + 1
                tool_call_str = message[tool_start:tool_end].strip()
                
                tool_call = json.loads(tool_call_str)
                tool_name = tool_call.get("tool_name")
                parameters = tool_call.get("parameters", {})
                
                # 调用工具
                result = self.mcp_tool_agent.call_tool(tool_name, parameters)
                
                # 替换消息中的工具调用
                new_message = message[:message.find("TOOL_CALL:")] + f"\n{result}"
                return new_message
                
            except Exception as e:
                return message + f"\n❌ 工具调用解析失败: {e}"
        
        return message

async def execute_mcp_task(task="使用工具分析当前目录的文件情况"):
    """执行集成MCP工具的任务"""
    print(f"\n🚀 开始执行MCP集成任务: '{task}'")
    print("=" * 80)
    
    # 1. 设置LLM配置
    llm_config = setup_llm_config()
    
    # 2. 创建MCP客户端
    mcp_client = MCPClient()
    mcp_tool_agent = MCPToolAgent(mcp_client)
    
    print(f"✅ MCP工具已就绪，可用工具: {list(mcp_tool_agent.tools.keys())}")
    
    # 3. 创建Agents
    agents = create_mcp_enhanced_agents(llm_config, mcp_tool_agent)
    tool_operator, data_analyst, project_coordinator, user_proxy = agents
    
    # 4. 创建群聊管理器
    mcp_manager = MCPGroupChatManager(
        [user_proxy, tool_operator, data_analyst, project_coordinator],
        llm_config,
        mcp_tool_agent
    )
    
    # 5. 构建任务指令
    task_message = f"""
    请团队协作完成以下任务：{task}
    
    工作流程：
    1. 工具操作员：使用MCP工具收集必要信息
    2. 数据分析师：分析工具提供的数据
    3. 项目协调员：整理分析结果，提供建议
    
    工具操作员可以使用以下工具：
    {mcp_tool_agent.get_tools_description()}
    
    请按顺序完成任务，充分利用可用工具。
    """
    
    try:
        print(f"\n🎬 开始多Agent + MCP工具协作...")
        print("=" * 80)
        
        # 启动对话
        result = user_proxy.initiate_chat(
            mcp_manager.manager,
            message=task_message,
        )
        
        print("\n" + "=" * 80)
        print("✅ MCP集成任务执行完成！")
        
        return result
        
    except Exception as e:
        print(f"\n❌ 任务执行失败: {e}")
        return None

def main():
    """主函数"""
    print("🤖 AutoGen + MCP Tools Demo")
    print("=" * 80)
    print("演示多Agent系统集成MCP工具")
    
    # 测试MCP工具
    print("\n🔧 测试MCP工具连接...")
    mcp_client = MCPClient()
    tools = mcp_client.get_available_tools()
    print(f"✅ 发现 {len(tools)} 个可用工具: {list(tools.keys())}")
    
    # 测试一个简单的工具调用
    test_result = mcp_client.call_tool_sync("current_time", {"format": "readable"})
    if test_result.get("success"):
        print(f"✅ 工具测试成功: {test_result['result']['current_time']}")
    else:
        print(f"❌ 工具测试失败: {test_result.get('error')}")
        return
    
    try:
        # 执行任务
        result = asyncio.run(execute_mcp_task())
        
        if result:
            print("\n📋 执行总结:")
            print("- 工具操作员使用MCP工具收集信息")
            print("- 数据分析师分析了工具结果")
            print("- 项目协调员提供了综合建议")
            print("- 团队成功完成MCP集成任务")
        
    except KeyboardInterrupt:
        print("\n⚠️ 用户中断执行")
    except Exception as e:
        print(f"\n❌ 程序执行错误: {e}")
        print("\n🔧 故障排除建议:")
        print("1. 检查MCP工具服务是否正常")
        print("2. 确认API密钥配置正确")
        print("3. 检查网络连接")

if __name__ == "__main__":
    main() 