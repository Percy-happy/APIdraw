# AI 画板应用

这是一个功能丰富的在线画板应用，支持手动绘画和API调用绘画，以及导出图片功能。

## 功能特点

### 1. 手动绘画
- 支持鼠标和触摸屏绘画
- 可调节画笔颜色和粗细
- 清空画板功能
- 导出绘画为PNG图片

### 2. API 控制
- 通过命令字符串绘制基本图形
- 提供JavaScript API接口供外部调用
- 支持绘制直线、圆形、矩形和文本
- API导出功能

## 如何使用

### 手动绘画
1. 在画布上按住鼠标左键或触摸屏幕并移动来绘画
2. 使用颜色选择器选择画笔颜色
3. 使用滑块调整画笔粗细
4. 点击"清空画板"按钮清除所有内容
5. 点击"导出图片"按钮将绘画保存为PNG文件

### API 命令

#### 命令字符串格式
在API命令输入框中，可以输入以下格式的命令：

```
// 绘制直线
 draw(line, x1, y1, x2, y2)

// 绘制圆形
 draw(circle, x, y, radius)

// 绘制矩形
 draw(rect, x, y, width, height)

// 绘制文本
 draw(text, x, y, "文本内容")

// 导出画布
 export()
```

输入命令后点击"执行命令"按钮或按Enter键执行。

#### JavaScript API
页面加载后，全局对象`window.AIDrawingAPI`可用于通过JavaScript控制画板：

```javascript
// 绘制直线
 AIDrawingAPI.drawLine(10, 10, 100, 100, "#ff0000", 5);

// 绘制圆形
 AIDrawingAPI.drawCircle(150, 150, 50, "#00ff00", 3);

// 绘制矩形
 AIDrawingAPI.drawRectangle(200, 200, 100, 80, "#0000ff", 2);

// 绘制文本
 AIDrawingAPI.drawText(50, 50, "Hello World", "#ff00ff", 24);

// 导出画布
 const dataUrl = AIDrawingAPI.export();

// 清空画布
 AIDrawingAPI.clear();

// 设置画笔颜色
 AIDrawingAPI.setColor("#ff9900");

// 设置画笔粗细
 AIDrawingAPI.setLineWidth(8);

// 执行命令字符串
 const result = AIDrawingAPI.executeCommand("draw(circle, 300, 300, 40)");
```

## 安装和运行

1. 将所有文件下载到本地文件夹
2. 使用任意现代浏览器打开`index.html`文件即可使用

## 兼容性

- 支持所有现代桌面浏览器（Chrome, Firefox, Safari, Edge）
- 支持移动设备上的触摸操作
- 响应式设计，适配不同屏幕尺寸

## 技术实现

### Web版
- HTML5 Canvas API 用于绘图
- 纯JavaScript实现所有功能
- CSS3 用于界面样式
- 支持鼠标和触摸事件

### Python版
- 使用PIL/Pillow库进行图像处理
- 支持本地绘图和远程控制Web版画板
- 提供与Web版相同的API接口

## Python API 使用指南

### 安装依赖

使用Python API前需要安装必要的依赖：

```bash
pip install pillow requests
```

### 基本使用

```python
from draw_api import AIDrawingAPI

# 创建本地模式API实例
api = AIDrawingAPI(width=800, height=600)

# 绘制图形
api.draw_line(10, 10, 100, 100, color='#ff0000', width=5)
api.draw_circle(150, 150, 50, color='#00ff00', width=3)
api.draw_rectangle(200, 200, 100, 80, color='#0000ff', width=2)
api.draw_text(50, 50, 'Hello World', color='#ff00ff', font_size=24)

# 保存图片
api.export('my_drawing.png')

# 显示图片
api.show()
```

### 远程模式

```python
# 连接到Web版画板（需要Web版正在运行）
api = AIDrawingAPI(mode='remote', url='http://localhost:8000')

# 绘制图形到远程画板
api.draw_circle(300, 300, 40)
api.set_color('#ff9900')
api.draw_line(100, 100, 400, 400)
```

### 命令字符串执行

```python
# 执行命令字符串
result = api.execute_command("draw(circle, 300, 300, 40)")
print(result)
```

### 所有API方法

- `draw_line(x1, y1, x2, y2, color=None, width=None)` - 绘制直线
- `draw_circle(x, y, radius, color=None, width=None)` - 绘制圆形
- `draw_rectangle(x, y, width_rect, height_rect, color=None, width=None)` - 绘制矩形
- `draw_text(x, y, text, color=None, font_size=20)` - 绘制文本
- `export(filename=None)` - 导出画布内容
- `clear()` - 清空画布
- `set_color(color)` - 设置画笔颜色
- `set_line_width(width)` - 设置画笔粗细
- `execute_command(command)` - 执行命令字符串
- `show()` - 显示当前画布（仅本地模式）

### 注意事项

- 远程模式需要Web版画板添加相应的API端点来接收命令
- 本地模式使用PIL/Pillow库进行图像处理
- 默认画布大小为800x600像素，可以在初始化时自定义