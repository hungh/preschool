from global_const import KEY_LOGIN, KEY_PASSWORD, KEY_NAME, DEBUG_MODE,\
    WRONG_CREDENTIAL, KEY_ARR_LETTER, KEY_ANSWER, KEY_GUEST_ANSWER, \
    KEY_LEVEL, KEY_IMAGE_NAME, GUEST_NAME
from config import DB_HOST, DB_PORT, DB_NAME
from utils import allowed_file
from flask import Flask, render_template, request, session
from werkzeug import secure_filename
from controller import add_guest, get_guest, add_user, get_user, \
    create_spell_entry, add_spell_answer_to_guest,\
    get_next_spell_entry, clear_spell_answer, get_spell_entry

from mongoengine import connect
import bcrypt
import os


app = Flask(__name__)
app.config.from_pyfile('config.py')
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RTGFHb11'
db = connect(DB_NAME, host=DB_HOST, port=DB_PORT)


def app_filter(d_func):
    def d_wrapper(*args, **kwargs):
        try:
            session[GUEST_NAME]
        except KeyError:
            return "You have logged out."
        return d_func(*args, **kwargs)

    return d_wrapper


def render_next_question(my_session):
    next_spell_entry = get_next_spell_entry(my_session[GUEST_NAME])
    if next_spell_entry:
        return render_template('work.html', msg=session[GUEST_NAME],
                               image_file='img/%s' % next_spell_entry.image_name,
                               arr_letter=next_spell_entry.array_letters,
                               arr_answer=list(next_spell_entry.answer))
    return None


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
    session[GUEST_NAME] = name
    first_spell = get_next_spell_entry(session[GUEST_NAME])
    if first_spell:
        return render_template('work.html', msg=name, image_file='img/%s' % first_spell.image_name,
                               arr_letter=first_spell.array_letters, arr_answer=list(first_spell.answer))
    return render_template('review.html', answers=get_guest(session[GUEST_NAME]).spell_answers)


@app.route("/review_test", methods=['GET'])
def review_test():
    return render_template('review.html', answers=get_guest(session[GUEST_NAME]).spell_answers)


@app.route("/back_to_test", methods=['GET'])
def back_to_test():
    first_spell = get_next_spell_entry(session[GUEST_NAME])
    if first_spell:
        return render_template('work.html', msg=session[GUEST_NAME], image_file='img/%s' % first_spell.image_name,
                               arr_letter=first_spell.array_letters, arr_answer=list(first_spell.answer))
    return review_test()


@app.route("/go_to_test", methods=['GET'])
def go_to_test():
    image_name = request.args.get('image_name', '')
    spell_entry = get_spell_entry(image_name)
    if spell_entry:
        return render_template('work.html', msg=session[GUEST_NAME], image_file='img/%s' % spell_entry.image_name,
                               arr_letter=spell_entry.array_letters, arr_answer=list(spell_entry.answer))
    return "Error retrieving data"



@app.route("/guest_answer", methods=['POST'])
@app_filter
def guest_answer():
    guest_ans = request.form[KEY_GUEST_ANSWER]
    image_name = request.form[KEY_IMAGE_NAME].split('/')[1]  # LINUX

    if guest_ans:
        add_spell_answer_to_guest(session[GUEST_NAME], image_name, guest_ans)

    next_question_rendered = render_next_question(session)
    if not next_question_rendered:
        return render_template('review.html', answers=get_guest(session[GUEST_NAME]).spell_answers)
    return next_question_rendered


@app.route("/retake_test", methods=['GET'])
def retake_test():
    clear_spell_answer(session[GUEST_NAME])
    return render_next_question(session)


@app.route("/updatepass",  methods=['POST'])
def update_password():
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
        # successful login
        session[GUEST_NAME] = login
        return render_template('spell_admin.html')

    return render_template("index.html", msg=WRONG_CREDENTIAL)


@app.route("/logout", methods=["POST", "GET"])
def logout_access():
    try:
        del session[GUEST_NAME]
    except KeyError:
        pass
    return render_template("index.html")


@app.route("/add_spell", methods=["POST"])
def add_spell():
    if not session[GUEST_NAME] or session[GUEST_NAME] != 'root':
        return "Access denied"

    f = request.files['image_name']
    if f and allowed_file(f.filename):
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
        arr_letter = request.form[KEY_ARR_LETTER]
        answer = request.form[KEY_ANSWER]
        level = request.form[KEY_LEVEL]

        if create_spell_entry(f.filename, list(arr_letter), answer, level):
            return render_template('spell_admin.html', msg='Successfully saved')
    return render_template('spell_admin.html', err='Failed to add entry')


@app.route("/test")
def test_db():
    return 'OK'


if __name__ == "__main__":
    app.run('0.0.0.0', debug=DEBUG_MODE)