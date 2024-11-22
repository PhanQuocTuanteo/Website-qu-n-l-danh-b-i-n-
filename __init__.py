from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL



app = Flask(__name__)
app.secret_key = 'many random bytes'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'crud'

mysql = MySQL(app)

@app.route('/')
def Index():
    # Check if user is logged in using session
    if 'username' in session:  # Check if the user is logged in
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM students ORDER BY id DESC")  # Retrieve all student records
        data = cur.fetchall()  # Fetch all results
        cur.close()
        return render_template('index2.html', students=data)  # Pass student data to the template
    return render_template('login.html')  # Render login page directly if not authenticated



@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == "POST":
        try:
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            
            # Log the data being inserted for debugging
            print(f"Inserting: Name={name}, Email={email}, Phone={phone}")
            
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO students (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
            mysql.connection.commit()
            flash("Chèn Dữ Liệu Thành Công")
        except Exception as e:
            print(f"Error: {str(e)}")  # Log the error to the console
            flash(f"An error occurred: {str(e)}")
        return redirect(url_for('Index'))




@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Xoá Dữ Liệu Thành Công")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM students WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('Index'))





@app.route('/update',methods=['POST','GET'])
def update():

    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE students
               SET name=%s, email=%s, phone=%s
               WHERE id=%s
            """, (name, email, phone, id_data))
        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('Index'))





@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash("Username and password are required.")
            return redirect(url_for('login'))

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM flask_users WHERE username=%s AND password=%s", (username, password))
        user = cur.fetchone()
        cur.close()

        if user:
            session['username'] = username
            flash("Đăng Nhập Thành Công")
            return redirect(url_for('Index'))
        flash("Đăng Nhập thất bại. Vui lòng kiểm tra lại ")
        return redirect(url_for('login'))
    
    return render_template('login.html')





@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove the username from the session
    return redirect(url_for('Index'))  # Redirect to the Index page (login page)









if __name__ == "__main__":
    app.run(debug=True)