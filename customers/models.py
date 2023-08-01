from django.db import models

# Create your models here.
from django.db import models

class Customer(models.Model):
    # Fields for personal details
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

    # Fields for business details
    company_name = models.CharField(max_length=200, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    website = models.URLField(max_length=200, blank=True)
    industry = models.CharField(max_length=100, blank=True)

    # Additional fields for social media profiles
    linkedin_profile = models.URLField(max_length=200, blank=True)
    twitter_profile = models.URLField(max_length=200, blank=True)
    facebook_profile = models.URLField(max_length=200, blank=True)

    # Fields for timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Company(models.Model):
    # Fields for company details
    name = models.CharField(max_length=200)
    website = models.URLField(max_length=200, blank=True)
    address = models.TextField(blank=True)
    employees = models.PositiveIntegerField(default=0)

    # Fields for industry classification
    industry = models.CharField(max_length=100, blank=True)
    company_type = models.CharField(max_length=100, blank=True)

    # Additional fields for social media profiles
    linkedin_profile = models.URLField(max_length=200, blank=True)
    twitter_profile = models.URLField(max_length=200, blank=True)
    facebook_profile = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return self.name

class Deal(models.Model):
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    closing_date = models.DateField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    is_won = models.BooleanField(default=False)

    # Fields for deal stages and probabilities
    STAGE_CHOICES = (
        ('Prospect', 'Prospect'),
        ('Qualification', 'Qualification'),
        ('Negotiation', 'Negotiation'),
        ('Closed Won', 'Closed Won'),
        ('Closed Lost', 'Closed Lost'),
    )
    stage = models.CharField(max_length=100, choices=STAGE_CHOICES, default='Prospect')
    probability = models.PositiveIntegerField(default=0)

    # Fields for timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    # Fields for task priority
    PRIORITY_CHOICES = (
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    )
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Medium')

    # Fields for task categories
    CATEGORY_CHOICES = (
        ('Follow-up', 'Follow-up'),
        ('Meeting', 'Meeting'),
        ('Call', 'Call'),
        ('Email', 'Email'),
    )
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Follow-up')

    # Fields for timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Note(models.Model):
    text = models.TextField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    # Fields for note type
    TYPE_CHOICES = (
        ('General', 'General'),
        ('Meeting', 'Meeting'),
        ('Call', 'Call'),
        ('Follow-up', 'Follow-up'),
    )
    note_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='General')

    # Fields for timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Note for {self.customer}"

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    # Fields for contact role
    ROLE_CHOICES = (
        ('Decision Maker', 'Decision Maker'),
        ('Influencer', 'Influencer'),
        ('Gatekeeper', 'Gatekeeper'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Decision Maker')

    # Fields for timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
