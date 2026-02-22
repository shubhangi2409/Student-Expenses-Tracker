from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Shu2409#'   # ✅ Updated Password
app.config['MYSQL_DB'] = 'expense_tracker'

mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM expenses")
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', expenses=data)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        amount = request.form['amount']
        category = request.form['category']
        date = request.form['date']
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO expenses (title, amount, category, date) VALUES (%s, %s, %s, %s)",
            (title, amount, category, date)
        )
        mysql.connection.commit()
        cur.close()
        return redirect('/')
    return render_template('add.html')

@app.route('/delete/<int:id>')
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM expenses WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)