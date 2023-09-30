from django.contrib import admin
from .models import Niche, Email, MarketingList, MarketingStatistic, DataSource, Tag

# Register your models here.
admin.site.register(Niche)
admin.site.register(Email)
admin.site.register(MarketingList)
admin.site.register(MarketingStatistic)


