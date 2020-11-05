from django.db import models

# Create your models here.
from django.db import models
import re
from datetime import date, datetime

# Create your models here.
class UserManager(models.Manager):
    def validate_registration(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        PASSWORD_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        # SpecialSym =['$', '@', '#', '%']
        if len(postData['first_name_txt']) < 2:
             errors["first_name"] = "First name should be at least 2 characters long."
        if len(postData['last_name_txt']) < 2:
             errors["last_name"] = "Last name should be at least 2 characters long."
        if not EMAIL_REGEX.match(postData['email_txt']):
            errors['email'] = ("Invalid email address!")
        elif User.objects.filter(email=postData['email_txt']):
            errors["email"] = "It looks like '" + postData['email_txt'] + "' has already registered. Try logging in."  
        if postData['b_day_dt'] == "":
            errors['b_day'] = "You must enter a birth date."
        else:
            # convert the birthdate into a date object
            b_day_date = datetime.strptime(postData['b_day_dt'], '%Y-%m-%d')
            if b_day_date > datetime.now():
                errors['b_day'] = "Your birthday must be in the past."
            # elif (datetime.now().year - b_day_date.year) < 13:
            #     errors['b_day'] = "You must be older than 13 years old to register on this site."
        if postData['password_txt'] != postData['conf_password_txt']:
            errors['conf_password'] = "Your password is different than your confirmed password. Please make sure they are the same."
        if len(postData['password_txt']) < 8:
                errors['password'] = "Your password should be at least 8 characters long."
        else:
            if not any(char.isdigit() for char in postData['password_txt']):
                errors['password'] = "Your password should contain at least one number."
            elif not any(char.islower() for char in postData['password_txt']):
                errors['password'] = "Your password should contain at least one lowercase letter."
            elif not any(char.isupper() for char in postData['password_txt']):
                errors['password'] = "Your password should contain at least one uppercase letter."
            # elif not any(char in SpecialSym for char in passwd): 
            #     errors['password'] = "Your password should have at least one of the symbols $@#')
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    #books_uploaded = a list of books this user has uploaded
    #favorite_books = a list of this user's favorite books
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class BookManager(models.Manager):
    def validate_data(self, postData):
        errors={}
        if len(postData['title_txt']) == 0:
             errors["title"] = "Please provide a book title."
        if len(postData['desc_txt']) < 5:
             errors["desc"] = "Book description must be longer than 5 characters."
        return errors
        
class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    uploaded_by = models.ForeignKey(User, related_name="books_uploaded", on_delete = models.CASCADE)
    favorite_users = models.ManyToManyField(User, related_name="favorite_books")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()