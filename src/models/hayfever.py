from mongoengine import Document, StringField

class Hayfever(Document):
    day = StringField()
    level = StringField()
    message = StringField()
