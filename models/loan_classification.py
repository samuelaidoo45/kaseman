from app.database import db

class LoanClassification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    loan_classification_name = db.Column(db.String(100), nullable=False)
    loan_classification_desc = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f'<Loan {self.id} - {self.loan_classification_name} - Classification: {self.loan_classification_name}>'

