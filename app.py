import os
from datetime import datetime, date
from flask import Flask, render_template, session, jsonify
from flask_cors import CORS
from config import Config
from models import db, User, Department, Student
from routes.auth_routes import auth_bp
from routes.dashboard_routes import dashboard_bp
from routes.student_routes import student_bp
from routes.attendance_routes import attendance_bp
from routes.marks_routes import marks_bp
from routes.fee_routes import fee_bp
from routes.timetable_routes import timetable_bp
from routes.report_routes import report_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Enable CORS for React frontend
    CORS(app, supports_credentials=True, origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:3000", "http://127.0.0.1:5173", "http://127.0.0.1:5174", "http://127.0.0.1:3000"])

    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Initialize extensions
    db.init_app(app)

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(attendance_bp)
    app.register_blueprint(marks_bp)
    app.register_blueprint(fee_bp)
    app.register_blueprint(timetable_bp)
    app.register_blueprint(report_bp)

    # Global template context processor
    @app.context_processor
    def inject_globals():
        current_user = None
        if 'user_id' in session:
            current_user = db.session.get(User, session['user_id'])
        
        return {
            'current_user': current_user,
            'current_year': date.today().year,
            'now': datetime.now(),
            'today_date': date.today().strftime('%A, %B %d, %Y'),
            'app_name': 'Student Management System'
        }

    # API endpoint to check user authentication
    @app.route('/api/auth/current-user')
    def get_current_user():
        if 'user_id' in session:
            user = db.session.get(User, session['user_id'])
            if user:
                return jsonify({
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'full_name': user.full_name,
                    'role': user.role
                }), 200
        return jsonify({'error': 'Unauthorized'}), 401

    # Error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        db.session.rollback()
        return render_template('errors/500.html'), 500

    return app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='127.0.0.1', port=5000) 
    
    
    
    
    
    
    
    
    
    
    
    
    
      