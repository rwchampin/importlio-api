from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify
from django.utils import timezone
import uuid
from users.models import UserAccount as Users
import readtime

POST_STATUS = (
    ('draft', 'Draft'),
    ('published', 'Published'),
)

class AutoSlugMixin(models.Model):
    slug = models.SlugField(blank=True, null=True, max_length=400)

    def save(self, *args, **kwargs):
        # If the post doesn't have a slug or has a temporary slug, generate a new one
        if not self.slug or self.slug.startswith('temp-slug-'):
            if self.title:
                self.slug = slugify(self.get_slug_source())
            else:
                self.slug = f'temp-slug-{uuid4()}'
        # If the post has a title and the slug doesn't start with 'temp-slug-', update the slug
        elif self.title and not self.slug.startswith('temp-slug-'):
            self.slug = slugify(self.get_slug_source())
        super().save(*args, **kwargs)

    def get_slug_source(self):
        raise NotImplementedError(
            "Subclasses of AutoSlugMixin must provide a get_slug_source() method.")

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
    # author = models.ForeignKey(User, on_delete=models.CASCADE)
    post_type = models.ForeignKey(
        PostType, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=400, blank=True, null=True)
    subtitle = models.CharField(max_length=400, blank=True, null=True)
    headline = models.CharField(max_length=400, blank=True, null=True)
    shadowText = models.CharField(max_length=300, blank=True, null=True)
    content = models.TextField(null=True, blank=True)
    excerpt = models.TextField(blank=True, null=True)
    published = models.DateTimeField(editable=False, default=timezone.now)
    categories = models.ManyToManyField(Category, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    custom_fields = GenericRelation('CustomFieldValue')
    readtime = models.CharField(max_length=20, blank=True, null=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    featured_image = models.ImageField(
        upload_to='featured_images/%Y/%m/%d/', blank=True, null=True)
    updated = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=50, choices=POST_STATUS, default='draft', blank=True, null=True)

    # SEO
    seo_title = models.CharField(max_length=400, blank=True, null=True)
    seo_description = models.TextField(blank=True, null=True)

    def get_slug_source(self):
        return self.title

    def get_readtime(self):
        result = readtime.of_text(self.content)
        return result.text

    def save(self, *args, **kwargs):
        if not self.published:
            self.published = timezone.now()
        if not self.updated:
            self.updated = timezone.now()
        if not self.slug:
            self.slug = slugify(self.get_slug_source())

        self.readtime = self.get_readtime()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Users, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.blog_post.title}"
    
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
