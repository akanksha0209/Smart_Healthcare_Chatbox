from __future__ import division, print_function

import cv2
from flask import Flask, render_template, redirect, request, url_for, flash
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
UPLOAD_FOLDER = 'C:/Users/akank/PycharmProjects/Smart Healthcare Chatbox/static/uploads'
UPLOAD_DISPLAY_FOLDER = 'C:/Users/akank/PycharmProjects/Smart Healthcare Chatbox/static/display_uploads'
# secret key
app.secret_key = "akanksha"
Bootstrap(app)
#
Model = load_model('best_model.h5')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_DISPLAY_FOLDER'] = UPLOAD_DISPLAY_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
lesion_classes_dict = {
    0: 'Melanocytic nevi',
    1: 'Melanoma-Cancerous',
    2: 'Benign keratosis-like lesions',
    3: 'Basal cell carcinoma-Cancerous',
    4: 'Actinic keratoses',
    5: 'Vascular lesions',
    6: 'Dermatofibroma'

}
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def model_predict(image_path, Model):
    img = tensorflow.keras.preprocessing.image.load_img(image_path, target_size=(224, 224, 3))
    x = tensorflow.keras.preprocessing.image.img_to_array(img)
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


@app.route('/upload', methods=["GET", "POST"])
def upload_form():
    if request.method == "POST":
        if request.files:
            ime = request.files["image"]
            if ime.filename == "":
                print("Image must have a filename")
                return redirect(request.url)
            if not allowed_file(ime.filename):
                print("Image extension is not allowed")
                return redirect(request.url)
            else:
                filename = secure_filename(ime.filename)
                ime.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                print("Image saved")
                flash('Image successfully uploaded')
                ime_location = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                ime.save(ime_location)
                ime_location_image = os.path.join(app.config["UPLOAD_DISPLAY_FOLDER"], filename)
                ime.save(ime_location_image)
                # full_filename = os.path.join(app.config['UPLOAD_DISPLAY_FOLDER'], filename)
                path = f"C:/Users/akank/PycharmProjects/Smart Healthcare Chatbox/static/display_uploads/{filename}"
                preds = model_predict(ime_location, Model)
                pred_class = preds.argmax(axis=-1)
                pr = lesion_classes_dict[pred_class[0]]
                predicted_result = str(pr)
                print(predicted_result)
                flash(predicted_result)

                return render_template('upload.html', filename=filename, prediction=0)
            # return redirect(request.url)

    return render_template('upload.html')


@app.route('/display/<filename>')
def display_image(filename):
    # print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='display_uploads/' + filename), code=301)

@app.route('/general_diseases')
def general_diseases():
    return render_template('disease.html')
# @app.route('/predict', methods=["GET", "POST"])
# def upload():
#     if request.method == "POST":
#         f = request.files['file']
#         basepath = os.path.dirname(__file__)
#         file_path = os.path.join(basepath, 'uploads', secure_filename(f.filename))
#         f.save(file_path)
#         preds = model_predict(file_path, Model)
#         pred_class = preds.argmax(axis=-1)
#         pr = lesion_classes_dict[pred_class[0]]
#         result = str(pr)
#         return result
#     return None


# @app.route('/upload')
# def predict():
#     return render_template('upload.html')
#
#
# @app.route('/upload', methods=["POST"])
# def upload_image():
#     if 'file' not in request.files:
#         flash('No file part')
#         return redirect(request.url)
#     file = request.files['file']
#     if file.filename == '':
#         flash('No image selected for uploading')
#         return redirect(request.url)
#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         # path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         #print(filename)
#         # print('upload_image filename: ' + filename)
#         flash('Image successfully uploaded and displayed below')
#         return render_template('upload.html', filename=filename)
#     else:
#         flash('Allowed image types are -> png, jpg, jpeg, gif')
#         return redirect(request.url)
#
#
# def disease_predict(file_path):
#     preds = model_predict(file_path, Model)
#     pred_class = preds.argmax(axis=-1)
#     pr = lesion_classes_dict[pred_class[0]]
#     result = str(pr)
#     return result


# @app.route('/predict', methods=["GET", "POST"])
# def upload():
#     if 'file' not in request.files:
#         flash('No file part')
#         return redirect(request.url)
#     file = request.files['file']
#     if file.filename == '':
#         flash('No image selected for uploading')
#         return redirect(request.url)
#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         file.save(file_path)
#         # print('upload_image filename: ' + filename)
#         flash('Image successfully uploaded and displayed below')
#         preds = model_predict(file_path, Model)
#         pred_class = preds.argmax(axis=-1)
#         pr = lesion_classes_dict[pred_class[0]]
#         result = str(pr)
#         return render_template('upload.html', filename=filename, result=result)
#     else:
#         flash('Allowed image types are -> png, jpg, jpeg, gif')
#         return redirect(request.url)

# result = ''
# file_path=''
# filename=''
# if request.method == "POST":
#     if 'file' not in request.files:
#         flash('No file part')
#         return redirect(request.url)
#     file = request.files['file']
#     if file.filename == '':
#         flash('No image selected for uploading')
#         return redirect(request.url)
#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         file_path=os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         file.save(file_path)
#         # print('upload_image filename: ' + filename)
#         flash('Image successfully uploaded and displayed below')
#     preds = model_predict(file_path, Model)
#     pred_class = preds.argmax(axis=-1)
#     pr = lesion_classes_dict[pred_class[0]]
#     result = str(pr)
#
# return render_template('home.html', result=result, filename=filename)

#
# @app.route('/display/<filename>')
# def display_image(filename):
#     # print('display_image filename: ' + filename)
#     return redirect(url_for('static', filename='uploads/' + filename), code=301)
if __name__ == '__main__':
    # db.create_all()
    app.run(debug=True)
# app.run(port=5000)
