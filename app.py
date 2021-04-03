from flask import Flask, session, redirect, render_template, request,url_for
import mysql.connector

app=Flask(__name__)
app.config['SECRET_KEY'] = 'jsu3cl3a87' 

#---------------------------------------data mysql connector 
db = mysql.connector.connect(
    host= "localhost",
    user="root",
    password="su3cl3jo3m6") 
#print(db)#<mysql.connector.connection.MySQLConnection object at 0x7ff783387af0>
cursor = db.cursor() 
cursor.execute("CREATE DATABASE IF NOT EXISTS solchiwebsite")
cursor.execute("USE solchiwebsite")
cursor.execute("CREATE TABLE IF NOT EXISTS users ( id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,name VARCHAR(255) NOT NULL, username VARCHAR(255) NOT NULL, password VARCHAR(255) NOT NULL,time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP)")

#-------------------------------------------------- home
@app.route("/")
def home():
    username = session.get('username') # 取session
    if username :
        return redirect("/member/")
    else:
        return render_template("index.html")
#----------------------------------------------------登入
@app.route("/signin",methods=["POST"])
def signin():
    #得到表單資料
    username=request.form["username"]
    password=request.form["password"]
    cursor.execute("SELECT username FROM users WHERE username = %s and password = %s",(username, password))
    currentUser = cursor.fetchone()
    # cursor.execute("SELECT username FROM users WHERE password = %s",(password,))
    # currentPassword = cursor.fetchone()

    if currentUser :
        session['username'] = username
        # session['password'] = password
        return redirect("/member/")
    else:
        return redirect(url_for('error', message="帳號或密碼輸入錯誤,或您尚未註冊"))
#----------------------------------------------------註冊
@app.route("/signup",methods=["POST"])
def signup():
    #得到表單資料
    name=request.form["name"] 
    username=request.form["username"]
    password=request.form["password"]
    #若輸入完整資訊執行以下程式
    if name and username and password:
        #在資料庫select與目前輸入的username相同的名稱
        cursor.execute("SELECT username FROM users WHERE username = %s",(username,))
        currentUsers = cursor.fetchone()
        #如果已經存在username導入錯誤畫面
        if currentUsers:
            return redirect(url_for('error', message="帳號已被註冊"))
        #其他:將資料嵌入資料庫
        else:
            val = (name, username, password)
            sql = "INSERT INTO users (name, username,password) VALUES (%s, %s, %s)"
            cursor.execute(sql, val)
            db.commit()

        return redirect("/")
        
    #若輸入不完整資訊導入錯誤頁面
    else:
        return redirect(url_for('error', message="輸入不完整"))

#----------------------------------------------------會員
@app.route("/member/")
def member():
    username = session.get('username')  # 取session
    if username:
        return render_template("member.html",memberName=username)
    else:
        return redirect("/")
#----------------------------------------------------錯誤
@app.route("/error/")
def error():
    data=request.args.get("message")
    return render_template("error.html",errormessage=data)
#----------------------------------------------------登出
@app.route("/signout")
def signout():
    username = session.get('username') 
    if username:
        session.pop('username', None)
        return redirect("/")
    else:
        return redirect("/")

if __name__=="__main__":
    app.run(port=3000)