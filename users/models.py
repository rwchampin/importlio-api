from django.db import models
import datetime
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin
)
from marketing.models import MarketingList
from django.utils import timezone
memberships = (
    ('SUBSCRIBER', 'Subscriber'),
    ('TRIAL', 'Trial'),
    ('BASIC', 'Basic'),
    ('PRO', 'Pro'),
    ('ENTERPRISE', 'Enterprise'),
    ('ADMIN', 'Admin'),
)

TRIAL_MEMBERSHIP_DURATION = 14




class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        email = email.lower()

        user = self.model(
            email=email,
            **kwargs
        )

        if password is not None:
            user.set_password(password)
            
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **kwargs):
        user = self.create_user(
            email,
            password=password,
            **kwargs
        )

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

    
class UserAccount(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    password = models.CharField(max_length=255, null=True, blank=True)
    amazon_associate_id = models.CharField(max_length=255, null=True, blank=True)
    
    # Contact Details
    phone = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True, max_length=255)
    
    # Location Details
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    tz = models.CharField(max_length=255, null=True, blank=True)
    region = models.CharField(max_length=255, null=True, blank=True)
    zip = models.CharField(max_length=255, null=True, blank=True)
    
    # Product Details
    # products = models.ManyToManyField('products.Product', blank=True)
    # product_lists = models.ManyToManyField('products.ProductList', blank=True)
    
    # Account Details
    account_type = models.CharField(max_length=255, choices=memberships, default=memberships[0][0])
    account_created = models.DateTimeField(auto_now_add=True)
    account_updated = models.DateTimeField(auto_now=True)
    account_active = models.BooleanField(default=True)
    
    # email lists
    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    
    def trial_days_remaining(self):
        if self.account_type == 'trial':
            if self.account_created + datetime.timedelta(days=TRIAL_MEMBERSHIP_DURATION) <= datetime.now():
                return 0
            else:
                return (self.account_created + datetime.timedelta(days=TRIAL_MEMBERSHIP_DURATION) - datetime.now()).days
        else:
            return 0
        
    def calculate_account_status(self):
        if self.account_type == 'trial':
            if self.account_created + datetime.timedelta(days=TRIAL_MEMBERSHIP_DURATION) <= datetime.now():
                self.account_active = False
                self.save()
                
    def email_lists_downloaded(self):
        lists = MarketingList.objects.filter(downloaded_by=self)
        return lists.count()
    
    def __str__(self):
        return self.email


class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name + ' - ' + self.email