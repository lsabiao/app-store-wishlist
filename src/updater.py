import bot
import sqlite3
from urllib import request, parse

def clean_query(query):
    return query.replace(";","").replace("--",'')

def open_db():
    con = sqlite3.connect("wishlist.db")
    cur = con.cursor()
    return [con,cur]

def close_db(db):
    db[0].commit()
    db[1].close()
    db[0].close()

def get_wishlist():
    db = open_db()
    all = db[1].execute(clean_query("SELECT id, name, price, rating, count, icon FROM app"))
    result = all.fetchall()
    close_db(db)
    return result

def add_new_app(id):
    print(f"Adding {id} to the wishlist.")
    app = bot.fetch(id)
    if(app):
        try:
            db = open_db()
            db[1].execute(clean_query(f"INSERT INTO app VALUES ('{id}', '{app.name}', {app.price}, {app.rating}, '{app.rating_amount}', '{app.icon}')"))
            close_db(db)
            return True
        except:
            raise
            return False


def compare_with_db(id):
    db = open_db()
    query = db[1].execute(clean_query(f"SELECT id, price, name FROM app where id='{id}'"))
    result = query.fetchone()
    close_db(db)
    id = result[0]
    price = float(result[1])
    name = result[2]

    print(f"Checking [{name}]: ", end="", flush=True)
    
    try:
        app = bot.fetch(id)
    except:
        app = None
    if(app):
        if(app.price < price): #better price!
            print(" {price} to {app.price}", flush=True)
            #notify
            
            #simple push
            data = parse.urlencode({'key': '<_YOUR_KEY_HERE_>', 'title': '{name}', 'msg': '{price} -> {app.price}', 'event': 'event'}).encode()
            req = request.Request("https://api.simplepush.io/send", data=data)
            request.urlopen(req)

        else:
            print("nothing to report", flush=True)

        db = open_db()
        db[1].execute(clean_query(f"UPDATE app SET name='{app.name}', price={app.price}, rating={app.rating}, count='{app.rating_amount}', icon='{app.icon}' WHERE id='{app.id}'"))
        close_db(db)
    else:
        print(f"App {name} does not exist", flush=True)

def delete_app(id):
    print(f"Deleting {id}.")
    db = open_db()
    db[1].execute(clean_query(f"DELETE FROM app WHERE id={id}"))
    close_db(db)

def update_db():
    print("Updating the database...")
    for app in get_wishlist():
        compare_with_db(app[0])

def id_from_url(url):
    try:
        id = int(url)
        return id
    except ValueError:
        full_url = url.split('/')
        for part in full_url:
            if('id' in part):
                possible_id = part.split('?')[0].strip('id').strip()
                try:
                    int(possible_id)
                    return(possible_id)
                except:
                    continue

if __name__ == "__main__":
    update_db()

