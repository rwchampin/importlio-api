from django.db.models.signals import pre_save
from django.dispatch import receiver
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from .models import Post

@receiver(pre_save, sender=Post)
def resize_featured_image(sender, instance, **kwargs):
    # Check if the instance is being created or updated and if there's a featured_image
    if instance._state.adding or not instance.featured_image:
        return

    # Open the original image using Pillow
    original_image = Image.open(instance.featured_image)

    # Resize the image to a fixed size (1920x1080) while maintaining aspect ratio
    original_image.thumbnail((1920, 1080))

    # Save the resized image back to the instance's featured_image field
    buffer = BytesIO()
    original_image.save(buffer, format="JPEG", quality=70)
    instance.featured_image.save(instance.featured_image.name, ContentFile(buffer.getvalue()), save=False)
