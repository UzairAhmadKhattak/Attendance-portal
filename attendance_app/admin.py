from django.contrib import admin
from .models import student,teacher,student_attendance
# Register your models here.

admin.site.register(student)
admin.site.register(teacher)
admin.site.register(student_attendance)

