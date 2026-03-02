"""
MCP Client - 连接MCP服务器并调用工具

这个客户端演示了：
1. 连接到MCP服务器
2. 获取可用工具列表
3. 调用工具
4. 读取资源

运行: python mcp_client.py
"""

import asyncio
import sys
from contextlib import asynccontextmanager

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPClient:
    """MCP客户端封装类"""
    
    def __init__(self):
        self.session: ClientSession | None = None
        self._client_context = None
        self._session_context = None
    
    async def connect(self, server_script: str = "mcp_server.py"):
        """连接到MCP服务器"""
        server_params = StdioServerParameters(
            command=sys.executable,  # 使用当前Python解释器
            args=[server_script],
            env=None
        )
        
        # 创建stdio客户端连接
        self._client_context = stdio_client(server_params)
        read, write = await self._client_context.__aenter__()
        
        # 创建会话
        self._session_context = ClientSession(read, write)
        self.session = await self._session_context.__aenter__()
        
        # 初始化连接
        await self.session.initialize()
        print("✅ 已连接到MCP服务器")
    
    async def disconnect(self):
        """断开连接"""
        if self._session_context:
            await self._session_context.__aexit__(None, None, None)
        if self._client_context:
            await self._client_context.__aexit__(None, None, None)
        print("👋 已断开MCP服务器连接")
    
    async def list_tools(self) -> list:
        """获取可用工具列表"""
        if not self.session:
            raise RuntimeError("未连接到服务器")
        
        result = await self.session.list_tools()
        return result.tools
    
    async def call_tool(self, name: str, arguments: dict) -> str:
        """调用工具"""
        if not self.session:
            raise RuntimeError("未连接到服务器")
        
        result = await self.session.call_tool(name, arguments)
        
        # 提取文本内容
        if result.content:
            return "\n".join(
                c.text for c in result.content if hasattr(c, 'text')
            )
        return ""
    
    async def list_resources(self) -> list:
        """获取可用资源列表"""
        if not self.session:
            raise RuntimeError("未连接到服务器")
        
        result = await self.session.list_resources()
        return result.resources
    
    async def read_resource(self, uri: str) -> str:
        """读取资源"""
        if not self.session:
            raise RuntimeError("未连接到服务器")
        
        result = await self.session.read_resource(uri)
        if result.contents:
            return "\n".join(
                c.text if hasattr(c, 'text') else str(c)
                for c in result.contents
            )
        return ""


async def demo():
    """演示MCP客户端功能"""
    client = MCPClient()
    
    try:
        # 连接服务器
        await client.connect()
        
        print("\n" + "=" * 50)
        print("📋 获取可用工具列表")
        print("=" * 50)
        tools = await client.list_tools()
        for tool in tools:
            print(f"  🔧 {tool.name}: {tool.description}")
        
        print("\n" + "=" * 50)
        print("🧮 测试计算器工具")
        print("=" * 50)
        result = await client.call_tool("calculator", {
            "operation": "multiply",
            "a": 7,
            "b": 8
        })
        print(f"  {result}")
        
        print("\n" + "=" * 50)
        print("⏰ 测试获取时间工具")
        print("=" * 50)
        result = await client.call_tool("get_current_time", {})
        print(f"  {result}")
        
        print("\n" + "=" * 50)
        print("📝 测试字符串工具")
        print("=" * 50)
        result = await client.call_tool("string_utils", {
            "action": "reverse",
            "text": "Hello MCP!"
        })
        print(f"  {result}")
        
        print("\n" + "=" * 50)
        print("📓 测试笔记管理工具")
        print("=" * 50)
        
        # 添加笔记
        result = await client.call_tool("note_manager", {
            "action": "add",
            "content": "这是第一条笔记"
        })
        print(f"  {result}")
        
        result = await client.call_tool("note_manager", {
            "action": "add",
            "content": "这是第二条笔记 - MCP演示"
        })
        print(f"  {result}")
        
        # 列出笔记
        result = await client.call_tool("note_manager", {
            "action": "list"
        })
        print(f"  {result}")
        
        print("\n" + "=" * 50)
        print("📦 测试资源读取")
        print("=" * 50)
        resources = await client.list_resources()
        for res in resources:
            print(f"  📁 {res.uri}: {res.description}")
        
        content = await client.read_resource("notes://all")
        print(f"  资源内容: {content}")
        
    finally:
        await client.disconnect()


if __name__ == "__main__":
    asyncio.run(demo())
