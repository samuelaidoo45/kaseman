# views/main_views.py
from flask import Blueprint, render_template,request
from app.database import db
from models.loan_classification import LoanClassification
from models.loan_classification_files import LoanClassificationFiles
from models.loan_classification_items import LoanClassificationItems
import pandas as pd
from datetime import date, timedelta
from datetime import datetime
from copy import deepcopy


bp = Blueprint('loan_classification', __name__)

@bp.route('/loan_classification')
def loan_classification():
    return render_template('test_1.html')

@bp.route('/loan_classification_upload/<int:id>', methods=['GET'])
def loan_classification_uploads(id):
    loan_classification_uploads = LoanClassificationFiles.query.filter_by(loan_class_id=id).all()
    
    serialized_loan_classification_uploads = []
    for classification in loan_classification_uploads:
        serialized_loan_classification_uploads.append({
            'id': classification.id,
            'branch_name': classification.branch_name,
        })
    
    return render_template('loan_classification_uploads.html',loan_class_uploads=serialized_loan_classification_uploads,loan_class_id=id)


@bp.route('/loan_file_upload/<int:id>', methods=['POST'])
def loan_file_upload(id):
    branchName = request.form.get('branchName')
    loanFile = request.files.get('loanFile')
    filename = loanFile.filename

    # Check if a file was uploaded
    if filename == '':
        return 'No file uploaded!'

    dataframe = pd.read_csv(loanFile)

    last_entry = LoanClassificationFiles.query.order_by(LoanClassificationFiles.id.desc()).first()

    if last_entry:
        last_index = last_entry.id + 1
    else:
        last_index = 1        

    #save loan class items
    loanClassificationItems = []

    for index, row in dataframe.iterrows():

        item = {
            "loan_class_file_id": last_index,
        }

        # Check if column exists before accessing its value
        if 'Application Id' in dataframe.columns:
            item["application_id"] = row['Application Id']
        if 'Company/Branch' in dataframe.columns:
            item["company_branch"] = row['Company/Branch']
        if 'Account' in dataframe.columns:
            item["account"] = row['Account']
        if 'Officer' in dataframe.columns:
            item["officer"] = row['Officer']
        if 'Product Name' in dataframe.columns:
            item["product_name"] = row['Product Name']
        if 'Customer' in dataframe.columns:
            item["customer"] = row['Customer']
        if 'Customer Name' in dataframe.columns:
            item["customer_name"] = row['Customer Name']
        if 'Opening Date' in dataframe.columns:
            item["opening_date"] = row['Opening Date']
        if 'First Pay Date' in dataframe.columns:
            item["first_pay_date"] = row['First Pay Date']
        if 'Maturity Date' in dataframe.columns:
            item["maturity_date"] = row['Maturity Date']
        if 'Term' in dataframe.columns:
            item["term"] = row['Term']
        if 'Ccy' in dataframe.columns:
            item["ccy"] = row['Ccy']
        if 'Commitment' in dataframe.columns:
            item["commitment"] = row['Commitment']
        if 'Principal' in dataframe.columns:
            item["principal"] = row['Principal']

        loanClassificationItems.append(item)

    db.session.bulk_insert_mappings(LoanClassificationItems, loanClassificationItems)
    db.session.commit()

    #Save loan class files
    new_loan_class_file = LoanClassificationFiles(branch_name=branchName,loan_class_id=id,filename=filename)

    db.session.add(new_loan_class_file)
    db.session.commit()

    loan_classification_uploads = LoanClassificationFiles.query.filter_by(loan_class_id=id).all()
    
    serialized_loan_classification_uploads = []
    for classification in loan_classification_uploads:
        serialized_loan_classification_uploads.append({
            'id': classification.id,
            'branch_name': classification.branch_name,
        })
    
    return render_template('loan_classification_uploads.html',loan_class_uploads=serialized_loan_classification_uploads,loan_class_id=id)
    
@bp.route('/create_loan_classification',methods=['POST'])
def create_loan_classification():
    loanClassYear = request.form.get('loanClassYear')
    loanClassMonth = request.form.get('loanClassMonth')
    loanClassDesc = request.form.get('loanClassDesc')

    loanClassName = loanClassMonth + " " + loanClassYear

    new_loan_class = LoanClassification(loan_classification_name=loanClassName,loan_classification_desc=loanClassDesc)

    db.session.add(new_loan_class)
    db.session.commit()

    loan_classifications = LoanClassification.query.all()  # Retrieve all loan classifications from the database
    
    serialized_loan_classifications = []
    for classification in loan_classifications:
        serialized_loan_classifications.append({
            'id': classification.id,
            'loan_classification_name': classification.loan_classification_name,
            'loan_classification_desc': classification.loan_classification_desc,
        })
    
    return render_template('index.html',loan_classes=serialized_loan_classifications)


def classify_loan(opening_date_str):
    from datetime import datetime  # Make sure you've imported datetime here
    # opening_date = datetime.strptime(opening_date_str, '%Y-%m-%d').date()
    
    opening_date = datetime.strptime(opening_date_str, '%d-%b-%y').date()

    # opening_date = datetime.strptime(opening_date_str, '%Y-%m-%d').date()
    days_outstanding = (date.today() - opening_date).days

    # Classify the loan based on days_difference
    if days_outstanding <= 30:
        return 'Current (Up to 30 days)'
    elif 31 <= days_outstanding <= 90:
        return 'OLEM (31 to 90 days)'
    elif 91 <= days_outstanding <= 180:
        return 'SUB-STAND (91 to 180 days)'
    elif 181 <= days_outstanding <= 360:
        return 'DOUTFUL (181 to 360 days)'
    else:
        return 'LOSS (Over 360 days)'   # Adjusted key here


@bp.route('/loan_classification_total/<int:id>')
def loan_classification_total(id):
    loan_classification_uploads = LoanClassificationFiles.query.filter_by(loan_class_id=id).all()

    branches_data = {}  # Dictionary to store all branches data

    # Define the default classifications and their structure
    default_classifications = {
        'Current (Up to 30 days)': {'Commitment': 0.0, 'Principal': 0.0, 'Count': 0},
        'OLEM (31 to 90 days)': {'Commitment': 0.0, 'Principal': 0.0, 'Count': 0},
        'SUB-STAND (91 to 180 days)': {'Commitment': 0.0, 'Principal': 0.0, 'Count': 0},
        'DOUTFUL (181 to 360 days)': {'Commitment': 0.0, 'Principal': 0.0, 'Count': 0},
        'LOSS (Over 360 days)': {'Commitment': 0.0, 'Principal': 0.0, 'Count': 0}
    }

    for classification in loan_classification_uploads:
        branch_name = classification.branch_name

        if branch_name not in branches_data:
            branches_data[branch_name] = {}

        loan_classification_items = LoanClassificationItems.query.filter_by(loan_class_file_id=classification.id).all()

        for item in loan_classification_items:
            product_name = item.product_name
            if item.opening_date is None:
                continue

            loan_classification = classify_loan(item.opening_date)

            # Ensure product is initialized with default classifications
            if product_name not in branches_data[branch_name]:
                branches_data[branch_name][product_name] = deepcopy(default_classifications)

            # Aggregate data for this product and classification
            branches_data[branch_name][product_name][loan_classification]['Commitment'] += float(item.commitment.replace(',', ''))
            branches_data[branch_name][product_name][loan_classification]['Principal'] += float(item.principal.replace(',', ''))
            branches_data[branch_name][product_name][loan_classification]['Count'] += 1

    return render_template('loan_classification_total.html', branches_data=branches_data,id=id)

