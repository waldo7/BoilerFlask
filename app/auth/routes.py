from datetime import datetime, timezone
from urllib.parse import urlparse, urljoin

from flask import current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

from app.auth import auth_bp
from app.auth.forms import (
    ForgotPasswordForm,
    LoginForm,
    RegistrationForm,
    ResetPasswordForm,
)
from app.extensions import db
from app.models.user import Role, User


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.netloc == ref_url.netloc


def get_limiter():
    limiter = current_app.extensions.get('limiter')
    if limiter:
        return limiter
    return type('NoOpLimiter', (), {'limit': lambda *a, **kw: lambda f: f})()


def rate_limit():
    limiter = current_app.extensions.get('limiter')
    if limiter:
        return limiter.limit("10 per minute")
    return lambda f: f


def generate_reset_token(user):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return s.dumps(str(user.id), salt='password-reset')


def verify_reset_token(token, max_age=3600):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        user_id = s.loads(token, salt='password-reset', max_age=max_age)
    except (SignatureExpired, BadSignature):
        return None
    return User.query.get(int(user_id))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in.', 'info')
        return redirect(url_for('main.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(form.password.data):
            if not user.is_active:
                flash('This account has been deactivated.', 'danger')
                return render_template('auth/login.html', form=form)
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page and is_safe_url(next_page):
                return redirect(next_page)
            return redirect(url_for('main.dashboard'))
        flash('Invalid email or password.', 'danger')

    return render_template('auth/login.html', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data.strip().lower(),
            role=Role.USER,
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=False)
        flash('Account created successfully. Welcome!', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('auth/register.html', form=form)


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        user = User.query.filter_by(email=email).first()

        if user:
            token = generate_reset_token(user)
            user.password_reset_requested_at = datetime.now(timezone.utc)
            db.session.commit()

            if current_app.config.get('DEBUG') and not current_app.config.get('TESTING'):
                reset_url = url_for('auth.reset_password', token=token, _external=True)
                print(f"Password reset URL for {user.email}: {reset_url}")
            else:
                try:
                    from flask_mail import Message
                    msg = Message(
                        subject='Password Reset — FlaskStuct',
                        sender=current_app.config['MAIL_DEFAULT_SENDER'],
                        recipients=[user.email],
                        body=f'Use this link to reset your password:\n\n{url_for("auth.reset_password", token=token, _external=True)}\n\nThis link expires in 1 hour.',
                    )
                    current_app.extensions['mail'].send(msg)
                except Exception as e:
                    print(f"Email send failed: {e}")

        return render_template('auth/reset_request_sent.html')

    return render_template('auth/forgot_password.html', form=form)


@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = verify_reset_token(token)
    if user is None or user.password_reset_requested_at is None:
        flash('This reset link is invalid. Please request a new one.', 'danger')
        return redirect(url_for('auth.forgot_password'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        user.password_reset_requested_at = None
        db.session.commit()
        flash('Password reset successfully. Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password.html', form=form)
