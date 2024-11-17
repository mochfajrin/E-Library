from django import forms
from django.contrib.auth.forms import UserCreationForm
from app.models import User, Book


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'placeholder': "Masukkan alamat email",
        "class": "form-control",
        "id": "email"
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': "Masukkan password",
        "class": "form-control",
        "id": "password"
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': "Konfirmasi password",
        "class": "form-control",
        "id": "confirmPassword"
    }))

    class Meta:
        model = User
        fields = ["email", "password1", "password2"]


class UserUpdateForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'placeholder': "Masukkan alamat email",
        "class": "form-control",
        "id": "email",
    }), required=False)
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': "Masukkan password",
        "class": "form-control",
        "id": "password",
    }), required=False)
    name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': "Masukkan nama",
        "class": "form-control",
        "type": "text",
        "id": "name",
    }))
    image = forms.ImageField(widget=forms.FileInput(attrs={
        "class": "form-control",
        "type": "file",
        "id": "image",
    }), required=False)

    class Meta:
        model = User
        fields = ["email", "password", "name", "image"]


class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'placeholder': "Masukkan alamat email",
        "class": "form-control",
        "id": "email"
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': "Masukkan password",
        "class": "form-control",
        "type": "password",
        "id": "password"
    }))

    class Meta:
        model = User
        fields = ["email", "password"]


class BookCreateForm(forms.ModelForm):
    file = forms.FileField(widget=forms.FileInput(attrs={
        "class": "form-control",
        "type": "file",
        "id": "file",
        "accept": "application/pdf"
    }))
    title = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': "Masukkan judul buku",
        "class": "form-control",
    }))
    author = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': "Masukkan penulis buku",
        "class": "form-control",
    }))
    genre = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': "Masukkan genre buku",
        "class": "form-control",
    }))
    year = forms.CharField(widget=forms.NumberInput(attrs={
        'placeholder': "Masukkan tahun terbit buku",
        "class": "form-control",
    }))
    description = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': "Masukkan deskripsi buku",
        "class": "form-control",
        "rows": 3
    }))

    class Meta:
        model = Book
        fields = [
            "title",
            "file",
            "author",
            "genre",
            "year",
            "description",
        ]


class BookUpdateForm(forms.ModelForm):
    file = forms.FileField(widget=forms.FileInput(attrs={
        "class": "form-control",
        "type": "file",
        "id": "file",
        "accept": "application/pdf"
    }), required=False)
    title = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': "Masukkan judul buku",
        "class": "form-control",
    }), required=False)
    author = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': "Masukkan penulis buku",
        "class": "form-control",
    }), required=False)
    genre = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': "Masukkan genre buku",
        "class": "form-control",
    }), required=False)
    year = forms.CharField(widget=forms.NumberInput(attrs={
        'placeholder': "Masukkan tahun terbit buku",
        "class": "form-control",
    }), required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': "Masukkan deskripsi buku",
        "class": "form-control",
        "rows": 3
    }), required=False)

    class Meta:
        model = Book
        fields = [
            "title",
            "file",
            "author",
            "genre",
            "year",
            "description",
        ]
