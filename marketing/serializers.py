from rest_framework import serializers
from .models import Email, Tag, MarketingList, MarketingStatistic
# Include the entire Niche JSON

class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class MarketingStatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketingStatistic
        fields = '__all__'
class PreviewMarketingListSerializer(serializers.ModelSerializer):
    # get a count of the total number of emails with a many to many relationahip
    email_count = serializers.SerializerMethodField()
    
    def get_email_count(self, obj):
        return obj.emails.count()
    class Meta:
        model = MarketingList
        fields = ['name', 'description', 'email_count', 'url', 'slug']

class MarketingListSerializer(serializers.ModelSerializer):
    # get a count of the total number of emails with a many to many relationahip
    emails = EmailSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    statistics = serializers.SerializerMethodField()
    
    def get_statistics(self, obj):
        return MarketingStatisticSerializer(obj.statistics.all(), many=True).data
    
    class Meta:
        model = MarketingList
        fields = '__all__'
        