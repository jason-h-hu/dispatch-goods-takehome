# Generated by Django 4.2.13 on 2024-06-27 19:45

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('first_name', models.CharField(help_text='aka personal name', max_length=64)),
                ('last_name', models.CharField(help_text='aka family name, surname', max_length=64)),
                ('age', models.IntegerField()),
                ('address', models.CharField(max_length=256)),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
            ],
        ),
    ]
