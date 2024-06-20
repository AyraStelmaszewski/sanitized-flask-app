from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import bleach

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'bloubloublou'
app.config['MYSQL_PASSWORD'] = 'blablabla'  
app.config['MYSQL_DB'] = 'hackerpoulette'

mysql = MySQL(app)

@app.route('/')
def welcome():
    return render_template('hello.html')

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get form data
        username = bleach.clean(request.form['username'])  # Sanitize username
        last_name = bleach.clean(request.form['lastName'])  # Sanitize last name
        email = bleach.clean(request.form['email'])  # Sanitize email
        country = bleach.clean(request.form['country'])  # Sanitize country
        gender = request.form['gender']  # Gender doesn't need sanitization
        services = request.form.getlist('service')  # Get list of selected services
        services_str = ','.join(services)  # Join the list into a string

        # Insert form data into the database
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(first_name, last_name, email, country, gender, service) VALUES (%s, %s, %s, %s, %s, %s)", # %s to avoid sql injection
                    (username, last_name, email, country, gender, services_str))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('success'))
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
