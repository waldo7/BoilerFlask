from flask import render_template
from flask_login import current_user, login_required

from app.main import main_bp


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
    return render_template('dashboard.html', user=current_user)
