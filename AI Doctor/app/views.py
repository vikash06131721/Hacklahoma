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
    data['past'] = None
    data['present']= None
    user = User.query.filter_by(id=current_user.get_id()).first()
    data['username'] = str(user.name)
    data['useremail'] = str(user.email)
    if request.method == 'POST':
        symptom = request.form.get('symptoms')
        past = request.form.get('presentHis')
        present = request.form.get('pastHis')
        limit = request.form.get("myRange")
        # import pdb;pdb.set_trace()
        # data['past'] = past
        # data['present']= present
        if past!="" or past!=None:
            symptom = symptom+ "past illness "+past
        if present!="" or present!=None: 
            symptom = symptom+ "present illness "+present
        
        params = {
            'instruction': "You are a helpful, respectful, and honest assistant. Always answer as helpfully as possible while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don’t know the answer to a question, please don’t share false information.",
            'input':symptom,
            'tokens':int(limit)

        }
        # import pdb;pdb.set_trace()
        print(symptom)
        print(present)
        print(past)
        print(limit)
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

