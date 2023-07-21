from django.urls import path
from .views import ProductViewSet

urlpatterns = [
    path(
        "products/scrape-product-page/",
        ProductViewSet.as_view({"get": "scrape_product_page"}),
        name="scrape-product-page",
    ),
    path(
        "products/scrape-multiple-products/",
        ProductViewSet.as_view({"post": "scrape_multiple_products"}),
        name="scrape-multiple-products",
    ),
    path(
        "products/scrape-results-page/",
        ProductViewSet.as_view({"get": "scrape_results_page"}),
        name="scrape-results-page",
    ),
]
