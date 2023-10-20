from app.database import db

class LoanClassificationItems(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    loan_class_file_id = db.Column(db.String(100), nullable=False)
    arrangement = db.Column(db.String(100), nullable=True)
    application_id = db.Column(db.String(100), nullable=True)
    company_branch = db.Column(db.String(100), nullable=True)
    account = db.Column(db.String(100), nullable=True)
    officer = db.Column(db.String(100), nullable=True)
    product_name = db.Column(db.String(100), nullable=True)
    customer = db.Column(db.String(100), nullable=True)
    customer_name = db.Column(db.String(100), nullable=True)
    opening_date = db.Column(db.String(100), nullable=True)
    first_pay_date = db.Column(db.String(100), nullable=True)
    maturity_date = db.Column(db.String(100), nullable=True)
    term = db.Column(db.String(100), nullable=True)
    ccy = db.Column(db.String(100), nullable=True)
    commitment = db.Column(db.String(100), nullable=True)
    principal = db.Column(db.String(100), nullable=True)
    due_date = db.Column(db.String(100), nullable=True)
    overdue = db.Column(db.String(100), nullable=True)
    resch_id = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f'<Loan {self.id} >'

















    def __repr__(self):
        return f'<Loan {self.id} - {self.loan_classification_name} - Classification: {self.loan_classification_name}>'

