from django.contrib import admin
from .models import Post, Category, Tag, PostType, PostIdeaUrl
# Register your models here.
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(PostType)
admin.site.register(PostIdeaUrl)


