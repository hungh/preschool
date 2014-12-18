from models import User, Guest, SpellEntry, MathEntry
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
    return Guest(login=login_name, spell_answers=dict(), math_answers=dict()).save()


def get_guest(login_name):
    """
    :param login_name: string
    :return: Document
    """
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
    """
    :param login_name: string
    :return: Document
    """
    return User.objects(login=login_name).first()


# Spelling entry section
@except_dup_key
def create_spell_entry(my_image_name, my_array_letters, my_answer, my_level):
    """
    :param my_image_name: string the name of image
    :param my_array_letters: array
    :param my_level: integer
    :return: Document
    """
    return SpellEntry(image_name=my_image_name, array_letters=my_array_letters,
                      level=my_level, answer=my_answer).save()


def get_spell_entry(my_image_name):
    """
    :param my_image_name: string
    :return: array of Document
    """
    return SpellEntry.objects(image_name=my_image_name).first()


# Math Section
@except_dup_key
def create_math_entry(my_expression, my_level):
    """
    :param my_expression: string
    :param my_level: integer
    :return: Document
    """
    return MathEntry(expression=my_expression, level=my_level).save()


def get_math_entry(my_expression):
    """
    :param my_expression: string
    :return: array of Document
    """
    return MathEntry.objects(expression=my_expression).first()


def get_img_key(image_name):
    return image_name.split('.')[0]


def get_next_spell_entry(guest_name):
    guest = Guest.objects(login=guest_name).first()
    spell_answers = guest.spell_answers

    for spell_entry in SpellEntry.objects():
        try:
            key_image = get_img_key(spell_entry.image_name)
            spell_answers[key_image]
        except KeyError:
            return spell_entry

    return None


def add_spell_answer_to_guest(guest_name, image_name, answer):
    guest = get_guest(guest_name)
    key_image = get_img_key(image_name)
    guest.spell_answers[key_image] = answer
    guest.save()


def clear_spell_answer(guest_name):
    guest = get_guest(guest_name)
    guest.spell_answers = dict()
    guest.save()








