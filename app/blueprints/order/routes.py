from datetime import datetime

from flask import render_template, redirect, url_for, flash, request, session
from flask_login import current_user, login_required
from db.database import session_scope
from db.models import CartItem, Order, OrderItem
from sqlalchemy.orm import joinedload

from . import order_blueprint

PICKUP_LOCATIONS = {
    'moscow_pobeda_23': 'г. Москва, ул. Победы, д. 23',
    'pushkina_kolotushkina': 'г. Москва, ул. Пушкина, д. Колотушкина',
    'esenina_karyselina': 'г. Москва, ул. Есенина, д. Каруселина'
}


@order_blueprint.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    if request.method == 'POST':
        selected_ids_raw = request.form.get('selected_items')
        selected_ids = selected_ids_raw.split(',') if selected_ids_raw else []

        if not selected_ids:
            flash('Выберите хотя бы один товар для оформления заказа', 'danger')
            return redirect(url_for('cart.cart'))

        session['selected_ids'] = selected_ids
        return redirect(url_for('order.checkout'))

    selected_ids = session.get('selected_ids')

    with session_scope() as db_session:
        if selected_ids:
            cart_items = db_session.query(CartItem).filter(
                CartItem.id.in_(selected_ids),
                CartItem.user_id == current_user.id
            ).all()
        else:
            cart_items = db_session.query(CartItem).filter_by(user_id=current_user.id).all()

        total = round(sum(item.book.price * item.count for item in cart_items), 2)

        return render_template('checkout.html',
                               cart_items=cart_items,
                               total=total,
                               pickup_locations=PICKUP_LOCATIONS,
                               delivery_date=datetime.utcnow().date().strftime('%Y-%m-%d'))


@order_blueprint.route('/confirm_order', methods=['POST'])
@login_required
def confirm_order():
    selected_ids = session.get('selected_ids', [])

    with session_scope() as db_session:
        cart_items = db_session.query(CartItem).filter(
            CartItem.id.in_(selected_ids),
            CartItem.user_id == current_user.id
        ).all()

        if not cart_items:
            flash('Не удалось найти выбранные товары', 'error')
            return redirect(url_for('cart.cart'))

        total = round(sum(item.book.price * item.count for item in cart_items), 2)

        delivery_method = request.form.get('delivery_method', '')
        address = request.form.get('address', '').strip()
        mail_address = request.form.get('mail_address', '').strip()
        pickup_location_key = request.form.get('pickup_location', '').strip()
        delivery_date_str = request.form.get('delivery_date', '').strip()

        if not delivery_method:
            flash('Пожалуйста, выберите способ доставки', 'danger')
            return redirect(url_for('order.checkout'))

        pickup_display_name = ''
        final_address = ''

        if delivery_method == 'courier':
            if not address:
                flash('Пожалуйста, укажите адрес для курьерской доставки', 'danger')
                return redirect(url_for('order.checkout'))
            final_address = address

        elif delivery_method == 'pickup':
            pickup_display_name = PICKUP_LOCATIONS.get(pickup_location_key, '')
            if not pickup_display_name:
                flash('Пожалуйста, выберите пункт самовывоза', 'danger')
                return redirect(url_for('order.checkout'))
            final_address = pickup_display_name

        elif delivery_method == 'mail':
            if not mail_address:
                flash('Пожалуйста, укажите почтовый адрес', 'danger')
                return redirect(url_for('order.checkout'))
            final_address = mail_address

        delivery_date = None
        if delivery_date_str:
            try:
                delivery_date = datetime.strptime(delivery_date_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Некорректный формат даты доставки', 'danger')
                return redirect(url_for('order.checkout'))

        order = Order(
            user_id=current_user.id,
            date=datetime.utcnow(),
            status='в обработке',
            address=final_address,
            delivery_date=delivery_date
        )
        db_session.add(order)
        db_session.flush()

        for item in cart_items:
            db_session.add(OrderItem(
                order_id=order.id,
                book_id=item.book_id,
                count=item.count,
                price=item.book.price
            ))

        for item in cart_items:
            db_session.delete(item)

        return render_template(
            'confirm_order.html',
            name=f'{current_user.name} {current_user.surname}',
            phone=current_user.phone,
            delivery_method=delivery_method,
            address=final_address,
            pickup_location=pickup_display_name,
            total=total,
            delivery_date=delivery_date_str or datetime.utcnow().date().strftime('%Y-%m-%d')
        )


@order_blueprint.route('/orders')
@login_required
def orders():
    with session_scope() as db_session:
        orders = db_session.query(Order).options(
            joinedload(Order.items).joinedload(OrderItem.book)
        ).filter_by(user_id=current_user.id).all()

        for order in orders:
            order.total_price = sum(item.price * item.count for item in order.items)

        return render_template('orders.html', orders=orders)


@order_blueprint.route('/order/<int:order_id>')
@login_required
def order_info(order_id):
    with session_scope() as db_session:
        order = db_session.query(Order).options(
            joinedload(Order.items).joinedload(OrderItem.book),
            joinedload(Order.user)
        ).filter_by(id=order_id, user_id=current_user.id).first()

        if not order:
            flash('Заказ не найден', 'danger')
            return redirect(url_for('order.orders'))

        order.total_price = sum(item.price * item.count for item in order.items)

        return render_template('order_info.html', order=order)


@order_blueprint.route('/order/<int:order_id>/cancel', methods=['POST'])
@login_required
def cancel_order(order_id):
    with session_scope() as db_session:
        order = db_session.query(Order).filter_by(id=order_id, user_id=current_user.id).first()
        if not order:
            flash('Заказ не найден', 'danger')
            return redirect(url_for('order.orders'))

        if order.status == 'отменен':
            flash('Заказ уже отменён', 'info')
            return redirect(url_for('order.order_info', order_id=order_id))

        order.status = 'отменен'
        flash('Заказ успешно отменён', 'success')
        return redirect(url_for('order.order_info', order_id=order_id))
