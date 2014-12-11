from mongoengine import *


class User(Document):
    login = StringField(max_length=50, required=True, unique=True)
    hash_string = StringField(max_length=61, required=True)

    meta = {'allow_inheritance': True}


class Guest(User):
    name = StringField(required=True)


class SpellEntry(Document):
    sid = FloatField(min_value=1, unique=True)
    image_name = StringField()
    array_letters = ListField(StringField(max_length=1, min_length=1))
    answer = StringField(required=True)
    level = IntField(min_value=1, max_value=9)


class MathEntry(Document):
    mid = FloatField(min_value=1, unique=True)
    expression = StringField(required=True)
    level = IntField(min_value=1, max_value=9)


class SpellAnswer(Document):
    owner = ReferenceField(Guest, reverse_delete_rule=CASCADE)
    spell_entry = ReferenceField(SpellEntry, required=True, reverse_delete_rule=CASCADE)
    answer = StringField()


class MathAnswer(Document):
    owner = ReferenceField(Guest, reverse_delete_rule=CASCADE)
    math_entry = ReferenceField(MathEntry, required=True, reverse_delete_rule=CASCADE)
    answer = StringField()
