from bottle import route, run, template, static_file
import updater

# Static Routes
@route("/static/css/<filepath:re:.*\.css>")
def css(filepath):
    return static_file(filepath, root="static/css")

@route("/static/font/<filepath:re:.*\.(eot|otf|svg|ttf|woff|woff2?)>")
def font(filepath):
    return static_file(filepath, root="static/font")

@route("/static/img/<filepath:re:.*\.(jpg|png|gif|ico|svg)>")
def img(filepath):
    return static_file(filepath, root="static/img")

@route("/static/js/<filepath:re:.*\.js>")
def js(filepath):
    return static_file(filepath, root="static/js")




@route('/')
def index():
    wishlist = list(updater.get_wishlist())
    return template("index.html", wishlist=wishlist)

run(host='0.0.0.0', port=8180, debug=True)
