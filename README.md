# AI 画板应用 / AI Drawing Board

这是一个功能丰富的在线画板应用，支持手动绘画和API调用绘画，以及导出图片功能。

This is a versatile drawing board application that supports both manual drawing and API-controlled drawing functionality, along with image export capabilities.

## 功能特点 / Features

### 1. 手动绘画 / Manual Drawing
- 支持鼠标和触摸屏绘画 / Draw using mouse or touch
- 可调节画笔颜色和粗细 / Adjust brush color and thickness
- 清空画板功能 / Clear canvas function
- 导出绘画为PNG图片 / Export canvas content as PNG image

### 2. API 控制 / API Drawing Control
- 通过命令字符串绘制基本图形 / Execute drawing commands through API input
- 提供JavaScript API接口供外部调用 / JavaScript API for external control
- 支持绘制直线、圆形、矩形和文本 / Draw lines, circles, rectangles, and text
- API导出功能 / Export functionality through API

## 如何使用 / How to Use

### 手动绘画 / Manual Drawing
1. 在画布上按住鼠标左键或触摸屏幕并移动来绘画 / Draw on canvas by holding mouse button or touching screen
2. 使用颜色选择器选择画笔颜色 / Select brush color from color picker
3. 使用滑块调整画笔粗细 / Adjust brush thickness using the slider
4. 点击"清空画板"按钮清除所有内容 / Click "Clear" button to reset the canvas
5. 点击"导出图片"按钮将绘画保存为PNG文件 / Click "Export" button to save as PNG

### API 命令 / API Commands

#### 命令字符串格式 / Command String Format
在API命令输入框中，可以输入以下格式的命令：

In the API command input area, you can enter commands in the following format:

```
// 绘制直线 / Draw a line
 draw(line, x1, y1, x2, y2)

// 绘制圆形 / Draw a circle
 draw(circle, x, y, radius)

// 绘制矩形 / Draw a rectangle
 draw(rect, x, y, width, height)

// 绘制文本 / Draw text
 draw(text, x, y, "文本内容")

// 导出画布 / Export canvas
 export()
```

输入命令后点击"执行命令"按钮或按Enter键执行。

After entering the command, click the "Execute" button or press Enter to run it.

#### JavaScript API
页面加载后，全局对象`window.AIDrawingAPI`可用于通过JavaScript控制画板：

After page load, the global object `window.AIDrawingAPI` can be used to control the drawing board through JavaScript:

```javascript
// 绘制直线 / Draw a line
 AIDrawingAPI.drawLine(10, 10, 100, 100, "#ff0000", 5);

// 绘制圆形 / Draw a circle
 AIDrawingAPI.drawCircle(150, 150, 50, "#00ff00", 3);

// 绘制矩形 / Draw a rectangle
 AIDrawingAPI.drawRectangle(200, 200, 100, 80, "#0000ff", 2);

// 绘制文本 / Draw text
 AIDrawingAPI.drawText(50, 50, "Hello World", "#ff00ff", 24);

// 导出画布 / Export canvas
 const dataUrl = AIDrawingAPI.export();

// 清空画布 / Clear canvas
 AIDrawingAPI.clear();

// 设置画笔颜色 / Set brush color
 AIDrawingAPI.setColor("#ff9900");

// 设置画笔粗细 / Set line width
 AIDrawingAPI.setLineWidth(8);

// 执行命令字符串 / Execute command string
 const result = AIDrawingAPI.executeCommand("draw(circle, 300, 300, 40)");
```

## 安装和运行 / Installation and Running

1. 将所有文件下载到本地文件夹 / Download all files to a local folder
2. 使用任意现代浏览器打开`index.html`文件即可使用 / Open the `index.html` file in any modern browser

## 兼容性 / Compatibility

- 支持所有现代桌面浏览器（Chrome, Firefox, Safari, Edge） / Supports all modern desktop browsers
- 支持移动设备上的触摸操作 / Touch support for mobile devices
- 响应式设计，适配不同屏幕尺寸 / Responsive design for different screen sizes

## 技术实现 / Technical Implementation

### Web版 / Web Version
- HTML5 Canvas API 用于绘图 / HTML5 Canvas API for drawing
- 纯JavaScript实现所有功能 / Pure JavaScript for all functionality
- CSS3 用于界面样式 / CSS3 for interface styling
- 支持鼠标和触摸事件 / Support for both mouse and touch events

### Python版 / Python Version
- 使用PIL/Pillow库进行图像处理 / Uses PIL/Pillow library for image processing
- 支持本地绘图和远程控制Web版画板 / Supports local drawing and remote control
- 提供与Web版相同的API接口 / Provides the same API interface as web version

## Python API 使用指南 / Python API Usage Guide

### 安装依赖 / Install Dependencies

使用Python API前需要安装必要的依赖：

Before using the Python API, install the necessary dependencies:

```bash
pip install pillow requests
```

### 基本使用 / Basic Usage

```python
from draw_api import AIDrawingAPI

# 创建本地模式API实例 / Create a local mode API instance
api = AIDrawingAPI(width=800, height=600)

# 绘制图形 / Draw shapes
api.draw_line(10, 10, 100, 100, color='#ff0000', width=5)
api.draw_circle(150, 150, 50, color='#00ff00', width=3)
api.draw_rectangle(200, 200, 100, 80, color='#0000ff', width=2)
api.draw_text(50, 50, 'Hello World', color='#ff00ff', font_size=24)

# 保存图片 / Save image
api.export('my_drawing.png')

# 显示图片 / Display image
api.show()
```

### 远程模式 / Remote Mode

```python
# 连接到Web版画板（需要Web版正在运行） / Connect to web drawing board
api = AIDrawingAPI(mode='remote', url='http://localhost:8000')

# 绘制图形到远程画板 / Draw shapes on remote board
api.draw_circle(300, 300, 40)
api.set_color('#ff9900')
api.draw_line(100, 100, 400, 400)
```

### 命令字符串执行 / Command String Execution

```python
# 执行命令字符串 / Execute command string
result = api.execute_command("draw(circle, 300, 300, 40)")
print(result)
```

### 所有API方法 / All API Methods

- `draw_line(x1, y1, x2, y2, color=None, width=None)` - 绘制直线 / Draw a line
- `draw_circle(x, y, radius, color=None, width=None)` - 绘制圆形 / Draw a circle
- `draw_rectangle(x, y, width_rect, height_rect, color=None, width=None)` - 绘制矩形 / Draw a rectangle
- `draw_text(x, y, text, color=None, font_size=20)` - 绘制文本 / Draw text
- `export(filename=None)` - 导出画布内容 / Export canvas content
- `clear()` - 清空画布 / Clear canvas
- `set_color(color)` - 设置画笔颜色 / Set brush color
- `set_line_width(width)` - 设置画笔粗细 / Set brush width
- `execute_command(command)` - 执行命令字符串 / Execute command string
- `show()` - 显示当前画布（仅本地模式） / Display current canvas (local mode only)

### 注意事项 / Notes

- 远程模式需要Web版画板添加相应的API端点来接收命令 / Remote mode requires web drawing board API endpoints
- 本地模式使用PIL/Pillow库进行图像处理 / Local mode uses PIL/Pillow for image processing
- 默认画布大小为800x600像素，可以在初始化时自定义 / Default canvas size is 800x600 pixels, customizable on initialization