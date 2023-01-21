# This will handle all the incoming
# and outgoing messages from external applications
# first Phase in from a Web client receiving json files from the banking system


import json
import random
import shutil
import time

import glob2

from src import db
from src.functions.Enums import TransactionType
from src.functions.genarators import TransactionUpdate, Getters
from src.functions.transactions import ChargeTransaction
from src.models.customer_model import Customer


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

    @staticmethod
    def transfer(from_acc, to_acc, amount):
        # from account, to account, amount
        remark = "Mobile Transfer"
        TransactionUpdate.transferTransactionUpdate(from_acc, to_acc, amount, remark, Getters.getSysDate().date)
        # TransactionUpdate.accChargeUpdate('TR', from_acc, Getters.getSysDate().date)
        ChargeTransaction(Getters.getSysDate().date, from_acc).charges(TransactionType.TRANSFER)
        details = {'response': 210, 'description': 'Trasnfer Done'}
        details_to_json = json.dumps(details)
        variable = random.randint(1111, 9999)
        with open("api/out/" + str(variable) + "_" + str(from_acc) + "_0210.txt", mode="w",
                  encoding="utf-8") as trnFile:
            trnFile.write(details_to_json)
        pass


class Receive:
    @staticmethod
    def inwards():
        nm = 0
        while nm < 1:
            for name in glob2.glob('api/in/*'):
                print(name)
                variable = random.randint(1111, 9999)
                with open(name, mode='r') as json_file:
                    try:
                        json_data = json.load(json_file)
                        if json_data['response'] == 200:
                            print("Transaction Successful! -- Response side")
                            try:
                                if json_data['request'] == 100:  # Balance Enquiry
                                    ac_num = json_data['account']
                                    print("this is acc number {}".format(ac_num))
                                    Enquiries.balance_enq(ac_num)
                                    print("-------Account Sent ---------")
                                elif json_data['request'] == 101:  # Transfer
                                    Process.transfer(json_data['from_account'], json_data['to_account'],
                                                     json_data['amount'])
                                    print("transfer Done")
                            except Exception as e:
                                print("no field----- {}".format(e))
                        elif json_data['response'] == 401:
                            print(json_data['description'])
                        else:
                            print("Transaction for account {} failed".format(json_data['Account']))
                    except Exception as e:
                        print("The Json file is not formatted well! {}".format(e))
                        variable = random.randint(1111, 9999)
                        shutil.move(name, 'api/rejects/' + str(variable))
                try:
                    shutil.move(name, 'api/processed/' + str(variable))
                except Exception as ee:
                    print("---------------     File Exists: {}    -----------------".format(ee))
            print("-------------------------Waiting stage here-----------------------")
            time.sleep(1)
            Receive.inwards()

    def outwards(self):
        pass


class Enquiries:
    @staticmethod
    def balance_enq(ac_number):
        # takes in account number
        acc_number = int(ac_number)
        variable = random.randint(1111, 9999)
        if db.session.query(Customer).filter_by(acc_number=acc_number).first():
            bal = db.session.query(Customer).filter_by(acc_number=acc_number).first()
            # json file with the account balance
            full_name = bal.first_name + " " + bal.last_name
            details = {'response': 210, 'name': full_name, 'account': bal.acc_number, 'balance': bal.working_bal}
            details_to_json = json.dumps(details)
            with open("api/out/" + str(variable) + "_" + str(acc_number) + "_0210.txt", mode="w",
                      encoding="utf-8") as enqFile:
                enqFile.write(details_to_json)
            return details_to_json
        else:
            # json response for no account found
            details = {'response': 401, 'description': 'account number failed'}
            details_to_json = json.dumps(details)
            with open("api/out/" + str(acc_number) + "_401.txt", mode="w", encoding="utf-8") as enqFile:
                enqFile.write(details_to_json)
            return details_to_json


class PaymentConfirmation:
    @staticmethod
    def data_validator():
        pass

    def pdfgen(self, file):
        pass
