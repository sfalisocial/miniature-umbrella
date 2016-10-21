from __future__ import unicode_literals
from django.db import models
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
import bcrypt
# Create your models here.
class UserManager(models.Manager):
    def login(self, post):
        user_list = User.objects.filter(email=post['email'])
        if user_list:
            user = user_list[0]
            if bcrypt.hashpw(post['password'].encode(), user.password.encode()) == user.password:
                return user
        return None

    def register(self, post):
        encrypted_password= bcrypt.hashpw(post['password'].encode(), bcrypt.gensalt())
        User.objects.create(first_name=post['first_name'], last_name=post['last_name'], email=post['email'], password= encrypted_password)

    def validate_user_info(self, post):
        errors = []
        if len(post['first_name']) == 0:
            errors.append("First Name is required")
        elif len(post['first_name']) < 2:
            errors.append("First Name must be at least 2 characters")
        elif not post['first_name'].isalpha():
            errors.append("First Name must consist of letters only")

        if len(post['last_name']) == 0:
                errors.append("Last Name is required")
        elif len(post['last_name']) < 2:
            errors.append("Last Name must be at least 2 characters")
        elif not post['last_name'].isalpha():
            errors.append("Last Name must consist of letters only")

        if len(post['email'])< 1:
            errors.append("Error: Email cannot be empty")
        elif not EMAIL_REGEX.match(post['email']):
            errors.append("Error: Email must be a valid email")

        if len(post['password'])<8:
            errors.append("Error: Password cannot be empty OR less than 8 characters")
        elif post['password'] != post['passconf']:
            errors.append("Error: Password doesn't match!")

        if len(User.objects.filter(email=post['email'])) > 0:
            errors.append("Email address unavailable!")
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
