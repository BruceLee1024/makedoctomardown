#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将对话内容转换为表格格式的Markdown文件
"""

import re

def convert_dialogue_to_table(input_file, output_file):
    """将对话内容转换为表格格式"""
    
    # 读取原始markdown文件
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 解析对话内容
    lines = content.strip().split('\n')
    table_rows = []
    current_speaker = ''
    current_time = ''
    current_content = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # 匹配发言人和时间戳
        speaker_match = re.match(r'(发言人[12])\s+(\d{2}:\d{2})', line)
        if speaker_match:
            # 如果有之前的内容，先保存
            if current_speaker and current_content:
                table_rows.append({
                    'time': current_time,
                    'speaker': current_speaker,
                    'content': ' '.join(current_content).strip()
                })
            
            # 开始新的发言
            current_speaker = speaker_match.group(1)
            current_time = speaker_match.group(2)
            current_content = []
            
            # 检查这一行是否有内容（在时间戳后面）
            content_part = line[speaker_match.end():].strip()
            if content_part:
                current_content.append(content_part)
        else:
            # 继续当前发言的内容
            if current_speaker:
                current_content.append(line)
    
    # 保存最后一个发言
    if current_speaker and current_content:
        table_rows.append({
            'time': current_time,
            'speaker': current_speaker,
            'content': ' '.join(current_content).strip()
        })
    
    # 生成表格格式的markdown
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('| 时间戳 | 发言人 | 内容 |\n')
        f.write('|--------|--------|------|\n')
        
        for row in table_rows:
            # 转义管道符
            content = row['content'].replace('|', '\\|')
            f.write(f'| {row["time"]} | {row["speaker"]} | {content} |\n')
    
    return len(table_rows)

if __name__ == "__main__":
    input_file = "徐工-华展_原文.md"
    output_file = "徐工-华展_原文_表格版.md"
    
    try:
        row_count = convert_dialogue_to_table(input_file, output_file)
        print(f"转换完成！共生成 {row_count} 行表格数据")
        print(f"文件已保存为：{output_file}")
    except Exception as e:
        print(f"转换失败：{e}")