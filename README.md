# MarkItDown Web 转换器

一个基于网页的文档转换工具，使用 MarkItDown 将各种文档格式转换为 Markdown。

## 🚀 快速开始

### 方法1：使用现有安装
```bash
# 启动网页服务
python3 server.py
```
浏览器将自动打开 http://localhost:5000

### 方法2：完整安装
```bash
# 安装依赖
pip install -r requirements.txt

# 启动网页服务
python3 server.py
```

## 📁 支持的格式

- **文档**: PDF, DOCX, DOC
- **表格**: XLSX, XLS
- **演示**: PPTX, PPT
- **网页**: HTML, HTM
- **文本**: TXT

## 🎯 使用方法

1. **上传文件**: 拖拽文件到上传区域或点击选择文件
2. **转换**: 点击"开始转换"按钮
3. **下载**: 转换完成后下载Markdown文件

## 🔧 高级用法

### 启动MCP服务器
```bash
# 启动独立的MCP服务器
python3 -m markitdown_mcp --http --host 127.0.0.1 --port 3002
```

### 命令行转换
```bash
# 单个文件转换
python3 -m markitdown input.pdf -o output.md

# 批量转换
python3 -m markitdown *.pdf -o output/
```

## 🌐 网页功能

- ✅ 拖拽上传
- ✅ 多文件支持
- ✅ 实时状态显示
- ✅ 下载转换结果
- ✅ 响应式设计
- ✅ 文件大小显示

## 📱 移动支持

网页完全响应式，支持手机和平板使用。

## 🔍 故障排除

### 服务器未连接
如果显示"服务器状态: 未连接"，请：
1. 确保已安装 markitdown-mcp: `pip install markitdown-mcp`
2. 启动MCP服务器: `python3 -m markitdown_mcp --http`

### 转换失败
1. 检查文件格式是否支持
2. 确保文件未损坏
3. 尝试使用命令行转换验证

## 🎨 自定义

可以修改以下文件进行自定义：
- `styles.css` - 样式表
- `app.js` - 前端逻辑
- `server.py` - 后端配置