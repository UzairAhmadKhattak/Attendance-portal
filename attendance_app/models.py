from email.utils import format_datetime
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

from pymysql import DataError

# today_date = datetime.now().strftime("%d-%m-%Y")

class student(models.Model):

    student_name = models.CharField(max_length = 20)

    student_father_name = models.CharField(max_length=20)

    student_cnic = models.CharField(max_length=13)

    student_dob = models.DateField()

    def __str__(self):
        return self.student_name


class teacher(models.Model):
    fk_teacher = models.ForeignKey(User,on_delete=models.CASCADE)
    teacher_responsiblity = models.CharField(max_length=20)
    
    def __str__(self):
        return self.fk_teacher.first_name


class student_attendance(models.Model):
    fk_student = models.ForeignKey(student, on_delete = models.CASCADE,unique= False)
    date = models.DateField(default=None)
    update_on_date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20)

    def __str__(self):
        return str(self.date)