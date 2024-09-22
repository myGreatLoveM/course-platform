from django.contrib import admin
from django.utils.html import format_html
from cloudinary import CloudinaryImage

from .models import Course, Lesson


class LessonInline(admin.StackedInline):
    model = Lesson
    readonly_fields = ["updated"]
    extra = 0

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline]
    list_display = ["title", "access", "status"]
    list_filter = ["access", "status"]
    fields = ["public_id", "title", "description",
              "access", "status", "image", "display_image"]
    readonly_fields = ["public_id", "display_image",]

    def display_image(self, obj, *args, **kwargs):
        url = obj.image_admin
        return format_html(f"<img src={url} />")
    
    display_image.short_description = "Current image"


# admin.site.register(Course, CourseAdmin)  
