from django.shortcuts import render, redirect

from OnlineLibrary.library.form import CreateProfileForm, EditProfileForm, DeleteProfileForm, AddBookForm, EditBookForm, \
    DeleteBookForm
from OnlineLibrary.library.models import Book
from OnlineLibrary.library.templatetags.check_profiles import has_profile


def home_page(request):
    profile = has_profile()
    if not profile:
        return redirect('create profile')
    books = Book.objects.prefetch_related('user__book_set').all()
    context = {
        'profile': profile,
        'books': books,
    }

    return render(request, 'home-with-profile.html', context)


def add_book_page(request):
    if request.method == 'POST':
        form = AddBookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    form = AddBookForm()
    context = {
        'form': form,
    }
    return render(request, 'add-book.html', context)


def edit_book_page(request, pk):
    book = Book.objects.get(pk=pk)
    if request.method == 'POST':
        form = EditBookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('home')
    form = EditBookForm(instance=book)
    context = {
        'form': form,
        'book': book,
    }
    return render(request, 'edit-book.html', context)


def details_book_page(request, pk):
    book = Book.objects.get(pk=pk)
    context = {
        'book': book,
    }
    return render(request, 'book-details.html', context)


def delete_book(request, pk):
    book = Book.objects.get(pk=pk)
    form = DeleteBookForm(request.POST, instance=book)
    form.save()
    return redirect('home')


def create_profile_page(request):
    if request.method == 'POST':
        form = CreateProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    form = CreateProfileForm()
    context = {
        'form': form,
    }
    return render(request, 'home-no-profile.html', context)


def profile_page(request):
    profile = has_profile()
    context = {
        'profile': profile,
    }
    return render(request, 'profile.html', context)


def edit_profile_page(request):
    profile = has_profile()
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile page')
    form = EditProfileForm(instance=profile)
    context = {
        'form': form,
    }
    return render(request, 'edit-profile.html', context)


def delete_profile_page(request):
    profile = has_profile()
    if request.method == 'POST':
        form = DeleteProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('home')
    form = DeleteProfileForm(instance=profile)
    context = {
        'form': form,
    }
    return render(request, 'delete-profile.html', context)
