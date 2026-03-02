"""
MCP Server - 提供工具给LLM Agent使用

这个服务器演示了MCP的核心概念：
1. 定义工具（Tools）- Agent可以调用的功能
2. 定义资源（Resources）- Agent可以读取的数据
3. 处理工具调用请求

运行: python mcp_server.py
"""

import json
from datetime import datetime
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    TextContent,
    Resource,
    ResourceTemplate,
)


# 创建MCP服务器实例
server = Server("demo-mcp-server")


# ============ 定义工具 ============

@server.list_tools()
async def list_tools() -> list[Tool]:
    """列出所有可用的工具"""
    return [
        Tool(
            name="calculator",
            description="执行基本数学运算（加、减、乘、除）",
            inputSchema={
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
        ),
        Tool(
            name="get_current_time",
            description="获取当前日期和时间",
            inputSchema={
                "type": "object",
                "properties": {
                    "format": {
                        "type": "string",
                        "description": "时间格式，如 '%Y-%m-%d %H:%M:%S'",
                        "default": "%Y-%m-%d %H:%M:%S"
                    }
                }
            }
        ),
        Tool(
            name="string_utils",
            description="字符串处理工具（反转、大写、小写、统计长度）",
            inputSchema={
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
        ),
        Tool(
            name="note_manager",
            description="简单的笔记管理工具（添加、列出、删除笔记）",
            inputSchema={
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
        )
    ]


# 内存中存储笔记
notes_storage: dict[int, dict] = {}
note_counter = 0


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """处理工具调用"""
    global note_counter
    
    if name == "calculator":
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
                return [TextContent(type="text", text="错误：除数不能为零")]
            result = a / b
        else:
            return [TextContent(type="text", text=f"未知操作：{op}")]
        
        return [TextContent(type="text", text=f"计算结果：{a} {op} {b} = {result}")]
    
    elif name == "get_current_time":
        fmt = arguments.get("format", "%Y-%m-%d %H:%M:%S")
        current_time = datetime.now().strftime(fmt)
        return [TextContent(type="text", text=f"当前时间：{current_time}")]
    
    elif name == "string_utils":
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
            return [TextContent(type="text", text=f"未知操作：{action}")]
        
        return [TextContent(type="text", text=f"处理结果：{result}")]
    
    elif name == "note_manager":
        action = arguments["action"]
        
        if action == "add":
            content = arguments.get("content", "")
            if not content:
                return [TextContent(type="text", text="错误：笔记内容不能为空")]
            note_counter += 1
            notes_storage[note_counter] = {
                "id": note_counter,
                "content": content,
                "created_at": datetime.now().isoformat()
            }
            return [TextContent(type="text", text=f"笔记已添加，ID: {note_counter}")]
        
        elif action == "list":
            if not notes_storage:
                return [TextContent(type="text", text="当前没有笔记")]
            notes_list = json.dumps(list(notes_storage.values()), ensure_ascii=False, indent=2)
            return [TextContent(type="text", text=f"所有笔记：\n{notes_list}")]
        
        elif action == "delete":
            note_id = arguments.get("note_id")
            if note_id is None:
                return [TextContent(type="text", text="错误：需要提供笔记ID")]
            if note_id not in notes_storage:
                return [TextContent(type="text", text=f"错误：笔记ID {note_id} 不存在")]
            del notes_storage[note_id]
            return [TextContent(type="text", text=f"笔记 {note_id} 已删除")]
        
        elif action == "clear":
            notes_storage.clear()
            return [TextContent(type="text", text="所有笔记已清空")]
        
        return [TextContent(type="text", text=f"未知操作：{action}")]
    
    return [TextContent(type="text", text=f"未知工具：{name}")]


# ============ 定义资源 ============

@server.list_resources()
async def list_resources() -> list[Resource]:
    """列出所有可用的资源"""
    return [
        Resource(
            uri="notes://all",
            name="All Notes",
            description="获取所有保存的笔记",
            mimeType="application/json"
        )
    ]


@server.read_resource()
async def read_resource(uri) -> str:
    """读取资源内容"""
    uri_str = str(uri)
    if uri_str == "notes://all":
        return json.dumps(list(notes_storage.values()), ensure_ascii=False, indent=2)
    raise ValueError(f"未知资源：{uri_str}")


async def main():
    """启动MCP服务器"""
    # 注意: 不能在这里使用 print()，因为 stdout 用于 MCP 协议通信
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
