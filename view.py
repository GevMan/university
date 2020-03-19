import os
import os.path as op
from app import app,db,mail
from flask import Flask, render_template,redirect,url_for,request,flash,json, session
from flask_paginate import Pagination
from models import university,users,state,role,department,degree, international_universities,country
from flask_admin.contrib import sqla
from flask_admin import Admin, AdminIndexView, form
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user,login_manager,LoginManager,login_user,logout_user
import mysql.connector
from flask_admin.menu import MenuLink
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from validate_email import validate_email


class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated

Admin = Admin(app, index_view=MyAdminIndexView())
Admin.add_view(MyModelView(users, db.session))
Admin.add_view(MyModelView(state, db.session))
Admin.add_view(MyModelView(role, db.session))
Admin.add_view(MyModelView(university, db.session))
Admin.add_view(MyModelView(department, db.session))
Admin.add_view(MyModelView(degree, db.session))
Admin.add_view(MyModelView(international_universities, db.session))
Admin.add_view(MyModelView(country, db.session))
Admin.add_link(MenuLink(name='Home Page', url='/'))

class LogoutMenuLink(MenuLink):

    def is_accessible(self):
        return current_user.is_authenticated

Admin.add_link(LogoutMenuLink(name='Log Out', category='', url="/logout_admin"))

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = ''

@login_manager.user_loader
def load_user(id):
    return users.query.get(int(id))

app.secret_key = 'secret_key'

@app.route('/')
def index():
    return render_template('homepage-1.html')

@app.route('/about')
def about():
    return render_template('about-us.html')


@app.route('/universities/page/<int:page_num>')
def universities(page_num):    
    university_state=state.query.filter(state.id == university.state_id).all()
    page = university.query.order_by(university.id).paginate(page=page_num, per_page=7, error_out=True)    
    text = request.args.get('text')
    search="%{}%".format(text)
    if request.args.get('state'):
        page = university.query.filter(db.and_(university.state_id == request.args.get('state'),university.name.like(search))).paginate(page=page_num, per_page=15, error_out=True)
    return render_template('career-opportunity.html',page = page, states = university_state)

@app.route('/login')
def login():
    return render_template('login-page.html')

@app.route('/signin' , methods = ['POST'])
def signin():
    
    user = users.query.filter(
        db.and_(users.email == request.form['email'], users.password == request.form['password'])).first()
    if user == None:
        error = 'Please try again'
        return render_template('login-page.html', error=error)
    if user != None:

        if user.role_id == 1:
            login_user(user)
            user = users.query.get(user.id)
            return (redirect(url_for('admin.index')))
        else:
            session['logged_in'] = True
            session['user'] = dict()
            session['user']['id'] = user.id
            session['user']['full_name'] = user.full_name

            return (redirect(url_for('index')))

@app.route('/logout')
def logout():
    session.pop('logged_in')
    session.clear()
    return redirect(url_for('login'))

@app.route('/logout_admin')
def logout_admin():
    logout_user()
    session.clear()
    return redirect(url_for('login'))

@app.route('/signup')
def signup(): 
    messages = None
    if request.args.get('messages') is not None:
        messages = json.loads(request.args.get('messages'))
    return render_template('register-page.html', errors = messages)

@app.route('/register',methods = ['POST'])
def reg():
    check_email = users.query.filter(users.email == request.form['email']).first()
    messages = dict()
    generate = generate_password_hash(request.form['password'])
    try: 
        if len(request.form['full_name'])<3:
            messages['full_name'] = 'Your name is too short'
        
        if len(request.form['password'])<6:
            messages['password'] = 'Password is too short'
        
        if request.form['password'] != request.form['verify_password']:
            messages['verify_password'] = 'Passwords must match'
        
        if not validate_email(request.form['email']):
            messages['email'] = 'Email is not valid'
        
        if check_email and check_email.email == request.form['email']:
            messages['email'] = 'Email already exists'
    
        if len(messages) > 0:
            return redirect(url_for('signup', messages=json.dumps(messages)))
        new_user = users(full_name = request.form['full_name'],email= request.form['email'], password = generate ,role_id = 2)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    except:
        pass
    return(redirect(url_for('signup',messages=json.dumps(messages))))

@app.route('/contact')
def contact():
    message = None
    if request.args.get('message') is not None:
        message = json.loads(request.args.get('message'))
    return render_template('contact.html',error = message)

@app.route("/sendMessage",methods=['POST'])
def sendMsg():
    message = dict()   
    try:
        if len(request.form['email'])<1:
            message = 'enter an email'
            
        if len(request.form['text'])<1:
            message = 'enter a text'
        msg = Message(request.form['full_name'], 
                    recipients=['gevman97@gmail.com'],
                    html="Email: " +request.form['email'] +'<br>'+ "  Message: " + request.form['text']+" ")
        mail.send(msg)
        return redirect(url_for('contact'))
    except:
        pass
    return(redirect(url_for('contact',message=json.dumps(message))))

@app.route('/department/<id>')
def university_dep(id):
    degrees=degree.query.all()
    univer = university.query.get_or_404(id) 
    university_department = department.query.filter(db.and_(department.university_id == id,department.degree == degree.id)).all()
    text = request.args.get('text')
    search = "%{}%".format(text)
    if request.args.get('degree'):
        university_department = department.query.filter(db.and_(department.university_id == id,department.degree ==request.args.get('degree'), department.name.like(search))).all()
    return render_template('university.html',dep=university_department, univer = univer,degree=degrees)

@app.route('/gallery')
def gallery():
    return render_template('galery.html')


@app.route('/story')
def story():
    return render_template('story.html')

@app.route('/events')
def events():
    return render_template('programs-events.html')

@app.route('/department/<id>/international')
def international(id):
    countries = country.query.filter(db.and_(country.id == international_universities.country, international_universities.university_id == id)).all()
    univer = international_universities.query.filter(db.and_(international_universities.country == country.id,international_universities.university_id == id)).all()
    return render_template('international.html' ,countries = countries, univer=univer)
