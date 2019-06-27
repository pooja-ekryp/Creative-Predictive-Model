
from flask import Flask, render_template
from datetime import datetime


from flask import Flask, render_template, request
from flask_mysqldb import MySQL
app = Flask(__name__)


app.config['MYSQL_HOST'] = '35.199.174.191'
app.config['MYSQL_USER'] = 'root1'
app.config['MYSQL_PASSWORD'] = 'Ekryp#1234'
app.config['MYSQL_DB'] = 'ml_reference'

mysql = MySQL(app)

#@app.route('/',methods=['GET', 'POST'])
#def index():
 #   return "welcome"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        #details = request.form
        unique_model_id = request.form.get('Model ID')
        user_id = request.form.get('User ID')
        date = request.form.get('Date')
        time = datetime.now().time()
        customer_id = request.form.get('Customer ID')
        customer_name = request.form.get('Name')
        model_name = request.form.get('Model Name')
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO ekryp_ml_model(unique_model_id,user_id,date,time,ekryp_customer_id,customer_name,model_name) VALUES (%s, %s,%s, %s,%s, %s,%s)", (unique_model_id,user_id,date,time,customer_id,customer_name,model_name))
        mysql.connection.commit()
        cur.close()
        print(customer_id)
    return 'success'



if __name__ == '__main__':
    app.run()
