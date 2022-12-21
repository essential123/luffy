from django.contrib import admin

# Register your models here.
from .models import Course, CourseCategory, CourseSection, Teacher, CourseChapter

admin.site.register(Course)
admin.site.register(CourseChapter)
admin.site.register(CourseSection)
admin.site.register(Teacher)
admin.site.register(CourseCategory)
