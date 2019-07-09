import os
from flask import Flask,render_template,flash, request, redirect, url_for,send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import json

import numpy as np
import pandas as panda
#import MySQLdb
#from flask_cors import CORS
#from flask_mysqldb import MySQL
import mysql.connector
from sqlalchemy import create_engine, MetaData, Table, Column, Date, BigInteger, SMALLINT, String, Float, Integer
from sqlalchemy.sql import exists
import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#from flask.ext.mysqldb import MySQL

import io
import csv

UPLOAD_FOLDER = 'C:/flask-vue-crud/vue-new/uploaded-files'
ALLOWED_EXTENSIONS = (['csv','xls'])  

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER





app.config.from_object(__name__)
Base = declarative_base()
db = SQLAlchemy(app)

engine=create_engine('mysql://root1:Ekryp#1234@35.199.174.191/ml_reference')

#class error_code(db.Model):
#    __tablename__ = 'error_code'
    #to create a column we use db.Column
#    code_id = db.Column('code_id', db.Integer, primary_key = True)
#    criticality = db.Column('criticality',db.Integer, primary_key = False)
#    code_type = db.Column('code_type', db.Integer, primary_key = False)
#    description = db.Column('description', db.Unicode, primary_key = False) 
#    machine_code = db.Column('machine_code',db.Integer, primary_key = False) 
#    include_in_priority_group = db.Column('include_in_priority_group', db.Integer, primary_key = False) 


# enable CORS
#CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/result',methods=['GET'])
def result():
    return "File Uploaded Successfully"

def allowed_file(filename):
    return '.' in filename and \
         filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS
# sanity check route
@app.route('/', methods=['POST'])
def upload_file():
    if 'file' in request.files:
        file=request.files['file']
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_input = csv.DictReader(stream)
        dummy=panda.DataFrame.from_dict(csv_input)

        #alter this to fit the info in df to match the columns in table
        df = panda.DataFrame({
            'code_id': dummy['code_id'],
            'priority': dummy['priority'],
            'code_type': dummy['code_type'], 
            'description': dummy['description'],
            'machine_code': dummy['machine_code'],
            'include_in_priority_group':dummy['include_in_priority_group']
            
        })
        print(df.head)
        df.to_sql(name='error_code',con=engine,if_exists='append',index=False)
        #print('csv_input',csv_input)
        #for row in csv_input:
        #    record = error_code(**{
        #    'code_id': row[0],
        #    'criticality': row[1],
        #    'code_type': row[2], 
        #    'description': row[3],
        #    'machine_code': row[4],
        #    'include_in_priority_group':row[5]
        #    })

            
            #prints the rows in the following format from miniFacts-Data.csv
            #'2012-07-21', '301', '40', '180.0', '40.0', '0.0', '5.0', '40.0', '78735', '64336.0', '78735', '0.0', '1968.375', '2144.53333333', '30.0', '1.14470294294', '35.0', '1.4403862828', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', 'CM18', '1', 'CM18 group', '1.0', 'Recycler', '3.0', 'Short', '8.0', 'Unknown'
            #print('row',row)
            #print('record', record)
        print('filename:',file.filename)
        #print(file)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        print(filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #tablename='error_code'
        #sqlEngine, sqlMeta = getSQlEngine()
        
        #pushToSQL(tableSchema,df,'error_code',sqlEngine,sqlMeta)
        return 'File saved'
    return 'Hello'
if __name__ == '__main__':
    app.run()