import os
from  flask  import  Flask , render_template, request, url_for, jsonify, redirect
import json
app = Flask(__name__)
#Home Page
@app.route('/AdventureNation')
def  HomepageSlected(name=None):
        return  render_template('home.html')
#Item Selected Page
@app.route('/AdventureNation/Situation')
@app.route('/AdventureNation/Situation/')
@app.route('/AdventureNation/Situation/<game>')
@app.route('/AdventureNation/Situation/<game>/<place>')
def GameSlected(game=None,place=None):
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
#Serch Selected Page
@app.route('/ccg_index/search')
@app.route('/ccg_index/search/<ccg>')
def  SearchSelected(ccg=None):
        return  render_template('search.html', ccg=ccg)
#about page
@app.route('/ccg_index/about')
def  AboutSelect(name=None):
        return render_template('ccginfo.html')
#image recovery

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

