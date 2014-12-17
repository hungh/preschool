from global_const import KEY_LOGIN, KEY_PASSWORD, KEY_NAME, DEBUG_MODE,\
    WRONG_CREDENTIAL, KEY_ARR_LETTER, KEY_ANSWER, KEY_GUEST_ANSWER, KEY_LEVEL, KEY_IMAGE_NAME, SESSION_GUEST
from config import DB_HOST, DB_PORT, DB_NAME
from utils import allowed_file
from flask import Flask, render_template, request, session
from werkzeug import secure_filename
from controller import add_guest, get_guest, add_user, get_user, \
    create_spell_entry, add_spell_answer_to_guest, get_next_spell_entry
from models import SpellEntry
from mongoengine import connect
import bcrypt
import os



app = Flask(__name__)
app.config.from_pyfile('config.py')
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RTGFHb11'
db = connect(DB_NAME, host=DB_HOST, port=DB_PORT)


@app.route('/')
def index_page():
    return render_template("index.html")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/register_enter", methods=['POST'])
def register_enter():
    name = request.form[KEY_NAME]
    existing_guest = get_guest(name)
    if not existing_guest:
        add_guest(name)
    # save guest name into session
    session[SESSION_GUEST] = name
    first_spell = get_next_spell_entry(session[SESSION_GUEST])
    if first_spell:
        return render_template('work.html', msg=name, image_file='img/%s' % first_spell.image_name,
                               arr_letter=first_spell.array_letters, arr_answer=list(first_spell.answer))
    return render_template('review.html', answers=get_guest(session[SESSION_GUEST]).spell_answers)


@app.route("/guest_answer", methods=['POST'])
def guest_answer():
    guest_ans = request.form[KEY_GUEST_ANSWER]
    image_name = request.form[KEY_IMAGE_NAME].split('/')[1]  # LINUX

    if guest_ans:
        add_spell_answer_to_guest(session[SESSION_GUEST], image_name, guest_ans)

    next_spell_entry = get_next_spell_entry(session[SESSION_GUEST])
    if next_spell_entry:
        return render_template('work.html', msg=session[SESSION_GUEST],
                               image_file='img/%s' % next_spell_entry.image_name,
                               arr_letter=next_spell_entry.array_letters,
                               arr_answer=list(next_spell_entry.answer))

    return render_template('review.html', answers=get_guest(session[SESSION_GUEST]).spell_answers)


@app.route("/updatepass",  methods=['POST'])
def updatepass():
    login = request.form[KEY_LOGIN]
    if login == 'root':
        root_user = get_user(login)
        if not root_user:
            if add_user(login, request.form[KEY_PASSWORD]):
                return "Updated"
    return "Invalid root setup"


@app.route("/login", methods=['POST'])
def login_access():
    login = request.form[KEY_LOGIN]
    password = request.form[KEY_PASSWORD]
    user = get_user(login)
    if not user:
        if login == 'root':
            return render_template('create_password.html', hidden_login=login)
        return render_template("index.html", msg=WRONG_CREDENTIAL)

    if bcrypt.checkpw(password, user.hash_string):
        return render_template('spell_admin.html')

    return render_template("index.html", msg=WRONG_CREDENTIAL)


@app.route("/add_spell", methods=["POST"])
def add_spell():
    f = request.files['image_name']
    if f and allowed_file(f.filename):
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
        arr_letter = request.form[KEY_ARR_LETTER]
        answer = request.form[KEY_ANSWER]
        level = request.form[KEY_LEVEL]

        if create_spell_entry(f.filename, arr_letter.split(','), answer, level):
            return render_template('spell_admin.html', msg='Successfully saved')
    return render_template('spell_admin.html', err='Failed to add entry')


@app.route("/test")
def test_db():
    return 'OK'


if __name__ == "__main__":
    app.run('0.0.0.0', debug=DEBUG_MODE)