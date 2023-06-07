from flask import Flask, render_template, request
import re
from dataclasses import dataclass
import mysql.connector

app = Flask(__name__)

# Database configuration
db_config = {
    'user': 'root',
    'password': 'password',
    'host': 'localhost',
    'database': 'wiley_edge_c361'
}

# Data class for user details
@dataclass
class UserDetails:
    name: str
    phone: str
    email: str
    country: str
    aadhaar: str
    pan: str

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route for user registration
@app.route('/register', methods=['POST'])
def register():
    # Get form data
    name = request.form['name']
    phone = request.form['phone']
    email = request.form['email']
    country = request.form['country']
    aadhaar = request.form['aadhaar']
    pan = request.form['pan']

    # Validate phone number using regex
    if not re.match(r'^[0-9]{10}$', phone):
        return 'Invalid phone number. It should be 10 digits.'

    # Validate email using regex
    if not re.match(r'^[a-zA-Z0-9._%+-]+@gmail.com$', email):
        return 'Invalid email. It should be in the format example@gmail.com.'

    # Validate Aadhaar number using regex
    if not re.match(r'^[0-9]{12}$', aadhaar):
        return 'Invalid Aadhaar number. It should be 12 digits.'

    # Validate PAN number using regex
    if not re.match(r'^[A-Za-z0-9]{10}$', pan):
        return 'Invalid PAN number. It should be 10 digits mixed with alphanumeric characters.'

    # Create UserDetails object
    user_details = UserDetails(name, phone, email, country, aadhaar, pan)

    # Save data to a text file
    try:
        with open('user_data.txt', 'a') as file:
            file.write(str(user_details) + '\n')
    except Exception as e:
        return 'Error occurred while saving data: ' + str(e)

    # Save data to MySQL database
    try:
        # Connect to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        create_table = """CREATE TABLE IF NOT EXISTS users789 (name varchar(255),phone bigint, email varchar(244),country varchar(20), aadhaar BIGINT, pan varchar(10))"""

        cursor.execute(create_table)
        print("Table created successfully")

        # Insert user details into the database
        insert_query = "INSERT INTO users789 (name, phone, email, country, aadhaar, pan) " \
                       "VALUES (%s, %s, %s, %s, %s, %s)"
        values = (user_details.name, user_details.phone, user_details.email,
                  user_details.country, user_details.aadhaar, user_details.pan)
        cursor.execute(insert_query, values)

        # Commit the changes
        conn.commit()

        return 'User registration successful!'
    except Exception as e:
        # Rollback the changes if an error occurred
        conn.rollback()
        return 'Error occurred while saving data to the database: ' + str(e)
    finally:
        # it will Close the database connection
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run()
