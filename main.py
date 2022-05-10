from flask import render_template, Flask, url_for
from forms.user import RegisterForm, LoginForm, LoadForm
import flask
import db_session
from users import User
from werkzeug.utils import redirect
from flask_login import LoginManager, UserMixin, current_user, login_user, login_required, logout_user
import sqlite3


app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'cucumber'
app = Flask(__name__)
app.config['SECRET_KEY'] = 'cucumber'
login = LoginManager(app)
login.login_view = 'auth.login'
login.init_app(app)


@login.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(int(user_id))


@app.route('/abc')
def abc():
    return render_template("abc.html", title="Главная")


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html", title="Главная")


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegisterForm()
    if form.submit.data:
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
            clas=form.clas.data,
            score=0
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template("registration.html", title="Регистрация", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.submit.data:
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)

    return render_template('login.html', title='Авторизация', form=form)


@app.route('/load', methods=['GET', 'POST'], endpoint="load")
@login_required
def profile():
    form = LoadForm()
    if form.submit.data:
        user = User()
        con = sqlite3.connect("db/users.db")
        cur = con.cursor()
        cur.execute(f"""INSERT INTO rewards(id, reward, deg) VALUES({current_user.id}, '{form.reward.data}',' {form.deg.data}')""")
        con.commit()
        con.close()

        user.make_calculations(current_user.id)
        return redirect(url_for("load"))

    return render_template('load.html', title='Личный кабинет', form=form, point=current_user.score)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/rating')
def rating():
    con = sqlite3.connect("db/users.db")
    cursor = con.cursor()
    items = cursor.execute("SELECT name, surname, clas, score FROM users").fetchall()
    items = sorted(items, key=lambda x: (x[3], x[0]), reverse=True)
    con.commit()
    con.close()

    return render_template('rating.html', title="Рейтинг", items=items)


if __name__ == '__main__':
    db_session.global_init("db/users.db")
    app.run(port=7777, host='127.0.0.1')
