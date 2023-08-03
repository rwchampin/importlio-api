from django.contrib import admin
from .models import Post, PostImage, Category, Tag, PostType,CustomFieldValue
# Register your models here.
admin.site.register(Post)
admin.site.register(PostImage)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(PostType)
admin.site.register(CustomFieldValue)