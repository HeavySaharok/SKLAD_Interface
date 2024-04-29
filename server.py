from flask import Flask, render_template, redirect, request, abort, make_response, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import abort, Api

from data.item_model import ItemModel
from data.operations_model import OperationModel
from data.ware_model import WareModel
from forms.user import RegisterForm, LoginForm
from forms.item import ItemForm
from forms.ware import WarehouseForm
from forms.control import ControlForm
from data.users import User
from data import db_session, jobs_api, users_resources
from db.db_processing import *

app = Flask(__name__)
api = Api(app)  # создадим объект RESTful-API
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@login_manager.user_loader
def load_user(user_id):
    """
    Загрузка пользователя
    """
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def main():
    db_session.global_init("db/main_database.db")
    app.run(debug=True)


@app.errorhandler(400)  # ошибка 400
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@app.errorhandler(404)  # ошибка 404
def not_found(_):
    return render_template('not_found.html')


@app.route('/new_warehouse', methods=['GET', 'POST'])
@login_required
def add_ware():
    """
    Добавляет строку склада в таблицу складов
    :return:
    """
    form = WarehouseForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        ware = WareModel()
        ware.name = form.wh_name.data
        create_table(ware.name)
        ware.coords = form.coords.data
        ware.limit = form.limit.data
        ware.fullness = form.fullness.data
        ware.desc = form.description.data
        db_sess.merge(ware)
        db_sess.commit()
        return redirect('/wares_list')
    return render_template('warehouses.html', title='Создание склада', form=form)


@app.route('/new_item', methods=['GET', 'POST'])
@login_required
def add_item():
    """
    Добавляет строку товара в таблицу продуктов
    """
    form = ItemForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        item = ItemModel()
        item.name = form.item_name.data
        item.category = form.category.data
        item.price = form.price.data
        item.weight = form.weight.data
        item.description = form.desc.data
        db_sess.merge(item)
        db_sess.commit()
        return redirect('/items_list')
    return render_template('new_item.html', title='Создание предмета', form=form)


@app.route('/edit_item/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_item(id):
    """
    Редактирование выбранного товара в общем списке
    """
    form = ItemForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        item = db_sess.query(ItemModel).filter(ItemModel.id == id).first()
        if item:
            form.item_name.data = item.name
            form.category.data = item.category
            form.price.data = item.price
            form.weight.data = item.weight
            form.desc.data = item.description
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        item = db_sess.query(ItemModel).filter(ItemModel.id == id).first()
        if item:
            item.name = form.item_name.data
            item.category = form.category.data
            item.price = form.price.data
            item.weight = form.weight.data
            item.description = form.desc.data
            db_sess.merge(item)
            db_sess.commit()
            return redirect('/items_list')
        else:
            abort(404)
    return render_template('new_item.html',
                           title='Редактирование продукта',
                           form=form)


@app.route('/items_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_item(id):
    """
    Удаление товара из общего списка продуктов
    """
    db_sess = db_session.create_session()
    items = db_sess.query(ItemModel).filter(ItemModel.id == id).first()
    if items:
        db_sess.delete(items)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/items_list')


@app.route('/wares_list/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_ware(id):
    """
    Изменение выбранного склада в общем списке
    """
    form = WarehouseForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        items = db_sess.query(WareModel).filter(WareModel.id == id).first()
        if items:
            form.wh_name.data = items.name
            form.coords.data = items.coords
            form.limit.data = items.limit
            form.fullness.data = items.fullness
            form.description.data = items.desc
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        items = db_sess.query(WareModel).filter(WareModel.id == id).first()
        if items:
            items.name = form.wh_name.data
            items.coords = form.coords.data
            items.limit = form.limit.data
            items.fullness = form.fullness.data
            items.desc = form.description.data
            db_sess.commit()
            return redirect('/wares_list')
        else:
            abort(404)
    return render_template('warehouses.html',
                           title='Редактирование склада',
                           form=form)


@app.route('/wares_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_ware(id):
    """
    Удаление выбранного склада в общем списке
    """
    db_sess = db_session.create_session()
    ware = db_sess.query(WareModel).filter(WareModel.id == id).first()
    if ware:
        delete_table(ware.name)
        db_sess.delete(ware)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/wares_list')


@app.route("/")
def main_menu():
    """
    Основная странца, на ней новости, но при желании можно впихнуть, что угодно
    """
    # with open('README.md', mode='r', encoding='utf-8') as readme:
    #     text = readme.readlines()
    db_sess = db_session.create_session()
    opers = db_sess.query(OperationModel).all()[:10]
    return render_template("main.html", title='Последние 10 операций', opers=opers)


@app.route("/items_list")
def items_list():
    """
    Отображение табилцы предметов
    """
    session = db_session.create_session()
    items = session.query(ItemModel).all()
    return render_template("items_table.html", items=items)


@app.route("/wares_list")
def sklad_list():
    """
    Отображение табилцы складов
    """
    session = db_session.create_session()
    warehouses = session.query(WareModel).all()
    return render_template("sklad_table.html", warehouses=warehouses)


@app.route("/wares_inventory/<name>", methods=['GET', 'POST'])
def sklad_inventory(name):
    """
    Отображение инвентаря склада
    """
    items = table_data(name)
    print(items)
    return render_template("sklad_inventory.html", items=items)


@app.route("/control", methods=['GET', 'POST'])
def control():
    """
    На этой страницы можно производить логистику между и вне складов
    """
    session = db_session.create_session()
    form = ControlForm()
    wares = session.query(WareModel).all()
    print(form.output.data, form.input.data, form.id_item.data, form.count.data)
    if form.validate_on_submit():
        table_edit(form.output.data, form.id_item.data, form.count.data, 'output')
        table_edit(form.input.data, form.id_item.data, form.count.data)
        operation = OperationModel()
        operation.product_id = form.id_item.data
        operation.prod_amount = form.count.data
        operation.send = form.output.data
        operation.receive = form.input.data
        operation.res_price = 0
        session.merge(operation)
        session.commit()
        return redirect('/')
    print(wares)
    return render_template("control.html", title="Управление складами", form=form, wares=wares)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    """
    Регистрация
    """
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            surname=form.surname.data,
            speciality=form.speciality.data,
            hashed_password=form.set_password(form.password.data)
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Вход в аккаунт
    """
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)  # тыц, там session
            return redirect("/")
        return render_template('login_2.html', message="Неправильный логин или пароль", form=form)
    return render_template('login_2.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    """
    Выход из аккаунта
    """
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    main()
