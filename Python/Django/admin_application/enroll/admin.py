from django.contrib import admin
from enroll.models import Student
# Register your models here.

class StudentAdmin(admin.ModelAdmin):
  list_display=('id','stuname','stuname','stuemail','stupass')
  
  
admin.site.register(Student,StudentAdmin)
# admin.site.register(Student)
