# Generated by Django 4.2.7 on 2023-12-21 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_student_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='info',
            field=models.TextField(blank=True, null=True, verbose_name='Информация о студенте'),
        ),
    ]
