#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将对话内容转换为表格格式的Markdown
"""

import re
import os
import sys  # 添加sys模块导入

def parse_dialogue_to_table(markdown_content):
    """解析对话内容并转换为表格格式"""
    lines = markdown_content.strip().split('\n')
    
    # 表格头部
    table_header = "| 时间戳 | 发言人 | 内容 |\n"
    table_separator = "|--------|--------|------|\n"
    
    # 用于存储表格行
    table_rows = []
    
    # 当前发言信息
    current_timestamp = ""
    current_speaker = ""
    current_content = []
    
    # 正则表达式匹配时间戳和发言人
    timestamp_pattern = r'(\d{2}:\d{2})'
    speaker_pattern = r'(发言人\d+)'
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # 检查是否是时间戳行
        timestamp_match = re.search(timestamp_pattern, line)
        speaker_match = re.search(speaker_pattern, line)
        
        if timestamp_match and speaker_match:
            # 如果有之前的发言，先保存
            if current_content:
                content = ' '.join(current_content).strip()
                if content:
                    table_rows.append(f"| {current_timestamp} | {current_speaker} | {content} |\n")
                
            # 开始新的发言
            current_timestamp = timestamp_match.group(1)
            current_speaker = speaker_match.group(1)
            current_content = []
            
            # 提取发言内容（去掉时间戳和发言人）
            content_part = re.sub(r'^.*?' + re.escape(current_speaker) + r'\s*' + re.escape(current_timestamp), '', line).strip()
            if content_part:
                current_content.append(content_part)
        else:
            # 如果是内容续行
            if current_speaker:
                current_content.append(line)
    
    # 保存最后一条发言
    if current_content and current_speaker and current_timestamp:
        content = ' '.join(current_content).strip()
        table_rows.append(f"| {current_timestamp} | {current_speaker} | {content} |\n")
    
    # 组合表格
    table_content = table_header + table_separator + ''.join(table_rows)
    
    return table_content

def convert_to_table_format(input_file, output_file=None):
    """将Markdown文件转换为表格格式"""
    try:
        if not os.path.exists(input_file):
            print(f"错误：文件 {input_file} 不存在")
            return False
            
        # 读取原始内容
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 转换为表格格式
        table_content = parse_dialogue_to_table(content)
        
        # 生成输出文件名
        if not output_file:
            base_name = os.path.splitext(os.path.basename(input_file))[0]
            output_file = f"{base_name}_表格版.md"
        
        # 保存表格格式
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(table_content)
        
        print(f"✅ 转换成功！")
        print(f"📁 输入文件：{input_file}")
        print(f"📁 输出文件：{output_file}")
        print(f"📊 共生成 {len(table_content.split(chr(10)))} 行表格")
        
        # 显示前5行作为预览
        preview_lines = table_content.split('\n')[:8]
        print(f"\n🔍 预览：")
        for line in preview_lines:
            print(line)
        
        return True
        
    except Exception as e:
        print(f"❌ 转换错误：{str(e)}")
        return False

def main():
    """主函数"""
    # 转换刚才生成的Markdown文件
    input_file = "徐佳-浙江省院_原文.md"
    output_file = "徐佳-浙江省院_原文_表格版.md"
    
    success = convert_to_table_format(input_file, output_file)
    
    if success:
        print("\n🎉 表格格式化完成！")
        print("您现在可以使用生成的表格版Markdown文件")
    else:
        print("\n💡 使用说明：")
        print("python3 format_table.py [输入文件] [输出文件]")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        convert_to_table_format(input_file, output_file)
    else:
        main()