from flask import render_template, flash, redirect, request, url_for
from flask_login import login_required, current_user
from db.database import session_scope
from db.models import User, CartItem
from sqlalchemy.orm import joinedload

from . import cart_blueprint


@cart_blueprint.route('/cart', methods=['GET'])
@login_required
def cart():
    with session_scope() as session:
        user = session.query(User).options(joinedload(User.cart_items).joinedload(CartItem.book)).get(current_user.id)
        total_sum = sum(item.book.price * item.count for item in user.cart_items)
        return render_template('cart.html', cart_items=user.cart_items, total_sum=total_sum)


@cart_blueprint.route('/add_to_cart/<int:book_id>', methods=['POST'])
@login_required
def add_to_cart(book_id):
    with session_scope() as session:
        try:
            quantity = max(int(request.form.get('count', 1)), 1)
        except ValueError:
            quantity = 1

        cart_item = session.query(CartItem).filter_by(user_id=current_user.id, book_id=book_id).first()

        if cart_item:
            cart_item.count += quantity
        else:
            new_item = CartItem(user_id=current_user.id, book_id=book_id, count=quantity)
            session.add(new_item)

        flash('Книга добавлена в корзину', 'success')

    return redirect(request.headers.get('Referer') or url_for('index.main'))


@cart_blueprint.route('/cart/update_cart/<int:item_id>', methods=['POST'])
@login_required
def update_cart(item_id):
    with session_scope() as session:
        item = session.query(CartItem).filter_by(user_id=current_user.id, id=item_id).first()
        if not item:
            return {'error': 'Товар не найден'}, 404

        data = request.get_json(silent=True)
        if not data or 'quantity' not in data:
            return {'error': 'Некорректные данные запроса'}, 400

        try:
            quantity = int(data['quantity'])
        except (ValueError, TypeError):
            return {'error': 'Неверный формат количества'}, 400

        if quantity < 1:
            session.delete(item)
            return {'message': 'Удалено'}, 200
        else:
            item.count = quantity
            return {'message': 'Обновлено', 'quantity': item.count}, 200


@cart_blueprint.route('/remove/<int:item_id>', methods=['POST'])
@login_required
def remove_item(item_id):
    with session_scope() as session:
        cart_item = session.query(CartItem).filter_by(
            id=item_id, user_id=current_user.id).first()

        if cart_item:
            session.delete(cart_item)
            flash('Товар удалён из корзины', 'success')
        else:
            flash('Товар не найден или уже удалён', 'warning')

    return redirect(url_for('cart.cart'))


@cart_blueprint.route('/delete_selected', methods=['POST'])
@login_required
def delete_selected():
    selected_ids = request.form.getlist('selected_items')
    if not selected_ids:
        flash('Не выбраны товары для удаления', 'warning')
        return redirect(url_for('cart.cart'))

    with session_scope() as session:
        items = session.query(CartItem).filter(
            CartItem.id.in_(selected_ids),
            CartItem.user_id == current_user.id
        ).all()
        for item in items:
            session.delete(item)

        flash(f'Удалено {len(items)} товаров из корзины', 'success')

    return redirect(url_for('cart.cart'))
