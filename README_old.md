# OnlyFish 钓鱼邮件演练平台

> 本项目仅限学习和研究用途，禁止任何形式的商业使用。

A phishing simulation and email management platform for security awareness training.

---

## 项目简介
OnlyFish 是一个用于安全意识培训的钓鱼邮件演练平台，支持邮件模板管理、收信人批量导入、邮件群发、后台管理等功能。适合企业、学校等组织进行内部安全演练。

## 主要功能
- 邮件模板管理与预览
- 支持自定义发件人名称、主题
- 收信人批量导入、清空
- 一键群发钓鱼演练邮件
- 邮件发送日志记录
- 管理后台（Flask + SQLite）

## 安装与运行
1. 克隆项目到本地：
   ```sh
   git clone https://github.com/你的用户名/onlyfish.git
   cd onlyfish
   ```
2. 安装依赖：
   ```sh
   pip install -r requirements.txt
   ```
3. 启动服务：
   ```sh
   python run.py --port 5001
   ```
4. 浏览器访问：
   ```
   http://127.0.0.1:5001/admin_xxx/email_manager
   ```
   （实际路径以终端输出为准）

## 配置说明
- 邮件配置文件：`instance/email_config.json`
- 邮件模板目录：`scripts/send_emails/email_templates/`
- 日志文件：`logs/app.log`

### 自定义安全密钥（可选）
如果需要更高安全性，可以自定义 Flask 应用的 SECRET_KEY：

1. 生成随机密钥：
   ```bash
   python -c "import secrets; print('SECRET_KEY = \"' + secrets.token_hex(32) + '\"')"
   ```

2. 修改 `app/config.py` 文件，将生成的密钥替换：
   ```python
   SECRET_KEY = 'your-generated-secret-key-here'
   ```

⚠️ **安全提示：请在上线或演练前务必修改/自定义所有钓鱼邮件模板内容，避免泄漏演示用企业、域名、邮箱、logo等敏感信息。建议将模板内容替换为你自己的组织信息和场景。**

## 依赖环境
- Python 3.7+
- Flask
- Flask-SQLAlchemy
- 其它见 requirements.txt

## 使用说明
1. 在后台页面填写 SMTP 配置、发件人名称、主题等。
2. 导入收信人邮箱（支持文本框或文件导入）。
3. 选择邮件模板，点击“一键发送钓鱼邮件”。
4. 查看发送结果和日志。

## License
> 本项目仅限学习和研究用途，禁止任何形式的商业使用。

---

# OnlyFish (English)

> This project is for learning and research purposes only. Commercial use is strictly prohibited.

A phishing simulation and bulk email platform for security awareness training.

## Features
- Email template management and preview
- Custom sender name and subject
- Bulk import/clear recipients
- One-click phishing email campaign
- Email sending logs


## Quick Start
1. Clone the repo:
   ```sh
   git clone https://github.com/yourname/onlyfish.git
   cd onlyfish
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run:
   ```sh
   python run.py --port 5001
   ```
4. Visit in browser:
   ```
   http://127.0.0.1:5001/admin_xxx/email_manager
   ```

## Config
- Email config: `instance/email_config.json`
- Templates: `scripts/send_emails/email_templates/`
- Logs: `logs/app.log`

## License
> This project is for learning and research purposes only. Commercial use is strictly prohibited.

---

## 生产部署建议
建议在生产环境使用 gunicorn + Nginx 部署，提高安全性和性能。

### 1. 使用 gunicorn 启动 Flask 服务
```sh
gunicorn -w 4 -b 127.0.0.1:5001 run:app
```

### 2. Nginx 反向代理配置示例
```
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 可选：静态资源托管
    location /static/ {
        alias /your/project/path/static/;
    }
}
```

### 3. 可选：HTTPS 配置
建议使用 certbot 等工具为 Nginx 配置免费 SSL 证书。

---
