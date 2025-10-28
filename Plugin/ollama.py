#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Ollama 连接模块 - 画板远程API集成

这个模块提供了与 Ollama API 交互的功能，并能自动检测和执行画板的远程API命令。
当AI输出包含画板远程API调用时，会自动转换并执行这些命令。
"""

import json
import re
import requests
import sys
import os

# 确保可以导入画板API（如果需要直接执行命令）
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from draw_api import DrawingAPI
except ImportError:
    print("警告：无法导入draw_api模块，将使用HTTP请求方式调用远程API")
    DrawingAPI = None


class OllamaDrawer:
    """
    Ollama 绘图助手
    
    连接Ollama并处理包含画板API命令的响应
    """
    
    def __init__(self, ollama_url="http://localhost:11434", draw_api_url="http://localhost:8000"):
        """
        初始化Ollama绘图助手
        
        Args:
            ollama_url (str): Ollama服务器地址
            draw_api_url (str): 画板远程API地址
        """
        self.ollama_url = ollama_url.rstrip('/')
        self.draw_api_url = draw_api_url.rstrip('/')
        self.session = requests.Session()
        
        # 远程画板API实例
        self.draw_api = None
        if DrawingAPI:
            try:
                self.draw_api = DrawingAPI(mode='remote', url=self.draw_api_url)
                print(f"已连接到远程画板API: {self.draw_api_url}")
            except Exception as e:
                print(f"无法初始化远程画板API: {e}，将使用HTTP请求方式")
        
        # 匹配远程API调用的正则表达式
        self.api_patterns = {
            'draw_line': re.compile(r'api\.draw_line\(([^)]+)\)'),
            'draw_circle': re.compile(r'api\.draw_circle\(([^)]+)\)'),
            'draw_rectangle': re.compile(r'api\.draw_rectangle\(([^)]+)\)'),
            'draw_text': re.compile(r'api\.draw_text\(([^)]+)\)'),
            'export': re.compile(r'api\.export\(([^)]*)\)'),
            'clear': re.compile(r'api\.clear\(\)'),
            'set_color': re.compile(r'api\.set_color\(([^)]+)\)'),
            'set_line_width': re.compile(r'api\.set_line_width\(([^)]+)\)'),
            'execute_command': re.compile(r'api\.execute_command\(([^)]+)\)')
        }
    
    def call_ollama(self, model, prompt):
        """
        调用Ollama生成响应
        
        Args:
            model (str): 使用的模型名称
            prompt (str): 提示文本
        
        Returns:
            str: 生成的文本响应
        """
        try:
            url = f"{self.ollama_url}/api/generate"
            data = {
                "model": model,
                "prompt": prompt,
                "stream": False
            }
            
            response = self.session.post(url, json=data)
            response.raise_for_status()
            result = response.json()
            return result.get("response", "")
        except Exception as e:
            return f"调用Ollama失败: {str(e)}"
    
    def extract_api_commands(self, text):
        """
        从文本中提取画板API命令
        
        Args:
            text (str): 包含可能API调用的文本
        
        Returns:
            list: 提取出的API命令列表 [(api_name, args_str)]
        """
        commands = []
        
        for api_name, pattern in self.api_patterns.items():
            matches = pattern.findall(text)
            for match in matches:
                commands.append((api_name, match))
        
        return commands
    
    def parse_args(self, args_str):
        """
        解析参数字符串
        
        Args:
            args_str (str): 参数字符串
        
        Returns:
            list: 解析后的参数列表
        """
        try:
            # 处理引号中的字符串
            quoted_values = re.findall(r'"([^"]*)"', args_str)
            # 替换引号中的字符串为占位符
            temp_args = args_str
            for i, val in enumerate(quoted_values):
                temp_args = temp_args.replace(f'"{val}"', f'__QUOTE_{i}__')
            
            # 分割参数
            args = [arg.strip() for arg in temp_args.split(',')]
            
            # 恢复引号中的字符串
            for i, val in enumerate(quoted_values):
                for j in range(len(args)):
                    if f'__QUOTE_{i}__' in args[j]:
                        args[j] = args[j].replace(f'__QUOTE_{i}__', val)
            
            # 转换数字
            parsed_args = []
            for arg in args:
                if arg == '':
                    parsed_args.append(None)
                elif arg.lower() == 'none':
                    parsed_args.append(None)
                elif arg.startswith('#'):
                    parsed_args.append(arg)  # 颜色值保持字符串
                elif arg.startswith('"') and arg.endswith('"'):
                    parsed_args.append(arg[1:-1])  # 移除引号
                elif arg.replace('.', '', 1).isdigit():
                    # 尝试转换为数字
                    if '.' in arg:
                        parsed_args.append(float(arg))
                    else:
                        parsed_args.append(int(arg))
                else:
                    parsed_args.append(arg)
            
            return parsed_args
        except Exception as e:
            print(f"解析参数失败: {e}")
            return []
    
    def execute_api_command(self, api_name, args_str):
        """
        执行画板API命令
        
        Args:
            api_name (str): API方法名
            args_str (str): 参数字符串
        
        Returns:
            bool: 执行是否成功
        """
        try:
            args = self.parse_args(args_str)
            print(f"执行命令: {api_name}({', '.join(str(arg) for arg in args)})")
            
            # 使用draw_api模块执行
            if self.draw_api:
                if api_name == 'draw_line':
                    self.draw_api.draw_line(*args)
                elif api_name == 'draw_circle':
                    self.draw_api.draw_circle(*args)
                elif api_name == 'draw_rectangle':
                    self.draw_api.draw_rectangle(*args)
                elif api_name == 'draw_text':
                    self.draw_api.draw_text(*args)
                elif api_name == 'export':
                    self.draw_api.export(*args)
                elif api_name == 'clear':
                    self.draw_api.clear()
                elif api_name == 'set_color':
                    self.draw_api.set_color(*args)
                elif api_name == 'set_line_width':
                    self.draw_api.set_line_width(*args)
                elif api_name == 'execute_command':
                    self.draw_api.execute_command(*args)
                return True
            else:
                # 使用HTTP请求执行
                return self.execute_api_via_http(api_name, args)
        
        except Exception as e:
            print(f"执行API命令失败: {e}")
            return False
    
    def execute_api_via_http(self, api_name, args):
        """
        通过HTTP请求执行API命令
        
        Args:
            api_name (str): API方法名
            args (list): 参数列表
        
        Returns:
            bool: 执行是否成功
        """
        try:
            url = f"{self.draw_api_url}/api/{api_name}"
            
            # 构建请求数据
            if api_name == 'draw_line' and len(args) >= 4:
                data = {
                    'x1': args[0], 'y1': args[1], 'x2': args[2], 'y2': args[3],
                    'color': args[4] if len(args) > 4 else None,
                    'width': args[5] if len(args) > 5 else None
                }
            elif api_name == 'draw_circle' and len(args) >= 3:
                data = {
                    'x': args[0], 'y': args[1], 'radius': args[2],
                    'color': args[3] if len(args) > 3 else None,
                    'width': args[4] if len(args) > 4 else None
                }
            elif api_name == 'draw_rectangle' and len(args) >= 4:
                data = {
                    'x': args[0], 'y': args[1], 'width': args[2], 'height': args[3],
                    'color': args[4] if len(args) > 4 else None,
                    'width': args[5] if len(args) > 5 else None
                }
            elif api_name == 'draw_text' and len(args) >= 3:
                data = {
                    'x': args[0], 'y': args[1], 'text': args[2],
                    'color': args[3] if len(args) > 3 else None,
                    'font_size': args[4] if len(args) > 4 else 20
                }
            elif api_name == 'export':
                data = {'filename': args[0] if args else None}
            elif api_name == 'set_color' and len(args) >= 1:
                data = {'color': args[0]}
            elif api_name == 'set_line_width' and len(args) >= 1:
                data = {'width': args[0]}
            elif api_name == 'execute_command' and len(args) >= 1:
                data = {'command': args[0]}
            elif api_name == 'clear':
                data = {}
            else:
                print(f"不支持的API命令或参数不足: {api_name}")
                return False
            
            # 发送HTTP请求
            response = self.session.post(url, json=data)
            response.raise_for_status()
            print(f"HTTP请求成功: {response.status_code}")
            return True
            
        except Exception as e:
            print(f"HTTP请求失败: {e}")
            return False
    
    def process_ollama_response(self, model, prompt):
        """
        处理Ollama响应，执行其中的API命令
        
        Args:
            model (str): Ollama模型名称
            prompt (str): 发送给Ollama的提示
        
        Returns:
            dict: 包含响应和执行结果的字典
        """
        # 调用Ollama获取响应
        response = self.call_ollama(model, prompt)
        print("\n=== Ollama 响应 ===")
        print(response)
        
        # 提取并执行API命令
        commands = self.extract_api_commands(response)
        
        if commands:
            print("\n=== 检测到API命令，开始执行 ===")
            results = []
            for api_name, args_str in commands:
                success = self.execute_api_command(api_name, args_str)
                results.append({
                    'command': f"{api_name}({args_str})",
                    'success': success
                })
            
            print("\n=== 执行完成 ===")
            return {
                'ollama_response': response,
                'commands_executed': results,
                'total_commands': len(commands),
                'successful_commands': sum(1 for r in results if r['success'])
            }
        else:
            print("\n未检测到API命令")
            return {
                'ollama_response': response,
                'commands_executed': [],
                'total_commands': 0,
                'successful_commands': 0
            }
    
    def __del__(self):
        """关闭会话"""
        try:
            self.session.close()
        except:
            pass

def main():
    """
    主函数，用于测试Ollama绘图助手
    """
    print("=== Ollama 画板连接助手 ===")
    print("这个工具可以连接Ollama并执行其中包含的画板API命令")
    
    # 创建实例
    drawer = OllamaDrawer()
    
    # 示例提示，包含API命令
    example_prompt = """
请生成一个简单的绘图API调用，在画板上：
1. 画一个红色的圆在中间位置
2. 画一条蓝色的线
3. 添加一些文本

请使用以下格式输出API调用：
api.draw_circle(400, 300, 50, "#ff0000", 2)
api.draw_line(100, 100, 500, 400, "#0000ff", 3)
api.draw_text(200, 500, "Hello 画板", "#000000", 24)
"""
    
    # 询问用户是否使用示例提示
    use_example = input("是否使用示例提示？(y/n): ")
    
    if use_example.lower() == 'y':
        prompt = example_prompt
    else:
        model = input("请输入Ollama模型名称 (默认: DeepSeek-r1): ") or "deepseek-r1"
        prompt = input("请输入提示文本: ")
    
    # 处理响应
    result = drawer.process_ollama_response(model, prompt)
    
    # 显示结果摘要
    print("\n=== 执行结果摘要 ===")
    print(f"检测到命令数: {result['total_commands']}")
    print(f"成功执行数: {result['successful_commands']}")
    
    for cmd in result['commands_executed']:
        status = "✓ 成功" if cmd['success'] else "✗ 失败"
        print(f"  {status}: {cmd['command']}")


if __name__ == "__main__":
    main()