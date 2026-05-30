import re
from getpass import getpass

import click

from app.extensions import db
from app.models.user import Role, User


def register_commands(app):
    @app.cli.command('create-admin')
    def create_admin():
        """Create an admin user interactively (prompts for email and password)."""
        email = input('Email: ').strip().lower()
        password = getpass('Password: ')
        confirm = getpass('Confirm password: ')

        if password != confirm:
            click.echo('Passwords do not match.', err=True)
            return

        if len(password) < 8:
            click.echo('Password must be at least 8 characters.', err=True)
            return

        count = sum(bool(re.search(p, password)) for p in [
            r'[A-Z]', r'[a-z]', r'[0-9]', r'[^A-Za-z0-9]'
        ])
        if count < 2:
            click.echo(
                'Password must contain at least 2 of: uppercase letter, '
                'lowercase letter, digit, or symbol.',
                err=True,
            )
            return

        if User.query.filter_by(email=email).first():
            click.echo(f'User {email} already exists.', err=True)
            return

        user = User(email=email, role=Role.ADMIN)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        click.echo(f'Admin user {email} created.')

    @app.cli.command('set-admin')
    @click.argument('email')
    @click.option(
        '--role',
        type=click.Choice(['user', 'admin', 'superuser']),
        default='admin',
    )
    def set_admin(email, role):
        """Set the role of an existing user."""
        user = User.query.filter_by(email=email.strip().lower()).first()
        if not user:
            click.echo(f'User {email} not found.', err=True)
            return

        user.role = Role(role)
        db.session.commit()
        click.echo(f'User {email} role set to {role}.')
