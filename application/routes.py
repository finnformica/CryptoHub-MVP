from application import app, db
from application.forms import TransactionForm
from application.models import Transaction, Buy, Sell

from application.utils import load_data, create_pivot_table, create_dataframe

from flask import render_template, flash, redirect, url_for, jsonify
import requests
from datetime import datetime
import pandas as pd

# ---- Features ----
# plot risk on same graph as portfolio valuation

# ---- BUGS ----
# implement a check before deleting transaction (modal hasn't been working)
# websockets for price data (Flask-SocketIO) (currently using coingecko API)

def submit(form):
    transaction = Transaction(
                type = form.type.data,
                coin = form.coin.data,
                currency = form.currency.data,
                price = form.price.data,
                quantity = form.quantity.data,
                date = form.date.data,
                total_spent = form.price.data * form.quantity.data + form.fees.data,
                fees = form.fees.data,
                notes = form.notes.data
            )
    db.session.add(transaction)
    db.session.commit()


@app.route('/dashboard')
def dashboard():
    form = TransactionForm()
    if form.validate_on_submit():
        flash('Transaction submitted!', 'success')
        submit(form)
        return redirect(url_for('dashboard'))

    return render_template('dashboard.html', form=form)


@app.route('/transactions', methods = ["GET", "POST"])
def transactions():
    transactions = Transaction.query.order_by(Transaction.date.desc())
    form = TransactionForm()
    if form.validate_on_submit():
        flash('Transaction submitted!', 'success')
        submit(form)
        return redirect(url_for('transactions'))
    return render_template('transactions.html', title='Transactions', form=form, transactions=transactions)


@app.route('/pivot', methods = ["GET", "POST"])
def pivot():
    form = TransactionForm()
    if form.validate_on_submit():
        flash('Transaction submitted!', 'success')
        submit(form)
        return redirect(url_for('pivot'))

    df = create_dataframe()

    return render_template('pivot.html', title='Dashboard', form=form, pivot=create_pivot_table(df))

@app.route('/pie_chart')
def pie_chart():

    return create_pivot_table(create_dataframe()).to_json()

@app.route('/delete/<int:transaction_id>', methods = ["GET", "POST"])
def delete(transaction_id):
    transaction = Transaction.query.get_or_404(int(transaction_id))
    db.session.delete(transaction)
    db.session.commit()

    flash('Your transaction has been deleted!', 'success')
    return redirect(url_for('transactions'))
