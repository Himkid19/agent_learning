"""
AutoGen + OpenRouter 简单Demo
展示多Agent协作执行任务："llm是什么"
"""
import asyncio
import os
import sys
from datetime import datetime

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from dotenv import load_dotenv
import autogen
from config.settings import get_settings

# 加载环境变量
load_dotenv()


def setup_llm_config():
    """设置LLM配置"""
    settings = get_settings()
    
    # 检查OpenRouter API密钥
    if not settings.openrouter_api_key:
        print("❌ 未找到OPENROUTER_API_KEY，请设置环境变量")
        print("可以运行: python setup_env.py")
        sys.exit(1)
    
    # AutoGen配置
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
    
    print(f"✅ LLM配置完成，使用模型: anthropic/claude-3-sonnet")
    return llm_config


def create_agents(llm_config):
    """创建Agent"""
    print("\n🤖 创建Agents...")
    
    # 1. 研究员Agent
    researcher = autogen.AssistantAgent(
        name="研究员",
        system_message="""你是一名专业的研究员。
        职责：
        - 深入研究和分析用户提出的问题
        - 收集相关信息和背景知识
        - 提供准确、全面的研究报告
        
        工作风格：严谨、客观、详细
        """,
        llm_config=llm_config,
    )
    
    # 2. 编写员Agent
    writer = autogen.AssistantAgent(
        name="编写员",
        system_message="""你是一名专业的内容编写员。
        职责：
        - 基于研究员提供的信息编写文章
        - 将复杂的技术概念转化为通俗易懂的内容
        - 确保文章结构清晰、逻辑性强
        
        工作风格：清晰、生动、易懂
        """,
        llm_config=llm_config,
    )
    
    # 3. 评审员Agent
    reviewer = autogen.AssistantAgent(
        name="评审员",
        system_message="""你是一名专业的内容评审员。
        职责：
        - 评审编写员的文章质量
        - 检查内容的准确性和完整性
        - 提供改进建议和最终总结
        
        工作风格：客观、严格、建设性
        """,
        llm_config=llm_config,
    )
    
    # 4. 用户代理（协调者）
    user_proxy = autogen.UserProxyAgent(
        name="协调者",
        system_message="你是任务协调者，负责管理整个工作流程。",
        human_input_mode="NEVER",  # 不需要人工输入
        max_consecutive_auto_reply=10,
        code_execution_config=False,  # 不执行代码
    )
    
    print(f"✅ 创建了4个Agents: 研究员、编写员、评审员、协调者")
    return researcher, writer, reviewer, user_proxy


def create_group_chat(agents, llm_config):
    """创建群聊"""
    researcher, writer, reviewer, user_proxy = agents
    
    print("\n💬 创建群聊...")
    
    # 创建群聊
    groupchat = autogen.GroupChat(
        agents=[user_proxy, researcher, writer, reviewer],
        messages=[],
        max_round=12,  # 最大轮次
        speaker_selection_method="round_robin",  # 轮流发言
    )
    
    # 创建群聊管理器，使用相同的llm_config
    manager = autogen.GroupChatManager(
        groupchat=groupchat,
        llm_config=llm_config,  # 使用有效的LLM配置
    )
    
    print(f"✅ 群聊创建完成，最大轮次: {groupchat.max_round}")
    return manager, user_proxy


def log_conversation_step(step, agent_name, message):
    """记录对话步骤"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"\n[{timestamp}] 📝 第{step}步 - {agent_name}")
    print(f"💭 {message[:200]}{'...' if len(message) > 200 else ''}")
    print("-" * 60)


async def execute_task(task="llm是什么"):
    """执行任务"""
    print(f"\n🚀 开始执行任务: '{task}'")
    print("=" * 80)
    
    # 1. 设置LLM配置
    llm_config = setup_llm_config()
    
    # 2. 创建Agents
    agents = create_agents(llm_config)
    
    # 3. 创建群聊
    manager, user_proxy = create_group_chat(agents, llm_config)
    
    # 4. 开始对话
    print(f"\n🎬 开始多Agent协作...")
    print(f"任务: {task}")
    print("=" * 80)
    
    # 构建任务指令
    task_message = f"""
    请团队协作完成以下任务：{task}
    
    工作流程：
    1. 研究员：深入研究这个问题，提供详细的背景信息
    2. 编写员：基于研究结果，写一篇通俗易懂的文章
    3. 评审员：评审文章质量，提供最终总结
    
    请按顺序完成，每个人都要发挥自己的专业能力。
    """
    
    try:
        # 启动对话
        result = user_proxy.initiate_chat(
            manager,
            message=task_message,
        )
        
        print("\n" + "=" * 80)
        print("✅ 任务执行完成！")
        
        return result
        
    except Exception as e:
        print(f"\n❌ 任务执行失败: {e}")
        return None


def main():
    """主函数"""
    print("🤖 AutoGen + OpenRouter Demo")
    print("=" * 80)
    print("演示多Agent协作回答问题：'llm是什么'")
    
    try:
        # 执行任务
        result = asyncio.run(execute_task("llm是什么"))
        
        if result:
            print("\n📋 执行总结:")
            print("- 研究员完成了深入研究")
            print("- 编写员创作了文章")
            print("- 评审员提供了评审意见")
            print("- 团队协作成功完成任务")
        
    except KeyboardInterrupt:
        print("\n⚠️ 用户中断执行")
    except Exception as e:
        print(f"\n❌ 程序执行错误: {e}")
        print("\n🔧 故障排除建议:")
        print("1. 检查API密钥是否正确设置")
        print("2. 确认网络连接正常")
        print("3. 运行: python setup_env.py 设置环境")


if __name__ == "__main__":
    main() 