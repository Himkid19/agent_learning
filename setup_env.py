"""
环境变量设置脚本
在Windows环境下帮助设置API密钥
"""
import os
import sys
from pathlib import Path

def create_env_file():
    """创建.env文件"""
    env_content = """# API密钥配置
# 请填入你的API密钥（至少需要一个）

# OpenAI API密钥
# 获取地址: https://platform.openai.com/api-keys
OPENAI_API_KEY=your_openai_api_key_here

# OpenRouter API密钥  
# 获取地址: https://openrouter.ai/keys
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Anthropic API密钥
# 获取地址: https://console.anthropic.com/
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# 其他配置（可选）
OPENAI_MODEL=gpt-4
OPENROUTER_MODEL=anthropic/claude-3-sonnet
"""
    
    env_file = Path(".env")
    if env_file.exists():
        print("⚠️  .env文件已存在，跳过创建")
        return
    
    try:
        with open(env_file, "w", encoding="utf-8") as f:
            f.write(env_content)
        print("✅ .env文件创建成功！")
        print("📝 请编辑.env文件，填入你的API密钥")
    except Exception as e:
        print(f"❌ 创建.env文件失败: {e}")

def check_env_vars():
    """检查环境变量"""
    print("🔍 检查环境变量...")
    
    # 加载.env文件
    from dotenv import load_dotenv
    load_dotenv()
    
    vars_to_check = [
        ("OPENAI_API_KEY", "OpenAI"),
        ("OPENROUTER_API_KEY", "OpenRouter"), 
        ("ANTHROPIC_API_KEY", "Anthropic")
    ]
    
    found_vars = []
    for var_name, provider in vars_to_check:
        value = os.getenv(var_name)
        if value and value != "your_openai_api_key_here" and value != "your_openrouter_api_key_here" and value != "your_anthropic_api_key_here":
            print(f"✅ {provider} API密钥: 已设置")
            found_vars.append(provider)
        else:
            print(f"❌ {provider} API密钥: 未设置")
    
    return found_vars

def set_env_vars_interactive():
    """交互式设置环境变量"""
    print("\n🔧 交互式设置API密钥")
    print("注意：这种方式只在当前会话中有效")
    
    # OpenAI
    openai_key = input("请输入OpenAI API密钥 (留空跳过): ").strip()
    if openai_key:
        os.environ["OPENAI_API_KEY"] = openai_key
        print("✅ OpenAI API密钥已设置")
    
    # OpenRouter
    openrouter_key = input("请输入OpenRouter API密钥 (留空跳过): ").strip()
    if openrouter_key:
        os.environ["OPENROUTER_API_KEY"] = openrouter_key
        print("✅ OpenRouter API密钥已设置")
    
    # Anthropic
    anthropic_key = input("请输入Anthropic API密钥 (留空跳过): ").strip()
    if anthropic_key:
        os.environ["ANTHROPIC_API_KEY"] = anthropic_key
        print("✅ Anthropic API密钥已设置")

def main():
    """主函数"""
    print("🚀 环境变量设置工具")
    print("=" * 50)
    
    # 创建.env文件
    create_env_file()
    
    # 检查现有环境变量
    found_vars = check_env_vars()
    
    if not found_vars:
        print("\n⚠️  未找到有效的API密钥")
        print("请选择设置方式:")
        print("1. 编辑.env文件（推荐）")
        print("2. 交互式设置（仅当前会话）")
        
        choice = input("请选择 (1/2): ").strip()
        
        if choice == "2":
            set_env_vars_interactive()
            print("\n✅ 环境变量设置完成！")
            print("现在可以运行测试脚本了")
        else:
            print("\n📝 请编辑.env文件，然后重新运行此脚本")
    else:
        print(f"\n✅ 找到 {len(found_vars)} 个API密钥: {', '.join(found_vars)}")
        print("现在可以运行测试脚本了")
    
    print("\n📖 获取API密钥:")
    print("- OpenAI: https://platform.openai.com/api-keys")
    print("- OpenRouter: https://openrouter.ai/keys") 
    print("- Anthropic: https://console.anthropic.com/")

if __name__ == "__main__":
    main() 