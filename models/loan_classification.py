from app.database import db

class LoanClassification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    loan_classification_name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Loan {self.loan_id} - Classification: {self.classification}>'

