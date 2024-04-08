#EMAIL VERIFICATION IMPLEMENTATION NOT DONE AS IT WILL REQ. TO SHARE PASSWORD

'''
app.config['MAIL_SERVER'] = 'sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = 'email@email.com'
app.config['MAIL_PASSWORD'] = '1234'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)


@app.route("/")
def index():
    msg = Message(subject='MoneyPipes Verification', sender='verify@moneypipes.com', recipients=[user_email])
    msg.body = "Your MoneyPipes verification code is {random.code}"
    mail.send(msg)
    return "Sent"
'''
your_country_name = "India"

from flask import Flask, render_template,request,redirect,session,jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
import json
import ipinfo
import sys
app = Flask(__name__)
app.secret_key = 'safekeyforgithub'  # Change this to a secure secret key

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/moneypipes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking
db = SQLAlchemy(app)

# Define the User model representing your MySQL table
class User(db.Model):
    fullname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), primary_key=True)
    password = db.Column(db.String(100), nullable=False)
class Likes(db.Model):
    email = db.Column(db.String(100), primary_key=True)
    postid = db.Column(db.Integer)
class Dislikes(db.Model):
    email = db.Column(db.String(100), primary_key=True)
    postid = db.Column(db.Integer)
class Pipes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    title = db.Column(db.String(100))
    content = db.Column(db.String(10000))
    fullname = db.Column(db.String(100))
    category = db.Column(db.String(1000))
    salary = db.Column(db.String(1000))
    country = db.Column(db.String(1000))
    likes =  db.Column(db.Integer)
    dislikes =  db.Column(db.Integer)
    fun = db.Column(db.String(100))

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    content = db.Column(db.String(10000))
    fullname = db.Column(db.String(100))
    type = db.Column(db.Integer,nullable = True)
    postid = db.Column(db.Integer)

def get_currency_symbol(country_name):
    # Make a GET request to REST Countries API
    response = requests.get(f"https://restcountries.com/v3.1/name/{country_name}")
    response_data = json.loads(response.text)
    for country in response_data:
        if "name" in country and "common" in country["name"] and country["name"]["common"] == country_name:
            currencies = country.get("currencies", {})
            if currencies:
                for currency_code, currency_info in currencies.items():
                    currency_symbol = currency_info.get("symbol")
                    if currency_symbol:
                        return currency_symbol
            else:
                return "Currency information not available"
    return "Country not found"

    
def login_check():
    if 'email' in session:
        if 'password' in session:
            user = User.query.filter_by(email=session['email'], password=session['password']).first()
            if user:
                return True
    return False

@app.context_processor
def inject_global_variables():
    global_variable = login_check()
    email = None
    if global_variable:
        email = session['email']
    access_token = "abe046fd96f568"
    handler = ipinfo.getHandler(access_token)
    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
    details = handler.getDetails(ip_address)
    if not 'country' in session:
        country_name =  your_country_name #details.Country Only works on hosted websites as public ip is required.
        session["country"] = country_name
    pipes = Pipes.query.filter_by(country=session["country"]).all()

    currency = get_currency_symbol(session["country"])
    return dict(global_variable=global_variable,pipes=pipes,email=email,city=session["country"],currency=currency)
@app.route("/search",methods=['POST','GET'])
def search():
    if request.method == "POST":
        cgory = request.form["jobs"]
        text = request.form["search"]
    else:
        return redirect ('/')
    if cgory == "None":
         pipes = Pipes.query.filter_by(country=session["country"]).filter(or_(Pipes.title.ilike(f"%{text}%"), Pipes.content.ilike(f"%{text}%"))).all()
    elif text == "None":
         pipes = Pipes.query.filter_by(country=session["country"],category = cgory).all()
    else:
         pipes = Pipes.query.filter_by(country=session["country"],category = cgory).filter(or_(Pipes.title.ilike(f"%{text}%"), Pipes.content.ilike(f"%{text}%"))).all()
    return render_template("index.html",pipes = pipes)
@app.route("/")
def index():
    
    return render_template("index.html")
@app.route("/post_data", methods=['POST','GET'])
def postdata():
    data = request.json
    pipe = Pipes.query.filter_by(id = data["postid"]).first()
    
    if pipe:
        if data["pressed"] == "like":
            
            check = Likes.query.filter_by(email=data["email"], postid=data["postid"]).first()
            if check:
                pipe.likes -=1
                db.session.delete(check)
            else:
                pipe.likes +=1
                new_q = Likes(email=data["email"],postid=data["postid"])

                # Add the new user to the database
                db.session.add(new_q)
             
        else:
            check = Dislikes.query.filter_by(email=data["email"], postid=data["postid"]).first()
            if check:
                pipe.dislikes -=1
                db.session.delete(check)
            else:
                pipe.dislikes +=1

                new_q = Dislikes(email=data["email"],postid=data["postid"])

                # Add the new user to the database
                db.session.add(new_q)    
        db.session.commit()
    return "GOOD"
@app.route("/post/<id>")
def post(id):
    epipe = Pipes.query.filter_by(id = id).first()
    ecomments = Comments.query.filter_by(postid = id,type=None).all()
    return render_template("post.html",epipe=epipe,ecomments=ecomments)

@app.route("/about")
def about():
    
    return render_template('about.html')
@app.route("/register")
def register():
    return render_template("register.html")
@app.route("/login", methods=['POST','GET'])
def login():
    if not login_check():
        message = None
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            user = User.query.filter_by(email=email, password=password).first()
            if user:
                session['email'] = user.email
                session['password'] = user.password
                session['fullname'] = user.fullname
                session.permanent = True 
                return redirect('/')
            else:
                message = "No account found / Incorrect password"
        return render_template("login.html",error=message)
   
    return redirect('/')
@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')
@app.route("/dashboard")
def dashboard():
    if login_check():
        mypipes = Pipes.query.filter_by(email=session['email']).first()
        return render_template("dashboard.html",mypipes=mypipes)
    return redirect('/login')
@app.route("/edit/<pipeid>", methods=['POST','GET'])
def edit(pipeid):
    
    if login_check():
        
        epipe = Pipes.query.filter_by(id = pipeid).first()
        if epipe.email != session['email']:
            return redirect ('/')
        if request.method == 'POST':

            title = request.form['title']
            content = request.form['content']
            category = request.form['jobs']
            salary = request.form['salary']
            country = request.form['country']

            epipe.title = title
            epipe.content = content
            epipe.category = category
            epipe.salary = salary
            epipe.country = country

            db.session.commit()
            return redirect('/')
        return render_template("edit.html",epipe=epipe)
    return redirect('/login')
@app.route('/upcountry', methods=['POST'])
def updatecountry():
    if request.method == "POST":
        country = request.form['country']
        session["country"] = country
        return redirect ('/')
@app.route('/add-user', methods=['POST'])
def add_user():
    
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        if user:
            return redirect('/register#ACCOUNT EXISTS WITH THAT EMAIL')
        # Create a new User object
        new_user = User(fullname=fullname, email=email, password=password)

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()
        session['email'] = email
        session['password'] = password
        session['fullname'] = fullname
        session.permanent = True 
        return redirect ('/dashboard')
@app.route('/add-comment', methods=['POST','GET'])
def add_comment():
    if login_check():
        if request.method == 'POST':
            
            data = request.json
            email = session['email']
            content = data['content']
            fullname = session['fullname']
            postid = data['postid']
            type = data['type']
            
            comment = Comments(fullname=fullname,postid=postid,type=type,content=content,email=email)
            db.session.add(comment)
            db.session.commit()
            return "LOGGED"
    else:
        return redirect ('/login')
@app.route('/get-replies', methods=['POST','GET'])
def get_replies():
        if request.method == 'POST':
            
            data = request.json
            comments  = Comments.query.filter_by(type = data["commentid"]).all()
            comments_list = []
            for comment in comments:
                comment_dict = {
                    "id": comment.id,
                    "content": comment.content,
                    "fullname":comment.fullname
                    # Add other attributes as needed
                }
                comments_list.append(comment_dict)
            return jsonify(comments_list)
@app.route('/add-pipe', methods=['POST','GET'])
def add_pipe():
    if login_check():
        if request.method == 'POST':
            email = session['email']
            password = session['password']
            user = User.query.filter_by(email=email,password=password).first()
            
            fullname = user.fullname

            title = request.form['title']
            content = request.form['content']
            category = request.form['jobs']
            salary = request.form['salary']
            country = request.form['country']
            fun = request.form['funrating']

            likes = 0
            dislikes = 0
            pipe = Pipes.query.filter_by(email=email).first()
            if pipe:
                return redirect('/edit/' + str(pipe.id))
            
            # Create a new User object
            new_pipe = Pipes(fullname=fullname,fun=fun,likes=likes,dislikes=dislikes,country=country,email=email, title=title,content=content,category=category,salary=salary)

            # Add the new user to the database
            db.session.add(new_pipe)
            db.session.commit()
    return redirect('/')
     
if __name__ == "__main__":
    app.run(host='0.0.0.0')

