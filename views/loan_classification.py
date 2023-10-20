# views/main_views.py
from flask import Blueprint, render_template,request
from app.database import db
from models.loan_classification import LoanClassification
from models.loan_classification_files import LoanClassificationFiles
from models.loan_classification_items import LoanClassificationItems
import pandas as pd



bp = Blueprint('loan_classification', __name__)

@bp.route('/loan_classification')
def loan_classification():
    return render_template('test_1.html')

@bp.route('/loan_classification_uploads')
def loan_classification_uploads():
    loan_classification_uploads = LoanClassificationFiles.query.all()  # Retrieve all loan classifications from the database
    
    serialized_loan_classification_uploads = []
    for classification in loan_classification_uploads:
        serialized_loan_classification_uploads.append({
            'id': classification.id,
            'branch_name': classification.branch_name,
        })
    
    return render_template('loan_classification_uploads.html',loan_class_uploads=serialized_loan_classification_uploads)


@bp.route('/loan_file_upload', methods=['POST'])
def loan_file_upload():
    branchName = request.form.get('branchName')
    loanFile = request.files.get('loanFile')
    filename = loanFile.filename

    print(loanFile.filename)
    # Check if a file was uploaded
    if filename == '':
        return 'No file uploaded!'

    # Extract data from the CSV
    dataframe = pd.read_csv(loanFile)
    print(dataframe)

    #save loan class items
    # loanClassificationItems = [
    #     {
    #         "loan_class_file_id": "LCFID_" + str(i),
    #         "arrangement": "Arrangement_" + str(i),
    #         "application_id": "AppID_" + str(i),
    #         "company_branch": "Branch_" + str(i),
    #         "account": "Account_" + str(i),
    #         "officer": "Officer_" + str(i),
    #         "product_name": "Product_" + str(i),
    #         "customer": "CustomerID_" + str(i),
    #         "customer_name": "Customer_" + str(i),
    #         "opening_date": "2023-01-" + str(i%28+1),  # Just to ensure we don't get an invalid date like 2023-01-30
    #         "first_pay_date": "2023-02-" + str(i%28+1),
    #         "maturity_date": "2023-03-" + str(i%28+1),
    #         "term": str(i),
    #         "ccy": "USD",
    #         "commitment": str(i*1000),
    #         "principal": str(i*1000 + 500),
    #         "due_date": "2023-04-" + str(i%28+1),
    #         "overdue": str(i*50),
    #         "resch_id": "ReschID_" + str(i),
    #         "status": "Active" if i%2 == 0 else "Inactive"
    #     }
    #     for i in range(10)  # creating 10 dummy records
    # ]

    loanClassificationItems = []

    for index, row in dataframe.iterrows():
        print("Index:",index)
        print(row);
        item = {
            "loan_class_file_id": index,
            # "arrangement": row[''],
            "application_id": row['Application Id'],
            "company_branch": row['Company/Branch'],
            "account": row['Account'],
            "officer": row['Officer'],
            "product_name": row['Product Name'],
            "customer": row['Customer'],
            "customer_name": row['Customer Name'],
            "opening_date": row['Opening Date'],
            "first_pay_date": row['First Pay Date'],
            "maturity_date": row['Maturity Date'],
            "term": row['Term'],
            "ccy": row['Ccy'],
            "commitment": row['Commitment'],
            "principal": row['Principal']
            # "due_date": row['Due Today'],
            # "overdue": row['Overdue'],
            # "resch_id": row['Resch Ind'],
            # "status": row['Status']
        }

    loanClassificationItems.append(item)

    print(loanClassificationItems)

    db.session.bulk_insert_mappings(LoanClassificationItems, loanClassificationItems)
    db.session.commit()

    #Save loan class files
    new_loan_class_file = LoanClassificationFiles(branch_name=branchName,loan_class_id='1',filename=filename)

    db.session.add(new_loan_class_file)
    db.session.commit()

    return branchName
    
@bp.route('/create_loan_classification',methods=['POST'])
def create_loan_classification():
    loanClassName = request.form.get('loanClassName')
    loanClassDesc = request.form.get('loanClassDesc')

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
