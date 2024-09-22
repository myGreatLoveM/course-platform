import helpers
from django.db import models
from cloudinary.models import CloudinaryField
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


class Course(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    # image = models.ImageField(
    #     upload_to=handle_upload,
    #     blank=True,
    #     null=True
    # )
    image = CloudinaryField("images", null=True)
    access = models.CharField(
        max_length=20,
        choices=AccessRequirement.choices,
        default=AccessRequirement.EMAIL_REQUIRED
    )
    status = models.CharField(
        max_length=20,
        choices=PublishStatus.choices,
        default=PublishStatus.DRAFT)

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



class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    description =models.TextField(blank=True, null=True)