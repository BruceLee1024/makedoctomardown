#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接转换Word文档到Markdown
"""

import os
import sys
from markitdown import MarkItDown

def convert_docx_to_markdown(docx_path):
    """转换Word文档到Markdown"""
    try:
        if not os.path.exists(docx_path):
            print(f"错误：文件 {docx_path} 不存在")
            return None
            
        print(f"正在转换：{docx_path}")
        
        # 初始化MarkItDown
        md = MarkItDown()
        
        # 转换文档
        result = md.convert(docx_path)
        
        if result and result.text_content:
            # 生成输出文件名
            base_name = os.path.splitext(os.path.basename(docx_path))[0]
            output_file = f"{base_name}.md"
            
            # 保存Markdown文件
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(result.text_content)
            
            print(f"转换完成！输出文件：{output_file}")
            print(f"文件大小：{len(result.text_content)} 字符")
            
            # 显示前500字符作为预览
            preview = result.text_content[:500]
            print(f"\n内容预览：\n{preview}...")
            
            return result.text_content
        else:
            print("转换失败：未能提取内容")
            return None
            
    except Exception as e:
        print(f"转换错误：{str(e)}")
        return None

if __name__ == "__main__":
    # 指定要转换的文件
    docx_file = "徐佳-浙江省院_原文.docx"
    
    # 转换文档
    content = convert_docx_to_markdown(docx_file)
    
    if content:
        print(f"\n✅ 成功转换文档，共 {len(content)} 字符")
    else:
        print("\n❌ 转换失败")