from flask import Flask, render_template, redirect, request, abort, make_response, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import reqparse, abort, Api, Resource

from data.item_model import ItemModel
from data.ware_model import WareModel
from data.jobs import Jobs
from forms.jobs import JobsForm
from forms.user import RegisterForm, LoginForm
from forms.item import ItemForm
from forms.ware import WarehouseForm
from data.users import User
from data import db_session, jobs_api, users_resources
from db_processing import create_table

app = Flask(__name__)
api = Api(app) # создадим объект RESTful-API
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def main():
    db_session.global_init("db/main_database.db")

    # для списка объектов
    api.add_resource(users_resources.UsersListResource, '/api/v2/users')

    # для одного объекта
    api.add_resource(users_resources.UsersResource, '/api/v2/users/<int:user_id>')

    app.register_blueprint(jobs_api.blueprint)
    app.run(debug=True)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@app.errorhandler(404)
def not_found(_):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/jobs', methods=['GET', 'POST'])
@login_required
def add_jobs():
    form = JobsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = Jobs()
        jobs.job = form.job.data
        jobs.team_leader = form.team_leader.data
        jobs.work_size = form.work_size.data
        jobs.collaborators = form.collaborators.data
        jobs.is_finished = form.is_finished.data
        current_user.jobs.append(jobs)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('jobs.html', title='Добавление новости', form=form)


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
        return redirect('/')
    return render_template('warehouses.html', title='Создание склада', form=form)


@app.route('/new_item', methods=['GET', 'POST'])
@login_required
def add_item():
    """
    Добавляет строку товара в таблицу продуктов
    :return:
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
        return redirect('/')
    return render_template('new_item.html', title='Создание предмета', form=form)


@app.route('/items_list/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_item(id):
    form = ItemForm
    if request.method == "GET":
        db_sess = db_session.create_session()
        items = db_sess.query(ItemModel).filter(ItemModel.id == id).first()
        if items:
            form.item_name.data = items.name
            form.category.data = items.category
            form.price.data = items.price
            form.weight.data = items.weight
            form.desc.data = items.desc
        else:
            abort(404)
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            items = db_sess.query(ItemModel).filter(ItemModel.id == id).first()
            if items:
                items.name = form.item_name.data
                items.category = form.category.data
                items.price = form.price.data
                items.weight = form.weight.data
                items.desc = form.desc.data
                db_sess.commit()
                return redirect('/')
            else:
                abort(404)
        return render_template('item_edit.html',
                               title='Редактирование продукта',
                               form=form)


@app.route('/items_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_item(id):
    db_sess = db_session.create_session()
    items = db_sess.query(ItemModel).filter(ItemModel.id == id).first()
    if items:
        db_sess.delete(items)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/wares_list/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_ware(id):
    form = WarehouseForm
    if request.method == "GET":
        db_sess = db_session.create_session()
        items = db_sess.query(WareModel).filter(WareModel.id == id).first()
        if items:
            form.wh_name.data = items.name
            form.coords.data = items.coords
            form.limit.data = items.limit
            form.fullness.data = items.fullness
            form.description.data = items.description
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
                items.description = form.description.data
                db_sess.commit()
                return redirect('/')
            else:
                abort(404)
        return render_template('ware_edit.html',
                               title='Редактирование склада',
                               form=form)


@app.route("/")
def main_menu():
    """
    Основная странца, на ней новости, но при желании можно впихнуть, что угодно
    :return:
    """
    with open('README.md', mode='r', encoding='utf-8') as readme:
        text = readme.readlines()
    return render_template("main.html")


@app.route("/i")
def index():
    """
    Тестовая страница для БД
    :return:
    """
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    users = session.query(User).all()
    names = {name.id: (name.surname, name.name) for name in users}
    return render_template("index.html", jobs=jobs, names=names)


@app.route("/items_list")
def items_list():
    """
    Отображение табилцы предметов
    :return:
    """
    session = db_session.create_session()
    items = session.query(ItemModel).all()
    return render_template("items_table.html", items=items)


@app.route("/sklads_list")
def sklad_list():
    """
    Отображение табилцы складов
    :return:
    """
    session = db_session.create_session()
    items = session.query(ItemModel).all()
    print(items)
    return render_template("sklad_table.html", items=items)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    """
    Регистрация
    :return:
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
    Вход вв аккаунт
    :return:
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
    '''
    Выход из аккаунта
    :return:
    '''
    logout_user()
    return redirect("/")

if __name__ == '__main__':
    main()
