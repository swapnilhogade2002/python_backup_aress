from django.contrib import admin
from.models import Blog

@admin.register(Blog)
class BlogModalAdmin(admin.ModelAdmin):
  list_display=['id','title','desc']