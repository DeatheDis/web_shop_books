from flask import render_template, redirect, url_for, flash
from . import public_info_blueprint


@public_info_blueprint.route('/contacts')
def contacts():
    return render_template('contact.html')


@public_info_blueprint.route('/delivery')
def delivery():
    return render_template('delivery.html')


@public_info_blueprint.route('/payment')
def payment():
    return render_template('payment.html')

