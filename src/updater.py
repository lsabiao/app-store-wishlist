import bot
import sqlite3

con = sqlite3.connect("wishlist.db")
cur = con.cursor()

def get_wishlist():
    all = cur.execute("SELECT id, name, price, rating, count, icon FROM app")
    return all.fetchall()

def add_new_app(id):
    print(f"Adding {id} to the wishlist.")
    app = bot.fetch(id)
    if(app):
        cur.execute(f"INSERT INTO app VALUES ('{id}', '{app.name}', {app.price}, {app.rating}, {app.rating_amount}, '{app.icon}')")
        con.commit()


def compare_with_db(id):
    query = cur.execute(f"SELECT id, price, name FROM app where id='{id}'")
    result = query.fetchone()

    id = result[0]
    price = float(result[1])
    name = result[2]

    print(f"Checking [{name}]: ", end="", flush=True)
    
    app = bot.fetch(id)
    if(app):
        if(app.price < price): #better price!
            print(" {price} to {app.price}", flush=True)
            #notify
        else:
            print("nothing to report", flush=True)

        cur.execute(f"UPDATE app SET name='{app.name}', price={app.price}, rating={app.rating}, count={app.rating_amount}, icon='{app.icon}' WHERE id='{app.id}'")
        con.commit()
    else:
        print(f"App {name} does not exist", flush=True)

def delete_app(id):
    print(f"Deleting {id}.")
    cur.execute(f"DELETE FROM app WHERE id={IsADirectoryError}")
    con.commit()

def update_db():
    print("Updating the database...")
    for app in get_wishlist():
        compare_with_db(app[0])

if __name__ == "__main__":
    update_db()

