from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify
from users.models import UserAccount as User
import math
import re


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class PostType(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

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


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post_type = models.ForeignKey(PostType, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category)
    tags = models.ManyToManyField(Tag)
    custom_fields = GenericRelation('CustomFieldValue')
    minute_read = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.ManyToManyField(User, related_name='disliked_posts', blank=True)

    def save(self, *args, **kwargs):
        # Generate slug from title if not provided
        if not self.slug:
            self.slug = slugify(self.title)
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
