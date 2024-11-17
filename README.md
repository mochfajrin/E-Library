# Django E-Library

## Get Started

### Creating Virtual Environment

```sh
python -m venv venv
```

### Enter the Virtual Environment

- Windows

```powershell
venv\Scripts\activate
```

- Linux

```bash
source venv\bin\activate
```

### Install Dependency

```bash
pip install -r requirements.txt
```

### Create PostgreSQL Database

```sh
CREATE DATABASE <YOUR_DATABASE_NAME>;
```

### Configure .Env

```sh
# DJANGO CONFIG

DJANGO_SECRET_KEY="your django secret key"

# DATABASE CONFIG

DATABASE_URL=psql://user:password@hostname:port/your_db
```

### Run Database Migration

```sh
python manage.py makemigrations
python manage.py migrate
```

### Run Django Application

```sh
python manage.py runserver

```

## Screenshots

### Registrasi

![](docs/assets/image/register.png)

### Login

![](docs/assets/image/login.png)

### Katalog

![](docs/assets/image/catalog.png)

### Unggah Buku atau Update Buku

![](docs/assets/image/edit.png)

### Detail Buku

![](docs/assets/image/detail.png)

### Favorit

![](docs/assets/image/favorite.png)

### Preview Buku

![](docs/assets/image/preview.png)
