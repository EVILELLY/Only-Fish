
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    department = db.Column(db.String(64))
    email = db.Column(db.String(128), unique=True, nullable=False)


class Credential(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password_hash = db.Column(db.String(256))
    raw_password = db.Column(db.String(128))  # 明文密码，仅用于演练环境
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    ip = db.Column(db.String(64))
    scene = db.Column(db.String(64))  # 钓鱼页面/场景标识
    user_agent = db.Column(db.String(256))  # 受害者UA
    extra_info = db.Column(db.Text)  # 预留扩展字段

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')
        self.raw_password = password  # 存储明文密码

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
