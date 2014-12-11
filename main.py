from global_const import KEY_LOGIN, KEY_PASSWORD, DEBUG_MODE, WRONG_CREDENTIAL
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index_page():
    return render_template("index.html")


@app.route("/login", methods=['POST'])
def login_access():
    login = request.form[KEY_LOGIN]
    password = request.form[KEY_PASSWORD]
    if login == 'hung' and password == 'password':
        return render_template('work.html', msg=login)
    else:
        return render_template("index.html", msg=WRONG_CREDENTIAL)


if __name__ == "__main__":
    app.run(debug=DEBUG_MODE)