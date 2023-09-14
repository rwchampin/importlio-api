from django.db import models
from django.utils.text import slugify
import readtime
import uuid
from django.utils import timezone

POST_STATUS = [
    ('draft', 'Draft'),
    ('published', 'Published'),
]
class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class PostType(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(PostType, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.name
        
class Post(models.Model):
    post_type = models.ForeignKey(
        'PostType', on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=400, blank=True, null=True)
    subtitle = models.CharField(max_length=400, blank=True, null=True)
    headline = models.CharField(max_length=400, blank=True, null=True)
    shadowText = models.CharField(max_length=300, blank=True, null=True)
    content = models.TextField(null=True, blank=True)
    excerpt = models.TextField(blank=True, null=True)
    published = models.DateTimeField(editable=False, default=timezone.now)
    categories = models.ManyToManyField('Category', blank=True, null=True)
    tags = models.ManyToManyField('Tag', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    read_time = models.IntegerField(blank=True, null=True)
    featured_image = models.ImageField(
        upload_to='featured_images/%Y/%m/%d/', blank=True, null=True)
    updated = models.DateTimeField(default=timezone.now)
    post_status = models.CharField(max_length=100, choices=POST_STATUS, default='draft')
    seo_title = models.CharField(max_length=400, blank=True, null=True)
    seo_description = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Update slug if title changes
        self.slug = slugify(self.title)

        # Calculate read time
        self.read_time = readtime.of_text(self.content).minutes

        # Handle empty title and slug
        if not self.title and not self.slug:
            total_posts = Post.objects.count()
            self.title = f'Untitled Post #{total_posts + 1}'
            self.slug = slugify(self.title)

        super(Post, self).save(*args, **kwargs)
        
        
    def __str__(self):
        return self.title

