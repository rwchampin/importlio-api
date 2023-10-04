from django.contrib import admin
from .models import Email, MarketingList, MarketingStatistic, Tag

# Register your models here.
admin.site.register(Email)
admin.site.register(MarketingList)
admin.site.register(MarketingStatistic)


