from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# Importation des modules pour resolutions des plaintes d'internet
# import xml.etree.cElementTree as ET

# importation du module qui fera l'extraction du xml depuis la HLR pour les Complaints_internet
from Complaints_internet.soap_module import Soap_class

# importation du module qui fera le tri de donnees du xml pour l'ajouter dans le dataset
import Complaints_internet.dataset_enrichment as read_xml

# importation du module qui fera l'extraction du log depuis la SGSN pour les Complaints_internet
# import Complaints_internet.sgsn_info_module
from Complaints_internet import sgsn_info_module

app = Flask(__name__)
app.config['SECRET_KEY'] = "my secret key"

#---------------------------------------------- Plaintes Internet ------------------------------------------------------------

class Msisdn_form_class(FlaskForm):
    msisdn = StringField("Enter the msisdn : ")
    submit = SubmitField("Submit")

@app.route('/internet_complaints', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def internet_complaints():
    msisdn = None
    msisdn_parameters = None
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

    # Parametre du xml issu de la Complaints_internet
    # imsi = None
    # encKey = None
    # algoId = None
    # kdbId = None
    # acsub = None
    # imsiActive = None
    # accTypeGSM = None
    # accTypeGERAN = None
    # accTypeUTRAN = None
    # odboc = None
    # odbic = None
    # odbr = None
    # odboprc = None
    # odbssm = None
    # odbgprs = None
    # odbsci = None
    # isActiveIMSI = None
    # msisdn = None
    # actIMSIGprs = None
    # obGprs = None
    # qosProfile = None
    # refPdpContextName = None
    # imeisv = None
    # ldapResponse = None

    # Validation du formulaire
    if msisdnForm.validate_on_submit():
        msisdn = msisdnForm.msisdn.data
        msisdnForm.msisdn.data = ''

        # Recuperation des inforamtions de l'abonne dans la HLR pour Complaints_internet
        msisdn = Soap_class(msisdn=msisdn)
        soap_xml_filename = msisdn.main()

        #
        sgsn_info_module.main(msisdn)

        # Enrichissement du dataset avec des inforamtions de l'abonne dans la Complaints_internet (ce dernier modifiera le contenu du dictionnaire )
        try:
            read_xml.put_data_in_dataset(soap_xml_filename, msisdn_info_results)
        except :
            messageErreur = 'Error -> file not closed:-) You must first closed the "dataset_internet.xlsx" file !'
            return messageErreur

        # Recuperation des inforamtions de l'abonne dans la SGSN pour Complaints_internet
            # zmmi_command = zmmi_zmmo_zmms_class(msisdn)
            # zmmi_command.main()
        # sgsn_info_module.main(msisdn)

    return render_template("complaints_internet/index.html",
                           # msisdn = msisdn_info_results['imsi'],
                           # imsi = msisdn_info_results,
                           msisdn_info_results = msisdn_info_results,
                           msisdn = msisdn,
                           # odboc= odboc,
                           # odbic = odbic,
                           # odbr = odbr,
                           # odboprc = odboprc,
                           msisdnForm = msisdnForm)

#---------------------------------------------- Plaintes d'appels ------------------------------------------------------------
@app.route('/calls_complaints')
def calls_complaints():
    return 'plaintes appels disponible tres bientot'

#---------------------------------------------- Plaintes de SMS ------------------------------------------------------------
@app.route('/sms_complaints')
def sms_complaints():
    return 'plaintes sms disponible tres bientot'

# Autres
@app.route('/others')
def others():
    return 'Autres traitements bientot disponible'

# CREATE A FORM CLASS
# class NameForm(FlaskForm):
#     name = StringField("What your name", validators=[DataRequired()])
#     submit = SubmitField("Submit")

# CREATE Name page
# @app.route('/name', methods=['GET', 'POST'])
# def name():
#     name = None
#     form = NameForm()
#     validate form
    # if form.validate_on_submit():
    #     name = form.name.data
    #     form.name.data = ''
    # return render_template("complaints_internet/index.html",
    #                        name = name,
    #                        form = form)

# if __name__ == '__main__':
#     app.config.update(ENV="development", DEBUG=True)
#     app.run(host='0.0.0.0', port= 8000)