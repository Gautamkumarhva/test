import csv
from flask import Flask, render_template, url_for, request, redirect
app = Flask(__name__)

# mysqlconnector
import pandas as pd
from sqlalchemy import create_engine, text
import mysql.connector

host = 'oege.ie.hva.nl'
database = 'zkumarg'
user = 'kumarg'
password = '3iJnwqAn8tLjm+ep'

# Establish connection using mysql.connector
connection = mysql.connector.connect(
    host=host,
    database=database,
    user=user,
    password=password
)

db_Info = connection.get_server_info()
print("Connected to MySQL Server version", db_Info)

# Create an engine using mysql connector 
engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{database}')

@app.route('/')
def homepage():
    return render_template('index.html')


@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)

@app.route('/personal')
def personal():
    cursor = connection.cursor()
    cursor.execute("SELECT hobby FROM interests")
    result = cursor.fetchall()
    interests = []
    for row in result:
        interests.append(row[0]) 
    cursor.close()
    return render_template('personal_interest.html', interests=interests)

# def write_to_file(data):
#     with open('database.txt', mode='a') as database:
#         email = data['email']
#         subject = data['subject']
#         message = data['message']
#         file = database.write(f'\n{email},{subject},{message}')


def write_to_csv(data):
    with open('database.csv', 'a', newline='') as csvfile:
        email = data['email']
        subject = data['subject']
        message = data['message']
        writer = csv.writer(csvfile)
        writer.writerow([email, subject, message])


@app.route('/submit_form', methods=['GET', 'POST'])
def submit_form():
    if request.method == 'POST':
        data = request.form.to_dict()
        write_to_csv(data)
        return redirect('/thankyou.html')
    else:
        return 'Something went wrong!'

if __name__ == '__main__':
    app.run(debug=True)
