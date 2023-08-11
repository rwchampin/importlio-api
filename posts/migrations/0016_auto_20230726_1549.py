# your_app_name/migrations/0001_initial.py
# your_app_name/migrations/0001_initial.py

from django.db import migrations, models, transaction
from django.utils.text import slugify

def generate_unique_slug(model, value, max_length):
    original_slug = slugify(value)[:max_length]
    slug = original_slug
    counter = 1
    while model.objects.filter(slug=slug).exists():
        slug = f"{original_slug}-{counter}"
        counter += 1
        if len(slug) > max_length:
            slug = slug[:max_length]

    return slug

def add_post_types(apps, schema_editor):
    PostType = apps.get_model('posts', 'PostType')
    post_types = [
        'Entrepreneurship and Startups',
        'Business Strategy',
        "Amazon Product Imports",
        "Shopify Dropshipping",
        "Ecommerce Strategies",
        "Product Management",
        "Dropship Business Tips"
        # Add more default post types here if needed
    ]

    with transaction.atomic():
        for post_type_name in post_types:
            post_type = PostType(name=post_type_name)
            post_type.save()
            
def add_categories(apps, schema_editor):
    Category = apps.get_model('posts', 'Category')
    categories = [
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
        # Add more default categories here if needed
    ]

    with transaction.atomic():
        for category_name in categories:
            slug = generate_unique_slug(Category, category_name, max_length=100)
            category = Category(name=category_name, slug=slug)
            category.save()

def add_tags(apps, schema_editor):
    Tag = apps.get_model('posts', 'Tag')
    tags = [
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
        # Add more default tags here if needed
    ]

    with transaction.atomic():
        for tag_name in tags:
            slug = generate_unique_slug(Tag, tag_name, max_length=100)
            tag = Tag(name=tag_name, slug=slug)
            tag.save()

 
class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0015_alter_post_published_at'),
    ]

    operations = [
        # Your other migrations operations go here

        migrations.RunPython(add_post_types),
        migrations.RunPython(add_categories),
        migrations.RunPython(add_tags),
    ]
