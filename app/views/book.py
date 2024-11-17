from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Q, Prefetch
from django.contrib import messages
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import pymupdf
import time
import math
from app.models import Book, BookPage, Favorite
from app.forms import BookCreateForm, BookUpdateForm
import os


@login_required
def catalog(request):
    page = int(request.GET.get("page", "1")) or 1
    search = request.GET.get("search")
    books = []
    favorite_books = Favorite.objects.filter(
        user_id=request.user.id).values_list("book_id", flat=True)

    if (search):
        books = Book.objects.filter(
            Q(title__icontains=search) |
            Q(year__icontains=search) |
            Q(description__icontains=search)
        ).prefetch_related(
            "bookpage_set").all().order_by("-id")
    else:
        books = Book.objects.prefetch_related(
            "bookpage_set").all().order_by("-id")

    total_page = math.ceil(len(books) / 12)

    if page > total_page and total_page > 0:
        return redirect(f"/catalog?page={total_page}")
    if page < 1:
        return redirect(f"/catalog?page=1")

    covers = []
    books_paginate = Paginator(books, 12).page(page)
    for book in books:
        covers.append(book.bookpage_set.first())
    covers_paginate = Paginator(covers, 12).page(page)
    books_zip = zip(books_paginate, covers_paginate)
    context = {
        "title": "Katalog",
        "books": books_zip,
        "meta": {
            "search": search,
            "favorite_books": favorite_books,
            "book_total": len(books),
            "book_total_page": total_page,
            "book_per_page": 12,
            "current_page": page,
            "prev_page": 1 if page == 1 else page - 1,
            "next_page": total_page if page == total_page else page + 1,
        }
    }
    return render(request, "pages/book_catalog.html", context)


@login_required
def favorite(request):
    page = int(request.GET.get("page", "1")) or 1
    search = request.GET.get("search")
    books = []
    favorite_books = Favorite.objects.filter(
        user_id=request.user.id).values_list("book_id", flat=True)

    if (search):
        books = Book.objects.filter(
            Q(title__icontains=search) |
            Q(year__icontains=search) |
            Q(description__icontains=search),
            id__in=favorite_books
        ).prefetch_related(
            "bookpage_set").order_by("-id")
    else:
        books = Book.objects.prefetch_related(
            "bookpage_set").filter(id__in=favorite_books).order_by("-id")

    total_page = math.ceil(len(books) / 12)
    print(len(books))

    if page > total_page and total_page > 0:
        return redirect(f"/favorite?page={total_page}")
    if page < 1:
        return redirect(f"/favorite?page=1")

    covers = []
    books_paginate = Paginator(books, 12).page(page)
    for book in books:
        covers.append(book.bookpage_set.first())
    covers_paginate = Paginator(covers, 12).page(page)
    books_zip = zip(books_paginate, covers_paginate)
    context = {
        "title": "Katalog",
        "books": books_zip,
        "meta": {
            "search": search,
            "favorite_books": favorite_books,
            "book_total": len(books),
            "book_total_page": total_page,
            "book_per_page": 12,
            "current_page": page,
            "prev_page": 1 if page == 1 else page - 1,
            "next_page": total_page if page == total_page else page + 1,
        }
    }
    return render(request, "pages/book_favorite.html", context)


@ login_required
def detail(request, id):
    keyword = request.GET.get("keyword")
    keywords = []
    book = get_object_or_404(Book, id=id)
    favorite = Favorite.objects.filter(
        user_id=request.user.id, book_id=book.id).first()

    if (keyword == "1"):
        fname = f'{settings.MEDIA_ROOT}/{book.file}'
        with pymupdf.open(fname) as doc:
            text = chr(12).join([page.get_text() for page in doc])
            text = text.lower()
            text = re.sub("&lt;/?.*.?&gt;", " &lt;&gt; ", text)
            text = re.sub("(\\d|\\W)+", " ", text)
            vectorize = TfidfVectorizer(
                stop_words="english", max_features=5)
            vectorize.fit_transform([text])
            keywords = vectorize.get_feature_names_out()

    if (book is None):
        return redirect('catalog')

    cover = book.bookpage_set.first()
    total_page = book.bookpage_set.count()
    context = {
        "user": request.user,
        "title": f"Book | {book.title}",
        "book": book,
        "cover": cover,
        "total_page": total_page,
        "keywords": keywords
    }

    if favorite != None:
        context["favorite_book_id"] = favorite.book_id

    return render(request, "pages/book_detail.html", context)


@ login_required
def upload(request):
    if (request.method == "POST"):
        form = BookCreateForm(
            request.POST,
            request.FILES,
            initial={"user_id": request.user.id}
        )
        if (form.is_valid()):
            book = form.save(commit=False)
            book.user_id = request.user.id
            book.save()
            book_pages = []
            doc = pymupdf.open(f'{settings.MEDIA_ROOT}/{book.file}')
            for page in doc:
                pix = page.get_pixmap()
                book_page_path = f'/book/{round(time.time() * 1000)}.png'
                fname = f'{settings.MEDIA_ROOT}{book_page_path}'
                book_pages.append(
                    BookPage(
                        book_id=book.id,
                        image=book_page_path
                    ))
                pix.save(fname)
            BookPage.objects.bulk_create(book_pages)

            return redirect("/catalog")
    else:
        form = BookCreateForm()
    return render(
        request,
        "pages/book_upload.html",
        {"title": "Upload Buku", "form": form}
    )


def update(request, id):
    book = get_object_or_404(Book, id=id, user_id=request.user.id)

    if (request.method == "POST"):
        form = BookUpdateForm(request.POST, request.FILES)

        if form.is_valid():
            file = form.cleaned_data["file"]
            title = form.cleaned_data["title"]
            author = form.cleaned_data["author"]
            genre = form.cleaned_data["genre"]
            year = form.cleaned_data["year"]
            description = form.cleaned_data["description"]

            if title:
                book.title = title

            if author:
                book.author = author

            if genre:
                book.genre = genre

            if year:
                book.year = year

            if description:
                book.year = year

            if file:
                book.file = request.FILES['file']
                book_pages = BookPage.objects.filter(book_id=book.id)
                book.save()

                for book_page in book_pages:
                    old_fname = f'{settings.MEDIA_ROOT}/{book_page.image}'
                    if os.path.exists(old_fname):
                        os.remove(old_fname)

                doc = pymupdf.open(f'{settings.MEDIA_ROOT}/{book.file}')
                new_book_pages = []

                for page in doc:
                    pix = page.get_pixmap()
                    book_page_path = f'/book/{round(time.time() * 1000)}.png'
                    fname = f'{settings.MEDIA_ROOT}{book_page_path}'
                    new_book_pages.append(
                        BookPage(
                            book_id=book.id,
                            image=book_page_path
                        ))

                    pix.save(fname)

                BookPage.objects.filter(book_id=id).delete()
                BookPage.objects.bulk_create(new_book_pages)

            book.save()
            old_file = f'{settings.MEDIA_ROOT}/documents/{file}'

            messages.success(request, "berhasil memperbarui buku")
            return redirect(f'/books/{id}')
    else:
        form = BookUpdateForm(initial={
            'title': book.title,
            'author': book.author,
            'genre': book.genre,
            'year': book.year,
            'description': book.description,
        })
    context = {"title": f"edit | {book.title}", "form": form}
    return render(request, "pages/book_edit.html", context)


@ login_required
def delete(request, id):
    user_id = request.user.id
    book = get_object_or_404(Book, id=id, user_id=user_id)
    book_pages = BookPage.objects.filter(book_id=book.id)

    old_file = f'{settings.MEDIA_ROOT}/documents/{book.file}'
    if os.path.exists(old_file):
        os.remove(old_file)

    for book_page in book_pages:
        fname = f'{settings.MEDIA_ROOT}/{book_page.image}'
        if os.path.exists(fname):
            os.remove(fname)

    if book.user_id != user_id:
        messages.error("Kamu bukan pemilik buku ini, tidak bisa menghapus!")
        return redirect(f"/books{id}")

    book_pages.delete()
    book.delete()
    messages.success(request, "Berhasil menghapus buku")
    return redirect("/catalog")


@login_required
def preview(request, id):
    page = int(request.GET.get("page", 1))
    book = get_object_or_404(Book, id=id)
    book_pages = BookPage.objects.filter(book_id=id).all()
    total_page = len(book_pages)
    if page > total_page or page < 0:
        return redirect(f"/books/{id}")
    book_page = book_pages[page - 1]
    context = {
        "title": f"Preview ",
        "book": book,
        "total_page": total_page - 1,
        "current_page": page,
        "book_page": book_page,
        "prev_page": 1 if page == 1 else page - 1,
        "next_page": total_page if page == total_page else page + 1,
    }
    return render(request, "pages/book_preview.html", context)


@login_required
def add_favorite(request, id):
    current_page = request.GET.get("current_page")
    book = get_object_or_404(Book, id=id)
    favorite = Favorite.objects.filter(
        book_id=book.id, user_id=request.user.id
    ).first()
    redirect_url = "catalog"

    if current_page == "detail":
        redirect_url = f"/books/{book.id}"

    if current_page == "favorite":
        redirect_url = "favorite"

    if favorite is not None:
        favorite.delete()
        messages.success(request, "Berhasil menghapus favorit")
        return redirect(redirect_url)

    Favorite.objects.create(user_id=request.user.id, book_id=book.id)
    messages.success(request, "Berhasil menambahkan ke favorit")
    return redirect(redirect_url)
