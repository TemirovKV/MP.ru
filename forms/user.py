from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, DateField, TextAreaField, BooleanField, SelectField, FileField
from wtforms.fields import EmailField
from wtforms.validators import DataRequired, Email


class RegisterForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    email = EmailField('E-mail', validators=[Email(), DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    clas = SelectField('В каком вы классе', validators=[DataRequired()], coerce=int, choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
    score = 0
    submit = SubmitField('Зарегестрироваться')


class LoginForm(FlaskForm):
    email = EmailField('E-mail', validators=[Email(), DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Авторизироваться')


class LoadForm(FlaskForm):
    reward = SelectField('Уровень конкурса', validators=[DataRequired()], choices=[("international_full-time", "Международный(очный)"),
                                                                                               ("all-Russian_full-time", "Всероссиский(очный)"),
                                                                                               ("interregional_full-time", "Межрегиональный(очный)"),
                                                                                               ("zonal_full-time", "Зональный(очный)"),
                                                                                               ("regional_full-time", "Областной(очный)"),
                                                                                               ("district_full-time", "Районый(очный)"),
                                                                                               ("municipal_full-time", "Муниципальный(очный)"),
                                                                                               ("international_correspondence", "Международный(заочный)"),
                                                                                               ("all-Russian_correspondence", "Всероссиский(заочный)")])

    deg = SelectField('Какое место вы заняли', validators=[DataRequired()], choices=[("grand_prix", "Первое место(Гран-при)"),
                                                                                                    ("second_deg", "Второе место"),
                                                                                                    ("third_deg", "Третье место"),
                                                                                                    ("participant", "Участник")])
    submit = SubmitField('Загрузить')
