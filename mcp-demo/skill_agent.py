"""
Skill Agent - 支持Skill概念的LLM Agent

Skill是一组相关功能的集合，类似于Semantic Kernel中的Skill/Plugin概念。
每个Skill包含：
- 名称和描述
- 一组相关工具（Functions）
- 执行逻辑（本地函数或MCP工具调用）

本Agent支持两种Skill类型：
1. 本地Skill (NativeSkill) - 直接在Python中实现的技能，无需MCP服务器
2. MCP Skill (MCPSkill)    - 从MCP服务器加载的技能，通过MCP协议调用

架构:
┌──────────────────────────────────────────────────────────────────┐
│                         Skill Agent                              │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌────────────┐   ┌───────────────────────────────────────┐    │
│   │    LLM     │   │           Skill Registry               │    │
│   │ (DeepSeek/ │   ├───────────────────────────────────────┤    │
│   │  OpenAI)   │   │  MathSkill  │ TimeSkill │  TextSkill  │    │
│   └────────────┘   │  (本地)    │  (本地)   │   (本地)    │    │
│         │          ├───────────────────────────────────────┤    │
│         │          │          NoteSkill (MCP)               │    │
│         ▼          └───────────────────────────────────────┘    │
│   Tool Dispatch ─────────────────────────────────────────────▶  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘

运行前需要设置环境变量:
- OPENAI_API_KEY: API密钥 (支持 DeepSeek 等 OpenAI 兼容 API)
- OPENAI_BASE_URL: API端点 (DeepSeek: https://api.deepseek.com)

运行: python skill_agent.py
"""

import asyncio
import json
import os
import sys
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Awaitable

from openai import AsyncOpenAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


# ============ Skill 数据结构 ============

@dataclass
class Skill:
    """
    Skill（技能）- 一组相关功能的集合

    每个Skill封装了一个特定领域的能力，包含：
    - 名称和描述
    - 该技能提供的工具列表（OpenAI格式）
    - 处理工具调用的回调函数
    """
    name: str
    description: str
    tools: list[dict] = field(default_factory=list)
    handler: Callable[[str, dict], Awaitable[str]] | None = None

    def get_tool_names(self) -> list[str]:
        """返回该Skill包含的所有工具名称"""
        return [t["function"]["name"] for t in self.tools]


class SkillRegistry:
    """
    Skill注册表 - 管理所有已注册的Skill

    负责：
    1. 注册和存储Skill
    2. 汇总所有Skill的工具供LLM使用
    3. 将工具调用分发到对应的Skill处理
    """

    def __init__(self):
        self._skills: dict[str, Skill] = {}

    def register(self, skill: Skill) -> None:
        """注册一个Skill"""
        self._skills[skill.name] = skill
        print(f"  ✅ 注册Skill: [{skill.name}] - {skill.description} "
              f"({len(skill.tools)} 个工具: {', '.join(skill.get_tool_names())})")

    def get_all_tools(self) -> list[dict]:
        """获取所有Skill的工具列表（OpenAI格式）"""
        tools = []
        for skill in self._skills.values():
            tools.extend(skill.tools)
        return tools

    async def dispatch(self, tool_name: str, arguments: dict) -> str:
        """
        将工具调用分发到对应的Skill

        遍历所有已注册的Skill，找到包含该工具的Skill并调用其handler。
        """
        for skill in self._skills.values():
            if tool_name in skill.get_tool_names():
                if skill.handler is None:
                    return f"Skill [{skill.name}] 未配置处理函数"
                return await skill.handler(tool_name, arguments)
        return f"未找到处理工具 '{tool_name}' 的Skill"

    def list_skills(self) -> list[Skill]:
        """返回所有已注册的Skill"""
        return list(self._skills.values())


# ============ 本地 Skill 定义 ============

def create_math_skill() -> Skill:
    """
    数学技能 (MathSkill) - 本地实现

    提供基本数学运算能力，直接在Python中计算，无需MCP服务器。
    """
    tools = [
        {
            "type": "function",
            "function": {
                "name": "math_calculate",
                "description": "执行基本数学运算（加、减、乘、除）",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation": {
                            "type": "string",
                            "enum": ["add", "subtract", "multiply", "divide"],
                            "description": "数学运算类型"
                        },
                        "a": {
                            "type": "number",
                            "description": "第一个数字"
                        },
                        "b": {
                            "type": "number",
                            "description": "第二个数字"
                        }
                    },
                    "required": ["operation", "a", "b"]
                }
            }
        }
    ]

    async def handler(tool_name: str, arguments: dict) -> str:
        op = arguments["operation"]
        a = arguments["a"]
        b = arguments["b"]

        if op == "add":
            result = a + b
        elif op == "subtract":
            result = a - b
        elif op == "multiply":
            result = a * b
        elif op == "divide":
            if b == 0:
                return f"错误：除法运算中除数不能为零 (a={a}, b={b})"
            result = a / b
        else:
            return f"未知运算：{op}"

        return f"计算结果：{a} {op} {b} = {result}"

    return Skill(
        name="MathSkill",
        description="数学计算技能，支持加减乘除运算",
        tools=tools,
        handler=handler
    )


def create_time_skill() -> Skill:
    """
    时间技能 (TimeSkill) - 本地实现

    提供时间查询能力，直接读取系统时间，无需MCP服务器。
    """
    tools = [
        {
            "type": "function",
            "function": {
                "name": "time_get_current",
                "description": "获取当前日期和时间",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "format": {
                            "type": "string",
                            "description": "时间格式，如 '%Y-%m-%d %H:%M:%S'",
                            "default": "%Y-%m-%d %H:%M:%S"
                        }
                    }
                }
            }
        }
    ]

    async def handler(tool_name: str, arguments: dict) -> str:
        fmt = arguments.get("format", "%Y-%m-%d %H:%M:%S")
        current_time = datetime.now().strftime(fmt)
        return f"当前时间：{current_time}"

    return Skill(
        name="TimeSkill",
        description="时间查询技能，可获取当前日期和时间",
        tools=tools,
        handler=handler
    )


def create_text_skill() -> Skill:
    """
    文本技能 (TextSkill) - 本地实现

    提供字符串处理能力，直接在Python中执行，无需MCP服务器。
    """
    tools = [
        {
            "type": "function",
            "function": {
                "name": "text_process",
                "description": "字符串处理工具（反转、大写、小写、统计长度）",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "enum": ["reverse", "upper", "lower", "length"],
                            "description": "要执行的字符串操作"
                        },
                        "text": {
                            "type": "string",
                            "description": "要处理的字符串"
                        }
                    },
                    "required": ["action", "text"]
                }
            }
        }
    ]

    async def handler(tool_name: str, arguments: dict) -> str:
        action = arguments["action"]
        text = arguments["text"]

        if action == "reverse":
            result = text[::-1]
        elif action == "upper":
            result = text.upper()
        elif action == "lower":
            result = text.lower()
        elif action == "length":
            result = str(len(text))
        else:
            return f"未知操作：{action}"

        return f"处理结果：{result}"

    return Skill(
        name="TextSkill",
        description="文本处理技能，支持反转、大小写转换、长度统计",
        tools=tools,
        handler=handler
    )


# ============ MCP Skill 工厂 ============

def create_note_skill(mcp_session: ClientSession) -> Skill:
    """
    笔记技能 (NoteSkill) - MCP实现

    提供笔记管理能力，通过MCP协议调用远程工具。
    这展示了如何将MCP工具包装成Skill。
    """
    tools = [
        {
            "type": "function",
            "function": {
                "name": "note_manage",
                "description": "笔记管理工具（添加、列出、删除、清空笔记）",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "enum": ["add", "list", "delete", "clear"],
                            "description": "笔记操作类型"
                        },
                        "content": {
                            "type": "string",
                            "description": "笔记内容（添加时需要）"
                        },
                        "note_id": {
                            "type": "integer",
                            "description": "笔记ID（删除时需要）"
                        }
                    },
                    "required": ["action"]
                }
            }
        }
    ]

    async def handler(tool_name: str, arguments: dict) -> str:
        # 通过MCP协议调用远程的 note_manager 工具
        result = await mcp_session.call_tool("note_manager", arguments)
        if result.content:
            return "\n".join(
                c.text for c in result.content if hasattr(c, "text")
            )
        return f"工具 {tool_name} 执行完成，无返回内容"

    return Skill(
        name="NoteSkill",
        description="笔记管理技能（通过MCP协议调用），支持添加、列出、删除笔记",
        tools=tools,
        handler=handler
    )


# ============ Skill Agent ============

class SkillAgent:
    """
    支持Skill的LLM Agent

    与基础 MCPAgent 的主要区别：
    - 工具被组织成有意义的"Skill"（技能），每个Skill负责一个能力域
    - 支持同时使用本地Skill和MCP Skill
    - SkillRegistry 统一管理所有Skill，实现工具的注册与分发
    - 工具名称带有Skill前缀（如 math_calculate、time_get_current），
      清晰表达了工具归属的Skill

    核心流程:
    User Query → LLM → Tool Call → SkillRegistry.dispatch → Skill.handler → Result → LLM
    """

    def __init__(self, model: str = "deepseek-chat"):
        self.model = model
        self.client = AsyncOpenAI(
            base_url=os.getenv("OPENAI_BASE_URL", "https://api.deepseek.com")
        )
        self.registry = SkillRegistry()
        self.session: ClientSession | None = None
        self._client_context = None
        self._session_context = None

    async def connect_mcp(self, server_script: str = "mcp_server.py"):
        """连接到MCP服务器并初始化MCP Skill"""
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
        print("✅ SkillAgent已连接到MCP服务器")

    async def disconnect(self):
        """断开MCP连接"""
        if self._session_context:
            await self._session_context.__aexit__(None, None, None)
        if self._client_context:
            await self._client_context.__aexit__(None, None, None)

    def register_native_skills(self):
        """注册所有本地Skill（无需MCP服务器）"""
        print("\n📦 注册本地Skill:")
        self.registry.register(create_math_skill())
        self.registry.register(create_time_skill())
        self.registry.register(create_text_skill())

    def register_mcp_skills(self):
        """注册MCP Skill（需要先调用 connect_mcp）"""
        if self.session is None:
            raise RuntimeError("请先调用 connect_mcp() 建立MCP连接")
        print("\n📦 注册MCP Skill:")
        self.registry.register(create_note_skill(self.session))

    async def chat(self, user_message: str) -> str:
        """
        处理用户消息，使用已注册的Skill完成任务

        流程:
        1. 收集所有已注册Skill的工具
        2. 发送用户消息和工具列表给LLM
        3. 如果LLM决定调用工具，通过SkillRegistry分发
        4. 将工具结果返回给LLM，继续直到得到最终答案
        """
        all_tools = self.registry.get_all_tools()

        # 构建系统提示，说明可用的Skill
        skills_info = "\n".join(
            f"- [{s.name}] {s.description}"
            for s in self.registry.list_skills()
        )

        messages = [
            {
                "role": "system",
                "content": f"""你是一个有帮助的AI助手，你拥有以下技能（Skills）：

{skills_info}

每个技能包含一组工具（Functions），当用户的请求需要使用工具时，请调用对应技能的工具。
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
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=all_tools if all_tools else None,
                tool_choice="auto"
            )

            assistant_message = response.choices[0].message

            # 没有工具调用，返回最终答案
            if not assistant_message.tool_calls:
                return assistant_message.content

            messages.append(assistant_message)

            for tool_call in assistant_message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)

                print(f"  🔧 调用Skill工具: {tool_name}")
                print(f"     参数: {tool_args}")

                # 通过SkillRegistry分发工具调用
                tool_result = await self.registry.dispatch(tool_name, tool_args)
                print(f"     结果: {tool_result}")

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_result
                })

            # 继续循环，让LLM处理工具结果


async def demo():
    """演示SkillAgent功能"""
    agent = SkillAgent()

    try:
        # 注册本地Skill（不需要MCP服务器）
        agent.register_native_skills()

        # 连接MCP服务器并注册MCP Skill
        await agent.connect_mcp()
        agent.register_mcp_skills()

        print("\n" + "=" * 60)
        print("💬 Skill Agent 演示")
        print("=" * 60)

        # 演示1: 使用MathSkill
        print("\n📌 用户: 帮我计算 123 乘以 456")
        response = await agent.chat("帮我计算 123 乘以 456")
        print(f"🤖 Agent: {response}")

        # 演示2: 使用TimeSkill
        print("\n📌 用户: 现在几点了？")
        response = await agent.chat("现在几点了？")
        print(f"🤖 Agent: {response}")

        # 演示3: 使用TextSkill
        print("\n📌 用户: 请把 'Hello Skill Agent' 转成大写")
        response = await agent.chat("请把 'Hello Skill Agent' 转成大写")
        print(f"🤖 Agent: {response}")

        # 演示4: 使用NoteSkill（MCP）
        print("\n📌 用户: 帮我添加一条笔记：学习了Skill Agent的实现原理")
        response = await agent.chat("帮我添加一条笔记：学习了Skill Agent的实现原理")
        print(f"🤖 Agent: {response}")

        print("\n📌 用户: 显示我所有的笔记")
        response = await agent.chat("显示我所有的笔记")
        print(f"🤖 Agent: {response}")

        # 演示5: 跨Skill组合任务
        print("\n📌 用户: 先计算 99 加 1，再把结果转成字符串并反转")
        response = await agent.chat("先计算 99 加 1，再把结果转成字符串并反转")
        print(f"🤖 Agent: {response}")

    finally:
        await agent.disconnect()


async def interactive():
    """交互模式"""
    agent = SkillAgent()

    try:
        agent.register_native_skills()
        await agent.connect_mcp()
        agent.register_mcp_skills()

        print("\n" + "=" * 60)
        print("💬 Skill Agent 交互模式")
        print("输入 'skills' 查看已注册的Skill")
        print("输入 'quit' 或 'exit' 退出")
        print("=" * 60)

        while True:
            print()
            user_input = input("📌 你: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ["quit", "exit", "q"]:
                print("👋 再见！")
                break

            if user_input.lower() == "skills":
                print("\n📋 已注册的Skills:")
                for skill in agent.registry.list_skills():
                    print(f"  [{skill.name}] {skill.description}")
                    for tool in skill.tools:
                        print(f"    🔧 {tool['function']['name']}: "
                              f"{tool['function']['description']}")
                continue

            try:
                response = await agent.chat(user_input)
                print(f"🤖 Agent: {response}")
            except Exception as e:
                print(f"❌ 错误: {e}")

    finally:
        await agent.disconnect()


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  警告: 未设置 OPENAI_API_KEY 环境变量")
        print("请设置 DeepSeek API Key:")
        print("  export OPENAI_API_KEY='sk-xxx'")
        print("\n将运行演示模式（需要有效的API密钥）...")

    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        asyncio.run(interactive())
    else:
        asyncio.run(demo())
