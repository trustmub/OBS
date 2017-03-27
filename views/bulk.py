from flask import Blueprint, render_template, redirect, request, url_for, flash
from werkzeug.utils import secure_filename
from functions.genarators import *
from models import Base, Customer, Transactions

bulk = Blueprint('bulk', __name__)

UPLOAD_FOLDER = "C:\\projects\\"
ALLOWED_EXTENSIONS = {'txt', 'csv'}

engine = create_engine('sqlite:///bnk.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@bulk.route('/bulk_salaries', methods=['POST', 'GET'])
def bulk_salaries():
    record = []
    if request.method == 'POST':
        file_name = secure_filename(request.files['salary_file'].filename)
        # load the file from the form
        file = request.files['salary_file']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Upload the file in the in the folder
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            location_and_name = os.path.join(UPLOAD_FOLDER, filename)

            with open('C:\\Projects\\' + filename, 'r') as f:
                f_contents = f.readline()
                for line in f:
                    record_line = line.split(',')
                    from_acc = int(record_line[0])
                    to_acc = int(record_line[1])
                    amount = float(record_line[2])
                    remark = record_line[3]
                    print(record_line)

                    TransactionUpdate.transferTransactionUpdate(from_acc, to_acc, amount, remark,
                                                                Getters.getSysDate().date)
                    TransactionUpdate.accChargeUpdate('TR', from_acc, Getters.getSysDate().date)

                    # print(line, end='')
        else:
            flash("Please Check file extension")
            return redirect(url_for('bulk.bulk_salaries'))
        return render_template('bulk/bulk_salaries.html', record=record, user=Nav.userDetails())
    else:
        return render_template('bulk/bulk_salaries.html', record=record, user=Nav.userDetails())


@bulk.route('/bulk_transfers')
def bulk_transfers():
    record = []
    return render_template('bulk/bulk_transfers.html', record=record, user=Nav.userDetails())
