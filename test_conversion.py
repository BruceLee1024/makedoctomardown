#!/usr/bin/env python3
"""
测试网页转换功能的简单脚本
"""

import requests
import os

def test_web_conversion():
    """测试网页转换功能"""
    url = 'http://localhost:5001/convert'
    
    # 检查是否存在测试文件
    test_files = [
        '2_原文.docx',
        'example.html'
    ]
    
    for test_file in test_files:
        if os.path.exists(test_file):
            print(f"正在测试转换: {test_file}")
            
            with open(test_file, 'rb') as f:
                files = {'file': (test_file, f)}
                try:
                    response = requests.post(url, files=files)
                    if response.status_code == 200:
                        print(f"✅ {test_file} 转换成功")
                        print(f"转换结果长度: {len(response.text)} 字符")
                        
                        # 保存转换结果
                        output_file = test_file.rsplit('.', 1)[0] + '_web.md'
                        with open(output_file, 'w', encoding='utf-8') as out:
                            out.write(response.text)
                        print(f"结果已保存到: {output_file}")
                    else:
                        print(f"❌ {test_file} 转换失败: {response.text}")
                except Exception as e:
                    print(f"❌ 请求失败: {e}")
            break
    else:
        print("没有找到测试文件，请先上传文件到网页界面测试")

if __name__ == '__main__':
    test_web_conversion()