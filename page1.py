
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
from flask import Flask, render_template, request
from flask_mysqldb import MySQL
app = Flask(__name__)


app.config['MYSQL_HOST'] = '35.199.174.191'
app.config['MYSQL_USER'] = 'root1'
app.config['MYSQL_PASSWORD'] = 'Ekryp#1234'
app.config['MYSQL_DB'] = 'ml_reference'

mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        details = request.form
        Unique_Model_Id = details['model_id']
        User_id = details['user_id']
        Date = details['date']
        time = datetime.now().time()
        customer_id = details['customer_id']
        customer_name = details['customer_name']
        model_name = details['model_name']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO ekryp_ml_model(Unique_Model_Id,User_id,Date,time,customer_id,customer_name,model_name) VALUES (%s, %s,%s, %s,%s, %s,%s)", (Unique_Model_Id,User_id,Date,time,customer_id,customer_name,model_name))
        mysql.connection.commit()
        cur.close()
        return 'success'
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
if __name__ == '__main__':
    app.run()