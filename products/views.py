from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from .utils import scrape_product


class ProductViewSet(ViewSet):
    authentication_classes = []
    permission_classes = []

    @action(detail=False, methods=["get"])
    def scrape_product_page(self, request):
        product_url = request.query_params.get("url")
        if not product_url:
            return Response({"error": "Product URL is required."}, status=400)

        product = scrape_product(product_url)
