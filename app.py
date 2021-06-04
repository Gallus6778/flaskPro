from flask import Flask, render_template, request, redirect, url_for, session, escape
# from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import InputRequired,Email,Length, DataRequired
import threading
from flask_mongoengine import MongoEngine

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
    "db": "flaskPro",
}
db = MongoEngine(app)
app.config['SECRET_KEY'] = "my secret key"

#---------------------------------------------- login form ------------------------------------------------------------
class LoginForm(FlaskForm):
    email = StringField("email")
    password = SubmitField("password")
    remember = BooleanField("remember me")
    submit = SubmitField("Submit")
#---------------------------------------------- login page's ------------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    # user = LoginForm
    # return render_template('users/register.html', user = user)
    if request.method == 'POST':
        # session['email'] = request.form['email']

        file = open('session.txt', 'w')
        file.write("email = " + request.form['email'])
        file.close()
        return redirect(url_for('index'))

    return render_template('users/register.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    user = LoginForm()
    return render_template('users/signup.html', user = user)

# @app.route('/')
@app.route('/', methods=['GET', 'POST'])
def index():
    # if request.method == 'POST':
    #     email = request.form['email']
    #     password = request.form['password']
    #     return redirect(url_for('dashboard'))
    # return render_template('users/index.html')
    try:
        file = open('sesion.txt', 'r')
        session = file.readline()
        file.close()
        if 'email' in session:
            email = session
            return 'Logged in as ' + email + '<br>' + "<b><a href = '/logout'>click here to log out</a></b>"
    except:
        return "You are not logged in <br><a href = '/login'>" + "click here to log in</a>"


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html')
#---------------------------------------------- Plaintes Internet ------------------------------------------------------------

class Msisdn_form_class(FlaskForm):
    msisdn = StringField("Enter the msisdn : ")
    submit = SubmitField("Submit")

# soap_xml_filename = 'None'S
# def soap_thread(msisdn_form):
#     msisdn = Soap_class(msisdn=msisdn_form)
#     soap_xml_filename = msisdn.main()
#     return soap_xml_filename




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

        # Recuperation des inforamtions de l'abonne dans la SGSN pour Complaints_internet
            # zmmi_command = zmmi_zmmo_zmms_class(msisdn)
            # zmmi_command.main()
        # th2 = threading.Thread(target=sgsn_info_module.main(msisdn_form))

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
