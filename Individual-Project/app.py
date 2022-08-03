from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {
  "apiKey": "AIzaSyCsdOBIIehLAbQKVJUMJhJVAW26Wcm_6C0",
  "authDomain": "y2-1st-project.firebaseapp.com",
  "projectId": "y2-1st-project",
  "storageBucket": "y2-1st-project.appspot.com",
  "messagingSenderId": "903066802788",
  "appId": "1:903066802788:web:00f5c5078acfe865e49d71",
  "measurementId": "G-KSKF1GJJT6",
  "databaseURL": "https://y2-1st-project-default-rtdb.europe-west1.firebasedatabase.app"}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database() 


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

#Code goes below here
@app.route('/', methods=['GET', 'POST'])
def signin():
	#return redirect(url_for("signin"))
	#return render_template("signin.html")
	error = ""
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		try:
			login_session['user'] = auth.sign_in_with_email_and_password(email, password)
			return redirect(url_for('home'))
		except:
			error = "Authentication failed"
			return redirect(url_for("signin"))
	else:
		return render_template("signin.html")
	 


@app.route('/signup', methods=['GET', 'POST'])
def signup():
	error = ""
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		try:
			login_session['user'] = auth.create_user_with_email_and_password(email, password)
			user = {
			"email": request.form['email'], "password" : request.form['password'], "full_name" : request.form['fname'],
			"user_name" : request.form['uname'], "bio" : request.form['bio']
			}
			db.child("users").child(login_session['user']["localId"]).set(user)
			return redirect(url_for('signin'))
		except:
			error = "Authentication failed"
			return redirect(url_for("signup"))
	return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
	if request.method == 'POST':
		tweet = {
		"title" : request.form['title'], "bio" : request.form['bio'], "uid" : login_session['user']["localId"] 
		}
		db.child("articles").push(tweet)
	return render_template("add_tweet.html")

@app.route('/tweets', methods=['GET', 'POST'])
def all_tweet():
	tweets = db.child("articles").get().val()
	users = db.child("users").get().val()
	return render_template("tweets.html", tweets= tweets, users=users)

@app.route('/home', methods=['GET', 'POST'])
def home():
	error = ""
	return render_template("home.html")


#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)