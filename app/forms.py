from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo, InputRequired


class RegisterForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired(message='Имя должно быть от 1 до 32 символов'),
                                          Length(1, 32)],
                       render_kw={'placeholder': 'Ваше имя'})
    surname = StringField('Фамилия', validators=[Length(1, 32)],
                          render_kw={'placeholder': 'Ваша фамилия'})
    email = StringField('Email', validators=[DataRequired(message='Это обязательное поле'),
                                             Email('Некорректный email')],
                        render_kw={'placeholder': 'example@mail.ru'})
    phone_number = StringField('Номер телефона: ', validators=[Length(min=1, max=20)],
                               render_kw={"placeholder": "+7 (999) 123-45-67",
                                          "pattern": r"^\+7\s?\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}$"})
    password = PasswordField(label='Пароль', validators=[DataRequired(), Length(min=8, max=36)],
                             render_kw={"placeholder": "Введите пароль"})
    confirm_password = PasswordField(label='Повторите Пароль', validators=[DataRequired(), EqualTo('password')],
                                     render_kw={"placeholder": "Повторите пароль"})
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()],
                        render_kw={"placeholder": "example@mail.ru"})
    password = PasswordField('Пароль',
                             render_kw={"placeholder": "Введите пароль"})
