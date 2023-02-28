import time
import datetime
import sqlite3
import threading
import subprocess
import updater
import hashlib
import bottle 

from bottle import (
    route,
    post,
    run, 
    template, 
    static_file, 
    redirect, 
    request,
    response,
)

def looper():
    while True:
        current_hour = datetime.datetime.now().hour
        print(current_hour, flush=True)
        if(current_hour > 22 and current_hour <=23):
            subprocess.run(["python", "updater.py"])
        time.sleep(3600)


#helper functions
def get_cookie(request):
    #this could be a decorator
    cookie = request.get_cookie("hash")
    con = sqlite3.connect("wishlist.db")
    cur = con.cursor()
    query = cur.execute(updater.clean_query(f"SELECT username FROM user WHERE cookie='{cookie}'"))
    result = query.fetchone()
    cur.close()
    con.close()
    if(result):
        pass
    else:
        redirect("/login")

def generate_cookie():
    return str(hash(int(time.time())))

def get_user(username,password):
    con = sqlite3.connect("wishlist.db")
    cur = con.cursor()
    password = hashlib.md5(password.encode()).hexdigest()
    query = cur.execute(updater.clean_query(f"SELECT username FROM user WHERE username='{username}' AND password='{password}'"))
    result = query.fetchone()
    cur.close()
    con.close()
    if(result):
        return True
    else:
        return False


# Static Routes
@route("/static/css/<filepath:re:.*\.css>")
def css(filepath):
    get_cookie(request)
    return static_file(filepath, root="static/css")


#real routes!
@route('/login')
def login():
    return template("login.html")


@post('/login')
def log_user():
    username = request.forms.get('username')
    password = request.forms.get('password')

    if(get_user(username,password)):
        #correct Login
        con = sqlite3.connect("wishlist.db")
        cur = con.cursor()
        generated_hash = generate_cookie()
        cur.execute(updater.clean_query(f"UPDATE user SET cookie='{generated_hash}'"))
        con.commit()
        cur.close()
        con.close()
        response.set_cookie("hash", generated_hash)

        redirect("/")
    redirect('/login')

@route('/')
def index():
    get_cookie(request)
    wishlist = list(updater.get_wishlist())
    return template("index.html", wishlist=wishlist)

@route('/update')
def update_database():
    get_cookie(request)
    updater.update_db()
    redirect('/?update=true')

@route('/add')
def add_app():
    get_cookie(request)
    to_add = request.query.get('id',False)
    if(to_add):
        id = updater.id_from_url(to_add)
        created = updater.add_new_app(id)
        if created:
            redirect('/?add=true')
    redirect('/?add=false')

@route('/delete')
def delete_app():
    get_cookie(request)
    to_delete = request.query.get('id',False)
    if(to_delete):
        updater.delete_app(to_delete)
    redirect('/?delete=true')





if __name__ == "__main__":
    run(host='0.0.0.0', port=8000, debug=True)


scheduler = threading.Thread(target= looper)
scheduler.start()
app = bottle.default_app()
