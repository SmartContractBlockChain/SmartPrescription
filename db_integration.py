from flask import Flask
from flask_mysqldb import MySQL
from flask import jsonify

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'SCBC'
app.config['MYSQL_PASSWORD'] = 'SCBC_PASS'
app.config['MYSQL_DB'] = 'smartPrescription'

mysql = MySQL(app)


@app.route('/', methods=['GET'])
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE id = 1")
    results = cur.fetchall()
    user = results[0]

    cur.close()

    return jsonify(firstName=user[1], lastName=user[2], userType=user[4])


if __name__ == '__main__':
    app.run()
