from mongoengine import *


class User(Document):
    login = StringField(max_length=50, required=True, unique=True)
    hash_string = StringField(max_length=61, required=True)


class Guest(Document):
    login = StringField(max_length=50, required=True, unique=True)


class SpellAnswer(Document):
    owner = ReferenceField(Guest, reverse_delete_rule=CASCADE)
    answer = StringField()
    meta = {
        'indexes': [
            {
                'fields': ['-owner', '-answer'],
                'unique': True
            }
        ]

    }

    def __str__(self):
        return 'Owner: %s - Answer: %s' % self.owner, self.answer


class MathAnswer(Document):
    owner = ReferenceField(Guest, reverse_delete_rule=CASCADE)
    answer = StringField()

    meta = {
        'indexes': [
            {
                'fields': ['-owner', '-answer'],
                'unique': True
            }
        ]

    }


class SpellEntry(Document):
    image_name = StringField(unique=True)
    array_letters = ListField(StringField(max_length=1, min_length=1))
    answer = StringField(required=True)
    level = IntField(min_value=1, max_value=9)
    user_answers = ListField(ReferenceField(SpellAnswer))


class MathEntry(Document):
    expression = StringField(required=True, unique=True)
    level = IntField(min_value=1, max_value=9)
    user_answers = ListField(ReferenceField(MathAnswer))


