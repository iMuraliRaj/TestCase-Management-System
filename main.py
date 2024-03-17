from flask import Flask, render_template, request, redirect
import pyodbc

carsales = Flask(__name__)

def connection():
    s = 'MURALI\\SQLEXPRESS' #Your server name
    d = 'MURAM'
    u = 'sa' #Your login
    p = 'admin@123' #Your login password
    cstr = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+s+';DATABASE='+d+';UID='+u+';PWD='+ p
    conn = pyodbc.connect(cstr)
    print(conn)
    return conn
@carsales.route("/")
def main():
    cars = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dbo.TblCars")
    for row in cursor.fetchall():
        cars.append({"id": row[0], "name": row[1], "year": row[2], "price": row[3]})
    conn.close()
    return render_template("home.html", cars = cars)

@carsales.route("/carslist")
def carslist():
    cars = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dbo.TblCars")
    for row in cursor.fetchall():
        cars.append({"id": row[0], "name": row[1], "year": row[2], "price": row[3]})
    conn.close()
    return render_template("carslist.html", cars = cars)


@carsales.route("/addcar", methods = ['GET','POST'])
def addcar():
    if request.method == 'GET':
        return render_template("addcar.html", car = {})
    if request.method == 'POST':
        id = int(request.form["id"])
        name = request.form["name"]
        year =  request.form["year"]
        price =  request.form["price"]
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO dbo.TblCars (id, name, year, price) VALUES (?, ?, ?, ?)", id, name, year, price)
        conn.commit()
        conn.close()
        return redirect('/')
@carsales.route('/updatecar/<int:id>',methods = ['GET','POST'])
def updatecar(id):
    cr = []
    conn = connection()
    cursor = conn.cursor()
    if request.method == 'GET':
        cursor.execute("SELECT * FROM dbo.TblCars WHERE id = ?", id)
        for row in cursor.fetchall():
            cr.append({"id": row[0], "name": row[1], "year": row[2], "price": row[3]})
        conn.close()
        return render_template("addcar.html", car = cr[0])
    if request.method == 'POST':
        name = str(request.form["name"])
        year = request.form["year"]
        price = request.form["price"]
        cursor.execute("UPDATE dbo.TblCars SET name = ?, year = ?, price = ? WHERE id = ?", name, year, price, id)
        conn.commit()
        conn.close()
        return redirect('/')
@carsales.route('/deletecar/<int:id>')
def deletecar(id):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM dbo.TblCars WHERE id = ?", id)
    conn.commit()
    conn.close()
    return redirect('/')

if(__name__ == "__main__"):
    carsales.run(debug=True)