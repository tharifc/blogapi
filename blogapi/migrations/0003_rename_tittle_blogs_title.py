# Generated by Django 4.0.4 on 2022-06-30 05:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogapi', '0002_blogs_image_blogs_liked_by_alter_blogs_author_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blogs',
            old_name='tittle',
            new_name='title',
        ),
    ]
