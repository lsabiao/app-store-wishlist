from bottle import route, run, template, static_file, redirect, request
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

#real routes!
@route('/')
def index():
    wishlist = list(updater.get_wishlist())
    return template("index.html", wishlist=wishlist)

@route('/update')
def update_database():
    updater.update_db()
    redirect('/?update=true')

@route('/add')
def add_app():
    to_add = request.query.get('id',False)
    if(to_add):
        id = updater.id_from_url(to_add)
        created = updater.add_new_app(id)
        if created:
            redirect('/?add=true')
    redirect('/?add=false')

@route('/delete')
def delete_app():
    to_delete = request.query.get('id',False)
    if(to_delete):
        updater.delete_app(to_delete)
    redirect('/?delete=true')

run(host='0.0.0.0', port=8180, debug=True)
