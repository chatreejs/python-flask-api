from flask_bcrypt import generate_password_hash, check_password_hash

from mongoengine import Document, StringField, EmailField, ReferenceField, ListField


class Users(Document):
    user_id = StringField(required=True, primary_key=True)
    username = StringField(required=True, unique=True)
    password = StringField(required=True, min_length=6, regex=None)
    firstName = StringField(required=True)
    lastName = StringField(required=True)
    email = EmailField(required=True, unique=True)
    subjects = ListField(ReferenceField('Subjects'))

    def generate_pw_hash(self):
        self.password = generate_password_hash(
            password=self.password).decode('utf-8')
    # Use documentation from BCrypt for password hashing
    generate_pw_hash.__doc__ = generate_password_hash.__doc__

    def check_pw_hash(self, password: str):
        return check_password_hash(pw_hash=self.password, password=password)
    # Use documentation from BCrypt for password hashing
    check_pw_hash.__doc__ = check_password_hash.__doc__

    def save(self, *args, **kwargs):
        # Overwrite Document save method to generate password hash prior to saving
        if self._created:
            self.generate_pw_hash()
        super(Users, self).save(*args, **kwargs)
