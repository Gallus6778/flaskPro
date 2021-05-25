# import zmmi_zmmo_zmms_module
# from Complaints_internet.zmmi_zmmo_zmms_module import zmmi_zmmo_zmms_class

from Complaints_internet.telnet_connexion import zmmi_zmmo_zmms_class
from Complaints_internet import txt_reader as mod

# import Complaints_internet.txt_reader as mod

# print('Execution complete')
# path_to_file = 'storage_txt_and_xlsx/10.124.206.68.txt'
# zmmi_zmmo_zmms_module = zmmi_zmmo_zmms_class('237669595858')
# zmmi_zmmo_zmms_module.main()
#
# txt_reader_obj = mod.txt_reader_class(path_to_file)
# txt_reader_obj.main()

def main(msisdn):

    print('Execution complete')
    path_to_file = 'Complaints_internet/storage_txt_and_xlsx/10.124.206.68.txt' #Complaints_internet/storage_txt_and_xlsx/
    zmmi_zmmo_zmms_module = zmmi_zmmo_zmms_class(msisdn)
    zmmi_zmmo_zmms_module.main()

    txt_reader_obj = mod.txt_reader_class(path_to_file)
    txt_reader_obj.main()
    # print(zmmi_zmmo_zmms_module.main())
if __name__ == "__main__":
    msisdn = '237669595858'
    main(msisdn)
    # zmmi_zmmo_zmms_module.main()
