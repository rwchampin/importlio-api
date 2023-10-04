from django.db import models
from django.utils.text import slugify
import readtime
import uuid
from django.utils import timezone
from PIL import Image
from django.core.exceptions import ValidationError

POST_STATUS = (
    ('draft', 'Draft'),
    ('published', 'Published'),
)

POST_THEME = (
    ('dark', 'Dark'),
    ('light', 'Light'),
)


class FeaturedImage(models.Model):
    filename = models.CharField(max_length=255, blank=True, null=True)
    original_image = models.ImageField(
        upload_to='featured_images/%Y/%m/%d/', blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    width = models.FloatField(blank=True, null=True)
    thumbnail = models.ImageField(
        upload_to='featured_images/thumbnail/%Y/%m/%d/', blank=True, null=True)
    medium = models.ImageField(
        upload_to='featured_images/medium/%Y/%m/%d/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Open the image
        image = Image.open(self.original_image)
        
        # Define the minimum dimensions
        min_width = 1280
        min_height = 1080
        
        # Check if the image dimensions meet the minimum requirements
        if image.width < min_width or image.height < min_height:
            raise ValidationError(f"Image dimensions must be at least {min_width}x{min_height}px")
        
        self.height = image.height
        self.width = image.width
        # Continue with the save process if dimensions are valid
        super(FeaturedImage, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.image.url
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
    
class PostTheme(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(PostTheme, self).save(*args, **kwargs)
        
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
    published = models.DateTimeField(editable=False,auto_now_add=True)
    categories = models.ManyToManyField('Category', blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    slug = models.SlugField(unique=True, blank=True, null=True, max_length=500)
    read_time = models.IntegerField(blank=True, null=True)
    featured_image = models.ImageField(
        upload_to='featured_images/%Y/%m/%d/', blank=True, null=True)
    optimized_image = models.ForeignKey(
        'FeaturedImage', on_delete=models.SET_NULL, blank=True, null=True)
    updated = models.DateTimeField( auto_now=True)
    post_status = models.CharField(max_length=100, choices=POST_STATUS, default='draft')
    seo_title = models.CharField(max_length=400, blank=True, null=True)
    seo_description = models.TextField(blank=True, null=True)
    seo_keywords = models.TextField(blank=True, null=True)

    # styles for the post
    shadow_text_theme = models.CharField(max_length=20, choices=POST_THEME, default='light')
    title_text_theme = models.CharField(max_length=20, choices=POST_THEME, default='light')
    subtitle_text_theme = models.CharField(max_length=20, choices=POST_THEME, default='light')
    headline_text_theme = models.CharField(max_length=20, choices=POST_THEME, default='light')
    
    
    def save(self, *args, **kwargs):
        # Update slug if title changes
        self.slug = slugify(self.title)

        # Calculate read time
        self.read_time = readtime.of_text(self.content).minutes

        if self.read_time <= 0:
            self.read_time = 1
            
        # Handle empty title and slug
        if not self.title and not self.slug:
            total_posts = Post.objects.count()
            self.title = f'Untitled Post #{total_posts + 1}'
            self.slug = slugify(self.title)

        super(Post, self).save(*args, **kwargs)
        
        
    def __str__(self):
        return self.title


class PostTopicIdeas(models.Model):
    topic = models.CharField(max_length=255, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.topic)
        super(PostTopicIdeas, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.topic