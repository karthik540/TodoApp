from flask import Flask , render_template , request , jsonify , session
import pymysql.cursors , os
from cryptography.fernet import Fernet

app = Flask(__name__)
app.secret_key = os.urandom(24)
encryption_secret_key = b'BrzB6MUAmWWzMUS6gA03Lwei8SKaTRIQGfXvvKVUsZE='
f = Fernet(encryption_secret_key)

@app.route('/')
def index():
    return render_template('index.html' , data = {})

@app.route('/app/agent' , methods= ['POST' , 'GET'])
def agent_registration():
    agent_id = request.form['agent_id']
    password = request.form['password']

    ####    Password encryption...
    encoded_message = password.encode()
    encrypted_password = f.encrypt(encoded_message)
    encrypted_password = encrypted_password.decode()
    print(encrypted_password)    

    ####    MySQl connection...
    connection = pymysql.connect(host = 'localhost' , user = 'root' , password = 'karthik540' , db = 'deku')
    cursor = connection.cursor()
    sql_query = "INSERT INTO agent (agent_id , password) VALUES(%s , %s);"
    data = (agent_id , encrypted_password)

    try:
        result = cursor.execute(sql_query , data)
    except:
        print('Registration UnSuccessful !')
        response = {
            'status' : 'account creation failed',
            'status_code' : 401
        }
        return jsonify(response)

    if result == 1:
        print('Registration Successful !')
        connection.commit()
        response = {
            'status' : 'account created',
            'status_code' : 200
        }
    else:
        print('Registration UnSuccessful !')
        response = {
            'status' : 'account creation failed',
            'status_code' : 401
        }
    return jsonify(response)

@app.route('/app/agent/auth' , methods= ['POST' , 'GET'])
def agent_authentication():
    agent_id = request.form['agent_id']
    password = request.form['password']

    connection = pymysql.connect(host = 'localhost' , user = 'root' , password = 'karthik540' , db = 'deku')
    cursor = connection.cursor()

    ####    Password decryption...
    sql_query = "SELECT password FROM agent WHERE agent_id= %s"
    data = (agent_id)
    result = cursor.execute(sql_query , data)

    if not result == 1:
        print('Logged in FAILED !')
        response = {
            'status' : 'failure',
            'status_code' : 401          
        }
        return jsonify(response)

    qdata = cursor.fetchone()
    decrypted_password = f.decrypt(qdata[0].encode())
    decrypted_password = decrypted_password.decode()
    if decrypted_password == password:
            print('Logged in Successfully !')
            session['agent_id'] = agent_id
            session['password'] = password
            session['loggedIn'] = True
            response = {
                'status' : 'success',
                'agent_id' : int(agent_id),
                'status_code' : 200          
            }
    else:
        print('Logged in FAILED !')
        response = {
            'status' : 'failure',
            'status_code' : 401          
        }
    return jsonify(response)

@app.route('/app/sites' , methods= ['POST' , 'GET'])
def addTodo():
    ###     Recieving all data...
    agent_id = request.args.get('agent', type = int)
    title = request.form['title']
    description = request.form['description']
    category = request.form['category']
    due_date = request.form['due_date']

    print(agent_id)
    print(title + description + category + due_date)

    
    ####    MySQl connection...
    connection = pymysql.connect(host = 'localhost' , user = 'root' , password = 'karthik540' , db = 'deku')
    cursor = connection.cursor()
    sql_query = "INSERT INTO todo (agent_id , title , description , category , due_date) VALUES(%s , %s , %s , %s , %s);"
    data = (agent_id , title , description , category , due_date)

    try:
        result = cursor.execute(sql_query , data)
    except:
        print('Save UnSuccessful !')
        response = {
            'status' : 'failed',
            'status_code' : 401
        }
        return jsonify(response)
    
    if result == 1:
        print('Save Successful !')
        connection.commit()
        response = {
            'status' : 'success',
            'status_code' : 200          
        }
    else:
        print('Save UnSuccessful !')
        response = {
            'status' : 'failed',
            'status_code' : 401
        }
    return jsonify(response)

@app.route('/app/sites/list/' , methods= ['GET'])
def todoList():
    ###     Recieving all data...
    agent_id = request.args.get('agent', type = int)

    ####    MySQl connection...
    connection = pymysql.connect(host = 'localhost' , user = 'root' , password = 'karthik540' , db = 'deku')
    cursor = connection.cursor()
    sql_query = "SELECT id , title , description , category , due_date FROM todo WHERE agent_id = %s ORDER BY due_date"
    data = (agent_id)

    try:
        result = cursor.execute(sql_query , data)
    except:
        print('Fetch UnSuccessful !')
        response = {
            'status' : 'failed',
            'status_code' : 401
        }
        return jsonify(response)
    
    qdata = cursor.fetchall()
    return jsonify(qdata)


if __name__ == '__main__':
    app.run(debug=True)