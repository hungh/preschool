from global_const import KEY_LOGIN, KEY_PASSWORD, DEBUG_MODE, WRONG_CREDENTIAL
from db_config import DB_HOST, DB_PORT, DB_NAME
from flask import Flask, render_template, request
from controller import add_guest, add_user, create_spell_entry, add_spell_entry
from controller import  get_spell_entry, create_math_entry, add_math_entry, get_math_entry
from mongoengine import connect

app = Flask(__name__)
app.config.from_pyfile('db_config.py')
db = connect(DB_NAME, host=DB_HOST, port=DB_PORT)


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


@app.route("/test")
def test_db():
    img_name = 'apple.png'
    guest_name = 'emma2'
    add_user('admin3', 'password')
    add_guest(guest_name)
    create_spell_entry(img_name, ['a', 's', 'p', 'p', 'k', 'l', 'e'], 'apple', 1)
    add_spell_entry(img_name, guest_name, 'apple2')
    for spell_entry in get_spell_entry(img_name, guest_name):
        print('Entry:' + spell_entry.answer)

    expression1 =  '2 + 3'
    create_math_entry(expression1, 1)
    add_math_entry(expression1, guest_name, '5')

    for math_entry in get_math_entry(expression1, guest_name):
        print('Entry:' + math_entry.answer)

    return 'OK'


if __name__ == "__main__":
    app.run(debug=DEBUG_MODE)