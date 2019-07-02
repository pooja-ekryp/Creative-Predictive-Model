from flask import Flask, render_template, request
from datetime import datetime
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
        e = cur.execute("SELECT ekryp_customer_id from ekryp_ml_model order by date DESC, time DESC LIMIT 1")
        print(e)
        ekryp_customer_id = e
        cur.close()
        customer_asset_identifier = request.form.get('customer_asset_identifier')
        Asset_Serial_Number = request.form.get('Asset_Serial_Number')
        service_request_date = request.form.get('service_request_date')
        incident_category = request.form.get('incident_category')
        incident_status = request.form.get('incident_status')
        Priority = request.form.get('Priority')
        cur1 = mysql.connection.cursor()
        cur1.execute("INSERT INTO service_request_history( ekryp_customer_id, customer_asset_identifier, Asset_serial_number, service_request_date, incident_category, incident_status, Priority) VALUES (%s,%s,%s,%s,%s,%s,%s)", (ekryp_customer_id,customer_asset_identifier, Asset_Serial_Number, service_request_date,incident_category,incident_status,Priority))
        mysql.connection.commit()
        cur1.close()
    return 'success'    

if __name__ == '__main__':
        app.run()