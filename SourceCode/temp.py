from  flask  import  Flask , render_template, url_for
app = Flask(__name__)

#Home Page
@app.route('/AdventureNation')
def  HomepageSlected(name=None):
        return  render_template('home.html')
#Item Selected Page
@app.route('/ccg_index/ccg')
@app.route('/ccg_index/ccg/')
@app.route('/ccg_index/ccg/<ccg>')
def  CCGSlected(ccg=None):
        return  render_template('item.html', ccg=ccg)
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
@app.route('/static/<img>')
def  static_example_img(img=None):
  start = '<img src="'
  url = url_for('static', filename = img + '.jpg')
  end = '">'
  return start+url+end, 200



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

