from bottle import route, run, template
import updater

@route('/')
def index():
    wishlist = list(updater.get_wishlist())
    return template("index.html", wishlist=wishlist)

run(host='0.0.0.0', port=8180, debug=True)