from flask import Flask, render_template, request
import datetime
from flask_mysqldb import MySQL 
app = Flask(__name__)

app.config['MYSQL_HOST'] = '35.199.174.191'
app.config['MYSQL_USER'] = 'root1'
app.config['MYSQL_PASSWORD'] = 'Ekryp#1234'
app.config['MYSQL_DB'] = 'ml_reference'

mysql = MySQL(app)

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        cur.execute("SELECT ekryp_customer_id,Unique_Model_Id  from ekryp_ml_model order by date DESC, time DESC LIMIT 1")
        for row in cur:
            print(row[0])
            print(row[1])
            ekryp_customer_id = row[0]
            Unique_Model_Id = row[1]

        print(ekryp_customer_id)
        cur.close()
       
        period_definition = request.form.get('period_definition')
        periods_for_error = request.form.get('periods_for_error')
        missing_period_before_exclusion = request.form.get('missing_period_before_exclusion')
        prediction_horizon = request.form.get('prediction_horizon')
        prediction_frequency = request.form.get('prediction_frequency')
        start_date = request.form.get('start_date')
        created_at = datetime.datetime.now()
        cur1 = mysql.connection.cursor()
        cur1.execute("INSERT INTO  Customer_Model_Configuration( ekryp_customer_id, Unique_Model_Id, period_definition, periods_for_error, missing_period_before_exclusion, prediction_horizon, prediction_frequency, start_date,created_at ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", (ekryp_customer_id, Unique_Model_Id, period_definition, periods_for_error, missing_period_before_exclusion, prediction_horizon, prediction_frequency, start_date,created_at  ))
        mysql.connection.commit()
        cur1.close()
    return 'success'    

if __name__ == '__main__':
        app.run()