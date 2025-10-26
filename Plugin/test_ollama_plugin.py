#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ollama 画板控制插件测试脚本

这个脚本演示了如何使用ollama_draw_plugin.py控制画板应用

使用说明：
1. 确保Ollama服务正在运行 (默认端口 11434)
2. 确保画板Web服务正在运行 (默认 http://localhost:8000)
3. 运行此测试脚本: python test_ollama_plugin.py
"""

import time
from ollama_draw_plugin import OllamaDrawPlugin

def test_basic_commands(plugin):
    """测试基本绘图命令"""
    print("\n=== 测试基本绘图命令 ===")
    
    # 测试绘制直线
    command = "draw(line,100,100,500,100)"
    print(f"执行: {command}")
    result = plugin.drawing_api.execute_command(command)
    print(f"结果: {result}")
    time.sleep(1)
    
    # 测试绘制圆形
    command = "draw(circle,300,200,50)"
    print(f"执行: {command}")
    result = plugin.drawing_api.execute_command(command)
    print(f"结果: {result}")
    time.sleep(1)
    
    # 测试绘制矩形
    command = "draw(rect,200,250,200,100)"
    print(f"执行: {command}")
    result = plugin.drawing_api.execute_command(command)
    print(f"结果: {result}")
    time.sleep(1)
    
    # 测试绘制文本
    command = 'draw(text,250,380,"Ollama测试")'
    print(f"执行: {command}")
    result = plugin.drawing_api.execute_command(command)
    print(f"结果: {result}")
    time.sleep(1)
    
    print("基本绘图命令测试完成!")

def test_natural_language_commands(plugin):
    """测试自然语言转命令功能"""
    print("\n=== 测试自然语言转命令 ===")
    
    # 测试几个简单的自然语言命令
    test_commands = [
        "在右上角画一个蓝色圆形",
        "在左下角写'Hello Ollama'",
        "从顶部中央到底部中央画一条红色直线",
        "画一个绿色矩形在中间位置"
    ]
    
    for natural_command in test_commands:
        print(f"\n自然语言: {natural_command}")
        
        # 获取Ollama生成的命令
        print("获取Ollama生成的命令...")
        api_command = plugin.query_ollama(natural_command)
        
        if api_command:
            print(f"生成的API命令: {api_command}")
            
            # 执行命令
            print("执行命令...")
            result = plugin.execute_command(api_command)
            print(f"执行结果: {result}")
        else:
            print("无法获取有效的API命令")
        
        time.sleep(2)  # 给用户时间查看结果
    
    print("自然语言转命令测试完成!")

def test_color_and_style(plugin):
    """测试颜色和样式设置"""
    print("\n=== 测试颜色和样式设置 ===")
    
    # 设置颜色为红色
    print("设置颜色为红色")
    plugin.drawing_api.set_color('#ff0000')
    time.sleep(1)
    
    # 绘制红色直线
    plugin.execute_command("draw(line,100,400,500,400)")
    time.sleep(1)
    
    # 设置线宽
    print("设置线宽为10")
    plugin.drawing_api.set_line_width(10)
    time.sleep(1)
    
    # 绘制粗线条
    plugin.execute_command("draw(line,100,450,500,450)")
    time.sleep(1)
    
    print("颜色和样式设置测试完成!")

def test_clear_canvas(plugin):
    """测试清空画布功能"""
    print("\n=== 测试清空画布 ===")
    
    # 提示用户
    input("按Enter键清空画布...")
    
    # 清空画布
    plugin.execute_command("clear()")
    print("画布已清空!")

def main():
    """主测试函数"""
    print("Ollama画板控制插件测试")
    print("=========================")
    
    try:
        # 创建插件实例
        print("\n初始化插件...")
        plugin = OllamaDrawPlugin()
        
        # 检查连接
        print("检查连接状态...")
        if not plugin.check_connections():
            print("错误: 无法连接到Ollama或画板服务")
            print("请确保:")
            print("1. Ollama服务正在运行 (http://localhost:11434)")
            print("2. 画板Web服务正在运行 (http://localhost:8000)")
            return
        
        print("\n连接成功，可以开始测试!")
        
        # 运行测试
        test_basic_commands(plugin)
        
        # 询问是否继续测试自然语言功能
        if input("\n是否测试自然语言转命令功能? (y/n): ").lower() == 'y':
            test_natural_language_commands(plugin)
        
        test_color_and_style(plugin)
        test_clear_canvas(plugin)
        
        print("\n测试完成!")
        print("\n使用说明:")
        print("1. 运行交互式模式: python ollama_draw_plugin.py")
        print("2. 通过浏览器使用Web界面: 打开 ollama_control.html")
        print("3. 使用自然语言描述你想要绘制的图形")
        
    except KeyboardInterrupt:
        print("\n测试已中断")
    except Exception as e:
        print(f"\n测试出错: {e}")

if __name__ == "__main__":
    main()