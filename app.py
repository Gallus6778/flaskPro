# import flask
import uuid
from flask import Flask, render_template, request, redirect, url_for, session, escape, g
# from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import InputRequired,Email,Length, DataRequired
import threading
from flask_mongoengine import MongoEngine
from flask_pymongo import PyMongo

from flask_login import LoginManager, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash


# Importation des modules pour resolutions des plaintes d'internet
# import xml.etree.cElementTree as ET

# importation du module qui fera l'extraction du xml depuis la HLR pour les Complaints_internet
from Complaints_internet.soap_module import Soap_class
# importation du module qui fera le tri de donnees du xml pour l'ajouter dans le dataset
import Complaints_internet.dataset_enrichment as read_xml
# importation du module qui fera l'extraction du log depuis la SGSN pour les Complaints_internet
from Complaints_internet import sgsn_info_module
# importation du module qui identifiera et corrigera depuis la SGSN et la HLR les Complaints_internet
from Complaints_internet.correct_complaints_module import Info_hlr

app = Flask(__name__)
# Bootstrap(app)

app.config['MONGODB_SETTINGS'] = {
    "db": "robic_db",
}
db = MongoEngine(app)
app.config['SECRET_KEY'] = "my secret key"
# app.config['MONGO_DBNAME'] = 'robic_db'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/robic_db'
# mongodb_client = PyMongo(app, uri="mongodb://localhost:27017/robic_db")
app.config['USE_SESSION_FOR_NEXT']=True
# db = mongodb_client.db


app.config["MONGO_URI"] = "mongodb://localhost:27017/robic_db"
mongo = PyMongo(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view="/"
login_manager.login_message = "You may to be identified"


@app.before_request
def before_request():
    if 'user_id' in session:
        users=mongo.db.users.find()
        for user in users:
            if user['id'] == session['user_id']:
                User = user
        g.User = User
class User:
    def __init__(self, username):
        self.username = username

    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_anonimous():
        return False

    def get_id(self):
        return self.username

    @staticmethod
    def check_password(password_hash, password):
        return check_password_hash(password_hash, password)

    @login_manager.user_loader
    def load_user(username):
        user = mongo.db.users.find_one({"username": username})
        if not user:
            return None
        return User(username=user['username'])

# @app.route('/')
# @app.route('/', methods=['GET'])
# def index():

    # db.users.insert_one({'name': "Gallus", 'email': "noahgallusfgi@gmail.com"})

    # try:
    #     file = open('sesion.txt', 'r')
    #     session = file.readline()
    #     file.close()
    #     email = ''
    #     if 'email' in session:
    #         email = session
    #     return 'Logged in as ' + email + '<br>' + "<b><a href = '/logout'>click here to log out</a></b>" + flask.jsonify([todo for todo in todos])
    # except:
    # return render_template('index.html')

#---------------------------------------------- login form ------------------------------------------------------------
class LoginForm(FlaskForm):
    email = StringField("email")
    password = SubmitField("password")
    remember = BooleanField("remember me")
    submit = SubmitField("Submit")

#---------------------------------------------- login page's ------------------------------------------------------------
@app.route('/', methods=['GET', 'POST'])
def home_page():
    session['next']=request.args.get('next')
    return render_template('users/login.html')

@app.route('/login', methods=['POST'])
def login():
    session.pop('user_id', None)
    user = mongo.db.users.find_one({"username": request.form["username"]})
    if user and User.check_password(user['password'], request.form['password']):
        session['user_id'] = user['id']
        user_obj = User(username=user['username'])
        login_user(user_obj)
        return redirect('/dashboard')
    else:
        error = 'login or password is incorrect !'
        return render_template('users/login.html', error=error)

@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if(request.method == 'POST'):
        username=request.form['username']
        # name=request.form['name']
        password=request.form['password']

        test=uuid.uuid4().hex

        user={"id":test, "username":username, "password":generate_password_hash(password)}# "login":login,
        mongo.db.users.insert_one(user)
        return redirect("/dashboard")
    return render_template('users/sign_in.html')

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')
#---------------------------------------------- Plaintes Internet ------------------------------------------------------------

class Msisdn_form_class(FlaskForm):
    msisdn = StringField("Enter the msisdn : ")
    submit = SubmitField("Submit")

@app.route('/internet_complaints', methods=['GET', 'POST'])
# @app.route('/', methods=['GET', 'POST'])
def internet_complaints():

    msisdn = None
    msisdn_parameters = None
    info_parameter = None
    msisdnForm = Msisdn_form_class()
    msisdn_info_results = {'imsi' : 'None',
                           'encKey' : 'None',
                           'algoId' : 'None',
                           'kdbId' : 'None',
                           'acsub' : 'None',
                           'imsiActive' : 'None',
                           'accTypeGSM' : 'None',
                           'accTypeGERAN' : 'None',
                           'accTypeUTRAN' : 'None',
                           'odboc' : 'None',
                           'odbic' : 'None',
                           'odbr' : 'None',
                           'odboprc' : 'None',
                           'odbssm' : 'None',
                           'odbgprs' : 'None',
                           'odbsci' : 'None',
                           'isActiveIMSI' : 'None',
                           'msisdn' : 'None',
                           'actIMSIGprs' : 'None',
                           'obGprs' : 'None',
                           'qosProfile' : 'None',
                           'refPdpContextName' : 'None',
                           'imeisv' : 'None',
                           'ldapResponse' : 'None'}

    # Validation du formulaire
    if msisdnForm.validate_on_submit():
        msisdn_form = msisdnForm.msisdn.data
        msisdnForm.msisdn.data = ''

        # Recuperation des inforamtions de l'abonne dans la HLR pour Complaints_internet
        # Thread 1
        # th1 = threading.Thread(target=soap_thread(msisdn_form))
        msisdn = Soap_class(msisdn=msisdn_form)
        soap_xml_filename = msisdn.main()

        #
        # sgsn_info_module.main(msisdn_form)

        # Enrichissement du dataset avec des inforamtions de l'abonne dans la Complaints_internet (ce dernier modifiera le contenu du dictionnaire )
        try:
            # read_xml.put_data_in_dataset(soap_thread(msisdn_form), msisdn_info_results)
            read_xml.put_data_in_dataset(soap_xml_filename, msisdn_info_results)
        except :
            messageErreur = 'Error -> file not closed:-) You must first closed the "dataset_internet.xlsx" file !'
            return messageErreur

        # ============================= Correction du probleme ===========================
        subscriber_info = Info_hlr()
        info_parameter = subscriber_info.main()

    return render_template("complaints_internet/index.html",
                           msisdn_info_results = msisdn_info_results,
                           msisdn = msisdn,
                           msisdn1 = info_parameter,
                           msisdnForm = msisdnForm)

#---------------------------------------------- Plaintes d'appels ------------------------------------------------------------
@app.route('/calls_complaints')
def calls_complaints():
    return 'plaintes appels disponible tres bientot'

#---------------------------------------------- Plaintes de SMS ------------------------------------------------------------
@app.route('/sms_complaints')
def sms_complaints():
    return 'plaintes sms disponible tres bientot'
