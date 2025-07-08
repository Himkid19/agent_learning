"""
项目配置文件
"""
import os
from typing import Optional
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()


class Settings:
    """应用配置类"""
    
    def __init__(self):
        # OpenAI配置
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.openai_api_base = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
        self.openai_model = os.getenv("OPENAI_MODEL", "gpt-4")
        
        # OpenRouter配置
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        self.openrouter_api_base = os.getenv("OPENROUTER_API_BASE", "https://openrouter.ai/api/v1")
        self.openrouter_model = os.getenv("OPENROUTER_MODEL", "google/gemini-2.5-flash")
        
        # Anthropic配置
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        
        # MCP配置
        self.mcp_server_host = os.getenv("MCP_SERVER_HOST", "localhost")
        self.mcp_server_port = int(os.getenv("MCP_SERVER_PORT", "3000"))
        
        # 数据库配置
        self.database_url = os.getenv("DATABASE_URL", "sqlite:///./agent_learning.db")
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        
        # Web应用配置
        self.app_host = os.getenv("APP_HOST", "0.0.0.0")
        self.app_port = int(os.getenv("APP_PORT", "8000"))
        self.debug = os.getenv("DEBUG", "True").lower() == "true"
        
        # 日志配置
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.log_file = os.getenv("LOG_FILE", "logs/agent_learning.log")
        
        # 外部服务
        self.firecrawl_api_key = os.getenv("FIRECRAWL_API_KEY")
        self.serpapi_api_key = os.getenv("SERPAPI_API_KEY")
        
        # 安全配置
        self.secret_key = os.getenv("SECRET_KEY", "your-secret-key-change-this")
        self.allowed_hosts = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1")


# 全局配置实例
settings = Settings()


def get_settings() -> Settings:
    """获取配置实例"""
    return settings 