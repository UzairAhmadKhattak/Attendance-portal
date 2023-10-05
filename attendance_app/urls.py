
from django.urls import path
from .views import teacher_profile, attendance_page, submit_attend,\
    edit_today_attendance, login_form, resgister, logout_form

urlpatterns = [
    path('user_profile/', teacher_profile, name="user_profile"),
    path("attendance", attendance_page, name="attendance"),
    path("submit", submit_attend, name="submit"),
    path("login", login_form, name="login"),
    path("user_profile/logout", logout_form, name="logout"),
    path("logout", logout_form, name="logout"),
    path("register", resgister, name="register"),
    path("user_profile/today_attendance/edit",
         edit_today_attendance, name="edit"),

]
