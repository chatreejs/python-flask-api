from mongoengine import Document, StringField

class Subjects(Document):
    subject_id = StringField(required=True, primary_key=True)
    code = StringField(required=True, unique=True)
    name = StringField(required=True)
    instructor = StringField(required=True)
