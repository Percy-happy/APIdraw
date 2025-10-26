#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ollama 画板控制插件

这个插件允许通过Ollama的自然语言处理能力来控制画板应用
工作流程: ollama → python → api → 画板
"""

import json
import requests
import re
import sys

def parse_command_input(prompt="请输入命令: "):
    """获取用户输入的命令"""
    try:
        return input(prompt)
    except KeyboardInterrupt:
        print("\n退出程序")
        sys.exit(0)

class OllamaDrawPlugin:
    """Ollama画板控制插件"""
    
    def __init__(self, ollama_url="http://localhost:11434", draw_api_url="http://localhost:8000"):
        """初始化Ollama Draw Plugin
        
        Args:
            ollama_url: Ollama服务地址
            draw_api_url: 画板API地址
        """
        self.ollama_url = ollama_url
        self.draw_api_url = draw_api_url
        
        # 导入DrawingAPI
        from draw_api import DrawingAPI
        self.drawing_api = DrawingAPI(draw_api_url, "remote")
        
        # 初始化提示词模板
        self.prompt_template = self._get_prompt_template()
        
    def check_connections(self):
        """检查Ollama和画板服务连接状态
        
        Returns:
            bool: 连接是否成功
        """
        # 检查Ollama连接
        try:
            response = requests.get(f"{self.ollama_url}/api/tags")
            if response.status_code != 200:
                print(f"无法连接到Ollama服务: {response.status_code}")
                return False
            print("✓ Ollama服务连接成功")
        except Exception as e:
            print(f"Ollama连接错误: {e}")
            return False
        
        # 检查画板连接
        try:
            # 使用DrawingAPI的execute_command方法测试连接
            test_result = self.drawing_api.execute_command("ping()")
            print("✓ 画板服务连接成功")
            return True
        except Exception as e:
            print(f"画板连接错误: {e}")
            return False
    
    def _get_prompt_template(self):
        """获取Ollama提示词模板"""
        return """
        你是一个专业的画板命令转换助手。请将用户的自然语言描述转换为画板API命令。
        
        可用的命令格式：
        1. 画直线: draw(line,x1,y1,x2,y2)
        2. 画圆形: draw(circle,x,y,radius)
        3. 画矩形: draw(rect,x,y,width,height)
        4. 写文本: draw(text,x,y,"content")
        5. 设置颜色: setColor(color)
           - color可以是颜色名称或十六进制代码
           - 例如: "red", "blue", "#ff0000", "#0000ff"
        6. 设置线宽: setLineWidth(width)
           - width是数字
        7. 清空画布: clear()
        8. 导出图片: export()
        
        画布大小假设为600x400像素。
        
        请注意：
        1. 只输出单个API命令，不要输出任何解释
        2. 确保命令格式完全正确
        3. 如果有多个操作，请按顺序思考并只输出第一个操作的命令
        4. 对于颜色，优先使用中文颜色名称或十六进制代码
        5. 对于文本内容，请确保使用双引号包围
        
        示例：
        用户: 在左上角画一个红色圆形
        助手: draw(circle,50,50,30)
        
        用户: 在右下角写'Hello World'
        助手: draw(text,500,350,"Hello World")
        
        用户: {user_input}
        """
    
    def query_ollama(self, user_input):
        """查询Ollama，将自然语言转换为API命令
        
        Args:
            user_input: 用户输入的自然语言命令
            
        Returns:
            str: 转换后的API命令
        """
        # 构建提示词
        prompt = self.prompt_template.format(user_input=user_input)
        
        # 调用Ollama API
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": "llama3",  # 使用llama3模型
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.2,  # 降低温度以获得更确定的输出
                        "max_tokens": 200
                    }
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                output = result.get("response", "").strip()
                
                # 提取命令（可能需要清理输出）
                command = self._extract_command(output)
                return command
            else:
                print(f"Ollama API错误: {response.status_code}")
                return None
        except Exception as e:
            print(f"调用Ollama时出错: {e}")
            return None
    
    def _extract_command(self, text):
        """从Ollama输出中提取命令
        
        Args:
            text: Ollama返回的文本
            
        Returns:
            str: 提取的命令
        """
        # 尝试匹配可能的命令格式
        patterns = [
            r'^([a-z]+\([^)]*\))$',  # 直接匹配命令格式
            r'助手:\s*([a-z]+\([^)]*\))',  # 匹配"助手: 命令"格式
            r'命令:\s*([a-z]+\([^)]*\))',  # 匹配"命令: 命令"格式
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)
        
        # 如果没有匹配到标准格式，尝试找可能的命令
        # 查找可能的函数调用
        potential_command = re.search(r'([a-z]+\([^)]*\))', text)
        if potential_command:
            return potential_command.group(1)
        
        return text  # 如果都没找到，返回原始文本
    
    def execute_command(self, command):
        """执行API命令
        
        Args:
            command: 要执行的命令
            
        Returns:
            str: 执行结果
        """
        try:
            # 解析命令
            cmd_match = re.match(r'^([a-z]+)\((.*?)\)$', command)
            if not cmd_match:
                return f"错误: 无效的命令格式 '{command}'"
            
            cmd_name = cmd_match.group(1)
            cmd_params = cmd_match.group(2)
            
            # 根据命令类型执行
            if cmd_name == "draw":
                # 解析draw命令的子命令
                draw_match = re.match(r'([a-z]+),(.*)', cmd_params)
                if not draw_match:
                    return "错误: draw命令格式错误"
                
                draw_type = draw_match.group(1)
                draw_params = draw_match.group(2).split(',')
                
                # 处理不同的绘图类型
                if draw_type == "line" and len(draw_params) >= 4:
                    x1, y1, x2, y2 = map(float, draw_params[:4])
                    return self.drawing_api.draw_line(x1, y1, x2, y2)
                elif draw_type == "circle" and len(draw_params) >= 3:
                    x, y, radius = map(float, draw_params[:3])
                    return self.drawing_api.draw_circle(x, y, radius)
                elif draw_type == "rect" and len(draw_params) >= 4:
                    x, y, width, height = map(float, draw_params[:4])
                    return self.drawing_api.draw_rectangle(x, y, width, height)
                elif draw_type == "text" and len(draw_params) >= 3:
                    x, y = map(float, draw_params[:2])
                    # 提取文本内容（可能包含逗号）
                    text_content = ','.join(draw_params[2:]).strip('"\'')
                    return self.drawing_api.draw_text(x, y, text_content)
                else:
                    return f"错误: 未知的绘图类型 '{draw_type}' 或参数不足"
            
            elif cmd_name == "setColor" and cmd_params:
                color = cmd_params.strip('"\'')
                return self.drawing_api.set_color(color)
            
            elif cmd_name == "setLineWidth" and cmd_params:
                try:
                    width = float(cmd_params)
                    return self.drawing_api.set_line_width(width)
                except ValueError:
                    return "错误: 线宽必须是数字"
            
            elif cmd_name == "clear":
                return self.drawing_api.clear()
            
            elif cmd_name == "export":
                return self.drawing_api.export()
            
            elif cmd_name == "ping":
                # 测试命令
                return "pong"
            
            else:
                # 尝试直接执行原始命令
                try:
                    return self.drawing_api.execute_command(command)
                except Exception as e:
                    return f"错误: 未知命令 '{cmd_name}' - {str(e)}"
        
        except Exception as e:
            return f"执行命令时出错: {str(e)}"
    
    def run_interactive(self):
        """运行交互式命令行模式"""
        print("===== Ollama 画板控制插件 =====")
        print("输入自然语言描述或直接输入API命令")
        print("输入 'exit' 或按 Ctrl+C 退出")
        print("输入 'help' 获取帮助")
        print("==============================\n")
        
        while True:
            command = parse_command_input("\n请输入: ")
            
            if command.lower() == "exit":
                print("退出程序")
                break
            
            if command.lower() == "help":
                self._show_help()
                continue
            
            # 检查是否是直接的API命令
            if re.match(r'^[a-z]+\([^)]*\)$', command):
                # 直接执行API命令
                result = self.execute_command(command)
                print(f"执行结果: {result}")
            else:
                # 尝试自然语言转API命令
                print("正在转换自然语言为API命令...")
                api_command = self.query_ollama(command)
                
                if api_command:
                    print(f"转换结果: {api_command}")
                    
                    # 执行转换后的命令
                    result = self.execute_command(api_command)
                    print(f"执行结果: {result}")
                else:
                    print("无法转换为有效的API命令")
    
    def _show_help(self):
        """显示帮助信息"""
        print("\n使用说明:")
        print("1. 自然语言输入 - 描述你想要绘制的内容")
        print("   例如: '在左上角画一个红色圆形'")
        print("   例如: '在中间写Hello World'")
        print("\n2. 直接API命令输入:")
        print("   - 画直线: draw(line,x1,y1,x2,y2)")
        print("   - 画圆形: draw(circle,x,y,radius)")
        print("   - 画矩形: draw(rect,x,y,width,height)")
        print("   - 写文本: draw(text,x,y,\"content\")")
        print("   - 设置颜色: setColor(color)")
        print("   - 设置线宽: setLineWidth(width)")
        print("   - 清空画布: clear()")
        print("   - 导出图片: export()")
        print("\n3. 其他命令:")
        print("   - help: 显示此帮助信息")
        print("   - exit: 退出程序")

def main():
    """主函数"""
    try:
        # 创建插件实例
        plugin = OllamaDrawPlugin()
        
        # 检查连接
        if not plugin.check_connections():
            print("\n请确保:")
            print("1. Ollama服务正在运行 (http://localhost:11434)")
            print("2. 画板Web服务正在运行 (http://localhost:8000)")
            return
        
        # 运行交互式模式
        plugin.run_interactive()
        
    except KeyboardInterrupt:
        print("\n退出程序")
    except Exception as e:
        print(f"运行时出错: {e}")

if __name__ == "__main__":
    main()