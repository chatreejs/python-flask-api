from mongoengine import Document, StringField

class Subjects(Document):
    code = StringField(required=True, unique=True)
    name = StringField(required=True)
    instructor = StringField(required=True)