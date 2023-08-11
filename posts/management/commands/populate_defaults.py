from django.core.management.base import BaseCommand
from posts.models import Tag, Category, PostType

class Command(BaseCommand):
    help = 'Populate default tags, categories, and post types'

    def handle(self, *args, **options):
        # Create default tags
        default_tags = [
            'Ecommerce',
            'Shopify',
            'Amazon',
            'Dropshipping',
            'Amazon Associates',
            'Affiliate Marketing',
            'SEO',
            'Ecommerce App',
            'Ecommerce Platform',
            'Ecommerce Website',
            'Ecommerce Store',
            'Ecommerce Business',
            'Ecommerce Marketing',
            "Dropship Products",
            "Shopify Importer",
            "Ecommerce SEO",
            "Online Business",
            "Product Listings",
            "Sourcing Suppliers",
            "Order Fulfillment",
            "Digital Marketing",
            "Customer Retention",
            "User Engagement"
        ]
        for tag_name in default_tags:
            Tag.objects.get_or_create(name=tag_name)

        # Create default categories
        default_categories = [
            'Ecommerce',
            'Shopify',
            'Amazon',
            'Dropshipping',
            "Amazon Dropshipping",
            "Shopify Store Setup",
            "Ecommerce Marketing",
            "Product Research",
            "Inventory Management",
            "Supplier Collaboration",
            "Payment Gateways",
            "Shipping Strategies",
            "Customer Experience",
            "Conversion Optimization"
        ]
        for category_name in default_categories:
            Category.objects.get_or_create(name=category_name)

        # Create default post types
        default_post_types = [
           'Entrepreneurship and Startups',
        'Business Strategy',
        "Amazon Product Imports",
        "Shopify Dropshipping",
        "Ecommerce Strategies",
        "Product Management",
        "Dropship Business Tips"
        ]
        for post_type_name, description in default_post_types:
            PostType.objects.get_or_create(name=post_type_name, description=description)

        self.stdout.write(self.style.SUCCESS('Default tags, categories, and post types added successfully.'))
