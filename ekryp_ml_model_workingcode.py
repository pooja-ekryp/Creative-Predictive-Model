from flask import Flask, render_template
from datetime import datetime
import mysql.connector
import pandas as pd
from sqlalchemy import create_engine
from flask import Flask, render_template, request
from flask_mysqldb import MySQL
app = Flask(__name__)


app.config['MYSQL_HOST'] = '35.199.174.191'
app.config['MYSQL_USER'] = 'root1'
app.config['MYSQL_PASSWORD'] = 'Ekryp#1234'
app.config['MYSQL_DB'] = 'ml_reference'
engine= create_engine("mysql://root1:Ekryp#1234@35.199.174.191/ml_reference")
mysql = MySQL(app)

#@app.route('/',methods=['GET', 'POST'])
#def index():
 #   return "welcome"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        #details = request.form
        
        #print(unique_model_id)
        #unique_model_id = request.form.get('unique_model_id')
        date = request.form.get('date')
        time = datetime.now().time()
        
        
        customer_name = request.form.get('customer_name')
        x = customer_name
        #query = 'select c.ekryp_customer_id from ml_reference.customer_map as c where c.customer_name="'+ x +'";'
        #customer_id = pd.read_sql( query, con = engine)
        
        model_name = request.form.get('model_name')

        dict = {
                'ARCA' : 1,
                'PROMETHEAN' : 2
                }
        print(dict)

        if(customer_name in dict):
            print("True")
            customer_id = dict.get(customer_name)
            print(customer_id)
        else:
            print("False")
        print(customer_id)
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO ekryp_ml_model(date,time,ekryp_customer_id,customer_name,model_name) VALUES (%s,%s,%s, %s, %s)", (date,time,customer_id,customer_name,model_name))
        mysql.connection.commit()
        cur.close()

        unique_model_id = pd.read_sql("select CONCAT(prefix,id) from ekryp_ml_model order by id desc limit 1",con = engine)
        
        unique_model_id = unique_model_id.min()
        cur2 = mysql.connection.cursor()
        cur2.execute("UPDATE ekryp_ml_model SET unique_model_id = %s order by id desc limit 1", (unique_model_id) )
        mysql.connection.commit()
        cur2.close()
        
    return 'success'

if __name__ == '__main__':
    app.run()