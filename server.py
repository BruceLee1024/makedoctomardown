#!/usr/bin/env python3
"""
MarkItDown Web Server
支持MCP服务的Web服务器，用于处理文件转换请求
"""

import os
import json
import tempfile
import subprocess
import requests
from flask import Flask, request, jsonify, send_file, send_from_directory
from werkzeug.utils import secure_filename
import threading
import webbrowser
import time
from format_table import parse_dialogue_to_table  # 导入表格格式化功能
from markitdown import MarkItDown


app = Flask(__name__)

# 配置
UPLOAD_FOLDER = tempfile.mkdtemp()
ALLOWED_EXTENSIONS = {
    'pdf', 'docx', 'doc', 'xlsx', 'xls', 
    'pptx', 'ppt', 'html', 'htm', 'txt'
}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB限制

# MCP服务配置
MCP_SERVER_URL = "http://localhost:3001"

def convert_with_mcp(file_path, filename, content_type):
    """使用MCP服务转换文件"""
    try:
        # 尝试多种可能的端点
        endpoints = [
            f"{MCP_SERVER_URL}/convert",
            f"{MCP_SERVER_URL}/mcp/convert",
            f"{MCP_SERVER_URL}/tools/call",
        ]
        
        with open(file_path, 'rb') as f:
            files = {'file': (filename, f, content_type or 'application/octet-stream')}
            
            # 首先尝试标准转换端点
            for endpoint in endpoints:
                try:
                    response = requests.post(endpoint, files=files, timeout=30)
                    if response.status_code == 200:
                        # 尝试解析JSON响应
                        try:
                            result = response.json()
                            if isinstance(result, dict):
                                return result.get('content', result.get('text', response.text))
                            return response.text
                        except:
                            return response.text
                except:
                    continue
        
        return None
    except Exception as e:
        print(f"MCP转换错误: {e}")
        return None

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('.', filename)

@app.route('/health')
def health_check():
    """检查服务状态"""
    return jsonify({'status': 'healthy', 'service': 'MarkItDown Web'})

@app.route('/mcp-status')
def mcp_status():
    """检查MCP服务状态"""
    try:
        response = requests.get(f"{MCP_SERVER_URL}/health", timeout=2)
        return jsonify({
            'mcp_running': response.status_code == 200,
            'mcp_url': MCP_SERVER_URL
        })
    except:
        return jsonify({
            'mcp_running': False,
            'mcp_url': MCP_SERVER_URL
        })

# 使用MCP服务的转换端点
@app.route('/convert', methods=['POST'])
def convert_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': '没有上传文件'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': '没有选择文件'}), 400
        
        # 获取格式参数
        format_type = request.form.get('format', 'markdown')
        use_mcp = request.form.get('use_mcp', 'false').lower() == 'true'
        
        # 创建临时文件
        temp_dir = tempfile.mkdtemp()
        input_path = os.path.join(temp_dir, file.filename)
        file.save(input_path)
        
        content = ""
        
        if use_mcp:
            # 使用MCP服务转换 - 尝试多种可能的端点
            try:
                content = convert_with_mcp(input_path, file.filename, file.content_type)
                if not content:
                    # MCP返回空内容，使用本地转换
                    md = MarkItDown()
                    result = md.convert(input_path)
                    content = result.text_content if result else ""
                    
            except Exception as e:
                # MCP连接失败，使用本地转换
                print(f"MCP转换失败: {e}，使用本地转换")
                md = MarkItDown()
                result = md.convert(input_path)
                content = result.text_content if result else ""
        else:
            # 使用本地转换
            md = MarkItDown()
            result = md.convert(input_path)
            content = result.text_content if result else ""
        
        if not content:
            return jsonify({'error': '转换失败'}), 500
        
        # 如果需要表格格式
        if format_type == 'table':
            content = parse_dialogue_to_table(content)
        
        # 清理临时文件
        os.remove(input_path)
        os.rmdir(temp_dir)
        
        return jsonify({
            'success': True,
            'content': content,
            'format': format_type,
            'used_mcp': use_mcp
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/start-mcp', methods=['POST'])
def start_mcp():
    """启动MCP服务器"""
    try:
        # 启动MCP服务器的命令
        cmd = ['python3', '-m', 'markitdown_mcp', '--http', '--host', '127.0.0.1', '--port', '3002']
        subprocess.Popen(cmd)
        
        # 等待服务器启动
        time.sleep(2)
        
        return jsonify({'success': True, 'message': 'MCP服务器已启动'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    import threading
    import webbrowser
    
    def open_browser():
        time.sleep(2)
        webbrowser.open('http://localhost:5003')
    
    print("🚀 MarkItDown Web服务器启动中...")
    print("📱 浏览器将自动打开 http://localhost:5003")
    print("🔧 如果浏览器未自动打开，请手动访问上述地址")
    
    threading.Thread(target=open_browser).start()
    app.run(host='0.0.0.0', port=5003, debug=False)