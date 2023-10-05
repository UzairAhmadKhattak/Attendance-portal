# Generated by Django 4.0.2 on 2022-10-03 09:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_name', models.CharField(max_length=20)),
                ('student_father_name', models.CharField(max_length=20)),
                ('student_cnic', models.CharField(max_length=13)),
                ('student_dob', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teacher_responsiblity', models.CharField(max_length=20)),
                ('fk_teacher', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='student_attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=None)),
                ('update_on_date', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(max_length=20)),
                ('fk_student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='attendance_app.student')),
            ],
        ),
    ]