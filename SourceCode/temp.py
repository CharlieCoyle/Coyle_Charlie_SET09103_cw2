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
	data = db.cursor().execute("SELECT username,password FROM accounts")
	data = data.fetchall()
	if data is None:
		print("wasnt saved bucko")
	password = password.encode("utf-8")
	for item in (data):
		if(username == item[0] and item[1].encode("utf-8") == bcrypt.hashpw(password,item[1].encode("utf-8"))):
			return True
	return False
def  update_account(conn, account):
	sql =''' UPDATE accounts
		SET favoraties = ?
		WHERE username = ?'''
	cur = conn.cursor()
	cur.execute(sql, account)


@app.route("/AdventureNation/Register", methods=["POST","GET"])
def  Registration():

        db = get_db()
        if request.method == "POST":
		db = get_db()
                username = request.form["username"]
                password = request.form["password"]
                password = password.encode("utf-8")
                hashedpw = bcrypt.hashpw(password, bcrypt.gensalt())
		favorite = 0
                if (hashedpw is not None and username is not None):
			print(hashedpw)
			print(username)
                        db.cursor().execute("INSERT INTO accounts(username, password, favorite) values (?,?,0)",(username,hashedpw))
                        db.commit()
			return redirect (url_for(".SignIn"))
        return render_template("SignUp.html")

@app.route("/AdventureNation/SignIn", methods=["POST","GET"])
def  SignIn():
	db = get_db()
	if request.method == "POST":
		username = request.form["username"]
		password = request.form["password"]
		if check_auth(username,password):
			session['Curent_User'] = username
			return redirect (url_for(".HomepageSlected"))
	return render_template("SignIn.html")

#Home Page
@app.route('/AdventureNation', methods=["POST","GET"])
def  HomepageSlected(name=None):
	if request.method == "POST":
		db = get_db
		favorite = request.form["FaveLocation"]
		conn = create_connection(db)
		with conn:
			Curent_user = session['Curent_User']
			if Curent_user is not null:
				update_account(conn,(favorite,Curent_User))
				return  render_template('home.html',Curent_User=Curent_User)
	try:
		Curent_User = session['Curent_User']
		return  render_template('home.html',Curent_User=Curent_User)
	except:
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
			try:
				Curent_User = session['Curent_User']
				return render_template('situation.html',UrlHelper=UrlHelper ,game=game, data=data, place=place, Curent_User=Curent_User)
			except:
				Curent_User = None
        			return render_template('situation.html',UrlHelper=UrlHelper ,game=game, data=data, place=place, Curent_User=Curent_User)
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

@app.route('/AdventureNation/Profile')
def  proflieload():
	favorite = None
	Curent_User = None
	try:
		Curent_User = session['Curent_User']
	except:
		favorite = None
	favrite = "GiantsLand"
	try:
		db = db_get()
		Curent_User = session['Curent_User']
		for item in  db.cursor().execute("SELECT * FROM accounts WHERE username='"+ Curent_User +"'"):
				favorite = item[2]
				print("WE did a thing")
		return render_template('Profile.html', Curent_User=Curent_User ,favorite=favorite)
	except:
		return render_template('Profile.html',Curent_User=Curent_User ,favorite=favorite)


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

