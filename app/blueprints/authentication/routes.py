from flask import render_template, redirect, url_for, flash, request, session
from app.forms import RegisterForm, LoginForm, ConfirmCodeForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import ChangePasswordForm
from db.database import session_scope
from db.models import User
import random

from . import auth_blueprint


@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        with session_scope() as this_session:
            email = this_session.query(User).filter_by(email=form.email.data).first()
            phone = this_session.query(User).filter_by(phone=form.phone_number.data).first()
            if email:
                flash('Пользователь с таким email уже зарегистрирован.', 'error')
                return redirect(url_for('auth.register'))
            if phone:
                flash('Пользователь с таким телефоном уже зарегистрирован.', 'error')
                return redirect(url_for('auth.register'))

            confirmation_code = str(random.randint(1000, 9999))
            session['pending_user'] = {
                'name': form.name.data,
                'surname': form.surname.data,
                'email': form.email.data,
                'phone_number': form.phone_number.data,
                'password_hash': generate_password_hash(form.password.data),
                'register_code': confirmation_code
            }
            return redirect(url_for('auth.confirm'))

    elif form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{form[field].label.text}: {error}', 'danger')

    return render_template('register.html', form=form)


@auth_blueprint.route('/confirm', methods=['GET', 'POST'])
def confirm():
    if 'pending_user' not in session:
        flash('Сначала зарегистрируйтесь.', 'warning')
        return redirect(url_for('auth.register'))

    form = ConfirmCodeForm()

    if request.method == 'GET':
        if request.args.get('resend') == 'resend':
            new_code = str(random.randint(1000, 9999))
            session['pending_user']['register_code'] = new_code
            flash(f'Код отправлен повторно: {new_code}', 'info')
            return redirect(url_for('auth.confirm'))

        if not session.get('confirmation_shown'):
            flash(f'Код: {session['pending_user']['register_code']}', 'success')
            session['confirmation_shown'] = True

    if form.validate_on_submit():
        entered_code = str(form.code.data).strip()
        stored_code = str(session['pending_user']['register_code']).strip()

        if entered_code == stored_code:
            user_data = session.pop('pending_user')
            session.pop('confirmation_shown', None)
            user = User(
                name=user_data['name'],
                surname=user_data['surname'],
                email=user_data['email'],
                phone=user_data['phone_number'],
                password_hash=user_data['password_hash']
            )
            with session_scope() as db_session:
                db_session.add(user)
            flash('Регистрация подтверждена! Теперь можете войти.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Неверный код подтверждения.', 'danger')

    return render_template('confirm_register.html', form=form)


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        with session_scope() as this_session:
            user = this_session.query(User).filter_by(email=form.email.data).first()
            if user and check_password_hash(user.password_hash, form.password.data):
                login_user(user=user)
                return redirect(url_for('index.main'))
        flash('Не удалось войти', 'danger')
    return render_template('login.html', form=form)


@auth_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index.main'))


@auth_blueprint.route('/profile')
@login_required
def profile():
    form = ChangePasswordForm()
    return render_template('profile.html', form=form)


@auth_blueprint.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    user_id = current_user.id
    with session_scope() as db_session:
        user = db_session.query(User).get(user_id)
        if not user:
            flash('Пользователь не найден.', 'danger')
            return redirect(url_for('auth.register'))

        db_session.delete(user)
        flash('Ваш аккаунт был успешно удалён.', 'success')

    logout_user()
    return redirect(url_for('auth.register'))


@auth_blueprint.route('/change-password', methods=['POST'])
@login_required
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        with session_scope() as db_session:
            user = db_session.query(User).get(current_user.id)
            if not check_password_hash(user.password_hash, form.current_password.data):
                flash('Текущий пароль неверен', 'danger')
                return redirect(url_for('auth.profile'))

            user.password_hash = generate_password_hash(form.new_password.data)
            db_session.add(user)
            flash('Пароль успешно изменён', 'success')
            return redirect(url_for('auth.profile'))

    for field, errors in form.errors.items():
        for error in errors:
            flash(f'{form[field].label.text}: {error}', 'danger')

    return redirect(url_for('auth.profile'))

