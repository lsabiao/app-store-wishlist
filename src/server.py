import time
import sqlite3

import updater

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



#helper functions
def get_cookie(request):
    #this could be a decorator
    cookie = request.get_cookie("hash")
    con = sqlite3.connect("wishlist.db")
    cur = con.cursor()
    query = cur.execute(f"SELECT username FROM user WHERE cookie='{cookie}'")
    result = query.fetchone()
    if(result):
        pass
    else:
        redirect("/login")

def generate_cookie():
    return str(hash(int(time.time())))

def get_user(username,password):
    con = sqlite3.connect("wishlist.db")
    cur = con.cursor()
    query = cur.execute(f"SELECT username FROM user WHERE username='{username}' AND password='{password}'")
    result = query.fetchone()
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
        cur.execute(f"UPDATE user SET cookie='{generated_hash}'")
        con.commit()
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

run(host='0.0.0.0', port=8180, debug=True)
