# MCP Demo - LLM Agent + MCP 演示项目

这是一个简单但完整的项目，用于演示 **LLM Agent** 与 **MCP (Model Context Protocol)** 的交互方式。

## 什么是 MCP？

MCP (Model Context Protocol) 是 Anthropic 提出的一个开放协议，用于标准化 LLM 应用与外部工具/数据源的通信方式。

```
┌─────────────────────────────────────────────────────────────────┐
│                        MCP 架构图                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌──────────┐     ┌─────────────┐     ┌──────────────────┐    │
│   │   用户   │────▶│  LLM Agent  │────▶│   MCP Client     │    │
│   └──────────┘     │  (GPT等)    │     │   (协议客户端)   │    │
│                    └─────────────┘     └────────┬─────────┘    │
│                          ▲                      │               │
│                          │                      │ stdio/SSE     │
│                          │                      ▼               │
│                    ┌─────────────┐     ┌──────────────────┐    │
│                    │  最终回答   │◀────│   MCP Server     │    │
│                    └─────────────┘     │   (工具+资源)    │    │
│                                        └──────────────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 项目结构

```
mcp-demo/
├── pyproject.toml      # 项目配置
├── mcp_server.py       # MCP服务器 - 提供工具和资源
├── mcp_client.py       # MCP客户端 - 连接服务器并调用工具
├── agent.py            # LLM Agent - 完整演示LLM+MCP交互
├── skill_agent.py      # Skill Agent - 支持Skill概念的LLM Agent
└── README.md           # 说明文档
```

## 核心组件说明

### 1. MCP Server (`mcp_server.py`)

MCP服务器负责提供**工具(Tools)**和**资源(Resources)**：

| 工具名 | 功能 |
|--------|------|
| `calculator` | 数学运算（加减乘除）|
| `get_current_time` | 获取当前时间 |
| `string_utils` | 字符串处理（反转、大小写、长度）|
| `note_manager` | 笔记管理（添加、列表、删除）|

### 2. MCP Client (`mcp_client.py`)

MCP客户端演示如何：
- 连接到MCP服务器
- 获取可用工具列表
- 调用工具并获取结果
- 读取资源

### 3. LLM Agent (`agent.py`)

Agent将LLM与MCP集成，实现完整的工作流程：

```
用户问题 → LLM分析 → 决定调用工具 → MCP调用 → 获取结果 → LLM生成回答
```

### 4. Skill Agent (`skill_agent.py`)

Skill Agent在LLM Agent的基础上引入了**Skill（技能）**的概念，将工具按能力域组织：

```
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
```

| Skill | 类型 | 工具 | 说明 |
|-------|------|------|------|
| `MathSkill` | 本地 | `math_calculate` | 数学四则运算 |
| `TimeSkill` | 本地 | `time_get_current` | 获取当前时间 |
| `TextSkill` | 本地 | `text_process` | 字符串处理 |
| `NoteSkill` | MCP | `note_manage` | 笔记管理（调用MCP服务器）|

## 快速开始

### 1. 安装依赖

```bash
cd mcp-demo
pip install -e .
```

或者直接安装依赖：

```bash
pip install mcp httpx openai
```

### 2. 测试MCP客户端（无需API密钥）

```bash
python mcp_client.py
```

这将演示MCP客户端直接连接服务器并调用工具。

### 3. 运行完整Agent演示

首先设置API密钥：

```bash
# Windows
set OPENAI_API_KEY=your-api-key

# Linux/Mac
export OPENAI_API_KEY=your-api-key
```

然后运行：

```bash
# 演示模式
python agent.py

# 交互模式
$env:OPENAI_API_KEY = "sk-xxx"
python agent.py --interactive
```

### 4. 运行Skill Agent演示

```bash
# 演示模式
python skill_agent.py

# 交互模式
python skill_agent.py --interactive
# 在交互模式中输入 'skills' 可查看已注册的所有Skill
```

## 代码示例

### 定义MCP工具

```python
@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="calculator",
            description="执行数学运算",
            inputSchema={
                "type": "object",
                "properties": {
                    "operation": {"type": "string", "enum": ["add", "subtract", "multiply", "divide"]},
                    "a": {"type": "number"},
                    "b": {"type": "number"}
                },
                "required": ["operation", "a", "b"]
            }
        )
    ]
```

### 调用MCP工具

```python
# 客户端调用
result = await client.call_tool("calculator", {
    "operation": "multiply",
    "a": 7,
    "b": 8
})
print(result)  # 计算结果：7 multiply 8 = 56
```

### Skill Agent集成本地Skill和MCP Skill

```python
# 创建SkillAgent
agent = SkillAgent()

# 注册本地Skill（无需MCP服务器）
agent.register_native_skills()

# 连接MCP服务器并注册MCP Skill
await agent.connect_mcp()
agent.register_mcp_skills()

# 使用Agent（LLM自动选择合适的Skill工具）
response = await agent.chat("帮我计算 99 + 1，再把结果转成字符串并反转")
```

### Agent集成LLM+MCP

```python
# Agent自动决定何时调用工具
response = await agent.chat("帮我计算 123 乘以 456")
# LLM分析 → 调用calculator工具 → 返回结果
```

## 扩展建议

1. **添加更多工具**：天气查询、文件操作、数据库访问等
2. **支持多个MCP服务器**：同时连接多个服务器获取更多工具
3. **添加资源管理**：配置文件、用户数据等
4. **使用SSE传输**：支持HTTP/SSE方式连接MCP服务器
5. **工具组合**：让Agent能够组合多个工具完成复杂任务

## 参考资料

- [MCP 官方文档](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)

## License

MIT
