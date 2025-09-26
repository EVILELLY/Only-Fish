
import os  # 导入os模块，用于读取环境变量

class Config:
    SECRET_KEY = 'only-fish-phishing-platform-secret-key-2025'  # Flask安全密钥，固定值确保开箱即用
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../instance/phishing.db'  # 数据库连接字符串，使用SQLite
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 关闭SQLAlchemy事件系统，节省资源
