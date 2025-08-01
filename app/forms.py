from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, PasswordField
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, InputRequired

MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 36


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
                               render_kw={'placeholder': '+7 (999) 123-45-67',
                                          'pattern': r'^\+7\s?\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}$'})
    password = PasswordField(label='Пароль',
                             validators=[DataRequired(), Length(min=MIN_PASSWORD_LENGTH, max=MAX_PASSWORD_LENGTH)],
                             render_kw={'placeholder': 'Введите пароль'})
    confirm_password = PasswordField(label='Повторите Пароль', validators=[DataRequired(), EqualTo('password')],
                                     render_kw={'placeholder': 'Повторите пароль'})
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()],
                        render_kw={'placeholder': 'example@mail.ru'})
    password = PasswordField('Пароль',
                             render_kw={'placeholder': 'Введите пароль'})


class ConfirmCodeForm(FlaskForm):
    code = StringField('Код подтверждения', validators=[DataRequired(), Length(min=4, max=4)])
    submit = SubmitField('Подтвердить')


class ContactForm(FlaskForm):
    name = StringField('Ваше имя', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(message='Пожалуйста, введите email'),
                                             Email(message='Введите корректный email адрес')])
    message = TextAreaField('Сообщение', validators=[DataRequired(), Length(min=10, max=1000)])
    submit = SubmitField('Отправить сообщение')


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Текущий пароль', validators=[DataRequired()],
                                     render_kw={'placeholder': 'Введите текущий пароль'})
    new_password = PasswordField('Новый пароль',
                                 validators=[DataRequired(), Length(min=MIN_PASSWORD_LENGTH, max=MAX_PASSWORD_LENGTH)],
                                 render_kw={'placeholder': 'Введите новый пароль'})
    confirm_password = PasswordField('Подтвердите новый пароль',
                                     validators=[DataRequired(),
                                                 EqualTo('new_password', message='Пароли не совпадают')],
                                     render_kw={'placeholder': 'Повторите новый пароль'})
    submit = SubmitField('Сменить пароль')


class ReviewForm(FlaskForm):
    review = TextAreaField('Комментарий', validators=[DataRequired(), Length(min=2, max=500)],
                           render_kw={'placeholder': 'Поделитесь мнением о книге', 'rows': 3})
    grade = SelectField('Оценка', choices=[
        ('5', '★★★★★'),
        ('4', '★★★★☆'),
        ('3', '★★★☆☆'),
        ('2', '★★☆☆☆'),
        ('1', '★☆☆☆☆')
    ], validators=[DataRequired()])
    submit = SubmitField('Отправить')
