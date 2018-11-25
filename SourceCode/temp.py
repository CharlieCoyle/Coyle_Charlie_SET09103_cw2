import os
import bcrypt
import sqlite3
from  flask  import  Flask , render_template, request, session ,url_for, jsonify, redirect, g
import json


from  flask  import Flask

app = Flask(__name__)
app.secret_key = 'gtdfU_FGGfkLOAAfc lxASsSSldxskl@'
db_location = "var/info.db"
def  get_db():
	db = getattr(g, 'db', None)
	if db is None:
		db = sqlite3.connect(db_location)
		g.db = db
	return db


@app.teardown_appcontext
def  close_db_connection(exception):
	db = getattr(g, 'db', None)
	if db is not None:
		db.close()

def  init_db():
	with app.app_context():
		db = get_db()
		with app.open_resource('schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()

def  check_auth(username , password):
	db = get_db()
	info = db.cursor().execute("SELECT username,password FROM accounts")
	info = info.fetchall()
	pasword = password.encode("utf-8")
	for item in (info):
		if(username == item[0] and item[1].encode("utf-8") == bcrypt.hashpw(password.item[1].encode("utf-8"))):
			return True
	return False


@app.route("/AdventureNation/Register", methods=["POST","GET"])
def  Registration():

        db = get_db()
        if request.method == "POST":
                username = request.form["username"]
                password = request.form["password"]
                password = password.encode("utf-8")
                hashedpw = bcrypt.hashpw(password, bcrypt.gensalt)
		favorite = None
                if (hashedpw is not None and username is not None):
                        db.cursor.execute("INSERT INTO accounts(username, password, favorite) values (?,?,?)",(username,hashedpw,favorite))
                        db.comit()
			return redirect (url_for(".SignIn"))
        return render_template("SignUp.html")


@app.route("/AdventureNation/SignIn", methods=["POST","GET"])
def  SignIn():
	db = get_db()
	if request.method == "POST":
		username = request.form['Username']
		password = request.form['Password']
		if check_auth(username,password):
			session['Curent_User'] = username
			return redirect (url_for(".HomepageSlected"))
	return render_template("SignIn.html")

#Home Page
@app.route('/AdventureNation')
def  HomepageSlected(name=None):
        return  render_template('home.html')
#Item Selected Page
@app.route('/AdventureNation/Situation')
@app.route('/AdventureNation/Situation/')
@app.route('/AdventureNation/Situation/<game>')
@app.route('/AdventureNation/Situation/<game>/<place>')
def  GameSlected(game=None,place=None):
	if place == "Exit":
		return redirect("http://set09103.napier.ac.uk:9120/AdventureNation", code=302)
	try:
       		SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
		if game is not None:
    			json_url = os.path.join(SITE_ROOT, "static/" + game + ".json" )
    			data = json.load(open(json_url))
			UrlHelper = game + "/"
		#if broken remove
		#for i, e in enumerate(data):
       		#	if  place == next(iter(e)):
            	#		return render_template('situation.html', game=game, data=e, place=place)
        		return render_template('situation.html',UrlHelper=UrlHelper ,game=game, data=data, place=place)
		return render_template('situation.html', game=game, place=place)
	except IOError:
		page ='''
        	<html><body>
         	<h1 style ="text-align: center"> This stoty is yet to be written</h1>
         	<h2 style ="text-align: center">The Story you are looking for dosen't exist<h2>
        	</body></html> '''
		return page, 404

@app.route('/getjson/<item>')
def  postJsonHandler(item=None):
    url = url_for ('static', filename = item + '.json')
    return "<a href=%s>file</a>" %  url

#error out page
@app.errorhandler(404)
def  page_not_Found(error):
        page ='''
	<html><body>
         <h1 style ="text-align: center"> 404 You seem to have gotten lost</h1>
         <h2 style ="text-align: center">The page you are looking for dosen't exist<h2>
        </body></html> '''
        return page, 404

if  __name__  == "__main__":
        app.run(host='0.0.0.0', debug=True)

