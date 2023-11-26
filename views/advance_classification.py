# views/main_views.py
from flask import Blueprint, render_template ,request
from models.loan_classification import LoanClassification
from models.loan_classification_files import LoanClassificationFiles
from models.loan_classification_items import LoanClassificationItems
from datetime import date, timedelta
from datetime import datetime
from copy import deepcopy


bp = Blueprint('returns', __name__)

@bp.route('/returns')
def returns():
    return render_template('returns.html')
    
@bp.route('/advances_main')
def advances_main():

    loan_classifications = LoanClassification.query.all()  # Retrieve all loan classifications from the database
    # Serialize the records into a JSON format
    serialized_loan_classifications = []
    for classification in loan_classifications:
        serialized_loan_classifications.append({
            'id': classification.id,
            'loan_classification_month': classification.loan_classification_name,
            'loan_classification_desc': classification.loan_classification_desc,
        })
    
    return render_template('advances_main.html',classification_months=serialized_loan_classifications)

def preprocess_data(data):
    processed_data = {}
    for key, sub_dict in data.items():

        # Check if sub_dict is empty, if so, fill with empty values
        if not sub_dict:
            sub_dict = {
                'Current (Up to 30 days)': '',
                'OLEM (31 to 90 days)': '',
                'SUB-STAND (91 to 180 days)': '',
                'DOUTFUL (181 to 360 days)': '',
                'LOSS (Over 360 days)': ''
            }

        processed_sub_dict = {}
        total = 0
        for sub_key, value in sub_dict.items():
            if value:
                # Remove commas and non-numeric characters except decimal point
                clean_value = value.replace(',', '').replace('%', '')
                try:
                    num_value = float(clean_value)
                except ValueError:
                    num_value = 0  # Set to 0 if conversion fails
            else:
                num_value = 0
            processed_sub_dict[sub_key] = num_value
            total += num_value

        if key == 'Provided Required':
            processed_sub_dict['Total'] = ''
        else:
            processed_sub_dict['Total'] = round(total,2)

        processed_data[key] = processed_sub_dict
    return processed_data

    
@bp.route('/create_advance_classification',methods=['POST'])
def create_advance_classification():
    previousMonth = request.form.get('previousMonth')
    currentMonth = request.form.get('currentMonth')

    advances_classification = {
        "previous": classification_total(previousMonth)[0],
        "new_advance": {'Current (Up to 30 days)':'','OLEM (31 to 90 days)':'','SUB-STAND (91 to 180 days)':'','DOUTFUL (181 to 360 days)':'','LOSS (Over 360 days)':''},
        "qrt_int_charged": {'Current (Up to 30 days)':'','OLEM (31 to 90 days)':'','SUB-STAND (91 to 180 days)':'','DOUTFUL (181 to 360 days)':'','LOSS (Over 360 days)':''},
        "less_amount_written_off":{'Current (Up to 30 days)':'','OLEM (31 to 90 days)':'','SUB-STAND (91 to 180 days)':'','DOUTFUL (181 to 360 days)':'','LOSS (Over 360 days)':''},
        "less_amount_recovered":{'Current (Up to 30 days)':'','OLEM (31 to 90 days)':'','SUB-STAND (91 to 180 days)':'','DOUTFUL (181 to 360 days)':'','LOSS (Over 360 days)':''},
        "changes_in_classification":{'Current (Up to 30 days)':'','OLEM (31 to 90 days)':'','SUB-STAND (91 to 180 days)':'','DOUTFUL (181 to 360 days)':'','LOSS (Over 360 days)':''},
        "current_balance": classification_total(currentMonth)[0],
        "allowable_security_and_near_cash": {'Current (Up to 30 days)':'','OLEM (31 to 90 days)':'','SUB-STAND (91 to 180 days)':'','DOUTFUL (181 to 360 days)':'','LOSS (Over 360 days)':''},
        "net_current_balance": classification_total(currentMonth)[0],
        "Provided Required": {'Current (Up to 30 days)':'1%','OLEM (31 to 90 days)':'10%','SUB-STAND (91 to 180 days)':'25%','DOUTFUL (181 to 360 days)':'50%','LOSS (Over 360 days)':'100%'},
        "amount_provided":classification_total(currentMonth)[1]
    }

    # print(advances_classification)
    processed_data = preprocess_data(advances_classification)

    return render_template('advances.html',advances_classification=processed_data)

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

def classification_total(id):

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

    return [formatted_totals,percent_totals]

def quaterly_interest_charge(id):
    return ''    

