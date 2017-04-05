# This will handle all the incoming
# and outgoing messages from external applications
# first Phase in from a Web client receiving json files from the banking system

import json
from functions.genarators import *


class Process:
    @staticmethod
    def received():
        # check if the INWARDS folder is empty
        # if its empty
        #   check again after 1 second
        # if Not Empty
        #   moves file to PROCESSING folder
        #   reads the contents of the file
        #   formats the contents for processing
        #   process the contents
        #   Generates a Response file to OUTWARDS folder        #
        #   moves the file to PROCESSED folder
        #   checks the
        stringOfJsonData = '{"name": "Zophie", "isCat": true, "miceCaught": 0,"felineIQ": null}'
        jsonDataAsPythonObject = json.loads(stringOfJsonData)
        print(jsonDataAsPythonObject)
        return jsonDataAsPythonObject

    def sent(self):
        pass


class Receive:
    def inwards(self):
        pass

    def outwards(self):
        pass


class Enquiries:
    @staticmethod
    def balance_enq(acc_number):
        # takes in account number
        acc_number = int(acc_number)

        if session.query(Customer).filter_by(acc_number=acc_number).first():
            bal = session.query(Customer).filter_by(acc_number=acc_number).first()
            # json file with the account balance
            full_name = bal.first_name + " " + bal.last_name
            details = {'Response': 200, 'Name': full_name, 'Account': bal.acc_number, 'Balance': bal.working_bal}
            details_to_json = json.dumps(details)
            with open("api/enquiry/" + str(acc_number) + "_200.txt", mode="w", encoding="utf-8") as enqFile:
                enqFile.write(details_to_json)
            return details_to_json
        else:
            # json response for no account found
            details = {'Response': 401, 'Description': 'account number failed'}
            details_to_json = json.dumps(details)
            with open("api/enquiry/" + str(acc_number) + "_401.txt", mode="w", encoding="utf-8") as enqFile:
                enqFile.write(details_to_json)
            return details_to_json
