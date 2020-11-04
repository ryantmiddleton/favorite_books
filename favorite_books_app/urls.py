from django.urls import path     
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('books', views.displayBooks),
    path('add_book', views.addBook),
    path('books/<int:book_id>', views.displayBook),
    path('update_book/<int:book_id>', views.updateBook),
    path('fav_books', views.getFavoriteBooks),
    path('add_favorite/<int:book_id>', views.addFavoriteBook),
    path('delete_favorite/<int:book_id>', views.deleteFavoriteBook),
    path('delete_book/<int:book_id>', views.deleteBook)

]