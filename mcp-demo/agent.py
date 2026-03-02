"""
LLM Agent with MCP - 演示LLM如何通过MCP调用工具

这个脚本展示了完整的Agent工作流程：
1. 用户提出问题/任务
2. LLM分析并决定需要调用哪些工具
3. 通过MCP协议调用工具
4. LLM根据工具返回结果生成最终回答

运行前需要设置环境变量:
- OPENAI_API_KEY: API密钥 (支持 DeepSeek 等 OpenAI 兼容 API)
- OPENAI_BASE_URL: API端点 (DeepSeek: https://api.deepseek.com)

运行: python agent.py
"""

import asyncio
import json
import os
import sys
from typing import Any

from openai import AsyncOpenAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPAgent:
    """
    LLM Agent + MCP 集成
    
    核心流程:
    User Query → LLM → Tool Calls → MCP Server → Tool Results → LLM → Final Response
    """
    
    def __init__(self, model: str = "deepseek-chat"):
        self.model = model
        self.client = AsyncOpenAI(
            base_url=os.getenv("OPENAI_BASE_URL", "https://api.deepseek.com")
        )
        self.session: ClientSession | None = None
        self._client_context = None
        self._session_context = None
        self.tools_cache: list[dict] = []
    
    async def connect_mcp(self, server_script: str = "mcp_server.py"):
        """连接到MCP服务器"""
        server_params = StdioServerParameters(
            command=sys.executable,
            args=[server_script],
            env=None
        )
        
        self._client_context = stdio_client(server_params)
        read, write = await self._client_context.__aenter__()
        
        self._session_context = ClientSession(read, write)
        self.session = await self._session_context.__aenter__()
        
        await self.session.initialize()
        
        # 获取并缓存工具列表
        await self._load_tools()
        print("✅ Agent已连接到MCP服务器")
    
    async def disconnect(self):
        """断开MCP连接"""
        if self._session_context:
            await self._session_context.__aexit__(None, None, None)
        if self._client_context:
            await self._client_context.__aexit__(None, None, None)
    
    async def _load_tools(self):
        """从MCP服务器加载工具定义，转换为OpenAI格式"""
        result = await self.session.list_tools()
        
        self.tools_cache = []
        for tool in result.tools:
            # 转换MCP工具格式为OpenAI函数调用格式
            self.tools_cache.append({
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.inputSchema
                }
            })
        
        print(f"📋 已加载 {len(self.tools_cache)} 个工具")
    
    async def _call_mcp_tool(self, name: str, arguments: dict) -> str:
        """通过MCP调用工具"""
        result = await self.session.call_tool(name, arguments)
        
        if result.content:
            return "\n".join(
                c.text for c in result.content if hasattr(c, 'text')
            )
        return "工具执行完成，无返回内容"
    
    async def chat(self, user_message: str) -> str:
        """
        处理用户消息，完整的Agent循环
        
        流程:
        1. 发送用户消息给LLM
        2. 如果LLM决定调用工具，执行工具调用
        3. 将工具结果返回给LLM
        4. 重复直到LLM给出最终答案
        """
        messages = [
            {
                "role": "system",
                "content": """你是一个helpful的AI助手，你可以使用以下工具来帮助用户：
                
1. calculator - 执行数学计算
2. get_current_time - 获取当前时间
3. string_utils - 字符串处理（反转、大小写转换、长度统计）
4. note_manager - 管理笔记（添加、列出、删除）

当用户的请求需要使用工具时，请调用相应的工具。
回答时请使用中文。"""
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
        
        print(f"\n🤔 思考中...")
        
        # Agent循环
        while True:
            # 调用LLM
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.tools_cache if self.tools_cache else None,
                tool_choice="auto"
            )
            
            assistant_message = response.choices[0].message
            
            # 如果没有工具调用，返回最终回答
            if not assistant_message.tool_calls:
                return assistant_message.content
            
            # 处理工具调用
            messages.append(assistant_message)
            
            for tool_call in assistant_message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)
                
                print(f"  🔧 调用工具: {tool_name}")
                print(f"     参数: {tool_args}")
                
                # 通过MCP调用工具
                tool_result = await self._call_mcp_tool(tool_name, tool_args)
                print(f"     结果: {tool_result}")
                
                # 将工具结果添加到消息中
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_result
                })
            
            # 继续循环，让LLM处理工具结果


async def demo():
    """演示Agent功能"""
    agent = MCPAgent()
    
    try:
        await agent.connect_mcp()
        
        print("\n" + "=" * 60)
        print("💬 LLM Agent + MCP 演示")
        print("=" * 60)
        
        # 演示1: 数学计算
        print("\n📌 用户: 帮我计算 123 乘以 456 等于多少？")
        response = await agent.chat("帮我计算 123 乘以 456 等于多少？")
        print(f"🤖 Agent: {response}")
        
        # 演示2: 时间查询  
        print("\n📌 用户: 现在几点了？")
        response = await agent.chat("现在几点了？")
        print(f"🤖 Agent: {response}")
        
        # 演示3: 字符串处理
        print("\n📌 用户: 请把 'Hello World' 反转一下")
        response = await agent.chat("请把 'Hello World' 反转一下")
        print(f"🤖 Agent: {response}")
        
        # 演示4: 笔记管理
        print("\n📌 用户: 帮我添加一条笔记：今天学习了MCP协议")
        response = await agent.chat("帮我添加一条笔记：今天学习了MCP协议")
        print(f"🤖 Agent: {response}")
        
        print("\n📌 用户: 显示我的所有笔记")
        response = await agent.chat("显示我的所有笔记")
        print(f"🤖 Agent: {response}")
        
        # 演示5: 复合任务
        print("\n📌 用户: 帮我计算 (25 + 75) 然后把结果转成字符串并反转")
        response = await agent.chat("帮我计算 25 加 75，然后把结果转成字符串并反转")
        print(f"🤖 Agent: {response}")
        
    finally:
        await agent.disconnect()


async def interactive():
    """交互模式"""
    agent = MCPAgent()
    
    try:
        await agent.connect_mcp()
        
        print("\n" + "=" * 60)
        print("💬 LLM Agent + MCP 交互模式")
        print("输入 'quit' 或 'exit' 退出")
        print("=" * 60)
        
        while True:
            print()
            user_input = input("📌 你: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 再见！")
                break
            
            try:
                response = await agent.chat(user_input)
                print(f"🤖 Agent: {response}")
            except Exception as e:
                print(f"❌ 错误: {e}")
        
    finally:
        await agent.disconnect()


if __name__ == "__main__":
    # 检查API密钥
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  警告: 未设置 OPENAI_API_KEY 环境变量")
        print("请设置 DeepSeek API Key:")
        print("  $env:OPENAI_API_KEY = 'sk-xxx'")
        print("\n将运行演示模式（需要有效的API密钥）...")
    
    # 选择模式
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        asyncio.run(interactive())
    else:
        asyncio.run(demo())
