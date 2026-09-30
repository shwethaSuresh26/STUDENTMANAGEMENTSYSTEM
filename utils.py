import os
from functools import wraps
from datetime import datetime, timezone
from flask import session, redirect, url_for, flash, request, current_app
from werkzeug.utils import secure_filename
from models import db, ActivityLog, User

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def log_activity(action_type, description, icon_class='bi-activity', user_id=None):
    try:
        uid = user_id or session.get('user_id')
        log = ActivityLog(
            user_id=uid,
            action_type=action_type,
            description=description,
            icon_class=icon_class,
            timestamp=datetime.now(timezone.utc)
        )
        db.session.add(log)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error logging activity: {e}")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def save_avatar(file_storage, student_id):
    if not file_storage or file_storage.filename == '':
        return 'default-avatar.svg'
    
    if file_storage and allowed_file(file_storage.filename):
        ext = file_storage.filename.rsplit('.', 1)[1].lower()
        filename = secure_filename(f"{student_id}_{int(datetime.now(timezone.utc).timestamp())}.{ext}")
        upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        os.makedirs(os.path.dirname(upload_path), exist_ok=True)
        file_storage.save(upload_path)
        return filename
    return 'default-avatar.svg'
