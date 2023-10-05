from operator import le
from pickletools import markobject
from unicodedata import name
from django.shortcuts import render, redirect, HttpResponse
from .models import student, student_attendance, teacher
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import date, datetime
from django.db import transaction
from datetime import datetime
from django.db.models import Count
import string
from django.contrib import messages
from .decorators import unauthenticated_user_only

today_date = datetime.now().strftime("%Y-%m-%d")


@login_required(login_url="login")
def teacher_profile(request):
    attendance_rows = []
    student_obj = student.objects.all()
    total_students = len(student_obj)
    marked_attendance = (student_attendance.objects.values(
        'date', "status").annotate(status_count=Count('date')).order_by())
    # print(marked_attendance)
    for data in marked_attendance:
        if data["status_count"] == total_students and data["status"] == "Present":
            total_present = data["status_count"]
            total_absent = total_students - total_present
            date = data["date"]
            date = datetime.strftime(date, "%Y-%m-%d")
            if date != today_date:
                edit_forbiden = "disabled"
            else:
                edit_forbiden = ""
            attendance_rows.append(
                [date, total_students, total_present, total_absent, edit_forbiden])

        elif data["status_count"] == total_students and data["status"] == "Absent":
            total_absent = data["status_count"]
            total_present = total_students - total_absent
            date = data["date"]
            date = datetime.strftime(date, "%Y-%m-%d")
            if date != today_date:
                edit_forbiden = "disabled"
            else:
                edit_forbiden = ""
            attendance_rows.append(
                [date, total_students, total_present, total_absent, edit_forbiden])

        elif data["status_count"] <= total_students and data["status"] == "Present":
            total_present = data["status_count"]
            total_absent = total_students - total_present
            date = data["date"]
            date = datetime.strftime(date, "%Y-%m-%d")
            if date != today_date:
                edit_forbiden = "disabled"
            else:
                edit_forbiden = ""
            attendance_rows.append(
                [date, total_students, total_present, total_absent, edit_forbiden])

    User_table = User.objects.filter(username=request.user)
    userinfo_id = User_table[0].id
    teacher_email = User_table[0].email
    teacher_name = User_table[0].first_name
    teacher_table = teacher.objects.filter(fk_teacher_id=userinfo_id)
    teacher_position = teacher_table[0].teacher_responsiblity

    teacher_info_list = [teacher_name, teacher_email, teacher_position]
    return render(request, "userprofile.html", {"attendance_result": attendance_rows, "teacher_info": teacher_info_list})


@login_required(login_url="login")
def attendance_page(request):
    attendance_results_from_db = student_attendance.objects.filter(
        date=str(today_date))
    if len(attendance_results_from_db) == 0:
        # pull data from user table and then pupolate into attendance page
        student_obj = student.objects.all()
        student_presnt_or_absent = ["empty" for _ in range(len(student_obj))]
        previse_attendace = ["empty" for _ in range(len(student_obj))]
        return render(request, "attendance.html", {"student_data": student_obj, "today_date": today_date, "status_list": student_presnt_or_absent, "previse_attendace": previse_attendace})
    else:
        return HttpResponse("""
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-+0n0xVW2eSR5OomGNYDnhzAbDsOXxcvSN1TPprVMTNDbiYZCxYbOOl7+AMvyTG2x" crossorigin="anonymous">
        
        <div class = "container">
        <h1>You have already submitted today attendance go back to userprofile
        and click on edit if you want to edit.
           
        <h1/>
        <a class ="btn btn-info" role = "button" href = "/alburhan/user_profile/">User profile<a/>
        <div/>
        """)


def submit_attend(request):
    student_presnt_or_absent = []
    student_obj = student.objects.all()

    if request.method == "POST":
        index_error_list = []

        for index, student_member in enumerate(student_obj):
            try:
                status = request.POST.getlist(student_member.student_name)[0]
                student_presnt_or_absent.append(status)
            except:
                student_presnt_or_absent.append("empty")
                index_error_list.append(index)
        previse_attendace = ["empty" for _ in range(len(student_obj))]
        if len(index_error_list) != 0:
            return render(request, "attendance.html", {"student_data": student_obj, "today_date": today_date,
                                                       "radio_error": "please_add", "radio_error_index": index_error_list, "status_list": student_presnt_or_absent, "previse_attendace": previse_attendace})
        today_data_student_table = student_attendance.objects.filter(
            date=today_date)

        # insert data in attendance table if it is not there
        if len(today_data_student_table) == 0:

            with transaction.atomic():
                for student_data_item, status in zip(student_obj, student_presnt_or_absent):
                    student_attendance_obj = student_attendance(
                        fk_student=student_data_item, status=status, date=today_date)
                    student_attendance_obj.save()

                return redirect("user_profile")

        # update student
        else:
            with transaction.atomic():
                for today_attendance_item, status in zip(today_data_student_table, student_presnt_or_absent):
                    today_attendance_item.status = status
                    today_attendance_item.save()

                return redirect("user_profile")


def edit_today_attendance(request):
    student_obj = student.objects.all()
    student_presnt_or_absent = ["empty" for _ in range(len(student_obj))]
    attendance_results_from_db = student_attendance.objects.filter(
        date=str(today_date))
    try:
        previse_attendace = [
            submitted_attendance .status for submitted_attendance in attendance_results_from_db]
    except:
        previse_attendace = ["empty" for _ in range(len(student_obj))]

    return render(request, "attendance.html", {"student_data": student_obj, "today_date": today_date, "status_list": student_presnt_or_absent, "previse_attendace": previse_attendace})


def validating_password(password):
    alpha_list = string.ascii_uppercase.replace('', ' ').strip().split(' ')
    symbols = string.punctuation.replace('', ' ').strip().split(' ')
    numb_list = string.digits.replace('', ' ').strip().split(' ')
    sys = []
    num = []
    alph = []
    for item in password:
        if item in symbols:
            sys.append(True)
        if item in numb_list:
            num.append(True)
        if item in alpha_list:
            alph.append(True)

    if True in sys and True in num and True in alph and len(password) > 7:
        return True
    else:
        return False


@unauthenticated_user_only
def resgister(request):

    if request.method == "POST":
        user_name = request.POST['user_name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2 and validating_password(password1):
            # if password1 == password2 and len(password1)>=2:

            if User.objects.filter(username=user_name).exists():

                messages.error(request, 'User Already Registered')
                return redirect('register')

            elif User.objects.filter(email=email).exists():

                messages.info(request, 'Email Exist')
                return redirect('register')

            else:
                user = User.objects.create_user(
                    username=user_name, first_name=user_name, password=password1, email=email)
                user.save()
                messages.success(request, 'User Registered')
                last_user_id = int(list(User.objects.all())[-1].id)
                teacher_role = teacher.objects.create(
                    teacher_responsiblity="Usthaz", fk_teacher_id=last_user_id)
                teacher_role.save()
                return redirect('login')

        else:
            messages.warning(request, 
                             """Password requirement:
                                Length > 8,
                                Upper case letters,
                                Special characters,
                                And
                                Numbers""")
            return redirect('register')
    else:
        return render(request, "register.html")


@unauthenticated_user_only
def login_form(request):
    if request.method == 'POST':
        user_name = request.POST['user_name']
        password = request.POST['password']
        user = authenticate(request, username=user_name, password=password)
        if user:
            login(request, user)
            return redirect('user_profile')
        else:
            print('invalid password or username')
            messages.info(request, 'Invalid Password Or User Name')
            return redirect('login')
    else:
        return render(request, "login.html")


def logout_form(request):
    logout(request)
    return redirect('login')
