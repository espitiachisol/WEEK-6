from flask import Flask, session, redirect, render_template, request,url_for
import mysql.connector

app=Flask(__name__)
app.config['SECRET_KEY'] = 'jsu3cl3a87' #session需設定的私鑰

#---------------------------------------data mysql connector 
#Python 連接 MySQL 資料庫
db = mysql.connector.connect(
    host= "localhost",
    user="root",
    password="su3cl3jo3m6") #mySQL當初設定的密碼
#print(db)#<mysql.connector.connection.MySQLConnection object at 0x7ff783387af0>
cursor = db.cursor() 
#建立資料庫
cursor.execute("CREATE DATABASE IF NOT EXISTS solchiwebsite")
#使用資料庫
cursor.execute("USE solchiwebsite")
#建立表單
cursor.execute("CREATE TABLE IF NOT EXISTS users ( id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,name VARCHAR(255) NOT NULL, username VARCHAR(255) NOT NULL, password VARCHAR(255) NOT NULL,time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP)")

#-------------------------------------------------- home
@app.route("/")#沒有特別設定方法的話，預設是["GET"]
def home():
    username = session.get('username') # 取session
    #如果session中有會員登入狀態，轉至會員頁面，若沒有呈現html主頁
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
    #根據登入的帳號密碼搜尋資料庫，是否有對應的帳號密碼
    cursor.execute("SELECT username FROM users WHERE username = %s and password = %s",(username, password))
    currentUser = cursor.fetchone()
    # cursor.execute("SELECT username FROM users WHERE password = %s",(password,))
    # currentPassword = cursor.fetchone()
    #若有，把username儲存到session裡，轉至會員頁面
    if currentUser :
        session['username'] = username
        # session['password'] = password
        return redirect("/member/")
    #若沒有，轉至錯誤頁面
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
    #得到query string的message內容
    data=request.args.get("message")
    #將message內容動態帶入到html檔中，呈現在頁面上
    return render_template("error.html",errormessage=data)
#----------------------------------------------------登出
@app.route("/signout")
def signout():
    #從session中取得username
    username = session.get('username') 
    #若有username將username刪除,轉至root
    if username:
        session.pop('username', None)
        return redirect("/")
    #若沒有,直接轉至root
    else:
        return redirect("/")

if __name__=="__main__":
    app.run(port=3000)