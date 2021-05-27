#!/usr/bin/python

from datetime import datetime
import asyncio, telnetlib3
import os
import time

class zmmi_zmmo_zmms_class:

    """ Module pour l'extraction des informations de la SGSN """

    def __init__(self, msisdn):

        self.server_ip = "10.124.206.68"
        self.user = "CHATBO"
        self.password = "1234567890"
        self.MSISDN = msisdn
        self.ZMMI = "ZMMI:MSISDN="
        self.ZMMO = "ZMMO:MSISDN="
        self.ZMMS = "ZMMS:MSISDN="
        # self.file_name = os.path.join('/', self.server_ip+ '.txt') #'-' + str(datetime.now()).replace(':', '-') +
        self.file_name = "Complaints_internet/storage_txt_and_xlsx/10.124.206.68.txt"

        f1 = open(self.file_name, "w")
        f1.close()

    # def msisdn_to_send(msisdn = "237669595858:;"):
    def msisdn_to_send(self, msisdn):
        return msisdn

    @asyncio.coroutine
    def shell(self, reader, writer):
        # MSISDN = msisdn_to_send()
        inc = 1
        while True:
            outp = yield from reader.read(65536)
            if outp == "":
                # print('enter')
                # End of File
                break
            elif 'ENTER USERNAME' in outp:
                writer.write(self.user)
                writer.write('\n\r' + self.password + '\n\r'
                             + self.ZMMI + self.MSISDN + ':;\n\r'
                             + self.ZMMO + self.MSISDN + ':;\n\r'
                             # + self.ZMMS + self.MSISDN + ':;\n\r'
                             )
            f1 = open(self.file_name, "a")  # server_ip + "_" + str(datetime.now()) +
            f1.write(outp)
            f1.close()
            if "COMMAND" in outp:
                # print(inc)
                inc += 1
                # print(outp)
                if inc == 3:
                    # print('End exe')
                    break
                else:
                    continue
            #     inc += 1
            # print(outp)
            # print(inc)
            # inc += 1

        # time.sleep(2)

    def main(self):
        loop = None
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError as ex:
            if "There is no current event loop in thread" in str(ex):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
        # loop = asyncio.get_event_loop()

        coro = telnetlib3.open_connection(self.server_ip, 23, shell=self.shell)
        reader, writer = loop.run_until_complete(coro)
        # print('debut-fin')

        loop.run_until_complete(writer.protocol.waiter_closed)
        file_name = self.file_name
        # return file_name

if __name__ == '__main__':
    zmmi_zmmo_zmms = zmmi_zmmo_zmms_class('237663744490')
    zmmi_zmmo_zmms.main()
    print("fin")