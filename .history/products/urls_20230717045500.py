from django.urls import path
from .views import ProductViewSet

urlpatterns = [
    path(
        "products/single",
        ProductViewSet.as_view({"get": "scrape_product_page"}),
        name="scrape-single-product",
    ),
    path(
        "products/multiple/",
        ProductViewSet.as_view({"post": "scrape_multiple_products"}),
        name="scrape-multiple-products",
    ),
    path(
        "products/scrape-results-page/",
        ProductViewSet.as_view({"get": "scrape_results_page"}),
        name="scrape-results-page",
    ),
]
