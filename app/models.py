from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import FileExtensionValidator
import time


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_field):
        if not email:
            raise ValueError("Invalid email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_field)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_field):
        extra_field.setdefault("is_staff", True)
        extra_field.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_field)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(
        max_length=255,
        default=f"user{round(time.time() * 1000)}",
    )
    image = models.ImageField(
        upload_to="user/",
        default="user/profile.png"
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self) -> str:
        return f"{self.email} {self.image} {self.name}"

    class Meta:
        db_table = "users"


class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=5000)
    author = models.CharField(max_length=255)
    year = models.PositiveIntegerField()
    genre = models.CharField(max_length=255)
    file = models.FileField(
        upload_to="documents/",
        validators=[FileExtensionValidator(["pdf"])])
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, blank=False)

    def __str__(self) -> str:
        return f"{self.title} {self.description} {self.author} {self.year}"

    class Meta:
        db_table = "books"


class Favorite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=False)
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, blank=False)

    class Meta:
        db_table = "favorites"
        unique_together = ('user', 'book')


class BookPage(models.Model):
    image = models.CharField(max_length=255)
    book = models.ForeignKey(
        Book, on_delete=models.PROTECT, blank=False)

    def __str__(self) -> str:
        return f'{self.image}'

    class Meta:
        db_table = "book_pages"
