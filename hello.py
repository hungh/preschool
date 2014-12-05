from flask import Flask, session, url_for, render_template, request, make_response, escape, redirect
from flask.ext.pymongo import PyMongo
from werkzeug import secure_filename

app = Flask(__name__)

mongo = PyMongo(app)

@app.route("/")
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])

    return 'You are not logged in' #redirect(url_for('login'))

@app.route("/hello/<uname>")
def hello(uname=None):
    #online_users = mongo.db.users.find({'online': True})
    return render_template('hello.html', name=uname)

@app.route('/login', methods=['POST', 'GET'])
def login():
    #msg = None
    if request.method == 'POST':
        #username = request.form['username']
        #password = request.form['password']
        pass
    elif request.method == 'GET':
        #username = request.args.get('username', '')
        #password = request.args.get('password', '')
        session['username'] = request.args.get('password', '')
        return redirect(url_for('index'))

#    _msg = "You have passed {} and {}".format(username, password)
#    resp = make_response(render_template('login.html', msg=_msg))
#    resp.set_cookie('username', 'hungtest')
#    return resp

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['the_file']
        f.save('/tmp/uploads/' + secure_filename(f.filename))
    return "Done!"



@app.route('/user/<username>')
def profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return '[DEBUG]Post %d' % post_id


@app.errorhandler(404)
def not_found(error):
    resp = make_response(render_template('error.html'), 404)
    resp.headers['X-BadMove'] = 'Busted'
    return resp

with app.test_request_context():
    url_for('static', filename='index.html')
    url_for('static', filename='hello.html')
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('login', next='/'))
    print(url_for('profile', username='John Doe'))

if __name__ == "__main__":
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run(host='0.0.0.0', debug=True)  # never use debug in PROD

