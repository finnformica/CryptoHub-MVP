from datetime import datetime
from application import db

class Transaction(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(4), nullable=False, default='Buy')
    coin = db.Column(db.String(5), nullable=False)
    currency = db.Column(db.String(5), nullable=False, default='USD')
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    total_spent = db.Column(db.Float, nullable=False)

    fees = db.Column(db.Float, nullable=False, default=0)
    notes = db.Column(db.String(200), nullable=True, default="")

    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Transaction('{self.coin}', '{self.currency}', '{self.price}', '{self.quantity}', '{self.date}')"


class Buy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coin = db.Column(db.String(5), nullable=False)
    value = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Buy('${self.value}', '{self.quantity}')"


class Sell(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coin = db.Column(db.String(5), nullable=False)
    value = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Sell('${self.value}', '{self.quantity}')"
