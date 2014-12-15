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
    :param my_answer: string
    :param my_level: integer
    :return: Document
    """
    return SpellEntry(image_name=my_image_name, array_letters=my_array_letters,
                      level=my_level, answer=my_answer, user_answers=[]).save()


@except_dup_key
def add_spell_entry(my_image_name, guest_name, guest_answer):
    """
    :param my_image_name: string file name of an image
    :param guest_name: string guest
    :param guest_answer: string
    """
    spell_entry = SpellEntry.objects(image_name=my_image_name).first()
    guest = get_guest(guest_name)
    if spell_entry:
        spell_answer = SpellAnswer(owner=guest, answer=guest_answer).save()
        spell_entry.user_answers.append(spell_answer)
        spell_entry.save()


def get_spell_entry(my_image_name, guest_name):
    """
    :param my_image_name: string
    :param guest_name: string
    :return: array of Document
    """
    same_owner_answer = []
    spell_entry = SpellEntry.objects(image_name=my_image_name).first()
    for one_answer in spell_entry.user_answers:
        if hasattr(one_answer, 'owner') and one_answer.owner.login == guest_name:
            same_owner_answer.append(one_answer)
    return same_owner_answer


# Math Section
@except_dup_key
def create_math_entry(my_expression, my_level):
    """
    :param my_expression: string
    :param my_level: integer
    :return: Document
    """
    return MathEntry(expression=my_expression, level=my_level, user_answers=[]).save()


@except_dup_key
def add_math_entry(my_expression, guest_name, guest_answer):
    """
    :param my_expression: string
    :param guest_name:  string
    :param guest_answer:  string
    """
    math_entry = MathEntry.objects(expression=my_expression).first()
    guest = get_guest(guest_name)
    if math_entry:
        math_answer = MathAnswer(owner=guest, answer=guest_answer).save()
        math_entry.user_answers.append(math_answer)
        math_entry.save()


def get_math_entry(my_expression, guest_name):
    """
    :param my_expression: string
    :param guest_name: string
    :return: array of Document
    """
    same_owner_answer = []
    math_entry = MathEntry.objects(expression=my_expression).first()
    for one_answer in math_entry.user_answers:
        if hasattr(one_answer, 'owner') and one_answer.owner.login == guest_name:
            same_owner_answer.append(one_answer)
    return same_owner_answer




