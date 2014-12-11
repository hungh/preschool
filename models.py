from mongoengine import *


class User(Document):
    login = StringField(max_length=50, required=True, unique=True)
    hash_string = StringField(max_length=61, required=True)


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


class SpellAnswer(EmbeddedDocument):
    spell_entry = ReferenceField(SpellEntry, required=True)
    answer = StringField()


class MathAnswer(EmbeddedDocument):
    math_entry = ReferenceField(MathEntry, required=True)
    answer = StringField()


class Guest(Document):
    name = StringField(required=True)
    spell_entries = ListField(EmbeddedDocumentField(SpellEntry))
    math_entries = ListField(EmbeddedDocumentField(MathAnswer))