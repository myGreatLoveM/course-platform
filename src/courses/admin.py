from django.contrib import admin
from django.utils.html import format_html
from cloudinary import CloudinaryImage
from helpers import get_cloudinary_image_object
from .models import Course, Lesson


class LessonInline(admin.StackedInline):
    model = Lesson
    readonly_fields = ["public_id", "updated", "display_image"]
    extra = 0

    def display_image(self, obj, *args, **kwargs):
        url = get_cloudinary_image_object(
            obj,
            field_name='thumbnail',
            width=200
        )
        return format_html(f"<img src={url} />")

    display_image.short_description = "Current image"


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline]
    list_display = ["title", "access", "status"]
    list_filter = ["access", "status"]
    fields = ["public_id", "title", "description",
              "access", "status", "image", "display_image"]
    readonly_fields = ["public_id", "display_image",]

    def display_image(self, obj, *args, **kwargs):
        url = get_cloudinary_image_object(
            obj,
            field_name='image',
            width=200
        )
        return format_html(f"<img src={url} />")
    
    display_image.short_description = "Current image"



# admin.site.register(Course, CourseAdmin)  
