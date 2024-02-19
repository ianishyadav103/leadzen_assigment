import secrets
from flask import Flask, render_template, request, redirect, jsonify, flash,url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager, login_user, current_user,login_required ,logout_user
from datetime import datetime


from flask_wtf import FlaskForm, CSRFProtect
from wtforms import (StringField,EmailField,PasswordField)
from wtforms.validators import InputRequired, Length


app = Flask(__name__) 
app.config['SECRET_KEY'] =  secrets.token_hex()

csrf = CSRFProtect(app)

app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
db = SQLAlchemy(app) 

login_manager = LoginManager(app)
login_manager.login_view = 'loginx'

@login_manager.user_loader 
def my_load_userx(user_id):
    return db.session.get(User,int(user_id))


####models#####
class User(UserMixin,db.Model): 
    id = db.Column(db.Integer, primary_key=True) 
    email = db.Column(db.String(100), unique=True,nullable=False)
    password = db.Column(db.String(100),nullable=False) 
    name = db.Column(db.String(1000),nullable=False)
    to_do = db.relationship('Todo', backref='user') 

class Todo(db.Model): 
    sno = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(150),nullable = False)
    desc = db.Column(db.String(600),nullable = False)
    status = db.Column(db.Boolean,nullable = False,default= False)
    date_created = db.Column(db.String(30),default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    user_idx = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    
'''
flask shell  
with app.app_context():
    db.create_all() #creates tables

'''

##For demo of flask forms
class MySignupForm(FlaskForm):
    email = EmailField('Email address',validators=[InputRequired(), Length(min=10, max=100)])
    name    = StringField('Name', validators=[InputRequired(), Length(max=100)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=10, max=100)])


####VIEWS###
@app.route("/")
@login_required
def home():
    temp_todo = current_user.to_do 
    return render_template("index.html",all_todo = temp_todo,hii="No Records",name=current_user.name) 


@app.route("/login")
def loginx():
    return render_template("login.html")


@app.route("/signupx", methods=['POST','GET'])
def signupx_p():
    formy = MySignupForm() 
    if(request.method == 'POST' and formy.validate_on_submit()):
        temp_user = User(email=request.form['email'],name=request.form['name'],password = generate_password_hash(request.form['password'], method='sha256'))
        db.session.add(temp_user)
        try:
            db.session.commit()
        except IntegrityError:
            flash('Email address already exists')
            db.session.rollback()
            return render_template("signup.html",formx = formy)
        return redirect('/login')
    return render_template("signup.html",formx = formy) 


@app.route("/login_p", methods=['POST'])
def loginx_p():
    temp_user = User.query.filter_by(email=request.form['email']).first()
    if not temp_user or not check_password_hash(temp_user.password, request.form['password']):
        flash('Invalid Credentials','error')
        return redirect('/login')
    else:
        login_user(temp_user)
        return redirect(url_for('home'))
    

@app.route("/logoutx")
def logoutx():
    logout_user()
    return redirect('/login')


@app.route("/addnotes")
@login_required
def addnotes():
    return render_template("addnotes.html",name=current_user.name)
 

@app.route("/savenotes", methods=['POST','GET'])
@login_required
def savenotes():
    if(request.method == 'POST'):
        temp_todo = Todo(title=request.form['title'],desc=request.form['desc'],user_idx = current_user.id)
        db.session.add(temp_todo)
        db.session.commit()
        flash('Notes Added!', 'mysuccess') 
    return redirect('/')


@app.route('/task/<string:op>/<int:idx>/') 
@login_required
def edit_or_delete(op,idx):
    temp_todo = Todo.query.filter_by(sno=idx,user_idx=current_user.id).first() 
    if(temp_todo):
        if(op[0]=='e'):
            temp_todo.status= int(op[1])
            db.session.add(temp_todo)
            db.session.commit()
            return jsonify({'data': "e"})
        elif(op=='d'):
            db.session.delete(temp_todo)
            db.session.commit()
            return jsonify({'data': "d"})
    
    return jsonify({'data': "Some error Occured"}) 


if __name__ == "__main__": 
    app.run(debug=True,port=8000)   

