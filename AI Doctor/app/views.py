from flask import Blueprint, render_template
from flask import render_template, request,redirect, url_for
from flask_login import login_required, current_user
from app.models import User
import requests
views = Blueprint('views',__name__)
# @views.route('/')
# def landing_page():
#     return render_template("signup.html")

@views.route('/home', methods=['GET', 'POST'])
@login_required
def get_content():
    data = {}
    data['output'] = None
    user = User.query.filter_by(id=current_user.get_id()).first()
    data['username'] = str(user.name)
    data['useremail'] = str(user.email)
    if request.method == 'POST':
        symptom = request.form.get('symptoms')
        params = {
            'param': symptom,
        }
        print(symptom)
        api_url = 'http://127.0.0.1:9000/return_pred'
        try:
            response = requests.post(api_url, json=params)
            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                data.update({'output': response.json()['output']})
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

