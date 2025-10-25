#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI画板Python API示例

这个脚本演示了如何使用draw_api.py模块进行本地绘图。
"""

from draw_api import AIDrawingAPI

def main():
    """主函数 - 演示API的各种功能"""
    print("=== AI画板Python API 示例 ===")
    
    # 创建本地模式的API实例
    print("\n1. 创建画布...")
    api = AIDrawingAPI(width=800, height=600)
    print(f"画布创建成功: {api.width}x{api.height}")
    
    # 绘制基本图形
    print("\n2. 绘制基本图形...")
    
    # 设置颜色和线宽
    api.set_color('#0000ff')  # 设置为蓝色
    api.set_line_width(3)
    print(f"当前设置: 颜色={api.current_color}, 线宽={api.current_width}")
    
    # 绘制直线
    print("绘制一条直线...")
    api.draw_line(50, 50, 200, 50)
    
    # 绘制圆形（不指定颜色和线宽，使用当前设置）
    print("绘制一个圆形...")
    api.draw_circle(150, 150, 80)
    
    # 绘制矩形（指定不同的颜色和线宽）
    print("绘制一个矩形...")
    api.draw_rectangle(300, 100, 150, 100, color='#ff0000', width=5)
    
    # 绘制文本
    print("绘制文本...")
    api.draw_text(100, 300, "Python AI 画板示例", color='#008000', font_size=24)
    
    # 使用命令字符串绘制
    print("\n3. 使用命令字符串绘制...")
    
    # 绘制另一条直线
    result = api.execute_command("draw(line,400,400,600,400)")
    print(f"命令执行结果: {result}")
    
    # 绘制一个小圆点
    api.execute_command("draw(circle,500,500,5)")
    
    # 创建一个简单的房子
    print("\n4. 绘制一个简单的房子...")
    
    # 房子主体（矩形）
    api.set_color('#8B4513')  # 棕色
    api.draw_rectangle(500, 300, 100, 150, width=2)
    
    # 屋顶（三角形，用两条线绘制）
    api.set_color('#FF0000')  # 红色
    api.draw_line(500, 300, 550, 250)
    api.draw_line(550, 250, 600, 300)
    
    # 门（矩形）
    api.set_color('#654321')  # 深棕色
    api.draw_rectangle(540, 370, 20, 80, width=2)
    
    # 窗户（矩形）
    api.set_color('#87CEEB')  # 天蓝色
    api.draw_rectangle(520, 330, 20, 20, width=2)
    api.draw_rectangle(560, 330, 20, 20, width=2)
    
    # 导出图片
    output_file = "python_drawing_example.png"
    print(f"\n5. 导出图片到: {output_file}")
    success = api.export(output_file)
    
    if success:
        print(f"✓ 图片成功保存到: {output_file}")
        
        # 询问是否显示图片
        show_image = input("\n是否显示图片？(y/n): ")
        if show_image.lower() == 'y':
            print("正在显示图片...")
            api.show()
    else:
        print("✗ 图片保存失败")
    
    # 显示API功能总结
    print("\n=== API功能总结 ===")
    print("1. 绘制直线: draw_line(x1, y1, x2, y2, color, width)")
    print("2. 绘制圆形: draw_circle(x, y, radius, color, width)")
    print("3. 绘制矩形: draw_rectangle(x, y, width, height, color, width)")
    print("4. 绘制文本: draw_text(x, y, text, color, font_size)")
    print("5. 导出图片: export(filename)")
    print("6. 清空画布: clear()")
    print("7. 设置颜色: set_color(color)")
    print("8. 设置线宽: set_line_width(width)")
    print("9. 执行命令: execute_command(command)")
    print("10. 显示图片: show()")
    
    print("\n示例完成！您可以修改此脚本尝试不同的绘图功能。")


if __name__ == "__main__":
    try:
        main()
    except ImportError as e:
        print(f"错误: 无法导入必要的库。请运行以下命令安装依赖：")
        print("  pip install pillow requests")
        print(f"错误详情: {e}")
    except Exception as e:
        print(f"发生错误: {e}")