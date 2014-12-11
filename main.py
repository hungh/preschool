from global_const import KEY_LOGIN, KEY_PASSWORD, DEBUG_MODE, WRONG_CREDENTIAL
from db_config import DB_HOST, DB_PORT, DB_NAME
from flask import Flask, render_template, request
from models import User, Guest, SpellEntry, MathEntry, SpellAnswer, MathAnswer
from mongoengine import connect, errors

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


    #admin = User(login="admin", hash_string="GHAFFASHDALSDHASJDA:DA877")
    #guest = Guest(login="guest", hash_string="FHSDADKANDAKSDASD", name="guest_name")
    #spell_entry = SpellEntry(sid=1, image_name="apple.png",
    #                            array_letters=['a', 's', 'p', 'p', 'k', 'l', 'e'], answer="apple", level=1)
    math_entry = MathEntry(mid=1, expression="2 + 3", level=1)




    #spell_answer = SpellAnswer(owner=guest, spell_entry=spell_entry, answer="applk")
    #spell_answer.save()
    #msg = "Saving spell answer"
    for spell_entry in SpellEntry.objects(sid='1'):
        res = spell_entry
        break

    for user in Guest.objects(name="guest_name"):
        guest_name = user
        break

    spell_answer = SpellAnswer(owner=guest_name, spell_entry=spell_entry, answer="applk")
    spell_answer.save()

    return res.image_name


if __name__ == "__main__":
    app.run(debug=DEBUG_MODE)