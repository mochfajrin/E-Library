# Generated by Django 4.2.16 on 2024-11-17 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_alter_book_file_alter_user_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(default='user1731808615853', max_length=255),
        ),
    ]