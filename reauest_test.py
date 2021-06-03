import xml.etree.cElementTree as ET
from Complaints_internet.soap_module import Soap_class

msisdn = Soap_class(msisdn='237669595858')
soap_xml_filename = msisdn.main()

# tree = ET.ElementTree(file=soap_xml_filename)
# 
# root = tree.getroot()
# msisdn_info_results = {}
# for books in root.findall('.//'):
# 
    # for attr in books:
        # if (attr.tag == 'imsi'):
            # msisdn_info_results[attr.tag] = attr.text
        # if (attr.tag == 'msisdnUsedForAlertingOfSMSServiceCentre'):
            # msisdn_info_results[attr.tag] = attr.text
# 
# print(msisdn_info_results)

# ==================================================================================================

# Extraction du contenu du fichier xml
tree = ET.ElementTree(file=soap_xml_filename)
root = tree.getroot()
inc = 1
msisdn_info_results = {}
for books in root.findall('.//'):

    for attr in books:
        if (attr.tag == 'imsi'):
            msisdn_info_results[attr.tag] = attr.text
            imsi = attr.text