from django.urls import path

from OnlineLibrary.library.views import home_page, add_book_page, edit_book_page, details_book_page, profile_page, \
    edit_profile_page, delete_profile_page, create_profile_page, delete_book

urlpatterns = [
    path('', home_page, name='home'),

    path('add/', add_book_page, name='add book'),
    path('edit/<int:pk>/', edit_book_page, name='edit book'),
    path('details/<int:pk>/', details_book_page, name='details book'),
    path('delete/<int:pk>/', delete_book, name='delete book'),

    path('profile/', profile_page, name='profile page'),
    path('profile/edit/', edit_profile_page, name='edit profile'),
    path('profile/delete/', delete_profile_page, name='delete profile'),
    path('profile/create/', create_profile_page, name='create profile'),

]
