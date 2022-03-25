import os
from flask import Flask, redirect, render_template, send_file, send_from_directory, url_for, request, flash
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename




app = Flask(__name__)
#This is my secret key
app.config['SECRET_KEY'] = b'X\x98\xb6\xaf5;\x00\xcb\xcf\xba\xbc\xb4\x98/\xc1`'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/WAD'
mongo = PyMongo(app)
UPLOAD_FOLDER = 'upload'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#Redirect default route to the profile page route
@app.route("/")
def source():
    return render_template("index.html")

#Display Sign Up file who is in the template folder
@app.route('/SingUp', methods=['GET','POST'])
def SignUp():
    #Display sign up page 
    if request.method == "GET":
        return render_template("SingUp.html")
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
            return redirect('/SingIn')
#Display Sign In or login page
@app.route('/SingIn', methods=['GET','POST'])
def SignIn():
    #Display sign up page 
    if request.method == "GET":
        return render_template("SingIn.html")
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

@app.route('/secret_page')
def secret_page():
    return render_template("secret_page.html")
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/upload',methods=['GET','POST'])
def upload():
    if request.method == "GET":
        return render_template("upload.html")
    else :
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',filename=filename))
@app.route('/upload/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)
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