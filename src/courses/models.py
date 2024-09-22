from django.db import models
from django.utils.text import slugify
from cloudinary.models import CloudinaryField
import helpers
import uuid
# from cloudinary import CloudinaryImage


helpers.cloudinary_init()


class AccessRequirement(models.TextChoices):
    ANYONE = "any", "Anyone"
    EMAIL_REQUIRED = "email_required", "Email Required"


class PublishStatus(models.TextChoices):
    PUBLISHED = "pub", "Published"
    COMING_SOON = "soon", "Coming Soon"
    DRAFT = "draft", "Draft"


def handle_upload(instance, filename):
    return f"{filename}"


def get_public_id(instance, *args, **kwargs):
    title = instance.title
    unique_id = str(uuid.uuid4()).replace("-", "")
    if not title:
        return unique_id
    slug = slugify(title)
    unique_id_short = str(uuid.uuid4()).replace("-", "")[:7]
    return f"{slug}-{unique_id_short}"


def get_public_id_prefix(instance, *args, **kwargs):
    public_id = instance.public_id
    if not public_id:
        return "courses"
    return f"courses/{public_id}"


def get_display_name(instance, *args, **kwargs):
    if instance.title:
        return instance.title
    return "Course Upload"


def get_tags(instance, *args, **kwargs):
    return ["course", "thumbnail"]


class Course(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    public_id = models.CharField(max_length=130, blank=True, null=True)
    # image = models.ImageField(
    #     upload_to=handle_upload,
    #     blank=True,
    #     null=True
    # )
    image = CloudinaryField("images",
                            null=True,
                            public_id_prefix=get_public_id_prefix,
                            display_name=get_display_name,
                            tags=get_tags)
    access = models.CharField(max_length=20,
                            choices=AccessRequirement.choices,
                            default=AccessRequirement.EMAIL_REQUIRED)
    status = models.CharField(max_length=20,
                            choices=PublishStatus.choices,
                            default=PublishStatus.DRAFT)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        if self.public_id == "" or self.public_id is None:
            self.public_id = get_public_id(self)
        super().save(*args, **kwargs)

    @property
    def is_published(self):
        return self.status == PublishStatus.PUBLISHED

    @property
    def image_admin(self):
        if not self.image:
            return ""
        image_options = {
            "width": 500
        }
        url = self.image.build_url(**image_options)
        return url

    def get_image_thumbnail(self, width=500, as_html=False):
        if not self.image:
            return ""
        image_options = {
            "width": width
        }
        if as_html:
            # CloudinaryImage(str(self.image)).image(**image_options)
            return self.image.image(**image_options)
        # CloudinaryImage(str(self.image)).build_url(**image_options)
        url = self.image.build_url(**image_options)
        return url

# Lesson.objects.all() # lesson queryset -> all rows
# Lesson.objects.first()
# course_obj = Course.objects.first()
# course_qs = Course.objects.filter(id=course_obj.id)
# Lesson.objects.filter(course__id=course_obj.id)
# course_obj.lesson_set.all()
# lesson_obj = Lesson.objects.first()
# ne_course_obj = lesson_obj.course
# ne_course_lessons = ne_course_obj.lesson_set.all()
# lesson_obj.course_id
# course_obj.lesson_set.all().order_by("-title")


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    # course_id
    title = models.CharField(max_length=120)
    public_id = models.CharField(max_length=130, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    thumbnail = CloudinaryField("image", blank=True, null=True)
    video = CloudinaryField("video", blank=True,
                            null=True, resource_type="video")
    order = models.IntegerField(default=0)
    can_preview = models.BooleanField(
        default=False, help_text="if user does not have access to this course, can they see?")
    status = models.CharField(
        max_length=20,
        choices=PublishStatus.choices,
        default=PublishStatus.PUBLISHED)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "-updated"]

    def save(self, *args, **kwargs):
        if self.public_id == "" or self.public_id is None:
            self.public_id = get_public_id(self)
        super().save(*args, **kwargs)
