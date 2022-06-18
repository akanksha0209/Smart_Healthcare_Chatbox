from __future__ import division, print_function

from flask import Flask, render_template, redirect, request, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length
from sqlalchemy import Column, Integer, String
import sys
import os
import glob
import re
from keras.models import Sequential
import numpy as np
import keras
import tensorflow

from PIL import Image, ImageOps
from keras.applications.mobilenet import MobileNet
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.models import Model, load_model
from keras.preprocessing.image import ImageDataGenerator
from werkzeug.utils import secure_filename
from keras.preprocessing import image

# from gevent.pywsgi import WGSIServer

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# secret key
app.secret_key = "akanksha"
Bootstrap(app)
#
Model = load_model('best_model.h5')

lesion_classes_dict = {
    0: 'Melanocytic nevi',
    1: 'Melanoma-Cancerous',
    2: 'Benign keratosis-like lesions',
    3: 'Basal cell carcinoma-Cancerous',
    4: 'Actinic keratoses',
    5: 'Vascular lesions',
    6: 'Dermatofibroma'

}

#
# def model_predict(img_path):
#     np.set_printoptions(suppress=True)
#
#     data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
#
#     # Replace this with the path to your image
#     image = Image.open(img_path)
#     # resizing the image to be at least 224x224
#
#     size = (224, 224)
#     image = ImageOps.fit(image, size, Image.ANTIALIAS)
#
#     # turn the image into a numpy array
#     image_array = np.array(image)
#
#     # Normalize the image
#     normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
#
#     # Load the image into the array
#     data[0] = normalized_image_array
#
#     # Load the model
#     model = tensorflow.keras.models.load_model('model.h5')
#
#     # run the inference
#     preds = ""
#     prediction = model.predict(data)
#     if np.argmax(prediction) == 0:
#         preds = f"Unripe😑"
#     elif np.argmax(prediction) == 1:
#         preds = f"Overripe😫"
#     else:
#         preds = f"ripe😄"
#
#     return preds


def model_predict(image_path, Model):
    img = image.load_img(image_path, target_size=(224, 224, 3))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    preds = Model.predict(x)
    return preds


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

    def add_person(self, name, age, phone_no, gender, pincode):
        new_user = PeopleLogin(name=name, age=age, phone_no=phone_no, gender=gender, pincode=pincode)

        db.session.add(new_user)
        db.session.commit()


db.create_all()


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/signup', methods=["GET", "POST"])
def signup():
    signup_form = SignUpForm()
    if signup_form.validate_on_submit():
        name = signup_form.name.data
        age = signup_form.age.data
        phone_no = signup_form.phone_no.data
        gender = signup_form.gender.data
        pincode = signup_form.pincode.data
        p = PeopleLogin()
        p.add_person(name, age, phone_no, gender, pincode)
        return render_template('home.html')

    return render_template('signup.html', form=signup_form)


@app.route('/login', methods=["GET", "POST"])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        name = login_form.name.data
        people = PeopleLogin.query.filter_by(name=name).first()
        print(people)
        if login_form.phone_no.data == people.phone_no:
            return render_template('home.html')
        else:
            return render_template('login.html', form=login_form)

    return render_template('login.html', form=login_form)


@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/chatbot', methods=["GET", "POST"])
def chatbot():
    return render_template('chatbot.html')


@app.route('/predict', methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        f = request.files['file']
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)
        preds = model_predict(file_path, Model)
        pred_class = preds.argmax(axis=-1)
        pr = lesion_classes_dict[pred_class[0]]
        result = str(pr)
        return result
    return None


if __name__ == '__main__':
    # db.create_all()
    app.run(debug=True)
