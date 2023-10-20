from app.database import db

class LoanClassificationFiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    branch_name = db.Column(db.String(100), nullable=False)
    loan_class_id = db.Column(db.String(100), nullable=True)
    filename = db.Column(db.String(100), nullable=True)


    def __repr__(self):
        return f'<Loan {self.id} >'

