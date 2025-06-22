from typing import Any
from django import forms
from django.contrib import admin
from .models import *
from django.db.models import *
from django.utils.html import format_html
from django.urls import reverse
from django.utils.http import urlencode


# Register your models here.
admin.site.site_header = "Admin Panel"
admin.site.site_title="Admin Dashboard"

class  PersonAdminForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = "__all__"
    def clean_first_name(self):
        if self.cleaned_data['first_name'] =="Spike":
            raise forms.ValidationError("Only Name")
        return self.cleaned_data["first_name"]

class LessonInline(admin.TabularInline):
    model = Lesson
    verbose_name_plural ="Lesson's details"
    classes = ('collapse',)

class CourseAdmin(admin.ModelAdmin):
    list_display=("title","publish_date","author","price")
    list_display_links=("author",)
    list_filter=("title","author")
    search_fields=("author",)
    inlines = (LessonInline,)
    
    
    @admin.display(boolean=True,description="Status_Price") 
    def full_title(self,obj):
        return True
    fieldsets=(('Book Details',{
            'fields':('title','author','description')
        }),('Book Extra Info',{
            'classes':('collapse','wide'),
            'fields':('price','status','publish_date'),
            'description':"Book's extra info."
        }))
    
    
@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display=("title","Course","position")
    list_filter=("Course",)
    search_fields=("Course__title",)
    autocomplete_fields=("Course",)
    ordering=("title",)
    list_per_page=3
admin.site.register(Course,CourseAdmin)



@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name","show_avg")
    list_display_links = ("first_name", "last_name")
    ordering = ("first_name", "last_name")
    form = PersonAdminForm
    
    
    @admin.display(description="Average")
    def show_avg(self,obj):
        result = SchoolGrade.objects.filter(student=obj).aggregate(Avg("grade"))
        avg = int(result["grade__avg"])
        color ="green"
        if avg < 90 and avg > 70:
            color = "blue"
        elif avg <=70 :
            color ="orange"
        else:
            color = "red"
        return format_html("<span style='color:{}'>{}</span>",color,avg)

    def get_form(self, request, obj, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["first_name"].label = "First Name"
        return form
    

@admin.register(SchoolCourse)
class SchoolCourseAdmin(admin.ModelAdmin):
    list_display=('name','year','view_student_link')
    list_filter=('year',)
    
    def view_student_link(Self,obj):
        count = obj.person_set.count()
        url = (
            reverse('admin:panel_person_changelist')+"?"+urlencode({"courses__id":f"{obj.id}"}))
        return format_html("<a href={}>{} students</a>",url,count)

@admin.register(SchoolGrade)
class SchoolGradeAdmin(admin.ModelAdmin):
    pass
