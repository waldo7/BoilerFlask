from flask import current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, logout_user

from app.extensions import db
from app.main import main_bp
from app.models.user import Role, User
from app.auth.forms import ChangePasswordForm


@main_bp.route('/')
def index():
    """Homepage — shows placeholder to confirm scaffold works."""
    return render_template('home.html')


@main_bp.route('/about')
def about():
    """Placeholder about page — extends base.html."""
    return render_template('about.html')


@main_bp.route('/contact')
def contact():
    """Placeholder contact page — extends base.html."""
    return render_template('contact.html')


@main_bp.route('/dashboard')
@login_required
def dashboard():
    total_users = None
    role_counts = {}
    sys_config = None

    if current_user.role.value in ['admin', 'superuser']:
        try:
            total_users = User.query.count()
            counts = db.session.query(User.role, db.func.count(User.id)).group_by(User.role).all()
            # counts is a list of tuples: (Role.ADMIN, 1), etc.
            for role_enum, count in counts:
                role_counts[role_enum.value] = count
        except Exception as e:
            # Catch exceptions gracefully so dashboard never crashes
            current_app.logger.error(f"Error in dashboard stats query: {e}")

    if current_user.role.value == 'admin':
        try:
            db_uri = current_app.config.get('SQLALCHEMY_DATABASE_URI', '')
            db_dialect = db_uri.split(':')[0] if db_uri else 'Unknown'
            sys_config = {
                'mail_server': f"{current_app.config.get('MAIL_SERVER', 'N/A')}:{current_app.config.get('MAIL_PORT', '')}",
                'ratelimit': current_app.config.get('RATELIMIT_DEFAULT', 'N/A'),
                'db_dialect': db_dialect
            }
        except Exception as e:
            current_app.logger.error(f"Error in dashboard sys_config: {e}")

    return render_template('dashboard.html', 
                           active_page='dashboard', 
                           total_users=total_users, 
                           role_counts=role_counts, 
                           sys_config=sys_config)


@main_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = ChangePasswordForm()
    
    sys_config = None
    if current_user.role.value in ['admin', 'superuser']:
        try:
            db_uri = current_app.config.get('SQLALCHEMY_DATABASE_URI', '')
            db_dialect = db_uri.split(':')[0] if db_uri else 'Unknown'
            sys_config = {
                'mail_server': f"{current_app.config.get('MAIL_SERVER', 'N/A')}:{current_app.config.get('MAIL_PORT', '')}",
                'ratelimit': current_app.config.get('RATELIMIT_DEFAULT', 'N/A'),
                'db_dialect': db_dialect
            }
        except Exception as e:
            current_app.logger.error(f"Error in settings sys_config: {e}")

    if form.validate_on_submit():
        if not current_user.check_password(form.current_password.data):
            form.current_password.errors.append('Incorrect current password.')
            return render_template('settings.html', active_page='settings', form=form, sys_config=sys_config)
            
        current_user.set_password(form.new_password.data)
        db.session.commit()
        
        logout_user()
        flash('Your password has been changed successfully. For security reasons, all active sessions have been terminated. Please log in again.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('settings.html', active_page='settings', form=form, sys_config=sys_config)
