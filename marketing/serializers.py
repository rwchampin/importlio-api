from rest_framework import serializers
from .models import DataSource, Niche, Email, Tag, MarketingList

class DataSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSource
        fields = '__all__'

class PreviewNicheSerializer(serializers.ModelSerializer):
    # Define a serializer for the Niche model
    class NicheSerializer(serializers.ModelSerializer):
        class Meta:
            model = Niche
            fields = '__all__'

    # Rename 'emails' field to 'email_count' and 'tags' field to 'tag_count'
    email_count = serializers.SerializerMethodField()
    tag_count = serializers.SerializerMethodField()
    niche = NicheSerializer()  # Include the entire Niche JSON

    def get_email_count(self, obj):
        return obj.emails.all().count()

    def get_tag_count(self, obj):
        return obj.tags.all().count()

    class Meta:
        model = Niche
        fields = '__all__'

class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class PreviewMarketingListSerializer(serializers.ModelSerializer):
    # niches = PreviewNicheSerializer(many=True, read_only=True)
    class Meta:
        model = MarketingList
        fields = '__all__'
