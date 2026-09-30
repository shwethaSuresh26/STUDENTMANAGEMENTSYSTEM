from datetime import datetime, timezone
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort, jsonify
from models import db, User
from utils import login_required, log_activity

auth_bp = Blueprint('auth', __name__)


def _wants_json():
    """Check if the client expects a JSON response (e.g. React frontend)."""
    return (
        request.is_json
        or request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        or 'application/json' in request.headers.get('Accept', '')
    )


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        if _wants_json():
            return jsonify({'status': 'already_logged_in'}), 200
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        identifier = request.form.get('identifier', '').strip()  # username or email
        password = request.form.get('password', '')
        remember = request.form.get('remember')

        if not identifier or not password:
            if _wants_json():
                return jsonify({'error': 'Please enter both username/email and password.'}), 400
            flash('Please enter both username/email and password.', 'danger')
            return render_template('auth/login.html')

        user = User.query.filter(
            (User.username == identifier) | (User.email == identifier)
        ).first()

        if user and user.check_password(password):
            session.clear()
            session['user_id'] = user.id
            session['username'] = user.username
            session['full_name'] = user.full_name
            session['role'] = user.role
            session.permanent = True
            
            user.last_login = datetime.now(timezone.utc)
            db.session.commit()

            log_activity('Auth', f"User '{user.username}' logged in successfully.", 'bi-box-arrow-in-right', user.id)
            
            if _wants_json():
                return jsonify({
                    'status': 'success',
                    'message': f"Welcome back, {user.full_name}!"
                }), 200
            
            flash(f"Welcome back, {user.full_name}!", 'success')
            next_page = request.args.get('next')
            if next_page and next_page.startswith('/'):
                return redirect(next_page)
            return redirect(url_for('dashboard.index'))
        else:
            if _wants_json():
                return jsonify({'error': 'Invalid username/email or password.'}), 401
            flash('Invalid username/email or password.', 'danger')

    return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():
    username = session.get('username', 'User')
    uid = session.get('user_id')
    if uid:
        log_activity('Auth', f"User '{username}' logged out.", 'bi-box-arrow-right', uid)
    session.clear()
    
    # Check if it's an API request
    if request.headers.get('Accept') == 'application/json':
        return jsonify({'status': 'success', 'message': 'Logged out successfully'}), 200
    
    flash('You have been safely logged out.', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    user = db.session.get(User, session['user_id'])
    if not user:
        abort(404)
    
    if request.method == 'POST':
        current_pwd = request.form.get('current_password', '')
        new_pwd = request.form.get('new_password', '')
        confirm_pwd = request.form.get('confirm_password', '')

        if not user.check_password(current_pwd):
            flash('Current password is incorrect.', 'danger')
            return render_template('auth/change_password.html', user=user)

        if len(new_pwd) < 6:
            flash('New password must be at least 6 characters long.', 'danger')
            return render_template('auth/change_password.html', user=user)

        if new_pwd != confirm_pwd:
            flash('New passwords do not match.', 'danger')
            return render_template('auth/change_password.html', user=user)

        user.set_password(new_pwd)
        db.session.commit()
        
        log_activity('Auth', f"User '{user.username}' changed their password.", 'bi-key-fill', user.id)
        flash('Password successfully updated!', 'success')
        return redirect(url_for('dashboard.index'))

    return render_template('auth/change_password.html', user=user)
