"""
LLM客户端测试脚本
用于验证LLM客户端是否正常工作
"""
import asyncio
import os
from typing import Dict, List
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.core.llm_client import LLMClient


async def test_openai_client():
    """测试OpenAI客户端"""
    print("=== 测试OpenAI客户端 ===")
    
    try:
        # 检查环境变量
        if not os.getenv("OPENAI_API_KEY"):
            print("❌ 未设置OPENAI_API_KEY环境变量")
            return False
        
        # 创建客户端
        client = LLMClient(provider="openai")
        
        # 测试简单对话
        messages = [
            {"role": "user", "content": "你好，请简单介绍一下自己"}
        ]
        
        print("发送消息:", messages[0]["content"])
        response = await client.chat_completion(messages, max_tokens=100)
        
        print("✅ OpenAI响应成功:")
        print(f"内容: {response['content']}")
        print(f"模型: {response['model']}")
        if response.get('usage'):
            print(f"使用情况: {response['usage']}")
        
        return True
        
    except Exception as e:
        print(f"❌ OpenAI测试失败: {str(e)}")
        return False


async def test_openrouter_client():
    """测试OpenRouter客户端"""
    print("\n=== 测试OpenRouter客户端 ===")
    
    try:
        # 检查环境变量
        if not os.getenv("OPENROUTER_API_KEY"):
            print("❌ 未设置OPENROUTER_API_KEY环境变量")
            return False
        
        # 创建客户端
        client = LLMClient(provider="openrouter")
        
        # 测试简单对话
        messages = [
            {"role": "user", "content": "用一句话解释什么是人工智能"}
        ]
        
        print("发送消息:", messages[0]["content"])
        response = await client.chat_completion(messages, max_tokens=50)
        
        print("✅ OpenRouter响应成功:")
        print(f"内容: {response['content']}")
        print(f"模型: {response['model']}")
        if response.get('usage'):
            print(f"使用情况: {response['usage']}")
        
        return True
        
    except Exception as e:
        print(f"❌ OpenRouter测试失败: {str(e)}")
        return False


async def test_anthropic_client():
    """测试Anthropic客户端"""
    print("\n=== 测试Anthropic客户端 ===")
    
    try:
        # 检查环境变量
        if not os.getenv("ANTHROPIC_API_KEY"):
            print("❌ 未设置ANTHROPIC_API_KEY环境变量")
            return False
        
        # 创建客户端
        client = LLMClient(provider="anthropic")
        
        # 测试简单对话
        messages = [
            {"role": "user", "content": "请用中文回答：什么是机器学习？"}
        ]
        
        print("发送消息:", messages[0]["content"])
        response = await client.chat_completion(messages, max_tokens=100)
        
        print("✅ Anthropic响应成功:")
        print(f"内容: {response['content']}")
        print(f"模型: {response['model']}")
        if response.get('usage'):
            print(f"使用情况: {response['usage']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Anthropic测试失败: {str(e)}")
        return False


async def test_text_completion():
    """测试文本完成功能"""
    print("\n=== 测试文本完成功能 ===")
    
    try:
        # 使用OpenAI测试文本完成
        if os.getenv("OPENAI_API_KEY"):
            client = LLMClient(provider="openai")
            prompt = "请完成这句话：人工智能的未来是"
            
            print("发送提示:", prompt)
            response = await client.text_completion(prompt, max_tokens=50)
            
            print("✅ 文本完成成功:")
            print(f"完整文本: {prompt}{response}")
            
            return True
        else:
            print("❌ 未设置OPENAI_API_KEY，跳过文本完成测试")
            return False
            
    except Exception as e:
        print(f"❌ 文本完成测试失败: {str(e)}")
        return False


async def main():
    """主测试函数"""
    print("🚀 开始LLM客户端测试...")
    print("注意：请确保已设置相应的API密钥环境变量")
    print()
    
    # 测试结果统计
    results = []
    
    # 测试各个客户端
    results.append(await test_openai_client())
    results.append(await test_openrouter_client())
    results.append(await test_anthropic_client())
    results.append(await test_text_completion())
    
    # 输出测试总结
    print("\n" + "="*50)
    print("📊 测试总结:")
    print(f"总测试数: {len(results)}")
    print(f"成功数: {sum(results)}")
    print(f"失败数: {len(results) - sum(results)}")
    
    if sum(results) > 0:
        print("✅ 至少有一个LLM客户端工作正常！")
    else:
        print("❌ 所有LLM客户端测试都失败了，请检查API密钥配置")


if __name__ == "__main__":
    # 运行测试
    asyncio.run(main()) 