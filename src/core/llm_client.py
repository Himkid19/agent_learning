"""
LLM客户端模块
支持OpenAI、OpenRouter、Anthropic等多种LLM API
"""
import os
from typing import Dict, List, Optional, Any
from abc import ABC, abstractmethod
import openai
import anthropic
from config.settings import get_settings


class BaseLLMClient(ABC):
    """LLM客户端基类"""
    
    @abstractmethod
    async def chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        **kwargs
    ) -> Dict[str, Any]:
        """聊天完成接口"""
        pass
    
    @abstractmethod
    async def text_completion(
        self, 
        prompt: str, 
        **kwargs
    ) -> str:
        """文本完成接口"""
        pass


class OpenAIClient(BaseLLMClient):
    """OpenAI客户端"""
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.settings = get_settings()
        self.api_key = api_key or self.settings.openai_api_key
        self.base_url = base_url or self.settings.openai_api_base
        self.model = self.settings.openai_model
        
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        
        self.client = openai.AsyncOpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
    
    async def chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        **kwargs
    ) -> Dict[str, Any]:
        """OpenAI聊天完成"""
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,  # type: ignore
                **kwargs
            )
            return {
                "content": response.choices[0].message.content,
                "usage": response.usage.dict() if response.usage else None,
                "model": response.model
            }
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    async def text_completion(self, prompt: str, **kwargs) -> str:
        """OpenAI文本完成"""
        messages = [{"role": "user", "content": prompt}]
        response = await self.chat_completion(messages, **kwargs)
        return response["content"]


class OpenRouterClient(BaseLLMClient):
    """OpenRouter客户端"""
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.settings = get_settings()
        self.api_key = api_key or self.settings.openrouter_api_key
        self.base_url = base_url or self.settings.openrouter_api_base
        self.model = self.settings.openrouter_model
        
        if not self.api_key:
            raise ValueError("OpenRouter API key is required")
        
        self.client = openai.AsyncOpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
    
    async def chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        **kwargs
    ) -> Dict[str, Any]:
        """OpenRouter聊天完成"""
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,  # type: ignore
                **kwargs
            )
            return {
                "content": response.choices[0].message.content,
                "usage": response.usage.dict() if response.usage else None,
                "model": response.model
            }
        except Exception as e:
            raise Exception(f"OpenRouter API error: {str(e)}")
    
    async def text_completion(self, prompt: str, **kwargs) -> str:
        """OpenRouter文本完成"""
        messages = [{"role": "user", "content": prompt}]
        response = await self.chat_completion(messages, **kwargs)
        return response["content"]


class AnthropicClient(BaseLLMClient):
    """Anthropic客户端"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.settings = get_settings()
        self.api_key = api_key or self.settings.anthropic_api_key
        
        if not self.api_key:
            raise ValueError("Anthropic API key is required")
        
        self.client = anthropic.AsyncAnthropic(api_key=self.api_key)
    
    async def chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        **kwargs
    ) -> Dict[str, Any]:
        """Anthropic聊天完成"""
        try:
            # 转换消息格式
            system_message = ""
            user_messages = []
            
            for msg in messages:
                if msg["role"] == "system":
                    system_message = msg["content"]
                elif msg["role"] in ["user", "assistant"]:
                    user_messages.append(msg)
            
            # 构建Anthropic格式的消息
            anthropic_messages = []
            for msg in user_messages:
                anthropic_messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
            
            # 准备参数
            create_kwargs = {
                "model": "claude-3-sonnet-20240229",
                "messages": anthropic_messages,
                **kwargs
            }
            
            # 只有在有system消息时才添加
            if system_message:
                create_kwargs["system"] = system_message
            
            response = await self.client.messages.create(**create_kwargs)
            
            return {
                "content": response.content[0].text,
                "usage": {
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens
                },
                "model": response.model
            }
        except Exception as e:
            raise Exception(f"Anthropic API error: {str(e)}")
    
    async def text_completion(self, prompt: str, **kwargs) -> str:
        """Anthropic文本完成"""
        messages = [{"role": "user", "content": prompt}]
        response = await self.chat_completion(messages, **kwargs)
        return response["content"]


class LLMClient:
    """LLM客户端管理器"""
    
    def __init__(self, provider: str = "openrouter"):
        self.provider = provider.lower()
        self.client = self._create_client()
    
    def _create_client(self) -> BaseLLMClient:
        """创建对应的LLM客户端"""
        if self.provider == "openai":
            return OpenAIClient()
        elif self.provider == "openrouter":
            return OpenRouterClient()
        elif self.provider == "anthropic":
            return AnthropicClient()
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")
    
    async def chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        **kwargs
    ) -> Dict[str, Any]:
        """聊天完成"""
        return await self.client.chat_completion(messages, **kwargs)
    
    async def text_completion(self, prompt: str, **kwargs) -> str:
        """文本完成"""
        return await self.client.text_completion(prompt, **kwargs)
    
    def switch_provider(self, provider: str):
        """切换LLM提供商"""
        self.provider = provider.lower()
        self.client = self._create_client() 