from django.db import models
from django.utils.text import slugify

list_level_TYPES = (
    ('1', 'Basic'),
    ('2', 'Pro'),
    ('3', 'Enterprise'),
)

class Niche(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class MarketingStatistic(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    niche = models.ForeignKey(Niche, related_name='statistics', on_delete=models.SET_NULL, null=True, blank=True)

    
    def __str__(self):
        return self.name

class DataSource(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Email(models.Model):
    email = models.EmailField(unique=True, max_length=255)
    niches = models.ManyToManyField(Niche, related_name='emails')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)
    niches = models.ManyToManyField(Niche, related_name='tags')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class MarketingList(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    level = models.CharField(max_length=1, choices=list_level_TYPES, default='1')
    fake = models.BooleanField(default=False)
    url = models.SlugField(blank=True, null=True, max_length=255)
    niches = models.ManyToManyField(Niche, related_name='marketing_lists')

    def save(self, *args, **kwargs):
        self.url = slugify(self.name)
        super(MarketingList, self).save(*args, **kwargs)
        # Calculate and update the size of the marketing list
        self.update_size()

    def update_size(self):
        # Calculate the total size by summing the sizes of emails for all associated niches
        total_size = Email.objects.filter(niches__in=self.niches.all()).count()
        self.marketingliststatistic_set.update_or_create(defaults={'size': total_size})

    def __str__(self):
        return self.name