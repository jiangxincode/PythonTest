"""
本地演示 - 无需API密钥

这个脚本演示MCP的核心概念，不需要LLM API。
它模拟了Agent决策过程，帮助理解MCP工作原理。

运行: python demo_local.py
"""

import asyncio
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def demo():
    """本地MCP演示"""
    
    print("=" * 60)
    print("🚀 MCP 本地演示 (无需API密钥)")
    print("=" * 60)
    
    # 连接MCP服务器
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["mcp_server.py"],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("\n✅ 已连接到MCP服务器")
            
            # 1. 展示工具列表
            print("\n" + "=" * 60)
            print("📋 步骤1: 获取可用工具")
            print("=" * 60)
            print("说明: Agent首先向MCP服务器查询可用的工具列表")
            print()
            
            tools_result = await session.list_tools()
            for tool in tools_result.tools:
                print(f"  🔧 {tool.name}")
                print(f"     描述: {tool.description}")
                print()
            
            # 2. 演示计算器
            print("=" * 60)
            print("🧮 步骤2: 调用计算器工具")
            print("=" * 60)
            print("场景: 用户问 '123 乘以 456 等于多少？'")
            print("Agent分析后决定调用 calculator 工具")
            print()
            
            result = await session.call_tool("calculator", {
                "operation": "multiply",
                "a": 123,
                "b": 456
            })
            print(f"调用: calculator(operation='multiply', a=123, b=456)")
            print(f"返回: {result.content[0].text}")
            print()
            
            # 3. 演示时间查询
            print("=" * 60)
            print("⏰ 步骤3: 调用时间工具")
            print("=" * 60)
            print("场景: 用户问 '现在几点了？'")
            print()
            
            result = await session.call_tool("get_current_time", {})
            print(f"调用: get_current_time()")
            print(f"返回: {result.content[0].text}")
            print()
            
            # 4. 演示字符串处理
            print("=" * 60)
            print("📝 步骤4: 调用字符串工具")
            print("=" * 60)
            print("场景: 用户说 '把Hello World反转一下'")
            print()
            
            result = await session.call_tool("string_utils", {
                "action": "reverse",
                "text": "Hello World"
            })
            print(f"调用: string_utils(action='reverse', text='Hello World')")
            print(f"返回: {result.content[0].text}")
            print()
            
            # 5. 演示笔记管理
            print("=" * 60)
            print("📓 步骤5: 调用笔记管理工具")
            print("=" * 60)
            print("场景: 用户说 '帮我记录一下今天学习了MCP'")
            print()
            
            result = await session.call_tool("note_manager", {
                "action": "add",
                "content": "今天学习了MCP协议"
            })
            print(f"调用: note_manager(action='add', content='今天学习了MCP协议')")
            print(f"返回: {result.content[0].text}")
            print()
            
            result = await session.call_tool("note_manager", {
                "action": "add",
                "content": "MCP可以让LLM调用外部工具"
            })
            print(f"调用: note_manager(action='add', content='MCP可以让LLM调用外部工具')")
            print(f"返回: {result.content[0].text}")
            print()
            
            print("场景: 用户说 '显示所有笔记'")
            print()
            result = await session.call_tool("note_manager", {
                "action": "list"
            })
            print(f"调用: note_manager(action='list')")
            print(f"返回: {result.content[0].text}")
            print()
            
            # 6. 演示资源读取
            print("=" * 60)
            print("📦 步骤6: 读取资源")
            print("=" * 60)
            print("说明: MCP除了工具，还支持资源(Resources)概念")
            print("资源是只读数据，Agent可以获取但不能修改")
            print()
            
            resources = await session.list_resources()
            for res in resources.resources:
                print(f"  📁 {res.uri}: {res.description}")
            
            content = await session.read_resource("notes://all")
            print(f"\n读取 notes://all 资源:")
            print(f"{content.contents[0].text if content.contents else '(空)'}")
            
            # 总结
            print()
            print("=" * 60)
            print("📚 MCP 工作流程总结")
            print("=" * 60)
            print("""
┌────────────────────────────────────────────────────────────┐
│                     完整工作流程                            │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  1. 用户提问: "帮我计算 123 × 456"                          │
│                    ↓                                       │
│  2. LLM分析需要调用工具                                     │
│                    ↓                                       │
│  3. Agent通过MCP协议调用calculator工具                      │
│     → MCP Client 发送请求                                  │
│     → MCP Server 执行计算                                  │
│     → 返回结果: 56088                                      │
│                    ↓                                       │
│  4. LLM根据结果生成自然语言回答                             │
│     "123乘以456等于56088"                                  │
│                                                            │
└────────────────────────────────────────────────────────────┘
""")
            print("演示完成! 👋")


if __name__ == "__main__":
    asyncio.run(demo())
