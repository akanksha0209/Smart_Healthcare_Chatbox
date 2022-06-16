from flask import Flask, render_template, redirect
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SeelectField
from wtforms.validators import DataRequired, Length
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# secret key
app.secret_key = "akanksha"
Bootstrap(app)

class LoginForm(FlaskForm):
    name=StringField(label="Name", validators=[DataRequired()])
@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    #db.create_all()
    app.run(debug=True)