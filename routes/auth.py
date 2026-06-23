from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('catalog.home'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        remember = request.form.get('remember') == 'on'

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            flash(f'Bem-vindo de volta, {user.username}!', 'success')
            return redirect(next_page or url_for('catalog.home'))
        else:
            flash('Email ou senha incorretos.', 'error')

    return render_template('login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('catalog.home'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')

        # Validations
        errors = []
        if len(username) < 3:
            errors.append('Nome de usuário deve ter pelo menos 3 caracteres.')
        if User.query.filter_by(username=username).first():
            errors.append('Nome de usuário já está em uso.')
        if User.query.filter_by(email=email).first():
            errors.append('Email já cadastrado.')
        if len(password) < 6:
            errors.append('Senha deve ter pelo menos 6 caracteres.')
        if password != confirm:
            errors.append('As senhas não coincidem.')

        if errors:
            for e in errors:
                flash(e, 'error')
        else:
            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash('Conta criada com sucesso! Bem-vindo ao StreamPy!', 'success')
            return redirect(url_for('catalog.home'))

    return render_template('register.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        if username and username != current_user.username:
            if User.query.filter_by(username=username).first():
                flash('Nome de usuário já está em uso.', 'error')
            else:
                current_user.username = username
                db.session.commit()
                flash('Perfil atualizado!', 'success')

    from models import WatchProgress, Watchlist
    watchlist = Watchlist.query.filter_by(user_id=current_user.id)\
                               .order_by(Watchlist.added_at.desc()).limit(10).all()
    history = WatchProgress.query.filter_by(user_id=current_user.id)\
                                 .order_by(WatchProgress.watched_at.desc()).limit(10).all()

    return render_template('profile.html', watchlist=watchlist, history=history)
