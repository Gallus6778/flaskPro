import requests
import sys
import string

# from replace_msisdn import Replace_xml_val_class  #from running this module as a script
from HLR.replace_msisdn import Replace_msisdn_in_xml_class

#------------------------------------------------------------------------------
import xml.etree.cElementTree as ET
#------------------------------------------------------------------------------

class Soap_class:
    def __init__(self, msisdn):
        self.msisdn = msisdn

    def main(self):
        url = "http://10.124.192.138:10081/ProvisioningGateway/services/SPMLHlrSubscriber45Service"

        # Modifier le fichier Request_by_MSISDN
        file_with_msisdn = Replace_msisdn_in_xml_class(self.msisdn)
        filename = file_with_msisdn.main()
        # print(filename)

        payload = filename
        headers = {'Content-Type': 'text/xml', 'charset': 'UTF-8', 'SOAPAction': 'http://10.124.192.138:10081/ProvisioningGateway/services/SPMLHlrSubscriber45Service'}

        with open(payload) as fd:
            r = requests.post(url, data=fd.read().replace("\n",""), headers=headers)
            response = r.content
            file = open('HLR/soapok.xml', 'w')
            file.write(response.decode('utf-8'))
            file.close()
        return 'HLR/soapok.xml'

if __name__ == "__main__":
    nbr = 237669595858
    msisdn = Soap_class(str(nbr))
    msisdn.main()