# 🎣 OnlyFish - 钓鱼邮件演练平台

<div align="center">

![OnlyFish Logo](https://img.shields.io/badge/OnlyFish-钓鱼演练平台-blueviolet?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.7+-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-Web框架-green?style=for-the-badge&logo=flask)
![License](https://img.shields.io/badge/License-学习研究用途-red?style=for-the-badge)

**一个专业的钓鱼邮件演练平台，用于企业安全意识培训**

[快速开始](#🚀-快速开始) • [功能特性](#✨-功能特性) • [界面预览](#📸-界面预览) • [配置说明](#⚙️-配置说明)

</div>

---

## 📋 项目简介

OnlyFish 是一个现代化的钓鱼邮件演练平台，专为企业、学校和组织的网络安全意识培训而设计。通过模拟真实的钓鱼攻击场景，帮助用户提高对钓鱼邮件的识别和防范能力。

### 🎯 设计理念
- **教育优先**：以安全教育为核心目标
- **界面现代**：采用现代化的紫色渐变设计
- **操作简单**：一键式操作，降低使用门槛
- **功能完整**：涵盖邮件发送、数据收集、结果分析的完整流程

---

## ✨ 功能特性

### 📧 邮件管理模块
- **📝 多模板支持**：内置多种钓鱼邮件模板
- **🎨 实时预览**：支持邮件模板的实时预览功能
- **📊 批量导入**：支持CSV文件批量导入收件人
- **⚙️ SMTP配置**：灵活的SMTP服务器配置
- **🚀 一键发送**：简单易用的批量邮件发送

### 🗂️ 凭证管理模块
- **📈 数据统计**：实时显示凭证收集和用户参与统计
- **🔍 智能筛选**：支持按用户名、IP、页面等条件筛选
- **📤 数据导出**：支持CSV格式导出分析数据
- **🗑️ 批量操作**：支持批量删除和管理功能

### 🎨 界面设计
- **🌈 现代美观**：紫色渐变背景，卡片式布局
- **📱 响应式设计**：完美适配桌面端和移动端
- **🎯 用户友好**：直观的操作界面，降低学习成本

---

## 🚀 快速开始

### 环境要求
- Python 3.7 或更高版本
- pip 包管理器

### 安装步骤

1. **克隆项目**
   ```bash
   git clone https://github.com/EVILELLY/Only-Fish.git
   cd Only-Fish
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **启动服务**
   ```bash
   python run.py --port 8080
   ```

4. **访问系统**
   打开浏览器访问终端显示的管理页面链接，例如：
   ```
   邮件管理：http://127.0.0.1:8080/admin_xxxxx/email_manager
   凭证管理：http://127.0.0.1:8080/admin_xxxxx/creds
   ```

---

## 📸 界面预览

### 邮件管理界面
现代化的卡片式设计，支持SMTP配置、模板选择、收件人管理等功能。

### 凭证管理界面  
统计面板 + 数据表格的设计，直观展示演练效果和收集到的数据。

### 钓鱼页面
高仿真的OA登录页面，用于模拟真实的钓鱼攻击场景。

---

## ⚙️ 配置说明

### 文件结构
```
Only-Fish/
├── app/                    # 应用核心代码
│   ├── templates/         # HTML模板文件
│   ├── routes/           # 路由处理
│   └── models/           # 数据模型
├── scripts/              # 邮件模板和脚本
│   └── send_emails/      
│       └── email_templates/  # 邮件模板目录
├── instance/             # 实例配置和数据库
├── logs/                 # 日志文件
└── malware/              # 模拟恶意文件
```

### SMTP 配置
在邮件管理界面配置SMTP服务器信息：
- **服务器地址**：如 `smtp.gmail.com`, `smtp.163.com`
- **端口**：587 (TLS) 或 465 (SSL)
- **发件人邮箱**：用于发送邮件的邮箱地址
- **授权码**：邮箱的SMTP授权码（非登录密码）

### 自定义安全密钥（可选）
如需更高安全性，可自定义 Flask 应用的 SECRET_KEY：

1. 生成随机密钥：
   ```bash
   python -c "import secrets; print('SECRET_KEY = \"' + secrets.token_hex(32) + '\"')"
   ```

2. 修改 `app/config.py` 文件中的密钥：
   ```python
   SECRET_KEY = 'your-generated-secret-key-here'
   ```

---

## 🛡️ 安全提示

> **⚠️ 重要提醒**
> 
> 1. **仅限内部使用**：本平台仅用于内部安全演练，禁止用于非法用途
> 2. **数据保护**：演练过程中收集的数据应妥善保管，演练结束后及时清理
> 3. **模板自定义**：使用前请务必修改邮件模板中的企业信息，替换为您的组织信息
> 4. **权限控制**：建议在内网环境中使用，避免暴露在公网
> 5. **事前通知**：进行演练前应获得相关部门的授权和员工的知情同意

---

## 🔧 高级配置

### 生产部署建议

使用 Gunicorn + Nginx 进行生产部署：

```bash
# 安装 Gunicorn
pip install gunicorn

# 启动应用
gunicorn -w 4 -b 127.0.0.1:8080 run:app
```

### Nginx 配置示例
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request 来帮助改进项目！

### 开发环境设置
```bash
# 克隆项目
git clone https://github.com/EVILELLY/Only-Fish.git
cd Only-Fish

# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或 .venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

---

## 📄 开源协议

本项目采用开源协议，但有以下限制：

- ✅ **允许**：学习、研究、内部安全培训使用
- ❌ **禁止**：商业用途、恶意攻击、未授权的渗透测试
- ⚠️ **要求**：使用者需承担相应的法律责任

---

## 📞 技术支持

如有问题或建议，请通过以下方式联系：

- 📧 提交 [GitHub Issue](https://github.com/EVILELLY/Only-Fish/issues)
- 💬 参与 [Discussion](https://github.com/EVILELLY/Only-Fish/discussions)

---

<div align="center">

**⭐ 如果这个项目对您有帮助，请给个 Star 支持一下！**

Made with ❤️ for cybersecurity education

</div>
