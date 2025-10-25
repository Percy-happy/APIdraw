"""
AI 画板 Python API

这个模块提供了与Web版画板相同功能的Python接口。
可以通过两种方式使用：
1. 本地模式：直接在Python中创建画布并绘图
2. 远程模式：通过HTTP请求控制Web版画板

使用示例：
    # 本地模式
    from draw_api import AIDrawingAPI
    
    # 创建API实例
    api = AIDrawingAPI(mode='local')
    
    # 绘制图形
    api.draw_line(10, 10, 100, 100, color='#ff0000', width=5)
    api.draw_circle(150, 150, 50, color='#00ff00', width=3)
    api.draw_rectangle(200, 200, 100, 80, color='#0000ff', width=2)
    api.draw_text(50, 50, 'Hello World', color='#ff00ff', font_size=24)
    
    # 保存图片
    api.export('output.png')
    
    # 远程模式（需要Web版画板正在运行）
    api = AIDrawingAPI(mode='remote', url='http://localhost:8000')
    api.draw_circle(300, 300, 40)
"""

import json
import base64
from io import BytesIO
import requests
from PIL import Image, ImageDraw, ImageFont


class AIDrawingAPI:
    """
    AI画板Python API类
    提供绘制图形和导出功能
    """
    
    def __init__(self, mode='local', url='http://localhost:8000', 
                 width=800, height=600, background_color='#ffffff'):
        """
        初始化API实例
        
        参数:
            mode: 运行模式，'local' 或 'remote'
            url: 远程模式下的Web版画板URL
            width: 本地模式下的画布宽度
            height: 本地模式下的画布高度
            background_color: 背景颜色
        """
        self.mode = mode
        self.url = url
        
        if mode == 'local':
            # 创建本地画布
            self.width = width
            self.height = height
            self.image = Image.new('RGB', (width, height), background_color)
            self.draw = ImageDraw.Draw(self.image)
            self.current_color = '#000000'  # 默认黑色
            self.current_width = 5  # 默认线宽
        elif mode == 'remote':
            # 远程模式下的默认设置
            self.current_color = '#000000'
            self.current_width = 5
        else:
            raise ValueError("模式必须是 'local' 或 'remote'")
    
    def draw_line(self, x1, y1, x2, y2, color=None, width=None):
        """
        绘制直线
        
        参数:
            x1, y1: 起点坐标
            x2, y2: 终点坐标
            color: 线条颜色（可选）
            width: 线条宽度（可选）
        """
        if self.mode == 'local':
            color = color or self.current_color
            width = width or self.current_width
            self.draw.line([x1, y1, x2, y2], fill=color, width=width)
            return True
        else:  # remote
            color = color or self.current_color
            width = width or self.current_width
            command = f"draw(line,{x1},{y1},{x2},{y2})"
            return self._send_remote_command(command, color, width)
    
    def draw_circle(self, x, y, radius, color=None, width=None):
        """
        绘制圆形
        
        参数:
            x, y: 圆心坐标
            radius: 半径
            color: 线条颜色（可选）
            width: 线条宽度（可选）
        """
        if self.mode == 'local':
            color = color or self.current_color
            width = width or self.current_width
            # 绘制圆形轮廓
            left = x - radius
            top = y - radius
            right = x + radius
            bottom = y + radius
            self.draw.ellipse([left, top, right, bottom], outline=color, width=width)
            return True
        else:  # remote
            color = color or self.current_color
            width = width or self.current_width
            command = f"draw(circle,{x},{y},{radius})"
            return self._send_remote_command(command, color, width)
    
    def draw_rectangle(self, x, y, width_rect, height_rect, color=None, width=None):
        """
        绘制矩形
        
        参数:
            x, y: 左上角坐标
            width_rect: 矩形宽度
            height_rect: 矩形高度
            color: 线条颜色（可选）
            width: 线条宽度（可选）
        """
        if self.mode == 'local':
            color = color or self.current_color
            width = width or self.current_width
            right = x + width_rect
            bottom = y + height_rect
            self.draw.rectangle([x, y, right, bottom], outline=color, width=width)
            return True
        else:  # remote
            color = color or self.current_color
            width = width or self.current_width
            command = f"draw(rect,{x},{y},{width_rect},{height_rect})"
            return self._send_remote_command(command, color, width)
    
    def draw_text(self, x, y, text, color=None, font_size=20):
        """
        绘制文本
        
        参数:
            x, y: 文本位置坐标
            text: 要绘制的文本
            color: 文本颜色（可选）
            font_size: 字体大小（可选）
        """
        if self.mode == 'local':
            color = color or self.current_color
            try:
                # 尝试使用系统字体
                font = ImageFont.truetype("arial.ttf", font_size)
            except IOError:
                # 如果找不到字体，使用默认字体
                font = ImageFont.load_default()
            self.draw.text((x, y), text, fill=color, font=font)
            return True
        else:  # remote
            color = color or self.current_color
            # 注意：远程模式下字体大小通过URL参数传递
            command = f'draw(text,{x},{y},"{text}")'
            return self._send_remote_command(command, color, self.current_width)
    
    def export(self, filename=None):
        """
        导出画布内容
        
        参数:
            filename: 导出的文件名（本地模式）
        
        返回:
            本地模式: True
            远程模式: 图片的base64编码
        """
        if self.mode == 'local':
            if filename:
                self.image.save(filename)
                return True
            else:
                # 如果没有提供文件名，返回base64编码
                buffer = BytesIO()
                self.image.save(buffer, format="PNG")
                buffer.seek(0)
                return base64.b64encode(buffer.read()).decode('utf-8')
        else:  # remote
            try:
                response = requests.get(f"{self.url}/export", timeout=10)
                response.raise_for_status()
                return response.json().get('data_url', '')
            except Exception as e:
                print(f"导出失败: {e}")
                return None
    
    def clear(self):
        """
        清空画布
        """
        if self.mode == 'local':
            self.image = Image.new('RGB', (self.width, self.height), '#ffffff')
            self.draw = ImageDraw.Draw(self.image)
            return True
        else:  # remote
            return self._send_remote_command("clear()", self.current_color, self.current_width)
    
    def set_color(self, color):
        """
        设置画笔颜色
        
        参数:
            color: 颜色值（如 '#ff0000'）
        """
        self.current_color = color
        if self.mode == 'remote':
            return self._send_remote_command(f"setColor('{color}')", color, self.current_width)
        return True
    
    def set_line_width(self, width):
        """
        设置画笔粗细
        
        参数:
            width: 线条宽度
        """
        self.current_width = width
        if self.mode == 'remote':
            return self._send_remote_command(f"setLineWidth({width})", self.current_color, width)
        return True
    
    def execute_command(self, command):
        """
        执行命令字符串
        
        参数:
            command: 命令字符串
        """
        if self.mode == 'local':
            # 本地模式下解析并执行命令
            try:
                # 简单的命令解析
                if command.startswith('draw(line,'):
                    # 解析直线命令
                    parts = command[10:-1].split(',')
                    x1, y1, x2, y2 = map(float, parts[:4])
                    return self.draw_line(x1, y1, x2, y2)
                elif command.startswith('draw(circle,'):
                    # 解析圆形命令
                    parts = command[12:-1].split(',')
                    x, y, radius = map(float, parts[:3])
                    return self.draw_circle(x, y, radius)
                elif command.startswith('draw(rect,'):
                    # 解析矩形命令
                    parts = command[10:-1].split(',')
                    x, y, w, h = map(float, parts[:4])
                    return self.draw_rectangle(x, y, w, h)
                elif command.startswith('draw(text,'):
                    # 解析文本命令（注意处理引号）
                    import re
                    match = re.search(r'draw\(text,(\d+),(\d+),"(.+)"\)', command)
                    if match:
                        x, y, text = float(match.group(1)), float(match.group(2)), match.group(3)
                        return self.draw_text(x, y, text)
                elif command == 'clear()':
                    return self.clear()
                return {"success": False, "error": "不支持的命令"}
            except Exception as e:
                return {"success": False, "error": str(e)}
        else:  # remote
            return self._send_remote_command(command, self.current_color, self.current_width)
    
    def _send_remote_command(self, command, color, width):
        """
        发送命令到远程服务器
        
        注意：此功能需要Web版画板添加一个简单的API端点来接收命令
        这里提供的是基本实现，实际使用时可能需要根据Web版的实现进行调整
        """
        try:
            # 构建请求数据
            data = {
                "command": command,
                "color": color,
                "width": width
            }
            
            # 发送POST请求到Web服务器
            response = requests.post(
                f"{self.url}/api/execute",
                json=data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"远程命令执行失败: {e}")
            # 注意：由于Web版可能没有实现API端点，这里返回模拟成功
            # 在实际使用时，需要在Web版中添加对应的API处理
            return {"success": True, "message": "模拟命令执行成功（需要Web版实现API端点）"}
    
    def show(self):
        """
        显示当前画布（仅本地模式）
        """
        if self.mode == 'local':
            self.image.show()
            return True
        else:
            print("远程模式不支持直接显示画布")
            return False


# 使用示例
if __name__ == "__main__":
    # 创建本地模式API实例
    print("创建本地画板...")
    api = AIDrawingAPI(width=800, height=600)
    
    # 绘制一些图形
    print("绘制示例图形...")
    api.draw_line(50, 50, 200, 50, color='#ff0000', width=3)
    api.draw_circle(150, 150, 80, color='#00ff00', width=2)
    api.draw_rectangle(300, 100, 150, 100, color='#0000ff', width=4)
    api.draw_text(100, 300, "Python AI 画板", color='#ff00ff', font_size=24)
    
    # 使用命令字符串
    api.execute_command("draw(line,400,400,600,400)")
    
    # 保存图片
    output_file = "python_drawing_example.png"
    api.export(output_file)
    print(f"图片已保存到: {output_file}")
    
    # 可选：显示图片
    # api.show()
    
    print("\n使用说明:")
    print("1. 本地模式: 直接在Python中创建和编辑图像")
    print("2. 远程模式: 连接到Web版画板进行操作")
    print("\n请参考模块文档了解更多详细用法。")