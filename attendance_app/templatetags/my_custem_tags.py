from django import template
from attendance_app.models import student
register = template.Library()

def return_name_list(list_index):
    student_obj = student.objects.all()
    student_unintertand = []
    for index in list_index:
        student_unintertand.append(student_obj[int(index)].student_name)
    return student_unintertand
register.simple_tag(name="return_name_list",func=return_name_list)

def zipp(list1,list2,list3):
    combined_list = zip(list(list1),list2,list3)
    return combined_list
register.simple_tag(name="zipp",func=zipp)

def increment(i):
    num = int(i) + 1
    return num

register.simple_tag(name="increment",func=increment)

