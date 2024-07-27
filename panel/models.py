from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator

# Create your models here.
class Person(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    course = models.ManyToManyField('SchoolCourse',blank=True)
    class Meta:
        verbose_name_plural="Students"
        
    def __str__(self):
        return f"{self.first_name}, {self.last_name}"
    
class SchoolCourse(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    class Meta:
        unique_together=("name","year")
    def __str__(self):
        return f"{self.name}, {self.year}"
        
class SchoolGrade(models.Model):
    student = models.ForeignKey(Person,on_delete=models.CASCADE)
    course = models.ForeignKey(SchoolCourse,on_delete=models.CASCADE)
    grade = models.PositiveIntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)])
    def __str__(self):
        return f"{self.student},{self.course}:{self.grade}"
    
    
class Course(models.Model):
    COURSE_STATUS = (
        ('draft','Draft'),
        ('published','Published')
    )
    title = models.CharField(max_length=120)
    description = models.TextField()
    publish_date = models.DateTimeField()
    price = models.IntegerField()
    author = models.CharField(max_length=200)
    status = models.CharField(default='draft',help_text="Enter field documentation", max_length=15, choices=COURSE_STATUS)
    
    def __str__(self):
        return self.title 
    
    def capital(self):
        return self.title.upper()


class Lesson(models.Model):
    title = models.CharField(max_length=200)
    Course = models.ForeignKey(Course, on_delete=models.SET_NULL,null=True)
    position = models.IntegerField()
    video_url = models.CharField(max_length=200)
    def __str__(self):
        return self.title
    
