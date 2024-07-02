import config
from flask import render_template, request, redirect, url_for, flash
from models import Customer, customer_schema
from customers import create, update, delete
from datetime import datetime


app = config.connex_app
app.add_api(config.basedir / "swagger.yml")

@app.route("/")
def home():
    customers = Customer.query.all()
    return render_template("home.html", customers=customers)

@app.route('/create_customer', methods=['GET', 'POST'])
def create_customer():
    if request.method == 'POST':
        customer_data = {
            'fname': request.form['fname'],
            'lname': request.form['lname'],
            'email': request.form['email'],
            'status': True
        }
        try:
            response, status_code = create(customer_data)
            message = f"Customer {response['fname']} {response['lname']} created successfully."

            return redirect(url_for('create_customer', message=message))
        except Exception as e:
            return render_template('create_customer.html', error=str(e))
            
    message = request.args.get('message', '')
    error = request.args.get('error', '')
    
    return render_template('create_customer.html', message=message, error=error)

@app.route('/update_customer', methods=['GET', 'POST'])
def update_customer():
    if request.method == 'POST':
        lname = request.form['lname']
        
        new_customer_data = {
            'lname': request.form['lname'],
            'fname': request.form['fname'],
            'email': request.form['email'],
            'status': request.form['status']
        }
        
        try:
            response, status_code = update(lname, new_customer_data)
            message = f"Customer {response['lname']} updated successfully."
            
            return redirect(url_for('update_customer', message=message))
        except Exception as e:
            return render_template('update_customer.html', error=str(e))
            
    message = request.args.get('message', '')
    error = request.args.get('error', '')
            
    return render_template('update_customer.html', message=message, error=error)

@app.route('/delete_customer', methods=['GET', 'POST'])
def delete_customer():
    if request.method == 'POST':
        lname = request.form['lname']
        try:
            response = delete(lname)
            message = response.get_data(as_text=True)
                
            return redirect(url_for('delete_customer', message=message))
        except Exception as e:
            return render_template('delete_customer.html', error=str(e))
    
    message = request.args.get('message', '')
    error = request.args.get('error', '')
    
    return render_template('delete_customer.html', message=message, error=error)


@app.route('/customers_list')
def customers_list():
    customers = Customer.query.all()

    serialized_customers = [customer_schema.dump(customer) for customer in customers]

    return render_template('customers_list.html', customers=serialized_customers)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
