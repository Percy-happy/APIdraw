# Ollama 画板连接助手

这个模块提供了与 Ollama API 交互的功能，并能自动检测和执行画板的远程API命令。当AI输出包含画板远程API调用时，会自动转换并执行这些命令。

## 功能特点

- 连接 Ollama 服务器并发送提示
- 自动从 Ollama 响应中提取画板 API 命令
- 支持执行多种画板操作（画线、画圆、画矩形、添加文本等）
- 提供两种执行模式：直接调用 API 模块或通过 HTTP 请求
- 友好的用户界面和错误处理
- 详细的执行结果反馈

## 安装要求

- Python 3.6 或更高版本
- 依赖库：`requests`

安装依赖：

```bash
pip install requests
```

## 使用方法

### 1. 直接运行脚本

你可以直接运行 `ollama.py` 脚本与模块交互：

```bash
python3 ollama.py
```

运行后，系统会提示你选择是否使用示例提示，或者输入自定义的模型名称和提示文本。

### 2. 作为模块导入

你也可以在自己的 Python 代码中导入并使用 `OllamaDrawer` 类：

```python
from ollama import OllamaDrawer

# 创建实例
drawer = OllamaDrawer(
    ollama_url="http://localhost:11434",  # Ollama 服务器地址
    draw_api_url="http://localhost:8000"  # 画板 API 地址
)

# 处理 Ollama 响应
result = drawer.process_ollama_response(
    model="llama2",  # 使用的模型
    prompt="请在画板上画一个红色的圆，然后添加一些文本"  # 提示内容
)

# 查看结果
print(f"检测到 {result['total_commands']} 个命令，成功执行 {result['successful_commands']} 个")
```

## API 命令支持

该模块支持以下画板 API 命令：

- `draw_line(x1, y1, x2, y2, color=None, width=None)` - 绘制线条
- `draw_circle(x, y, radius, color=None, width=None)` - 绘制圆形
- `draw_rectangle(x, y, width, height, color=None, width=None)` - 绘制矩形
- `draw_text(x, y, text, color=None, font_size=20)` - 绘制文本
- `export(filename=None)` - 导出画板
- `clear()` - 清空画板
- `set_color(color)` - 设置颜色
- `set_line_width(width)` - 设置线宽
- `execute_command(command)` - 执行命令

## 工作原理

1. **连接 Ollama**：通过 Ollama 的 API 发送提示并获取响应
2. **提取命令**：使用正则表达式从 Ollama 响应中识别 API 调用
3. **解析参数**：智能解析命令参数，包括数字、字符串和颜色值
4. **执行命令**：
   - 优先尝试使用直接导入的 API 模块
   - 如失败，则通过 HTTP 请求调用远程 API
5. **反馈结果**：提供详细的执行结果和状态报告

## 示例

### 示例提示格式

当使用 Ollama 生成 API 命令时，建议使用以下格式提示：

```
请在画板上创建一个简单的图形：
1. 画一个蓝色的圆在中间位置
2. 画一条红色的线从左上角到右下角
3. 在底部添加文本"Ollama 绘制"

请使用以下格式输出 API 调用：
api.draw_circle(400, 300, 50, "#0000ff", 2)
api.draw_line(100, 100, 700, 500, "#ff0000", 3)
api.draw_text(350, 550, "Ollama 绘制", "#000000", 24)
```

### 执行结果示例

```
=== Ollama 响应 ===
根据您的要求，我已经生成了以下 API 调用：
api.draw_circle(400, 300, 50, "#0000ff", 2)
api.draw_line(100, 100, 700, 500, "#ff0000", 3)
api.draw_text(350, 550, "Ollama 绘制", "#000000", 24)

=== 检测到API命令，开始执行 ===
执行命令: draw_circle(400, 300, 50, #0000ff, 2)
HTTP请求成功: 200
执行命令: draw_line(100, 100, 700, 500, #ff0000, 3)
HTTP请求成功: 200
执行命令: draw_text(350, 550, Ollama 绘制, #000000, 24)
HTTP请求成功: 200

=== 执行完成 ===

=== 执行结果摘要 ===
检测到命令数: 3
成功执行数: 3
  ✓ 成功: draw_circle(400, 300, 50, "#0000ff", 2)
  ✓ 成功: draw_line(100, 100, 700, 500, "#ff0000", 3)
  ✓ 成功: draw_text(350, 550, "Ollama 绘制", "#000000", 24)
```

## 常见问题

### Q: 连接 Ollama 失败怎么办？

A: 请确保 Ollama 服务正在运行，默认地址是 http://localhost:11434。如果你的 Ollama 安装在不同地址，请在创建实例时指定。

### Q: 执行 API 命令失败怎么办？

A: 检查以下几点：

- 确保画板应用正在运行
- 确认远程 API 地址正确（默认 http://localhost:8000）
- 检查 API 参数是否符合要求
- 查看错误信息以确定具体原因

### Q: 可以支持其他模型吗？

A: 是的，你可以使用任何 Ollama 支持的模型，只需在调用时指定模型名称即可。

## 开发者说明

### 自定义配置

你可以在创建 `OllamaDrawer` 实例时自定义配置：

```python
drawer = OllamaDrawer(
    ollama_url="http://custom-ollama-server:11434",  # 自定义 Ollama 地址
    draw_api_url="http://custom-draw-server:8080"    # 自定义画板 API 地址
)
```

### 扩展支持的 API 命令

要添加新的 API 命令支持，需要：

1. 在 `api_patterns` 字典中添加新的正则表达式模式
2. 在 `execute_api_command` 和 `execute_api_via_http` 方法中添加对应的处理逻辑

## 许可证
