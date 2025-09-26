
import os  # 导入os模块，用于读取环境变量

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')  # Flask安全密钥，必须通过环境变量设置
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../instance/phishing.db'  # 数据库连接字符串，使用SQLite
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 关闭SQLAlchemy事件系统，节省资源
