from django.db import models
from users.models import UserAccount as User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
import math
import re


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class PostType(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Field(models.Model):
    post_type = models.ForeignKey(PostType, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    field_type = models.CharField(max_length=100)  # Example: CharField, TextField, etc.
    is_required = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post_type = models.ForeignKey(PostType, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category)
    tags = models.ManyToManyField(Tag)
    custom_fields = GenericRelation('CustomFieldValue')
    minute_read = models.IntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    dislikes = models.ManyToManyField(User, related_name='disliked_posts', blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Calculate approximate minute read based on word count
        word_count = len(re.findall(r'\w+', self.content))
        self.minute_read = math.ceil(word_count / 200)  # Assuming average reading speed of 200 words per minute
        super().save(*args, **kwargs)


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images/%Y/%m/%d/')
    is_featured = models.BooleanField(default=False)
    
    def __str__(self):
        return self.post.title