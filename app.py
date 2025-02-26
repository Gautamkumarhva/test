import csv
from flask import Flask, render_template, url_for, request, redirect
import pandas as pd
from sqlalchemy import create_engine, text
import mysql.connector
import os
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

app = Flask(__name__)

KEY_VAULT_URL = os.getenv("KEY_VAULT_URL", "https://KeyVault2025xyz.vault.azure.net/")

credential = DefaultAzureCredential()

client = SecretClient(vault_url=KEY_VAULT_URL, credential=credential)

db_host = client.get_secret("DBHost").value
db_name = client.get_secret("DBName").value
db_user = client.get_secret("DBUser").value
db_password = client.get_secret("Secretsecret").value


# Establish connection using mysql.connector
connection = mysql.connector.connect(
    host=db_host,
    database=db_name,
    user=db_user,
    password=db_password
)

db_Info = connection.get_server_info()
print("Connected to MySQL Server version", db_Info)

# Create an engine using mysql connector 
engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}')

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


if __name__ == '__main__':
    app.run(debug=True)
