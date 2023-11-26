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
    
    loan_classifications = LoanClassification.query.filter_by(id=id).all()  # Retrieve all loan classifications from the database
    
    return render_template('loan_classification_uploads.html',loan_class_uploads=serialized_loan_classification_uploads,loan_class_id=id,loan_class_date=loan_classifications[0].loan_classification_name)


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
        if 'Due Today' in dataframe.columns:
            item["due_date"] = row['Due Today']
        if 'Overdue' in dataframe.columns:
            item["overdue"] = row['Overdue']
        if 'Status' in dataframe.columns:
            item["status"] = row['Status']

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


def classify_loan(maturity_date_str):
    from datetime import datetime  # Make sure you've imported datetime here
    # opening_date = datetime.strptime(opening_date_str, '%Y-%m-%d').date()
    
    maturity_date = datetime.strptime(maturity_date_str, '%d-%b-%y').date()

    # opening_date = datetime.strptime(opening_date_str, '%Y-%m-%d').date()
    days_outstanding = (date.today() - maturity_date).days

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

def get_unified_product_name(product_name):
    if product_name in ['Salary Loan', 'Personal Loan']:
        return "Salary/Personal Loan"
    return product_name

def parse_principal(principal_str):
    try:
         if principal_str is not None:
            return float(principal_str.replace(',', ''))
         else:
            return 0.0
    except ValueError:
        return 0.0 

@bp.route('/top_loans/<int:id>')
def top_loans(id):
    top_loans = {}

    loan_classification_uploads = LoanClassificationFiles.query.filter_by(loan_class_id=id).all()

    for classification in loan_classification_uploads:
        branch_name = classification.branch_name

        if branch_name not in top_loans:
            top_loans[branch_name] = []

        # Fetch all loan items associated with the classification ID
        top_loan_items = LoanClassificationItems.query.filter_by(loan_class_file_id=classification.id).all()

        # Sort all fetched items by principal in descending order
        sorted_loan_items = sorted(top_loan_items, key=lambda item: parse_principal(item.principal), reverse=True)

        # Limit the sorted list to the top 20 items
        top_20_loan_items = sorted_loan_items[:20]

        top_loans[branch_name].extend(top_20_loan_items)

    combined_loans = []
    for branch in top_loans:
        for loan in top_loans[branch]:
            combined_loans.append((branch, loan))

    # Sort the combined loans by principal, in descending order
    combined_loans_sorted = sorted(combined_loans, key=lambda x: parse_principal(x[1].principal), reverse=True)

    # Select the top 20 loans from the combined list
    top_20_combined_loans = combined_loans_sorted[:20]

    return render_template('top_loans.html',id=id,top_loans=top_loans,top_20_overall_loans=top_20_combined_loans)


@bp.route('/loan_classification_total/<int:id>')
def loan_classification_total(id):
    loan_classification_uploads = LoanClassificationFiles.query.filter_by(loan_class_id=id).all()

    branches_data = {}  # Dictionary to store all branches data

    branches_column_data = {}

    # Define the default classifications and their structure
    default_classifications = {
        'Current (Up to 30 days)': {'Commitment': 0.00, 'Principal': 0.00, 'Count': 0},
        'OLEM (31 to 90 days)': {'Commitment': 0.00, 'Principal': 0.00, 'Count': 0},
        'SUB-STAND (91 to 180 days)': {'Commitment': 0.00, 'Principal': 0.00, 'Count': 0},
        'DOUTFUL (181 to 360 days)': {'Commitment': 0.00, 'Principal': 0.00, 'Count': 0},
        'LOSS (Over 360 days)': {'Commitment': 0.00, 'Principal': 0.00, 'Count': 0}
    }

    for classification in loan_classification_uploads:
        branch_name = classification.branch_name

        if branch_name not in branches_data:
            branches_data[branch_name] = {}
            branches_column_data[branch_name] = {
                'Current (Up to 30 days)':  0.00,
                'OLEM (31 to 90 days)' : 0.00,
                'SUB-STAND (91 to 180 days)':0.00,
                'DOUTFUL (181 to 360 days)': 0.00,
                'LOSS (Over 360 days)': 0.00
            }

        loan_classification_items = LoanClassificationItems.query.filter_by(loan_class_file_id=classification.id).all()

        for item in loan_classification_items:
            product_name = item.product_name
            # print(product_name)
            unified_product_name = get_unified_product_name(product_name)
            # print(unified_product_name)
            if item.opening_date is None:
                continue

            loan_classification = classify_loan(item.maturity_date)

            # Ensure product is initialized with default classifications
            if unified_product_name not in branches_data[branch_name]:
                branches_data[branch_name][unified_product_name] = deepcopy(default_classifications)

            # Aggregate data for this product and classification
            if item.overdue is not None:
                overdue_value = float(item.overdue.replace(',', ''))
            else:
                overdue_value = 0.0

            if item.due_date is not None:
                due_date_value = float(item.due_date.replace(',', ''))
            else:
                due_date_value = 0.0

            if item.principal is not None:
                principal_value = float(item.principal.replace(',', ''))
            else:
                principal_value = 0.0

            # Use the function to get the unified product name

            # Perform the calculation using the unified product name
            branches_data[branch_name][unified_product_name][loan_classification]['Commitment'] += overdue_value + due_date_value + principal_value

            # branches_data[branch_name][product_name][loan_classification]['Commitment'] += overdue_value + due_date_value + principal_value

            # branches_data[branch_name][product_name][loan_classification]['Commitment'] += float(item.overdue) + float(item.due_date) + float(item.principal.replace(',', ''))
            branches_data[branch_name][unified_product_name][loan_classification]['Principal'] += float(item.principal.replace(',', ''))
            branches_data[branch_name][unified_product_name][loan_classification]['Count'] += 1

            branches_column_data[branch_name][loan_classification] += round((overdue_value + due_date_value + principal_value),2)

            # Round the values to 2 decimal places
            branches_data[branch_name][unified_product_name][loan_classification]['Commitment'] = round(branches_data[branch_name][unified_product_name][loan_classification]['Commitment'], 2)
            branches_data[branch_name][unified_product_name][loan_classification]['Principal'] = round(branches_data[branch_name][unified_product_name][loan_classification]['Principal'], 2)

    totals = {}

    # Iterate over each branch to calculate the total for each category
    for branch in branches_column_data:
        for category in branches_column_data[branch]:
            # If the category is not already in the totals dictionary, add it with its current value
            if category not in totals:
                totals[category] = (round((branches_column_data[branch][category]),2))
            # If the category is already in the totals dictionary, increment it by its current value
            else:
                totals[category] += (round((branches_column_data[branch][category]),2))

    # The totals dictionary now contains the sum for each category across all branches

    # # Calculate 1% of the totals for each category
    # percent_totals = {category: "{:,.2f}".format(round(total * 0.01,2)) for category, total in totals.items()}

    # Define the percentages for each category
    category_percentages = {
        'Current (Up to 30 days)': 0.01,  # 1%
        'OLEM (31 to 90 days)': 0.10,     # 10%
        'SUB-STAND (91 to 180 days)': 0.25, # 25%
        'DOUTFUL (181 to 360 days)': 0.50,  # 50%
        'LOSS (Over 360 days)': 1.00       # 100%
    }

    # Assuming 'totals' is a dictionary with categories as keys and their corresponding total values
    # Update percent_totals to calculate the percentage of the total for each category

    percent_totals = {category: "{:,.2f}".format(round(totals.get(category, 0) * category_percentages.get(category, 0), 2)) for category in category_percentages}

    formatted_totals = {category: "{:,.2f}".format(total) for category, total in totals.items()}

    return render_template('loan_classification_total.html', branches_data=branches_data,id=id,branches_column_total=branches_column_data,totals=formatted_totals,percent_totals=percent_totals)


@bp.route('/delete_loan_classification/<int:id>')
def delete_loan_classification(id):

    loan_classification_files = LoanClassificationFiles.query.filter_by(loan_class_id=id).all()

    # Delete associated LoanClassificationItems and LoanClassificationFiles
    for file in loan_classification_files:
        # Retrieve and delete associated LoanClassificationItems
        loan_classification_items_to_delete = LoanClassificationItems.query.filter_by(loan_class_file_id=file.id).all()
        for item in loan_classification_items_to_delete:
            db.session.delete(item)

        # Delete the LoanClassificationFile
        db.session.delete(file)

    # Retrieve and delete the LoanClassification object with the given id
    loan_classification_to_delete = LoanClassification.query.get(id)
    if loan_classification_to_delete:
        db.session.delete(loan_classification_to_delete)

    # Commit the changes to the database
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


@bp.route('/classification_advances/<int:id>')
def classification_advances(id):

    return render_template('advances.html',id=id,)







