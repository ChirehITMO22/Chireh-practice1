from crypt import methods
from curses import flash
from flask import Flask, redirect, render_template, send_file, send_from_directory, url_for, request
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os




app = Flask(__name__)
#This is my secret key
app.config['SECRET_KEY'] = b'X\x98\xb6\xaf5;\x00\xcb\xcf\xba\xbc\xb4\x98/\xc1`'
app.config['MONGO_URI'] = 'mongodb://localhost:27018/practice1'
mongo = PyMongo(app)

#Redirect default route to the profile page route
@app.route("/")
def index():
    return render_template('index.html')


#Display Sign Up file who is in the template folder
@app.route('/SingUp', methods=['GET','POST'])
def SignUp():
    #Display sign up page 
    if request.method == "GET":
        return render_template("SignUp.html")
    else:
        #store username and password from form
        username = request.form.get('username')
        password = request.form.get('password')

        #check if username exist
        if mongo.db.users.count_documents({'username':username}) != 0:
            flash('Username already exists !!!')
            return redirect('/SingUp')
        #for a new user
        else:
            #store username end password in DB
            mongo.db.users.insert_one({
                'username': username,
                'password': password})
            
            #flash message for succes
            flash('Signed in !!!!')
            redirect('/SingIn')

#Display Sign In or login page
@app.route('/SingUp', methods=['GET','POST'])
def SignUp():
    #Display sign up page 
    if request.method == "GET":
        return render_template("SignIn.html")
    else:
         #store username and password from form
        username = request.form.get('username')
        password = request.form.get('password')

        #check username
        if mongo.db.users.find_one({'username':username}) != 0:
            flash('Connected ')
            return redirect('/secret_page')
        #for a new user
        else:
            flash('password or username incorrect ')
            return render_template("SignIn.html")


#Define the icon of the site
@app.route("/favicon.ico")
def favicon():
    return send_from_directory("static","favicon.ico","assets/icon/icon2.png")
#Customize the error page
@app.errorhandler(404)
def page_not_found(error):
    return render_template('not_found_page.html'), 404
if __name__ == "__main__":
    app.run("localhost",port=5000,debug=True)