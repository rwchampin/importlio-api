from django.db import models
from django.utils.text import slugify

list_level_TYPES = (
    ('1', 'Basic'),
    ('2', 'Pro'),
    ('3', 'Enterprise'),
)

# slugify mixin that makes a slug field and updates it on every save and uses the models
# name field as the default field to slugify
# auto slugify mixin and if no title it names it untitled<num of eisting untitled + 1>
class AutoSlugMixin(models.Model):
    slug = models.SlugField(blank=True, null=True, max_length=255)
    class Meta:
        abstract = True
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        else:
            #amount of existing slugs with the same name + 1
            self.slug = slugify(self.name) + str(self.__class__.objects.filter(slug__startswith=slugify(self.name)).count() + 1)
        super(AutoSlugMixin, self).save(*args, **kwargs)
        
        

class MarketingStatistic(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    marketing_list = models.ForeignKey('MarketingList', related_name='statistics', on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.name
 

class Email(models.Model):
    email = models.EmailField(unique=True, max_length=255)
    marketing_list = models.ManyToManyField('MarketingList', related_name='email_marketing_list')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

class ListType(AutoSlugMixin, models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return self.name


class Tag(AutoSlugMixin, models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class MarketingList(AutoSlugMixin, models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    level = models.CharField(max_length=1, choices=list_level_TYPES, default='1')
    emails = models.ManyToManyField(Email, related_name='marketing_list_emails', blank=True)
    type = models.ForeignKey(ListType, related_name='type', on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='tags', blank=True)
    # downloaded_by = models.ManyToManyField(UserAccount, related_name='downloaded_by', blank=True)
    downloaded_by = models.CharField(max_length=255, blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True, null=True)
    is_populating = models.BooleanField(default=False, blank=True, null=True)
    limit = models.IntegerField(default=0, blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    
    