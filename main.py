from flask import Flask, render_template, request, redirect
from livereload import Server
import json
import random

app = Flask(__name__)


@app.route("/",methods=['GET','POST'])
def home(name=None):
    with open('static/password.json',mode='r') as jsonFile:
        read_password = json.load(jsonFile)
    expense = 0
    check_password = read_password[0]['Password']
    with open('static/db.json',mode='r') as jsonFile:
        read_data = json.load(jsonFile)
    if request.method == 'POST':
        expense = request.form['item-price']
        read_data[0][request.form['item-name'].title()]={
            "Name": request.form['item-name'].title(),
            "Quantity": request.form['item-quantity'],
            "Unit": request.form['item-unit'],
            "Price": request.form['item-price']
        }
    with open('static/bank.json',mode='r') as jsonFile:
        bank_data = json.load(jsonFile)
        current = bank_data[0]['Bank']['Wallet'] = bank_data[0]['Bank']['Wallet'] - int(expense)
    with open('static/bank.json',mode='w') as jsonFile:
        json.dump(bank_data, jsonFile, indent=4)
    
    total_price = []
    total_quantity = []

    for items in read_data[0].values():
       total_price.append(int(items['Price']))
       total_quantity.append(int(items['Quantity']))
    
    tootal_quantity_data = sum(total_quantity)
    total_price_data = sum(total_price)
    with open('static/db.json',mode='w') as jsonFile:
        json.dump(read_data, jsonFile, indent=4)

    context = {
        'items': read_data[0],
        'tpd': total_price_data,
        'tqd': tootal_quantity_data,
        'credentials':check_password
    }

    
    return render_template('index.html', name=name, context=context)


@app.route("/delete",methods=['GET','POST'])
def delete():
    with open('static/db.json',mode='r') as jsonFile:
        read_data = json.load(jsonFile)
    if request.method == 'POST':
        testdata = request.form['item-id']
        read_data[0].pop(testdata)
    with open('static/db.json',mode='w') as jsonFile:
        json.dump(read_data, jsonFile, indent=4)
    
    return redirect('http://192.168.2.3:8000/')


# sales page
@app.route("/sales",methods=['GET','POST'])
def sales():
    with open('static/password.json',mode='r') as jsonFile:
        read_password = json.load(jsonFile)
    check_password = read_password[0]['Password']
    with open('static/bank.json',mode='r') as jsonFile:
        read_data = json.load(jsonFile)
    
    context = {
        'bank': read_data[0],
        'credentials':check_password
    }

    return render_template('sales.html',context=context)

@app.route("/add_todays_income",methods=['GET','POST'])
def add_income():
    with open('static/bank.json',mode='r') as jsonFile:
        read_data = json.load(jsonFile)
    if request.method == "POST":
        income_generated = request.form['income']
        print(income_generated)
    current = read_data[0]['Bank']['Wallet'] = read_data[0]['Bank']['Wallet'] + int(income_generated)
    print(current)
    with open('static/bank.json',mode='w') as jsonFile:
        json.dump(read_data, jsonFile, indent=4)
    
    return redirect('/sales')


@app.route("/add_todays_expense",methods=['GET','POST'])
def add_expense():
    with open('static/bank.json',mode='r') as jsonFile:
        read_data = json.load(jsonFile)
    if request.method == "POST":
        expense_generated = request.form['expense']
        print(expense_generated)
    current = read_data[0]['Bank']['Wallet'] = read_data[0]['Bank']['Wallet'] - int(expense_generated)
    print(current)
    with open('static/bank.json',mode='w') as jsonFile:
        json.dump(read_data, jsonFile, indent=4)
    
    return redirect('/sales')
    
@app.route("/authentication",methods=['GET','POST'])
def is_authenticated():
    with open('static/password.json',mode='r') as jsonFile:
        read_password = json.load(jsonFile)
    if request.method == "POST":
        input_password = request.form['app-password']
        read_password[0]['Password']=input_password
    with open('static/password.json',mode='w') as jsonFile:
        json.dump(read_password, jsonFile, indent=4)
    return redirect('/')

@app.route("/logout",methods=['GET','POST'])
def logout():
     with open('static/password.json',mode='r') as jsonFile:
        read_password = json.load(jsonFile)
        read_password[0]['Password']='null'
     with open('static/password.json',mode='w') as jsonFile:
        json.dump(read_password, jsonFile, indent=4)
     return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
