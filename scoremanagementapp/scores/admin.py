from django import forms
from django.contrib import admin
from django.urls import path
from .models import Instructor, Student, MyClass, Subject, Score, Forum, Comment

# Register your models here.

class ScoreAppAdminSite(admin.AdminSite):
    site_header = 'Hệ thống quản lý điểm'

    def get_urls(self):
        return [
            path('course-stats/', self.stats_view)
        ] + super().get_urls()
    
    def stats_view(self, request):
        pass

admin_site = ScoreAppAdminSite(name='myadmin')

@admin.display(description="Class")
def myclass(obj):
    return obj.myclass.name + " - " + obj.myclass.major

class InstructorAdmin(admin.ModelAdmin):
    list_display = ['fullname', 'major']

class StudentAdmin(admin.ModelAdmin):
    list_display = ['fullname', myclass]

class MyClassAdmin(admin.ModelAdmin):
    list_display = ['name', 'major']

class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', myclass, 'instructor', 'start_time', 'end_time']

class ScoreAdmin(admin.ModelAdmin):
    list_display = ['point', 'subject', 'student']

class CommentInlineAdmin(admin.StackedInline):
    model = Comment
    fk_name = 'forum'

class ForumAdmin(admin.ModelAdmin):
    list_display = ['content', 'creator', 'is_hided']
    inlines = [CommentInlineAdmin,]

admin_site.register(Instructor, InstructorAdmin)
admin_site.register(Student, StudentAdmin)
admin_site.register(MyClass, MyClassAdmin)
admin_site.register(Subject, SubjectAdmin)
admin_site.register(Score, ScoreAdmin)
admin_site.register(Forum, ForumAdmin)