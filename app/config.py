
import os  # 导入os模块，用于读取环境变量

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'cab5cfcd9cb8a1177a588a5c8879aafbea317fe8a4f81c8bb13006cabd4a475e'  # Flask安全密钥，用于会话等
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../instance/phishing.db'  # 数据库连接字符串，使用SQLite
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 关闭SQLAlchemy事件系统，节省资源
