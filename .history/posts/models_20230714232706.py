from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify
from users.models import UserAccount as User
import math
import re


class AutoSlugMixin(models.Model):
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.get_slug_source())
        super().save(*args, **kwargs)

    def get_slug_source(self):
        raise NotImplementedError("Subclasses of AutoSlugMixin must provide a get_slug_source() method.")

    class Meta:
        abstract = True


class Category(AutoSlugMixin):
    name = models.CharField(max_length=100)

    def get_slug_source(self):
        return self.name

    def __str__(self):
        return self.name


class Tag(AutoSlugMixin):
    name = models.CharField(max_length=100)

    def get_slug_source(self):
        return self.name

    def __str__(self):
        return self.name


class PostType(AutoSlugMixin):
    name = models.CharField(max_length=100)

    def get_slug_source(self):
        return self.name

    def __str__(self):
        return self.name


class Field(models.Model):
    post_type = models.ForeignKey(PostType, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    field_type = models.CharField(max_length=100, choices=(
        ('CharField', 'CharField'),
        ('TextField', 'TextField'),
    ))
    is_required = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Post(AutoSlugMixin):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post_type = models.ForeignKey(PostType, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    custom_fields = GenericRelation('CustomFieldValue')
    minute_read = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    preview = models.TextField()
    
    def get_slug_source(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.get_slug_source())

        # Calculate approximate minute read based on word count
        word_count = len(re.findall(r'\w+', self.content))
        self.minute_read = math.ceil(word_count / 200)  # Assuming average reading speed of 200 words per minute
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images/%Y/%m/%d/')
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.post.title


class CustomFieldValue(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    value = models.TextField()

    def __str__(self):
        return f'{self.field} - {self.content_object}'
