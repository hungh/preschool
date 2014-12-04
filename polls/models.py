#from django.db import models
from mongoengine import *

# Create your models here.
connection = connect('test', host='10.10.13.226')


class User(Document):
    email = StringField(required=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)


class Comment(EmbeddedDocument):
    content = StringField()
    name = StringField(max_length=120)


class Post(Document):
    title = StringField(max_length=120, required=True)
    author = ReferenceField(User, reverse_delete_rule=CASCADE)
    tags = ListField(StringField(max_length=30))
    comments = ListField(EmbeddedDocumentField(Comment))

    meta = {'allow_inheritance': True}


class TextPost(Post):
    content = StringField()


class ImagePost(Post):
    image_path = StringField()


class LinkPost(Post):
    link_url = StringField()

hung = User(email='hungh@example.com', first_name='Hung', last_name='H').save()
john = User(email='john@example.com', first_name='John', last_name='Nguyen').save()

post1 = TextPost(title='Fun with MongoEngine', author=john)
post1.content = 'Took a look at MongoEngine today, looks pretty cool.'
post1.tags = ['mongodb', 'mongoengine']
post1.save()

post2 = LinkPost(title='MongoEngine Documentation', author=hung)
post2.link_url = 'http://docs.mongoengine.com/'
post2.tags = ['mongoengine']
post2.save()


print("Show all POST...")

for post in Post.objects:
    print(post.title)


print("Show all text posts...")
for post in TextPost.objects:
    print(post.content)

print('Posts with tags = mongodb')
for post in Post.objects(tags='mongodb'):
    print(post.title)


print('Number of Posts with tags = mongodb')
num_posts = Post.objects(tags='mongodb').count()
print('Found %d posts with tag "mongodb"' % num_posts)
