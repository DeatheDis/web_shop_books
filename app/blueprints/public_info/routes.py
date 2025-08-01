from flask import render_template, redirect, url_for, flash
from app.forms import ContactForm
from flask_login import current_user

from . import public_info_blueprint


@public_info_blueprint.route('/contacts', methods=['GET', 'POST'])
def contacts():
    if current_user.is_authenticated:
        form = ContactForm(name=current_user.name, email=current_user.email)
    else:
        form = ContactForm()

    if form.validate_on_submit():
        flash('Спасибо за ваше сообщение!', 'success')
        return redirect(url_for('public_info.contacts'))
    else:
        if form.errors:
            flash('Пожалуйста, исправьте ошибки в форме', 'danger')

    return render_template('contact.html', form=form)


@public_info_blueprint.route('/delivery')
def delivery():
    return render_template('delivery.html')


@public_info_blueprint.route('/payment')
def payment():
    return render_template('payment.html')

