# Import libraries
from flask import Flask, request, url_for, redirect, render_template

# Instantiate Flask functionality
app = Flask(__name__)

# Sample data
transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 300}
]

# Read operation
@app.route('/')
def get_transactions():
    return render_template('transactions.html', transactions=transactions, total_balance=sum(t['amount'] for t in transactions))

# Create operation
@app.route('/add', methods=['GET','POST'])
def add_transaction():
    if request.method=='GET':
        return render_template('form.html')
    
    if request.method=='POST':
        transaction = {
              'id': len(transactions)+1,
              'date': request.form['date'],
              'amount': float(request.form['amount'])
             }
        if transaction:
            transactions.append(transaction)
            return redirect(url_for("get_transactions"))
        else:
            return {'message': 'Missing transaction details'}, 404

# Update operation
@app.route('/edit/<int:transaction_id>', methods=['GET', 'POST'])
def edit_transaction(transaction_id):
    # Check if the request method is POST (form submission)
    if request.method == 'POST':
        # Extract the updated values from the form fields
        date = request.form['date']           # Get the 'date' field value from the form
        amount = float(request.form['amount'])# Get the 'amount' field value from the form and convert it to a float
        # Find the transaction with the matching ID and update its values
        for transaction in transactions:
            if transaction['id'] == transaction_id:
                transaction['date'] = date       # Update the 'date' field of the transaction
                transaction['amount'] = amount   # Update the 'amount' field of the transaction
                break                            # Exit the loop once the transaction is found and updated
        # Redirect to the transactions list page after updating the transaction
        return redirect(url_for("get_transactions"))
    
    # If the request method is GET, find the transaction with the matching ID and render the edit form
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            # Render the edit form template and pass the transaction to be edited
            return render_template("edit.html", transaction=transaction)
    # If the transaction with the specified ID is not found, handle this case (optional)
    return {"message": "Transaction not found"}, 404

# Delete operation
@app.route('/delete/<int:transaction_id>')
def delete_transaction(transaction_id):
    for transaction in transactions:
        if transaction['id']==transaction_id:
            transactions.remove(transaction)
            break
    return redirect(url_for("get_transactions"))

@app.route('/search', methods=['GET', 'POST'])
def search_transactions():
    if request.method=='POST':
        mini = float(request.form['min_amount'])
        maxi = float(request.form['max_amount'])
        filtered_transactions=[]
        for transaction in transactions:
            if transaction['amount']>=mini and transaction['amount']<=maxi:
                filtered_transactions.append(transaction)
        
        return render_template('transactions.html', transactions=filtered_transactions)
    
    return render_template('search.html')

# Run the Flask app
if __name__=='__main__':
    app.run(debug=True) 