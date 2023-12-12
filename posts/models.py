from django.db import models
from django.utils.text import slugify
import readtime
from django.utils import timezone
from PIL import Image
from django.core.exceptions import ValidationError
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage as storage
from django.core.files import File
from django.core.files.uploadedfile import InMemoryUploadedFile 
from .filler_words import clean_slug

POST_STATUS = (
    ('new', 'New'),
    ('draft', 'Draft'),
    ('published', 'Published'),
)

POST_THEME = (
    ('dark', 'Dark'),
    ('light', 'Light'),
)

RESPONSIVE_IMAGE_SIZES = (
    ('mobile', 768),
    ('tablet', 1280),
    ('desktop', 1920),
)
 
 
class SlugMixin(models.Model):
    slug = models.SlugField(unique=True, blank=True, null=True, max_length=500)
    
    def save(self, *args, **kwargs):
        slug = self.name
        # remove any filler words
        
        self.slug = slugify(slug)
        super(SlugMixin, self).save(*args, **kwargs)
        
    class Meta:
        abstract = True
        
          
class ThumbnailImage(SlugMixin, models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(
        upload_to='featured_images/', blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    width = models.FloatField(blank=True, null=True)
    aspect_ratio = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    alt = models.CharField(max_length=255, blank=True, null=True)

class FeaturedImage(SlugMixin, models.Model):
    image = models.ImageField(
        upload_to='featured_images/', blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    alt = models.CharField(max_length=255, blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    width = models.FloatField(blank=True, null=True)
    aspect_ratio = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    def save(self, *args, **kwargs):
        # Open the image
        image = Image.open(self.image)
        
        # save image dimensions
        self.height = image.height
        self.width = image.width
        self.aspect_ratio = image.width / image.height
        
        # save image
        super(FeaturedImage, self).save(*args, **kwargs)
            
    
    def __str__(self):
        return self.image.url
    
class Tag(SlugMixin, models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Category(SlugMixin, models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class PostType(SlugMixin, models.Model):
    name = models.CharField(max_length=255)
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

class PostOutlineItem(models.Model):
    text = models.CharField(max_length=255)
    order = models.IntegerField()
    
    def __str__(self):
        return self.text
    
class PostOutline(models.Model):
    name = models.CharField(max_length=255)
    text = models.TextField()
    items = models.ManyToManyField(PostOutlineItem, blank=True)
    
class PostSection(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(
        upload_to='featured_images/', blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    html_id = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return self.name
class Post(models.Model):
    post_type = models.ForeignKey(
        'PostType', on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=400, blank=True, null=True)
    subtitle = models.CharField(max_length=400, blank=True, null=True)
    headline = models.CharField(max_length=400, blank=True, null=True)
    shadowText = models.CharField(max_length=300, blank=True, null=True)
    content = models.TextField(null=True, blank=True)
    excerpt = models.TextField(blank=True, null=True)
    published = models.DateTimeField(editable=False,auto_now_add=True)
    categories = models.ManyToManyField('Category', blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    word_count = models.IntegerField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True, max_length=500)
    read_time = models.IntegerField(blank=True, null=True)
    featured_image = models.ImageField(
        upload_to='featured_images/', blank=True, null=True)
    mobile_image = models.ImageField(
        upload_to='featured_images/', blank=True, null=True)
    tablet_image = models.ImageField(
        upload_to='featured_images/', blank=True, null=True)
    desktop_image = models.ImageField(
        upload_to='featured_images/', blank=True, null=True)
    image_alt_text = models.CharField(max_length=255, blank=True, null=True)
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
        if self.post_status == 'new':
            count = Post.objects.filter(post_status='draft').count()
            self.post_status = 'draft'
            self.title = f'New Draft {count + 1}'
            self.content = 'New Draft'
        

            
        # Update slug if title changes
        self.slug = clean_slug(self.title)

        # Calculate word count
        if self.content:
            self.word_count = len(self.content.split())
        
        # Calculate read time
        if self.content:
            self.read_time = readtime.of_text(self.content).minutes

        # if content is not present, set read time to 0
        else:
            self.read_time = 1
            
        
        # Create thumbnail and tablet images
        # if self.featured_image:
        #     original_image = Image.open(self.featured_image)
            
        #     # Check if the image format is not JPEG
        #     if original_image.format != 'JPEG':
        #         # Convert to JPEG
        #         byte_array = BytesIO()
        #         original_image.convert('RGB').save(byte_array, format='JPEG')
        #         self.featured_image.save(
        #             f"{self.slug}.jpg", 
        #             ContentFile(byte_array.getvalue()), 
        #             save=False
        #         )
        #         original_image = Image.open(self.featured_image.path)  # Re-open the saved jpeg image

        #     for image_type, size in RESPONSIVE_IMAGE_SIZES:
        #         if image_type == 'mobile':
        #             img_field = 'mobile_image'
        #         elif image_type == 'tablet':
        #             img_field = 'tablet_image'
        #         else:
        #             img_field = 'desktop_image'
                
        #         # Resizing logic
        #         aspect_ratio = original_image.width / original_image.height
        #         new_height = int(size / aspect_ratio)
        #         resized_image = original_image.resize((size, new_height), Image.LANCZOS)
                
        #         # Save the resized images
        #         thumb_io = BytesIO()
        #         resized_image.save(thumb_io, format='JPEG')
                
        #         thumb_file = ContentFile(thumb_io.getvalue())
        #         thumb_filename = f"{self.slug}_{image_type}.jpg"
        #         getattr(self, img_field).save(thumb_filename, thumb_file, save=False)

        # Save the object because we made changes to the file fields
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
    
class PostRephraseSegment(models.Model):
    html = models.TextField()
    segment_index = models.IntegerField()
    
class PostRephrase(models.Model):
    url = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    headline = models.CharField(max_length=255, blank=True, null=True)
    shadowText = models.CharField(max_length=300, blank=True, null=True)
    excerpt = models.TextField(blank=True, null=True)
    seo_title = models.CharField(max_length=400, blank=True, null=True)
    seo_description = models.TextField(blank=True, null=True)
    seo_keywords = models.TextField(blank=True, null=True)
    html = models.TextField()
    current_segment = models.IntegerField()
    segments = models.ManyToManyField(PostRephraseSegment, blank=True)
    rephrased_content = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.text