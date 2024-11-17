from django.urls import path


from app.views import book, user

urlpatterns = [
    path("", book.catalog, name="catalog"),
    path("catalog", book.catalog, name="catalog"),
    path("books/<id>/", book.detail, name="book_detail"),
    path("books/edit/<id>/", book.update, name="book_edit"),
    path("books/delete/<id>/", book.delete, name="book_edit"),
    path("books/favorite/<id>/", book.add_favorite, name="add_favorite"),
    path("favorite", book.favorite, name="favorite"),
    path("books/preview/<id>/", book.preview, name="book_preview"),
    path("login", user.login, name="login"),
    path("register", user.register, name="register"),
    path("logout", user.logout, name="logout"),
    path("profile", user.profile, name="profile"),
    path("upload", book.upload, name="upload"),
]
