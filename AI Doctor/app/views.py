from flask import Blueprint, render_template
from flask import Flask, render_template, request, redirect, url_for
import requests
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
from app import models
from app.models import User, Medication
from datetime import date, datetime
from . import db  

views = Blueprint('views',__name__)
# @views.route('/')
# def landing_page():
#     return render_template("signup.html")

@views.route('/home', methods=['GET', 'POST'])
@login_required
def get_content():
    data = None
    if request.method == 'POST':
        symptom = request.form.get('Symptoms')
        params = {
            'instruction': "You are a helpful, respectful, and honest assistant. Always answer as helpfully as possible while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don’t know the answer to a question, please don’t share false information.",
            'input':symptom
        }
        print(symptom)
        # import pdb;pdb.set_trace()
        api_url = 'http://127.0.0.1:9000/return_pred'
        try:
            response = requests.post(api_url, json=params)
            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                data = response.json()
                return render_template("index.html", data=data)
            else:
                error = 'Failed to fetch data. Status code:' + str(response.status_code)
                return render_template("index.html", data=error)
        except requests.exceptions.RequestException as e:
            return render_template("index.html", data=e)
    return render_template("index.html", data=data)

@views.route('/signup/')
def signup_page():
    return render_template("signup.html")

