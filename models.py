from mongoengine import *


class User(Document):
    login = StringField(max_length=50, required=True, unique=True)
    hash_string = StringField(max_length=61, required=True)


class Guest(Document):
    login = StringField(max_length=50, required=True, unique=True)
    spell_answers = DictField()  # image_name, answer
    math_answers = DictField()   # expression, answer


class SpellEntry(Document):
    image_name = StringField(required=True, unique=True)
    array_letters = ListField(StringField(max_length=1, min_length=1), required=True)
    answer = StringField(required=True)
    level = IntField(min_value=1, max_value=9)


class MathEntry(Document):
    expression = StringField(required=True, unique=True)
    answer = StringField(required=True)
    level = IntField(min_value=1, max_value=9)
