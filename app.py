from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# Importation des modules pour resolutions des plaintes d'internet
import xml.etree.cElementTree as ET
from HLR.soap_module import Soap_class

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
    msisdnForm = Msisdn_form_class()
    msisdn_info_results = {}
    imsi = None
    odboc = None
    odbic = None
    odbr = None
    odboprc = None

    # Validation du formulaire
    if msisdnForm.validate_on_submit():
        msisdn = msisdnForm.msisdn.data
        msisdnForm.msisdn.data = ''

        # Recuperation des inforamtions de l'abonne dans la HLR
        msisdn = Soap_class(msisdn=msisdn)
        soap_xml_filename = msisdn.main()

        # Extraction du contenu du fichier xml
        tree = ET.ElementTree(file=soap_xml_filename)
        root = tree.getroot()
        for books in root.findall('.//'):

            for attr in books:
                if (attr.tag == 'imsi'):
                    msisdn_info_results[attr.tag] = attr.text
                    imsi = attr.text

                if (attr.tag == 'msisdnUsedForAlertingOfSMSServiceCentre'):
                    msisdn_info_results[attr.tag] = attr.text
                    msisdn = attr.text

                if (attr.tag == 'odboc'):
                    odboc = attr.text

                if (attr.tag == 'odbic'):
                    odbic = attr.text

                if (attr.tag == 'odbr'):
                    odbr = attr.text

                if (attr.tag == 'odboprc'):
                    odboprc = attr.text
        # print(msisdn_info_results)

    return render_template("complaints_internet/index.html",
                           # msisdn = msisdn_info_results,
                           imsi = imsi,
                           msisdn = msisdn,
                           odboc= odboc,
                           odbic = odbic,
                           odbr = odbr,
                           odboprc = odboprc,
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
    # app.run(host='0.0.0.0', port= 8000)