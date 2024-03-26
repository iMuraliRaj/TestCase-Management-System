from flask import Flask, render_template, request, redirect
import pyodbc

carsales = Flask(__name__)

def connection():
    s = 'MURALI\\SQLEXPRESS' #Your server name
    d = 'spanqa'
    u = 'sa' #Your login
    p = 'admin@123' #Your login password
    cstr = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+s+';DATABASE='+d+';UID='+u+';PWD='+ p
    conn = pyodbc.connect(cstr)
    print(conn)
    return conn


@carsales.route("/")
def main():
    modules = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM module_details where status='1'")
    for row in cursor.fetchall():
        modules.append({"code": row[0], "module": row[1], "description": row[2]})
    conn.close()
    return render_template("module.html", modules = modules)


@carsales.route("/addmodule", methods = ['GET','POST'])
def addmodule():
    f = open("demofile2.txt", "a")

    if request.method == 'GET':
        return render_template("addmodule.html", car = {})
    
    if request.method == 'POST':

        module = request.form["module"]
        description = request.form["description"]

        conn = connection()
        cursor = conn.cursor()

        modules = []
        cursor.execute("SELECT * FROM module_details")
        for row in cursor.fetchall():
            modules.append({"code": row[0], "module": row[1], "description": row[2]})

        module_count = len(modules)

        f.write(str(module_count))
                

        code = module_count+1

        qry = "insert into module_details values('{code}','{module}','{description}','1')".format(code =code, module = module,description=description)

       
        f.write(qry)
        f.close()

        cursor.execute(qry)
        conn.commit()
        conn.close()
        return redirect('/')
    


@carsales.route('/updatemodule/<code>',methods = ['GET','POST'])
def updatecar(code):
    modules = []
    conn = connection()
    cursor = conn.cursor()
    if request.method == 'GET':
        qry = "select * from module_details where code='{code}'".format(code=code)
        cursor.execute(qry)
        for row in cursor.fetchall():
            modules.append({"code": row[0], "module": row[1], "description": row[2]})
        conn.close()


        return render_template("addmodule.html", car = modules[0])
    
    if request.method == 'POST':

        module = request.form["module"]
        description = request.form["description"]

        f = open("demofile2.txt", "a")

        qry = "update module_details set modulename ='{module}' where code ='{code}'".format(module=module,code=code)       

        f.write(qry)
        f.close()

        cursor.execute(qry)

        qry = "update module_details set description ='{description}' where code ='{code}'".format(description=description,code=code)       

        cursor.execute(qry)

        conn.commit()
        conn.close()
        return redirect('/')



@carsales.route('/deletemodule/<code>')
def deletemodule(code):
    conn = connection()
    cursor = conn.cursor()

    f = open("demofile2.txt", "w")

    qry = "update module_details set status='-1' where code='"+code+"'"

    f.write(qry)
    f.close()

    cursor.execute(qry)
    conn.commit()
    conn.close()
    return redirect('/')

if(__name__ == "__main__"):
    carsales.run(debug=True,port=8001)