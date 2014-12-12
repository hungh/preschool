from models import User, Guest, SpellEntry, MathEntry, SpellAnswer, MathAnswer
from mongoengine import errors
import bcrypt


# Duplicate Key exception decorator
def except_dup_key(my_func):
    def decorated_wrapper(*args):
        ret_obj = None
        try:
            ret_obj = my_func(*args)
        except errors.NotUniqueError:
            print('Duplicated key found for a call %s' % my_func.__name__)
            pass
        return ret_obj

    return decorated_wrapper


@except_dup_key
def add_guest(login_name):
    """
    :param login_name: string
    :return: Document
    """
    return Guest(login=login_name).save()


def get_guest(login_name):
    return Guest.objects(login=login_name).first()


@except_dup_key
def add_user(login_name, password):
    """
    :param login_name: string
    :param password: string
    :return: Document
    """
    my_hash = bcrypt.hashpw(password, bcrypt.gensalt())
    return User(login=login_name, hash_string=my_hash).save()


def get_user(login_name):
    return User.objects(login=login_name).first()


@except_dup_key
def create_spell_entry(my_image_name, my_array_letters, my_answer, my_level):
    return SpellEntry(image_name=my_image_name, array_letters=my_array_letters,
                      level=my_level, answer=my_answer, user_answers=[]).save()


@except_dup_key
def add_spell_entry(my_image_name, guest_name, guest_answer):
    spell_entry = SpellEntry.objects(image_name=my_image_name).first()
    guest = get_guest(guest_name)
    if spell_entry:
        spell_answer = SpellAnswer(owner=guest, answer=guest_answer).save()
        spell_entry.user_answers.append(spell_answer)
        spell_entry.save()


def get_spell_entry(my_image_name, guest_name):
    same_owner_answer = []
    spell_entry = SpellEntry.objects(image_name=my_image_name).first()
    for one_answer in spell_entry.user_answers:
        if hasattr(one_answer, 'owner') and one_answer.owner.login == guest_name:
            same_owner_answer.append(one_answer)
    return same_owner_answer




