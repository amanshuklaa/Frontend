from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import base64
import io
from PIL import Image
from io import BytesIO
import re
app = Flask(__name__)


ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Amanshukla72@127.0.0.1/Frontend'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://rlnceahsllombz:ed7b83438d42b151f94294b09b7376baea422f74f267ca492b12daef6a270e39@ec2-107-20-230-70.compute-1.amazonaws.com:5432/d88b9uokp3ov9f'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Feedback(db.Model):
    __tablename__ = 'cost_information'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    lastname = db.Column(db.String(200))
    emailaddress = db.Column(db.String(200))
    gender = db.Column(db.String(200))
    city = db.Column(db.String(200))
    country = db.Column(db.String(200))
    password = db.Column(db.String(200))
   

    def __init__(self, name, lastname, emailaddress,gender,city,country,password):
        self.name = name
        self.lastname = lastname
        self.emailaddress = emailaddress
        self.gender = gender
        self.city = city
        self.country = country
        self.password = password
        

class Feedbacks(db.Model):
    __tablename__ = 'product_information'
    id = db.Column(db.Integer, primary_key=True)
    Productname = db.Column(db.String(200), unique=True)
    image = db.Column(db.String(1000000))
    description = db.Column(db.String(2000))
    
    


    def __init__(self, Productname, image, description):
        self.Productname = Productname
        self.image = image
        self.description = description
        
       

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')







@app.route('/submit', methods=['POST'])
def submit():

    if request.method == 'POST':
            email = request.form['email']
            password = request.form['pwd']  
            print(email,password)
        # name = request.form['name']
        # lastname = request.form['lastname']
        # emailaddress = request.form['emailaddress']
        # male = request.form['male']
        # female = request.form['female']
        # city = request.form['city']
        # country = request.form['country']
        # password = request.form['password']
        #print(name, lastname, emailaddress, male,female ,city,country,password)
        # if name == '' or emailaddress == '' or password =='':
        #     return render_template('index.html', message='Please enter required fields')
        # if db.session.query(Feedback).filter(Feedback.emailaddress == emailaddress).count() == 0:
        #     data = Feedback(customer, dealer, rating, comments)
        #     db.session.add(data)
        #     db.session.commit()
        #     return render_template('success.html')
        # return render_template('index.html', message='You have already submitted feedback')
    return 'post request'
   


@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        lastname = request.form['lastname']
        emailaddress = request.form['emailaddress']
        gender = request.form['gender']
        city = request.form['city']
        country = request.form['country']
        password = request.form['password']
        # print(name, lastname, emailaddress,gender,city,country,password)
        if name == '' or emailaddress == '' or password =='' or lastname == '' or gender == '' or city == '' or country == '':
            return render_template('signup.html', message='Please enter required fields')
        if db.session.query(Feedback).filter(Feedback.emailaddress == emailaddress).count() == 0:
            data = Feedback(name, lastname, emailaddress, gender,city,country,password)
            db.session.add(data)
            db.session.commit()
        return render_template('index.html')
    return render_template('index.html', message='You have already register Please login')
 
@app.route('/login', methods=['POST'])
def login():
    useremail = request.form['email']
    userpas = request.form['pwd']

    # print(useremail,userpas)
    # return render_template('login.html')
    user = db.session.query(Feedback).filter_by(emailaddress= useremail).first()
    if user:
        if user.password == userpas:
            return render_template('login.html')
        # print(user)

@app.route('/addproduct',methods= ['POST'])
def addProduc():
    
    productname =  request.form['productname']
    # print("Posted file: {}".format(request.files['uploadimage']))
    files = request.files['uploadimage'].read()
    #print(files)
    image_string = base64.b64encode(files)
    # image_string = io.BytesIO(base64.b64encode(files))
    # print("imagestring",len(image_string))
    description=  request.form['discription']
    #print(productname,image_string,description)
   
    
    data = Feedbacks(productname, image_string, description)
    db.session.add(data)
    db.session.commit()
    productnamedb = db.session.query(Feedbacks.Productname)
    productimage = db.session.query(Feedbacks.image)
    productdescription = db.session.query(Feedbacks.description)
   
    
        

    return render_template('login.html', prodname = productnamedb,img = productimage ,desc = productdescription)

if __name__ == '__main__':
    app.run()
    