from flask import Flask, render_template, redirect
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length
from sqlalchemy import Column, Integer, String

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# secret key
app.secret_key = "akanksha"
Bootstrap(app)


class SignUpForm(FlaskForm):
    name = StringField(label="Name", validators=[DataRequired()])
    age = StringField(label="Age", validators=[DataRequired()])
    phone_no = StringField(label="Phone Number", validators=[DataRequired()])
    gender = StringField(label='Gender', validators=[DataRequired()])
    pincode = StringField(label="Pincode", validators=[DataRequired()])
    submit = SubmitField(label="Submit")


class LoginForm(FlaskForm):
    name = StringField(label="Name", validators=[DataRequired()])
    phone_no = StringField(label="Phone Number", validators=[DataRequired()])
    submit = SubmitField(label="Submit")


class PeopleLogin(db.Model):
    __tablename__ = 'people login '
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(String, nullable=False)
    phone_no = Column(String, unique=True, nullable=False)
    gender = Column(String, nullable=False)
    pincode = Column(String, nullable=False)


db.create_all()


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    people = PeopleLogin.query.all()

    if login_form.validate_on_submit():
        for person in people:
            if login_form.name.data == f'{person}' and login_form.phone_no.data == person.phone_no:
                return render_template('home.html')

    return render_template('login.html', form=login_form)


if __name__ == '__main__':
    # db.create_all()
    app.run(debug=True)
