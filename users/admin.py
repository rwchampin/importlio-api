from django.contrib import admin
from .models import UserAccount, ContactMessage
# Register your models here.
admin.site.register(UserAccount)
admin.site.register(ContactMessage)