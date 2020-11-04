from django.shortcuts import render, redirect
from favorite_books_app.models import User, Book
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):
    context = {
        'all_users':User.objects.all()
    }
    return render(request, "register_login.html", context)

def register(request):
     # include some logic to validate user input before adding them to the database!
    if request.method == "POST":
        errors = User.objects.validate_data(request.POST)
        if len(errors) > 0:
            for key, errormsg in errors.items():
                messages.error(request, errormsg)
            return redirect("/")
        else:
            password = request.POST['password_txt']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()  # create the hash    
            print(pw_hash)      # prints something like b'$2b$12$sqjyok5RQccl9S6eFLhEPuaRaJCcH3Esl2RWLm/cimMIEnhnLb7iC'    
            # be sure you set up your database so it can store password hashes this long (60 characters)
            # make sure you put the hashed password in the database, not the one from the form!
            new_user=User.objects.create(
                first_name=request.POST['first_name_txt'],
                last_name=request.POST['last_name_txt'],
                email=request.POST['email_txt'],
                password=pw_hash
            )
            request.session['user_id'] = new_user.id
            request.session['user_name'] = f'{new_user.first_name} {new_user.last_name}'
            return redirect("/books") # never render on a post, always redirect!
    return redirect("/")

def login(request):
    if request.method =='POST':
        # see if the username provided exists in the database
        user = User.objects.filter(email=request.POST['email_txt']) # why are we using filter here instead of get?
        if user: # note that we take advantage of truthiness here: an empty list will return false
            logged_user = user[0]
            # assuming we only have one user with this username, the user would be first in the list we get back
            # of course, we should have some logic to prevent duplicates of usernames when we create users
            # use bcrypt's check_password_hash method, passing the hash from our database and the password from the form
            if bcrypt.checkpw(request.POST['password_txt'].encode(), logged_user.password.encode()):
                # if we get True after checking the password, we may put the user id in session
                request.session['user_id'] = logged_user.id
                request.session['user_name'] = f'{logged_user.first_name} {logged_user.last_name}'
                # never render on a post, always redirect!
                return redirect("/books")
        # if we didn't find anything in the database by searching by username or if the passwords don't match, 
        # redirect back to a safe route
        return redirect("/")
    return redirect("/")

def logout(request):
    request.session.flush()
    return redirect("/")

def displayBooks (request):
    context = {
        'all_books':Book.objects.all(),
        'cur_user':User.objects.get(id=request.session['user_id'])
    }
    return render(request, "books_list.html", context)

def addBook(request):
    if request.method =='POST':
        errors = Book.objects.validate_data(request.POST)
        if len(errors) > 0:
            for key, errormsg in errors.items():
                messages.error(request, errormsg)
            return redirect("/")
        else:
            new_book = Book.objects.create(
                title=request.POST['title_txt'],
                description=request.POST['desc_txt'],
                uploaded_by=User.objects.get(id=request.session['user_id']),
            )
            # Make the book a favorite of the user who uploaded it
            new_book.favorite_users.add(new_book.uploaded_by)
            return redirect ("/books")
    return redirect("/")

def displayBook(request, book_id):
    context = {
        'book':Book.objects.get(id=book_id),
        'cur_user':User.objects.get(id=request.session['user_id'])
    }
    return render(request, "book_detail.html", context)

def updateBook(request, book_id):
    if request.method =='POST':
        errors = Book.objects.validate_data(request.POST)
        if len(errors) > 0:
            for key, errormsg in errors.items():
                messages.error(request, errormsg)
            return redirect("/")
        else:
            update_book = Book.objects.get(id=book_id)
            update_book.title=request.POST['title_txt']
            update_book.description=request.POST['desc_txt']
            update_book.save()
            # Make the book a favorite of the user who uploaded it
            return redirect ("/books/"+str(book_id))
    return redirect("/")

def deleteBook(request, book_id):
    Book.objects.get(id=book_id).delete()
    return redirect ("/books")

def addFavoriteBook(request, book_id):
    Book.objects.get(id=book_id).favorite_users.add(User.objects.get(id=request.session['user_id']))
    return redirect("/books")

def deleteFavoriteBook(request, book_id):
    User.objects.get(id=request.session['user_id']).favorite_books.remove(Book.objects.get(id=book_id))
    return redirect("/books/" + str(book_id))

def getFavoriteBooks(request):
    context = {
        'cur_user':User.objects.get(id=request.session['user_id'])
    }
    return render(request, "favorite_books.html", context)